""" schema for processing """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .base import AindCoreModel, AindModel


class ProcessName(Enum):
    """Data processing type labels"""

    EPHYS_PREPROCESSING = "Ephys preprocessing"
    EPHYS_POSTPROCESSING = "Ephys postprocessing"
    IMAGE_IMPORTING = "Image importing"
    IMAGE_ATLAS_ALIGNMENT = "Image atlas alignment"
    IMAGE_DESTRIPING = "Image destriping"
    IMAGE_THRESHOLDING = "Image thresholding"
    IMAGE_TILE_FUSING = "Image tile fusing"
    IMAGE_TILE_PROJECTION = "Image tile projection"
    IMAGE_TILE_STITCHING = "Image tile stitching"
    FILE_CONVERSION = "File format conversion"
    OTHER = "Other"
    SPIKE_SORTING = "Spike sorting"


class DataProcess(AindModel):
    """Description of a single processing step"""

    name: ProcessName = Field(..., title="Name")
    version: str = Field(
        ..., description="Version of the software used", title="Version"
    )
    start_date_time: datetime = Field(..., title="Start date time")
    end_date_time: datetime = Field(..., title="End date time")
    input_location: str = Field(
        ..., description="Path to data inputs", title="Input location"
    )
    output_location: str = Field(
        ..., description="Path to data outputs", title="Output location"
    )
    code_url: str = Field(
        ..., description="Path to code respository", title="Code URL"
    )
    parameters: Dict[str, Any]
    notes: Optional[str] = None


class Processing(AindCoreModel):
    """Desription of all processes run on data"""

    schema_version: str = Field(
        "0.1.0",
        description="Schema version",
        title="Schema version",
        const=True,
    )
    pipeline_version: Optional[str] = Field(
        None, description="Version of the pipeline", title="Pipeline version"
    )
    pipeline_url: Optional[str] = Field(
        None, description="URL to the pipeline code", title="Pipeline URL"
    )
    data_processes: List[DataProcess] = Field(
        ..., title="Data processing", unique_items=True
    )
