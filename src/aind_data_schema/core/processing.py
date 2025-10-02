"""schema for processing"""

import re
import warnings
from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional

from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import MemoryUnit, UnitlessUnit
from pydantic import Field, SkipValidation, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel, GenericModel
from aind_data_schema.components.identifiers import Code
from aind_data_schema.components.wrappers import AssetPath
from aind_data_schema.utils.merge import merge_notes, merge_optional_list
from aind_data_schema.utils.validators import TimeValidation


class ProcessStage(str, Enum):
    """Stages of processing"""

    PROCESSING = "Processing"
    ANALYSIS = "Analysis"


class ResourceTimestamped(DataModel):
    """Description of resource usage at a moment in time"""

    timestamp: AwareDatetimeWithDefault = Field(..., title="Timestamp")
    usage: float = Field(..., title="Usage")


class ResourceUsage(DataModel):
    """Description of resources used by a process"""

    os: str = Field(..., title="Operating system")
    architecture: str = Field(..., title="Architecture")
    cpu: Optional[str] = Field(default=None, title="CPU name")
    cpu_cores: Optional[int] = Field(default=None, title="CPU cores")
    gpu: Optional[str] = Field(default=None, title="GPU name")
    system_memory: Optional[float] = Field(default=None, title="System memory")
    system_memory_unit: Optional[MemoryUnit] = Field(default=None, title="System memory unit")
    ram: Optional[float] = Field(default=None, title="System RAM")
    ram_unit: Optional[MemoryUnit] = Field(default=None, title="Ram unit")

    cpu_usage: Optional[List[ResourceTimestamped]] = Field(default=None, title="CPU usage")
    gpu_usage: Optional[List[ResourceTimestamped]] = Field(default=None, title="GPU usage")
    ram_usage: Optional[List[ResourceTimestamped]] = Field(default=None, title="RAM usage")
    usage_unit: str = Field(default=UnitlessUnit.PERCENT, title="Usage unit")


class DataProcess(DataModel):
    """Description of a single processing step"""

    process_type: ProcessName = Field(..., title="Process type")
    name: str = Field(
        default="",
        title="Name",
        description=("Unique name of the processing step.", " If not provided, the type will be used as the name."),
    )
    stage: ProcessStage = Field(..., title="Processing stage")
    code: Code = Field(..., title="Code", description="Code used for processing")
    experimenters: List[str] = Field(..., title="Experimenters", description="People responsible for processing")
    pipeline_name: Optional[str] = Field(
        default=None, title="Pipeline name", description="Pipeline names must exist in Processing.pipelines"
    )
    start_date_time: Annotated[AwareDatetimeWithDefault, TimeValidation.AFTER] = Field(..., title="Start date time")
    end_date_time: Optional[Annotated[AwareDatetimeWithDefault, TimeValidation.AFTER]] = Field(
        default=None, title="End date time"
    )
    output_path: Optional[AssetPath] = Field(
        default=None, title="Output path", description="Path to processing outputs, if stored."
    )
    output_parameters: GenericModel = Field(default=GenericModel(), description="Output parameters", title="Outputs")
    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)
    resources: Optional[ResourceUsage] = Field(default=None, title="Process resource usage")

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("process_type") == ProcessName.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if 'process_type' is Other. Describe the type of processing in the notes field."
            )
        return value

    @model_validator(mode="after")
    def fill_default_name(self) -> "DataProcess":
        """Fill in default name if not provided"""

        if not self.name:
            self.name = self.process_type
        return self


