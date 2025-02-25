""" schema for processing """

from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import MemoryUnit, UnitlessUnit
from pydantic import Field, SkipValidation, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import (
    DataCoreModel,
    GenericModel,
    GenericModelType,
    DataModel,
    AwareDatetimeWithDefault,
)
from aind_data_schema.components.identifiers import Person, Code


class ProcessStage(str, Enum):
    """Stages of processing"""

    PROCESSING = "Processing"
    ANALYSIS = "Analysis"


class RegistrationType(str, Enum):
    """Types of registration"""

    INTER = "Inter-channel"
    INTRA = "Intra-channel"


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

    name: ProcessName = Field(..., title="Name")
    stage: ProcessStage = Field(..., title="Processing stage")
    experimenters: List[Person] = Field(..., title="experimenters", description="People responsible for processing")
    code: Code = Field(..., title="Code used for processing")
    pipeline_steps: Optional[List[ProcessName]] = Field(
        default=None,
        title="Pipeline steps",
        description=(
            "For pipeline processes (ProcessName.PIPELINE), steps should indicate the DataProcess objects",
            " that are part of the pipeline. Each object must show up in the data_processes list.",
        ),
    )
    start_date_time: AwareDatetimeWithDefault = Field(..., title="Start date time")
    end_date_time: AwareDatetimeWithDefault = Field(..., title="End date time")
    # allowing multiple input locations, to be replaced by CompositeData object in future
    input_location: Union[str, List[str]] = Field(..., description="Path(s) to data inputs", title="Input location")
    output_location: str = Field(..., description="Path to data outputs", title="Output location")
    parameters: GenericModelType = Field(default=GenericModel(), title="Parameters")
    outputs: GenericModelType = Field(default=GenericModel(), description="Output parameters", title="Outputs")
    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)
    resources: Optional[ResourceUsage] = Field(default=None, title="Process resource usage")

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("name") == ProcessName.OTHER and not value:
            raise ValueError("Notes cannot be empty if 'name' is Other. Describe the process name in the notes field.")
        return value


class Processing(DataCoreModel):
    """Description of all processes run on data"""

    _DESCRIBED_BY_URL: str = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/processing.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.3"]] = Field(default="2.0.3")

    data_processes: List[DataProcess] = Field(..., title="Data processing")
    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="before")
    def validate_pipeline_steps(cls, values):
        """Validator for pipeline_steps"""

        if not values.get("data_processes"):
            # No data processes, this is probably a test asset
            return values

        data_processes = values["data_processes"]
        # Coerce types if needed
        data_processes = [DataProcess(**process) if not isinstance(process, DataProcess) else process for process in data_processes]

        for process in data_processes:
            # For each process, make sure it's either a pipeline and has all its processes downstream

            if process.name == ProcessName.PIPELINE:

                if not hasattr(process, "pipeline_steps") or not process.pipeline_steps:
                    raise ValueError("Pipeline processes should have a pipeline_steps attribute.")

                # Validate that all steps show up in the data_processes list
                for step in process.pipeline_steps:
                    if step not in [p.name for p in data_processes]:
                        raise ValueError(f"Pipeline step '{step}' not found in data_processes.")
            # Or make sure it doesn't have any pipeline steps
            elif hasattr(process, "pipeline_steps") and process.pipeline_steps:
                raise ValueError("pipeline_steps should only be provided for ProcessName.PIPELINE processes.")

        return values

    @field_validator("data_processes", mode="after")
    def validate_data_processes(cls, value: List[DataProcess]) -> List[DataProcess]:
        """Validator for data_processes"""

        if any([isinstance(process, list) for process in value]):
            raise ValueError("data_processes should not be a list of lists.")

        return value
