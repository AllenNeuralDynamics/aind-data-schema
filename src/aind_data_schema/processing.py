""" schema for processing """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, root_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.imaging.tile import Tile


class ProcessName(Enum):
    """Data processing type labels"""

    ANALYSIS = "Analysis"
    DENOISING = "Denoising"
    EPHYS_CURATION = "Ephys curation"
    EPHYS_POSTPROCESSING = "Ephys postprocessing"
    EPHYS_PREPROCESSING = "Ephys preprocessing"
    EPHYS_VISUALIZATION = "Ephys visualization"
    FIDUCIAL_SEGMENTATION = "Fiducial segmentation"
    IMAGE_ATLAS_ALIGNMENT = "Image atlas alignment"
    IMAGE_BACKGROUND_SUBTRACTION = "Image background subtraction"
    IMAGE_CELL_SEGMENTATION = "Image cell segmentation"
    IMAGE_CELL_QUANTIFICATION = "Image cell quantification"
    IMAGE_DESTRIPING = "Image destriping"
    IMAGE_IMPORTING = "Image importing"
    IMAGE_THRESHOLDING = "Image thresholding"
    IMAGE_TILE_ALIGNMENT = "Image tile alignment"
    IMAGE_TILE_FUSING = "Image tile fusing"
    IMAGE_TILE_PROJECTION = "Image tile projection"
    FILE_CONVERSION = "File format conversion"
    MANUAL_ANNOTATION = "Manual annotation"
    NEUROPIL_SUBTRACTION = "Neuropil subtraction"
    OTHER = "Other"
    REGISTRATION_TO_TEMPLATE = "Registration to template"
    SKULL_STRIPPING = "Skull stripping"
    SPIKE_SORTING = "Spike sorting"
    SPATIAL_TIMESERIES_DEMIXING = "Spatial timeseries demixing"
    VIDEO_MOTION_CORRECTION = "Video motion correction"
    VIDEO_PLANE_DECROSSTALK = "Video plane decrosstalk"
    VIDEO_ROI_CLASSIFICATION = "Video ROI classification"
    VIDEO_ROI_SEGMENTATION = "Video ROI segmentation"
    VIDEO_ROI_TIMESERIES_EXTRACTION = "Video ROI timeseries extraction"


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
    outputs: Optional[Dict[str, Any]] = Field(None, description="Output parameters", title="Outputs")
    notes: Optional[str] = Field(None, title="Notes")

    @root_validator
    def validate_other(cls, v):
        """Validator for other/notes"""

        if v.get("name") == ProcessName.OTHER and not v.get("notes"):
            raise ValueError("Notes cannot be empty if 'name' is Other. Describe the process name in the notes field.")
        return v


class PipelineProcess(AindModel):
    """Description of a Processing Pipeline"""

    data_processes: List[DataProcess] = Field(..., title="Data processing", unique_items=True)
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


class Processing(AindCoreModel):
    """Description of all processes run on data"""

    schema_version: str = Field(
        "0.3.0",
        description="Schema version",
        title="Schema version",
        const=True,
    )
    processing_pipeline: PipelineProcess = Field(
        ..., description="Pipeline used to process data", title="Processing Pipeline"
    )
    analyses: Optional[List[AnalysisProcess]] = Field(
        None, description="Analysis steps taken after processing", title="Analysis Steps"
    )
    notes: Optional[str] = Field(None, title="Notes")


class RegistrationType(Enum):
    """Types of registration"""

    INTER = "Inter-channel"
    INTRA = "Intra-channel"


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
