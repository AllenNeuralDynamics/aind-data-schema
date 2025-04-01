"""schema for processing"""

import warnings
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional

from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import MemoryUnit, UnitlessUnit
from pydantic import Field, SkipValidation, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel, GenericModel, GenericModelType
from aind_data_schema.components.identifiers import Code, Person
from aind_data_schema.utils.merge import merge_notes


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
    experimenters: List[Person] = Field(..., title="Experimenters", description="People responsible for processing")
    pipeline_steps: Optional[List[str]] = Field(
        default=None,
        title="Pipeline steps",
        description=(
            "For pipeline processes (ProcessName.PIPELINE) only, list names of all DataProcess objects",
            " that are part of the pipeline. Each object must show up in the data_processes list.",
        ),
    )
    start_date_time: AwareDatetimeWithDefault = Field(..., title="Start date time")
    end_date_time: AwareDatetimeWithDefault = Field(..., title="End date time")
    output_path: Optional[Path] = Field(
        default=None, title="Output path", description="Path to processing outputs, if stored."
    )
    output_parameters: GenericModelType = Field(
        default=GenericModel(), description="Output parameters", title="Outputs"
    )
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
    schema_version: SkipValidation[Literal["2.0.42"]] = Field(default="2.0.42")

    data_processes: List[DataProcess] = Field(..., title="Data processing")
    notes: Optional[str] = Field(default=None, title="Notes")

    process_graph: Dict[str, List[str]] = Field(
        ...,
        title="Process graph",
        description=(
            "Directed graph of processing steps. Each key is a process name, and the value is a list of process names",
            " that are inputs to the key process.",
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
        # rename in process_graph
        self.process_graph[new_name] = self.process_graph.pop(old_name)
        # replace old_name in process_graph values
        for value in self.process_graph.values():
            if old_name in value:
                value[value.index(old_name)] = new_name

    @classmethod
    def create_with_sequential_process_graph(cls, data_processes: List[DataProcess], **kwargs) -> "Processing":
        """Generate a sequential process graph from a list of DataProcess objects"""

        process_graph = {}
        for i, process in enumerate(data_processes):
            if i == 0:
                process_graph[process.name] = []
            else:
                process_graph[process.name] = [data_processes[i - 1].name]
        return cls(process_graph=process_graph, data_processes=data_processes, **kwargs)

    @model_validator(mode="after")
    def validate_process_graph(self) -> "Processing":
        """Check that the same processes are represented in data_processes and process_graph"""

        if not hasattr(self, "data_processes"):  # bypass for testing
            return self

        processes = set(self.process_names)
        # Validate that all processes have a unique name
        if len(processes) != len(self.data_processes):
            raise ValueError("data_processes must have unique names.")

        graph_processes = set(self.process_graph.keys())
        missing_processes = processes - graph_processes
        if missing_processes:
            raise ValueError(
                f"process_graph must include all processes in data_processes. Missing processes: {missing_processes}"
            )
        missing_processes = graph_processes - processes
        if missing_processes:
            raise ValueError(
                f"data_processes must include all processes in process_graph. Missing processes: {missing_processes}"
            )
        return self

    @model_validator(mode="after")
    def validate_pipeline_steps(self) -> "Processing":
        """Validator for pipeline_steps"""

        if not hasattr(self, "data_processes"):  # bypass for testing
            return self

        for process in self.data_processes:
            # For each process, make sure it's either a pipeline and has all its processes downstream
            if process.process_type == ProcessName.PIPELINE:
                if not hasattr(process, "pipeline_steps") or not process.pipeline_steps:
                    raise ValueError("Pipeline processes should have a pipeline_steps attribute.")

                # Validate that all referenced processes are in the data_processes list
                for step in process.pipeline_steps:
                    if step not in self.process_names:
                        raise ValueError(
                            f"Processing step '{step}' not found in data_processes",
                            f" (reference in process '{process.name}').",
                        )

            # Or make sure it doesn't have any pipeline steps
            elif hasattr(process, "pipeline_steps") and process.pipeline_steps:
                raise ValueError("pipeline_steps should only be provided for ProcessName.PIPELINE processes.")

        return self

    def __add__(self, other: "Processing") -> "Processing":
        """Combine two Processing objects"""

        # Check for incompatible schema_version
        if self.schema_version != other.schema_version:
            raise ValueError("Cannot add Processing objects with different schema versions.")

        # Copy self and other to avoid modifying in place
        self = self.model_copy(deep=True)
        other = other.model_copy(deep=True)

        # Check for repeated process names
        repeated_processes = set(self.process_names) & set(other.process_names)
        if repeated_processes:
            warnings.warn(f"Processing objects have repeated processes: {repeated_processes}. Renaming duplicates.")
            for name in repeated_processes:
                new_name = next((f"{name}_{i}" for i in range(1, 100) if f"{name}_{i}" not in self.process_names))
                other.rename_process(name, new_name)

        # Merge process graphs - start with self's graph and update with other's graph
        combined_process_graph = self.process_graph.copy()
        combined_process_graph.update(other.process_graph)

        # link self's output to other's input
        # note that this only makes sense if self has a single output process
        # and other has a single input process
        if len(self.data_processes) > 0 and len(other.data_processes) > 0:
            combined_process_graph[other.data_processes[0].name] = [self.data_processes[-1].name]

        return Processing(
            data_processes=self.data_processes + other.data_processes,
            process_graph=combined_process_graph,
            notes=merge_notes(self.notes, other.notes),
        )
