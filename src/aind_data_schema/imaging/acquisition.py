""" schema describing imaging acquisition """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel, EnumSubset
from aind_data_schema.device import SizeUnit
from aind_data_schema.imaging.tile import AcquisitionTile
from aind_data_schema.processing import ProcessName


class AxisName(Enum):
    """Image axis name"""

    X = "X"
    Y = "Y"
    Z = "Z"


class Direction(Enum):
    """Anatomical direction name"""

    LR = "Left_to_right"
    RL = "Right_to_left"
    AP = "Anterior_to_posterior"
    PA = "Posterior_to_anterior"
    IS = "Inferior_to_superior"
    SI = "Superior_to_inferior"
    OTHER = "Other"


class Axis(AindModel):
    """Description of an image axis"""

    name: AxisName = Field(..., title="Name")
    dimension: int = Field(
        ...,
        description="Reference axis number for stitching",
        title="Dimension",
    )
    direction: Direction = Field(
        ...,
        description="Tissue direction as the value of axis increases. If Other describe in notes.",
    )
    unit: SizeUnit = Field(SizeUnit.UM, title="Axis physical units")

    @staticmethod
    def from_direction_code(code) -> List[Axis]:
        """Convert direction codes like 'RAS' or 'PLA' into a set of axis objects"""
        direction_lookup = {
            "L": Direction.LR,
            "R": Direction.RL,
            "A": Direction.AP,
            "P": Direction.PA,
            "I": Direction.IS,
            "S": Direction.SI,
        }

        name_lookup = [AxisName.X, AxisName.Y, AxisName.Z]

        axes = []
        for i, c in enumerate(code):
            axis = Axis(name=name_lookup[i], direction=direction_lookup[c], dimension=i)
            axes.append(axis)

        return axes


class Immersion(AindModel):
    """Description of immersion media"""

    medium: str = Field(..., title="Immersion medium")
    refractive_index: Decimal = Field(..., title="Index of refraction")


class ProcessingSteps(AindModel):
    """Description of downstream processing steps"""

    channel_name: str = Field(..., title="Channel name")
    process_name: List[
        EnumSubset[
            ProcessName.IMAGE_IMPORTING,
            ProcessName.IMAGE_BACKGROUND_SUBTRACTION,
            ProcessName.IMAGE_CELL_SEGMENTATION,
            ProcessName.IMAGE_DESTRIPING,
            ProcessName.IMAGE_THRESHOLDING,
            ProcessName.IMAGE_TILE_ALIGNMENT,
            ProcessName.IMAGE_TILE_FUSING,
            ProcessName.IMAGE_TILE_PROJECTION,
            ProcessName.FILE_CONVERSION,
        ]
    ]


class Acquisition(AindCoreModel):
    """Description of an imaging acquisition session"""

    schema_version: str = Field("0.4.6", description="schema version", title="Version", const=True)
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    specimen_id: str = Field(..., title="Specimen ID")
    subject_id: Optional[str] = Field(None, title="Subject ID")
    instrument_id: str = Field(..., title="Instrument ID")
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    session_type: Optional[str] = Field(None, title="Session type")
    tiles: List[AcquisitionTile] = Field(..., title="Acquisition tiles")
    axes: List[Axis] = Field(..., title="Acquisition axes")
    chamber_immersion: Immersion = Field(..., title="Acquisition chamber immersion data")
    sample_immersion: Optional[Immersion] = Field(None, title="Acquisition sample immersion data")
    active_objectives: Optional[List[str]] = Field(None, title="List of objectives used in this acquisition.")
    local_storage_directory: Optional[str] = Field(None, title="Local storage directory")
    external_storage_directory: Optional[str] = Field(None, title="External storage directory")
    processing_steps: Optional[List[ProcessingSteps]] = Field(
        None,
        title="Processing steps",
        description="List of downstream processing steps planned for each channel",
    )
    notes: Optional[str] = Field(None, title="Notes")
