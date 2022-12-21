""" schema describing imaging acquisition """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field

from ..base import AindCoreModel, AindModel


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
    voxel_size: float = Field(..., title="Voxel size (um)")
    volume_size: float = Field(
        ...,
        description="Size of the volume for this dimension.",
        title="Volume size (um)",
    )

    @staticmethod
    def from_direction_code(code, voxel_sizes, volume_sizes) -> List[Axis]:
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
            axis = Axis(
                name=name_lookup[i],
                direction=direction_lookup[c],
                dimension=i,
                voxel_size=voxel_sizes[i],
                volume_size=volume_sizes[i],
            )
            axes.append(axis)

        return axes


class Channel(AindModel):
    """Description of a channel"""

    channel: int = Field(..., title="Channel")
    enabled: Optional[bool] = Field(None, title="Enabled")
    laser_wavelength: int = Field(
        ..., title="Wavelength (nm)", units="nm", ge=300, le=1000
    )
    laser_power: float = Field(..., title="Power (mW)", units="mW", le=2000)
    filter_wheel_index: int = Field(..., title="Filter wheel index")


class Position(AindModel):
    """Description of stage position"""

    x_start_um: float
    x_end_um: float
    x_step_um: float
    y_start_um: float
    y_end_um: float
    y_step_um: float
    z_start_um: float
    z_end_um: float
    z_step_um: float


class Acquisition(AindCoreModel):
    """Description of an imaging acquisition session"""

    version: str = Field(
        "0.3.0", description="schema version", title="Version", const="True"
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    subject_id: int = Field(..., title="Subject ID")
    instrument_id: str = Field(..., title="Instrument ID")
    session_end_time: datetime = Field(..., title="Session end time")
    local_storage_directory: Optional[str] = Field(
        None, title="Local storage directory"
    )
    external_storage_directory: Optional[str] = Field(
        None, title="External storage directory"
    )
    tile_prefix: Optional[str] = Field(
        None,
        description="Zstacks will be named: <tile_prefix>_<x>_<y>_<wavelength>.tiff",
        title="Tile prefix",
    )
    tile_overlap_x: Optional[float] = Field(
        None, title="Tile overlap x (percent)", ge=0, le=100
    )
    tile_overlap_y: Optional[float] = Field(
        None, title="Tile overlap y (percent)", ge=0, le=100
    )
    step_size_z: Optional[float] = Field(None, title="Step size z (um)")
    axes: Optional[List[Axis]] = Field(None, title="Axes", unique_items=True)
    additional_parameters: Optional[str] = Field(
        None, title="Additional parameters"
    )
    positions: List[Position] = Field(
        ..., title="Positions", unique_items=True
    )
    channels: List[Channel] = Field(..., title="Channels", unique_items=True)
    daqs: Optional[List[dict]] = Field(None, title="DAQ", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
