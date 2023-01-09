""" schema describing imaging acquisition """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field
from pydantic.types import conlist

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
    unit: str = Field("micrometer", title="Axis physical units")

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


class Channel(AindModel):
    """Description of a channel"""

    channel_name: str = Field(..., title="Channel")
    laser_wavelength: int = Field(..., title="Wavelength", ge=300, le=1000)
    laser_wavelength_unit: str = Field("nanometer", title="Laser wavelength unit")
    laser_power: float = Field(..., title="Laser power", le=2000)
    laser_power_unit: float = Field("milliwatt", title="Laser power unit")
    filter_wheel_index: int = Field(..., title="Filter wheel index")


class Scale3dTransform(AindModel):
    """Values to be vector-multiplied with a 3D position, equivalent to the diagonals of a 3x3 transform matrix.
    Represents voxel spacing if used as the first applied coordinate transform.
    """

    type: str = Field("scale", title="transformation type")
    scale: conlist(float, min_items=3, max_items=3) = Field(..., title="3D scale parameters")


class Translation3dTransform(AindModel):
    """Values to be vector-added to a 3D position. Often needed to specify a Tile's origin."""

    type: str = Field("translation", title="transformation type")
    translation: conlist(float, min_items=3, max_items=3) = Field(..., title="3D translation parameters")


class Tile(AindModel):
    """Description of an image tile"""

    coordinate_transformations: List[Union[Scale3dTransform, Translation3dTransform]] = Field(
        ..., title="Tile coordinate transformations"
    )
    channel: Channel = Field(..., title="Channel")
    file_name: Optional[str] = Field(None, title="File name")
    notes: Optional[str] = Field(None, title="Notes")
    imaging_angle: int = Field(0, title="Imaging angle")
    imaging_angle_unit: str = Field("degree", title="Imaging angle unit")


class Immersion(AindModel):
    """Description of immersion media"""

    medium: str = Field(..., title="Immersion medium")
    refractive_index: float = Field(..., title="Index of refraction")


class Acquisition(AindCoreModel):
    """Description of an imaging acquisition session"""

    version: str = Field("0.4.0", description="schema version", title="Version", const=True)
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
    chamber_immersion: Immersion = Field(..., title="Acquisition chamber immersion data")
    sample_immersion: Optional[Immersion] = Field(None, title="Acquisition sample immersion data")
    active_objectives: Optional[List[str]] = Field(None, title="List of objectives used in this acquisition.")
    local_storage_directory: Optional[str] = Field(None, title="Local storage directory")
    external_storage_directory: Optional[str] = Field(None, title="External storage directory")
