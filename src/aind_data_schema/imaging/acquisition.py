""" schema describing imaging acquisition """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

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
            axis = Axis(
                name=name_lookup[i], direction=direction_lookup[c], dimension=i
            )
            axes.append(axis)

        return axes


class Channel(AindModel):
    """Description of a channel"""

    channel_name: str = Field(..., title="Channel")
    laser_wavelength: int = Field(
        ..., title="Wavelength (nm)", units="nm", ge=300, le=1000
    )
    laser_power: float = Field(..., title="Power (mW)", units="mW", le=2000)
    filter_wheel_index: int = Field(..., title="Filter wheel index")


class TilePosition(AindModel):
    """Description of stage position"""

    x_start: float = Field(..., title="X start")
    x_end: float = Field(..., title="X end")
    x_step: float = Field(..., title="X step")
    y_start: float = Field(..., title="Y start")
    y_end: float = Field(..., title="Y end")
    y_step: float = Field(..., title="Y step")
    z_start: float = Field(..., title="Z start")
    z_end: float = Field(..., title="Z end")
    z_step: float = Field(..., title="Z step")
    unit: str = Field("μm", title="Tile position units", const=True)


class VoxelSize(AindModel):
    """Description of the size of a 3D grid cell"""

    size_x: float = Field(..., title="X size")
    size_y: float = Field(..., title="Y size")
    size_z: float = Field(..., title="Z size")
    unit: str = Field("μm", title="size units", const=True)


class Tile(AindModel):
    """Description of an image tile"""

    voxel_size: VoxelSize = Field(..., title="Voxel size")
    position: TilePosition = Field(..., title="Tile position")
    channel: Channel = Field(..., title="Channel")
    daq_params: Dict = Field(..., title="DAQ parameters")
    file_name: Optional[str] = Field(None, title="File name")
    notes: Optional[str] = Field(None, title="Notes")


class Acquisition(AindCoreModel):
    """Description of an imaging acquisition session"""

    version: str = Field(
        "0.4.0", description="schema version", title="Version", const="True"
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    subject_id: str = Field(..., title="Subject ID")
    instrument_id: str = Field(..., title="Instrument ID")
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    tiles: List[Tile] = Field(..., title="Acquisition tiles")
    axes: List[Axis] = Field(..., title="Acquisition axes")
    local_storage_directory: Optional[str] = Field(
        None, title="Local storage directory"
    )
    external_storage_directory: Optional[str] = Field(
        None, title="External storage directory"
    )