class Processing(DataCoreModel):
    """Description of all processes run on data"""

    _DESCRIBED_BY_URL: str = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/processing.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.1.1"]] = Field(default="2.1.1")

    data_processes: List[DataProcess] = Field(..., title="Data processing")
    pipelines: Optional[List[Code]] = Field(
        default=None,
        title="Pipelines",
        description=(
            "For processing done with pipelines, list the repositories here. Pipelines must use the name field "
            ",and be referenced in the pipeline_name field of a DataProcess."
        ),
    )
    notes: Optional[str] = Field(default=None, title="Notes")

    dependency_graph: Optional[Dict[str, List[str]]] = Field(
        default=None,
        title="Dependency graph",
        description=(
            "Directed graph of processing step dependencies. Each key is a process name, and the value is a list of "
            "process names that are inputs to that process."
        ),
    )

    @property
    def process_names(self) -> List[str]:
        """Return the names of data processes"""
        return [process.name for process in self.data_processes]

    def rename_process(self, old_name: str, new_name: str) -> None:
        """Rename a process in the processing object, including all references"""

        for process in self.data_processes:
            if process.name == old_name:
                process.name = new_name
                break
        else:
            raise ValueError(f"Process '{old_name}' not found in data_processes.")
        # rename in dependency_graph
        self.dependency_graph[new_name] = self.dependency_graph.pop(old_name)
        # replace old_name in dependency_graph values
        for value in self.dependency_graph.values():
            if old_name in value:
                value[value.index(old_name)] = new_name

    @model_validator(mode="after")
    def order_processes(self) -> "Processing":
        """Ensure that processes are ordered by start_date_time"""

        if not hasattr(self, "data_processes") or not self.data_processes:
            return self

        # Check if any processes are out of order
        start_times = [process.start_date_time for process in self.data_processes]
        if not all(start_times[i] <= start_times[i + 1] for i in range(len(start_times) - 1)):
            # Sort processes by start_date_time
            self.data_processes.sort(key=lambda x: x.start_date_time)
            self.notes = (
                "Processes were reordered by start_date_time"
                if not self.notes
                else f"{self.notes}; Processes were reordered by start_date_time"
            )

        return self

    @classmethod
    def create_with_sequential_process_graph(cls, data_processes: List[DataProcess], **kwargs) -> "Processing":
        """Generate a sequential process graph from a list of DataProcess objects"""

        dependency_graph = {}
        for i, process in enumerate(data_processes):
            if i == 0:
                dependency_graph[process.name] = []
            else:
                dependency_graph[process.name] = [data_processes[i - 1].name]
        return cls(dependency_graph=dependency_graph, data_processes=data_processes, **kwargs)

    @model_validator(mode="after")
    @classmethod
    def validate_process_graph(cls, values):
        """Check that the same processes are represented in data_processes and dependency_graph"""

        if not hasattr(values, "data_processes"):  # bypass for testing
            return values

        # If the dependency_graph is None, then no need to validate
        if values.dependency_graph is None:
            return values

        processes = set(values.process_names)
        # Validate that all processes have a unique name
        if len(processes) != len(values.data_processes):
            raise ValueError("data_processes must have unique names.")

        graph_processes = set(values.dependency_graph.keys())
        missing_processes = processes - graph_processes
        if missing_processes:
            raise ValueError(
                f"dependency_graph must include all processes in data_processes. Missing processes: {missing_processes}"
            )
        missing_processes = graph_processes - processes
        if missing_processes:
            raise ValueError(
                f"data_processes must include all processes in dependency_graph. Missing processes: {missing_processes}"
            )
        return values

    @model_validator(mode="after")
    @classmethod
    def validate_pipeline_names(cls, values):
        """Ensure that all pipeline names in the processes are in the pipelines list"""

        if not hasattr(values, "data_processes"):  # bypass for testing
            return values

        pipeline_names = [pipeline.name for pipeline in values.pipelines] if values.pipelines else []

        for process in values.data_processes:
            if process.pipeline_name and process.pipeline_name not in pipeline_names:
                raise ValueError(f"Pipeline name '{process.pipeline_name}' not found in pipelines list.")

        return values

    def __add__(self, other: "Processing") -> "Processing":
        """Combine two Processing objects"""

        # Check for incompatible schema_version
        if self.schema_version != other.schema_version:
            raise ValueError("Cannot add Processing objects with different schema versions.")

        # Copy self and other to avoid modifying in place
        self = self.model_copy(deep=True)
        other = other.model_copy(deep=True)

        # Check and update repeated process names
        repeated_processes = set(self.process_names) & set(other.process_names)
        if repeated_processes:
            warnings.warn(f"Processing objects have repeated processes: {repeated_processes}. Renaming duplicates.")
            for name in sorted(repeated_processes):
                # find base name if name is in the form of name_1, name_2, etc.
                base_name = re.sub(r"_\d+$", "", name)  # Remove existing numeric suffix

                # Create a new unique name by incrementing the suffix
                existing_names = set(self.process_names + other.process_names)

                # Start with base name, try with incrementing suffixes until we find an unused name
                new_name = name
                i = 1
                while new_name in existing_names:
                    new_name = f"{base_name}_{i}"
                    i += 1
                other.rename_process(name, new_name)

        # Merge process graphs - start with self's graph and update with other's graph
        combined_process_graph = self.dependency_graph.copy()
        combined_process_graph.update(other.dependency_graph)

        # link self's output to other's input
        # note that this only makes sense if self has a single output process
        # and other has a single input process
        if len(self.data_processes) > 0 and len(other.data_processes) > 0:
            combined_process_graph[other.data_processes[0].name] = [self.data_processes[-1].name]

        return Processing(
            pipelines=merge_optional_list(self.pipelines, other.pipelines),
            data_processes=self.data_processes + other.data_processes,
            dependency_graph=combined_process_graph,
            notes=merge_notes(self.notes, other.notes),
        )
