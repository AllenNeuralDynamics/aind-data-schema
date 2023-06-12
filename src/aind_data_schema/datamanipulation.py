""" schema for processing """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.imaging.tile import Tile
from aind_data_schema.processing import ProcessName


class TouchTypes(Enum):
    ANALYSIS = "Analysis"
    PROCESSING = "Processing"
    CURATION = "Curation"
    SORTING = "Sorting"


class DataTouchInfo:
    touch_type: TouchTypes = Field(..., title="Manipulation type")
    start_date_time: datetime = Field(..., title="Start date time")
    end_date_time: datetime = Field(..., title="End date time")
    input_location: str = Field(..., description="Path to data inputs", title="Input location")
    output_location: str = Field(..., description="Path to data outputs", title="Output location")
    notes: Optional[str] = None


class CodeManipulation:
    code_url: str = Field(..., description="Path to code respository", title="Code URL")
    code_version: Optional[str] = Field(None, description="Version of the code", title="Code version")
    input_parameters: Dict[str, Any] = Field(..., title="Input parameters")
    output_parameters: Optional[Dict[str, Any]] = Field(..., title="Output parameters")
    outputs: Optional[Dict[str, Any]] = Field(None, description="Output parameters", title="Outputs")


class AnalysisStep(AindModel):
    """Description of a single processing step"""

    analysis_name: str = Field(..., description="Name of the analysis method used", title="Analysis name")
    touch_info: DataTouchInfo = Field(..., description="General information regarding the data manipulation performed")
    analysis_code: CodeManipulation = Field(..., description="Info regarding code used to manipulate data")


class DataProcess(AindModel):
    """Description of a single processing step"""

    name: ProcessName = Field(..., title="Name")
    touch_info: DataTouchInfo = Field(..., description="General information regarding the data manipulation performed")
    analysis_code: CodeManipulation = Field(..., description="Info regarding code used to manipulate data")


class Processing(AindCoreModel):
    """Description of all processes run on data"""

    schema_version: str = Field(
        "0.2.1",
        description="Schema version",
        title="Schema version",
        const=True,
    )
    pipeline_version: Optional[str] = Field(None, description="Version of the pipeline", title="Pipeline version")
    pipeline_url: Optional[str] = Field(None, description="URL to the pipeline code", title="Pipeline URL")
    data_processes: List[AnalysisStep] = Field(..., title="Data processing", unique_items=True)
