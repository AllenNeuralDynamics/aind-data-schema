"""" Models related to imaging tiles and their transformations """

from typing import Annotated, List, Optional, Union

from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel
from aind_data_schema.components.configs import LaserConfig, LightEmittingDiodeConfig
from aind_data_schema.components.coordinates import CoordinateTransform


class Channel(DataModel):
    """Description of a channel"""

    channel_name: str = Field(..., title="Channel")
    detector_name: str = Field(..., title="Detector name", description="Must match device name")
    additional_device_names: Optional[List[str]] = Field(default=[], title="Additional device names")
    # excitation
    light_sources: List[
        Annotated[
            Union[
                LightEmittingDiodeConfig,
                LaserConfig,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(..., title="Light source configurations")
    # emission
    filters: List[str] = Field(..., title="Filter names")


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


class AcquisitionTile(Tile):
    """Description of acquisition tile"""

    channel: Channel = Field(..., title="Channel")
    notes: Optional[str] = Field(default=None, title="Notes")
    imaging_angle: int = Field(default=0, title="Imaging angle")
    imaging_angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Imaging angle unit")
    acquisition_start_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Acquisition start time")
    acquisition_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Acquisition end time")
