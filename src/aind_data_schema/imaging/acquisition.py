""" schema describing imaging acquisition """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


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


class Axis(BaseModel):
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


class Laser(BaseModel):
    """Description of a laser"""

    name: str = Field(..., title="Name")
    channel: int = Field(..., title="Channel")
    enabled: Optional[bool] = Field(None, title="Enabled")
    wavelength: int = Field(..., title="Wavelength (nm)")
    power: float = Field(..., title="Power")


class Position(BaseModel):
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


class Acquisition(BaseModel):
    """Description of an imaging acquisition session"""

    version: str = Field(
        "0.1.1", description="schema version", title="Version", const="True"
    )
    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/aind-data-schema/blob/main/src/aind-data-schema/imaging/acquisition.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    specimen_id: int = Field(..., title="Specimen ID")
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
        None, title="Tile overlap x (percent)"
    )
    tile_overlap_y: Optional[float] = Field(
        None, title="Tile overlap y (percent)"
    )
    step_size_z: Optional[float] = Field(None, title="Step size z (um)")
    axes: Optional[List[Axis]] = Field(None, title="Axes", unique_items=True)
    additional_parameters: Optional[str] = Field(
        None, title="Additional parameters"
    )
    positions: List[Position] = Field(
        ..., title="Positions", unique_items=True
    )
    lasers: List[Laser] = Field(..., title="Lasers", unique_items=True)
    daqs: Optional[List[dict]] = Field(None, title="DAQ", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
