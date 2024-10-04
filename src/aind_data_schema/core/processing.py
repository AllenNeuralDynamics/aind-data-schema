""" schema for processing """

from enum import Enum
from typing import List, Literal, Optional

from aind_data_schema_models.process_names import ProcessName
from pydantic import Field, ValidationInfo, model_validator, field_validator

from aind_data_schema.base import AindCoreModel, AindGeneric, AindGenericType, AindModel, AwareDatetimeWithDefault
from aind_data_schema.components.tile import Tile
from aind_data_schema_models.units import MemoryUnit, UnitlessUnit


class RegistrationType(str, Enum):
    """Types of registration"""

    INTER = "Inter-channel"
    INTRA = "Intra-channel"


class ResourceTimestamped(AindModel):
    """Description of resource usage at a moment in time"""

    timestamp: AwareDatetimeWithDefault = Field(..., title="Timestamp")
    usage: float = Field(..., title="Usage")


class ResourceUsage(AindModel):
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

    @model_validator(mode="after")
    def check_value_and_unit(cls, values):
        """Ensure that all valued fields have units"""
        if values.system_memory and not values.system_memory_unit:
            raise ValueError("System memory unit is required if system memory is provided.")
        if values.ram and not values.ram_unit:
            raise ValueError("RAM unit is required if RAM is provided.")
        return values


class DataProcess(AindModel):
    """Description of a single processing step"""

    name: ProcessName = Field(..., title="Name")
    software_version: str = Field(..., description="Version of the software used", title="Version")
    start_date_time: AwareDatetimeWithDefault = Field(..., title="Start date time")
    end_date_time: AwareDatetimeWithDefault = Field(..., title="End date time")
    input_location: str = Field(..., description="Path to data inputs", title="Input location")
    output_location: str = Field(..., description="Path to data outputs", title="Output location")
    code_url: str = Field(..., description="Path to code repository", title="Code URL")
    code_version: Optional[str] = Field(default=None, description="Version of the code", title="Code version")
    parameters: AindGenericType = Field(..., title="Parameters")
    outputs: AindGenericType = Field(AindGeneric(), description="Output parameters", title="Outputs")
    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)
    resources: Optional[ResourceUsage] = Field(default=None, title="Process resource usage")

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("name") == ProcessName.OTHER and not value:
            raise ValueError("Notes cannot be empty if 'name' is Other. Describe the process name in the notes field.")
        return value


class PipelineProcess(AindModel):
    """Description of a Processing Pipeline"""

    data_processes: List[DataProcess] = Field(..., title="Data processing")
    processor_full_name: str = Field(
        ..., title="Processor Full Name", description="Name of person responsible for processing pipeline"
    )
    pipeline_version: Optional[str] = Field(
        default=None, description="Version of the pipeline", title="Pipeline version"
    )
    pipeline_url: Optional[str] = Field(default=None, description="URL to the pipeline code", title="Pipeline URL")
    note: Optional[str] = Field(default=None, title="Notes")


class AnalysisProcess(DataProcess):
    """Description of an Analysis"""

    name: ProcessName = Field(ProcessName.ANALYSIS, title="Process name")
    analyst_full_name: str = Field(
        ..., title="Analyst Full Name", description="Name of person responsible for running analysis"
    )
    description: str = Field(..., title="Analysis Description")


#  TODO: Check where this class is supposed to be invoked?
class Registration(DataProcess):
    """Description of tile alignment coordinate transformations"""

    registration_type: RegistrationType = Field(
        ...,
        title="Registration type",
        description="Either inter channel across different channels or intra channel",
    )
    registration_channel: Optional[int] = Field(
        default=None,
        title="Registration channel",
        description="Channel registered to when inter channel",
    )
    tiles: List[Tile] = Field(..., title="Data tiles")


class Processing(AindCoreModel):
    """Description of all processes run on data"""

    _DESCRIBED_BY_URL: str = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/processing.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.1.1"] = Field("1.1.1")

    processing_pipeline: PipelineProcess = Field(
        ..., description="Pipeline used to process data", title="Processing Pipeline"
    )
    analyses: List[AnalysisProcess] = Field(
        default=[], description="Analysis steps taken after processing", title="Analysis Steps"
    )
    notes: Optional[str] = Field(default=None, title="Notes")
