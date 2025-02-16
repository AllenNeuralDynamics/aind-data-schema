""" schema for processing """

from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import MemoryUnit, UnitlessUnit
from aind_data_schema.core.quality_control import Stage
from pydantic import Field, SkipValidation, ValidationInfo, field_validator

from aind_data_schema.base import (
    DataCoreModel,
    GenericModel,
    GenericModelType,
    DataModel,
    AwareDatetimeWithDefault,
)
from aind_data_schema.components.identifiers import Person


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
    stage: Stage = Field(..., title="Processing stage")
    experimenters: List[Person] = Field(
        ..., title="experimenters", description="People responsible for processing"
    )
    software_version: Optional[str] = Field(default=None, description="Version of the software used", title="Version")
    start_date_time: AwareDatetimeWithDefault = Field(..., title="Start date time")
    end_date_time: AwareDatetimeWithDefault = Field(..., title="End date time")
    # allowing multiple input locations, to be replaced by CompositeData object in future
    input_location: Union[str, List[str]] = Field(..., description="Path(s) to data inputs", title="Input location")
    output_location: str = Field(..., description="Path to data outputs", title="Output location")
    code_url: str = Field(..., description="Path to code repository", title="Code URL")
    code_version: Optional[str] = Field(default=None, description="Version of the code", title="Code version")
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
    schema_version: SkipValidation[Literal["1.1.6"]] = Field(default="1.1.6")

    data_processes: List[DataProcess] = Field(..., title="Data processing")
    notes: Optional[str] = Field(default=None, title="Notes")
