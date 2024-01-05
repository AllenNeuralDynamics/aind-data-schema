""" schema for processing """

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import Field, ValidationInfo, field_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.imaging.tile import Tile
from aind_data_schema.models.process_names import ProcessName


class RegistrationType(str, Enum):
    """Types of registration"""

    INTER = "Inter-channel"
    INTRA = "Intra-channel"


class DataProcess(AindModel):
    """Description of a single processing step"""

    name: ProcessName = Field(..., title="Name")
    software_version: str = Field(..., description="Version of the software used", title="Version")
    start_date_time: datetime = Field(..., title="Start date time")
    end_date_time: datetime = Field(..., title="End date time")
    input_location: str = Field(..., description="Path to data inputs", title="Input location")
    output_location: str = Field(..., description="Path to data outputs", title="Output location")
    code_url: str = Field(..., description="Path to code repository", title="Code URL")
    code_version: Optional[str] = Field(None, description="Version of the code", title="Code version")
    parameters: Dict[str, Any] = Field(..., title="Parameters")
    outputs: Dict[str, Any] = Field(dict(), description="Output parameters", title="Outputs")
    notes: Optional[str] = Field(None, title="Notes", validate_default=True)

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
    pipeline_version: Optional[str] = Field(None, description="Version of the pipeline", title="Pipeline version")
    pipeline_url: Optional[str] = Field(None, description="URL to the pipeline code", title="Pipeline URL")
    note: Optional[str] = Field(None, title="Notes")


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
        None,
        title="Registration channel",
        description="Channel registered to when inter channel",
    )
    tiles: List[Tile] = Field(..., title="Data tiles")


class Processing(AindCoreModel):
    """Description of all processes run on data"""

    _DESCRIBED_BY_URL: str = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/processing.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.4.3"] = Field("0.4.3")

    processing_pipeline: PipelineProcess = Field(
        ..., description="Pipeline used to process data", title="Processing Pipeline"
    )
    analyses: List[AnalysisProcess] = Field(
        default=[], description="Analysis steps taken after processing", title="Analysis Steps"
    )
    notes: Optional[str] = Field(None, title="Notes")
