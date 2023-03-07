""" schema for processing """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.imaging.tile import Tile


class ProcessName(Enum):
    """Data processing type labels"""

    EPHYS_CURATION = "Ephys curation"
    EPHYS_PREPROCESSING = "Ephys preprocessing"
    EPHYS_POSTPROCESSING = "Ephys postprocessing"
    EPHYS_VISUALIZATION = "Ephys visualization"
    IMAGE_IMPORTING = "Image importing"
    IMAGE_ATLAS_ALIGNMENT = "Image atlas alignment"
    IMAGE_BACKGROUND_SUBTRACTION = "Image background subtraction"
    IMAGE_CELL_SEGMENTATION = "Image cell segmentation"
    IMAGE_DESTRIPING = "Image destriping"
    IMAGE_THRESHOLDING = "Image thresholding"
    IMAGE_TILE_ALIGNMENT = "Image tile alignment"
    IMAGE_TILE_FUSING = "Image tile fusing"
    IMAGE_TILE_PROJECTION = "Image tile projection"
    FILE_CONVERSION = "File format conversion"
    OTHER = "Other"
    SPIKE_SORTING = "Spike sorting"


class DataProcess(AindModel):
    """Description of a single processing step"""

    name: ProcessName = Field(..., title="Name")
    version: str = Field(..., description="Version of the software used", title="Version")
    start_date_time: datetime = Field(..., title="Start date time")
    end_date_time: datetime = Field(..., title="End date time")
    input_location: str = Field(..., description="Path to data inputs", title="Input location")
    output_location: str = Field(..., description="Path to data outputs", title="Output location")
    code_url: str = Field(..., description="Path to code respository", title="Code URL")
    code_version: Optional[str] = Field(None, description="Version of the code", title="Code version")
    parameters: Dict[str, Any]
    notes: Optional[str] = None


class Processing(AindCoreModel):
    """Description of all processes run on data"""

    schema_version: str = Field(
        "0.1.0",
        description="Schema version",
        title="Schema version",
        const=True,
    )
    pipeline_version: Optional[str] = Field(None, description="Version of the pipeline", title="Pipeline version")
    pipeline_url: Optional[str] = Field(None, description="URL to the pipeline code", title="Pipeline URL")
    data_processes: List[DataProcess] = Field(..., title="Data processing", unique_items=True)


class Stitching(DataProcess):
    """Description of tile alignment coordinate transformations"""

    schema_version: str = Field("0.1.1", description="schema version for stitching", title="Version", const=True)

    tiles: List[Tile] = Field(..., title="Data tiles")
