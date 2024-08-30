"""" Models related to imaging tiles and their transformations """

from typing import List, Optional, Union

from aind_data_schema_models.units import AngleUnit, PowerUnit, SizeUnit
from pydantic import Field
from typing_extensions import Annotated

from aind_data_schema.base import AindModel, AwareDatetimeWithDefault
from aind_data_schema.components.coordinates import (
    Affine3dTransform,
    Rotation3dTransform,
    Scale3dTransform,
    Translation3dTransform,
)


class Channel(AindModel):
    """Description of a channel"""

    channel_name: str = Field(..., title="Channel")
    light_source_name: str = Field(..., title="Light source name", description="Must match device name")
    filter_names: List[str] = Field(..., title="Filter names", description="Must match device names")
    detector_name: str = Field(..., title="Detector name", description="Must match device name")
    additional_device_names: List[str] = Field(default=[], title="Additional device names")
    # excitation
    excitation_wavelength: int = Field(..., title="Wavelength", ge=300, le=1000)
    excitation_wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Laser wavelength unit")
    excitation_power: float = Field(..., title="Laser power", le=2000)
    excitation_power_unit: PowerUnit = Field(default=PowerUnit.MW, title="Laser power unit")
    # emission
    filter_wheel_index: int = Field(..., title="Filter wheel index")
    # dilation
    dilation: Optional[int] = Field(default=None, title="Dilation (pixels)")
    dilation_unit: SizeUnit = Field(default=SizeUnit.PX, title="Dilation unit")
    description: Optional[str] = Field(default=None, title="Description")


class Tile(AindModel):
    """Description of an image tile"""

    coordinate_transformations: List[
        Annotated[
            Union[
                Scale3dTransform,
                Translation3dTransform,
                Rotation3dTransform,
                Affine3dTransform,
            ],
            Field(discriminator="type"),
        ]
    ] = Field(..., title="Tile coordinate transformations")
    file_name: Optional[str] = Field(default=None, title="File name")


class AcquisitionTile(Tile):
    """Description of acquisition tile"""

    channel: Channel = Field(..., title="Channel")
    notes: Optional[str] = Field(default=None, title="Notes")
    imaging_angle: int = Field(default=0, title="Imaging angle")
    imaging_angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Imaging angle unit")
    acquisition_start_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Acquisition start time")
    acquisition_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Acquisition end time")
