"""" Models related to imaging tiles and their transformations """

from typing import List, Optional

from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel
from aind_data_schema.components.coordinates import CoordinateTransform


class Channel(DataModel):
    """Description of a channel"""

    channel_name: str = Field(..., title="Channel")
    intended_measurement: Optional[str] = Field(default=None, title="Intended measurement",
                                                description="What signal is this channel measuring")
    detector_name: str = Field(..., title="Detector name", description="Must match device name")
    additional_device_names: Optional[List[str]] = Field(default=None, title="Additional device names")
    # excitation
    light_sources: List[str] = Field(..., title="Light sources")
    excitation_filters: Optional[List[str]] = Field(default=None, title="Excitation filters")
    # emission
    emission_filters: Optional[List[str]] = Field(default=None, title="Emission filter names")


class SlapChannel(Channel):
    """Description of a channel for Slap"""

    dilation: Optional[int] = Field(default=None, title="Dilation (pixels)")
    dilation_unit: Optional[SizeUnit] = Field(default=None, title="Dilation unit")
    description: Optional[str] = Field(default=None, title="Description")
    # TODO: dilation and unit might need to be required here


class Tile(DataModel):
    """Description of an image tile"""

    coordinate_transform: CoordinateTransform = Field(..., title="Tile coordinate transformations")
    file_name: Optional[str] = Field(default=None, title="File name")
    imaging_angle: int = Field(default=0, title="Imaging angle")
    imaging_angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Imaging angle unit")
    tile_start_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Tile acquisition start time")
    tile_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Tile acquisition end time")
    notes: Optional[str] = Field(default=None, title="Notes")


class SPIMChannel(Channel):
    """Description of a light sheet channel"""

    tiles: List[Tile] = Field(..., title="Tiles")

