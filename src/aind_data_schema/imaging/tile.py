"""" Models related to imaging tiles and their transformations """

from decimal import Decimal
from typing import List, Literal, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindModel
from aind_data_schema.models.units import AngleUnit, PowerUnit, SizeUnit


class Channel(AindModel):
    """Description of a channel"""

    channel_name: str = Field(..., title="Channel")
    light_source_name: str = Field(..., title="Light source name", description="Must match device name")
    filter_names: List[str] = Field(..., title="Filter names", description="Must match device names")
    detector_name: str = Field(..., title="Detector name", description="Must match device name")
    additional_device_names: List[str] = Field(default=[], title="Additional device names")
    # excitation
    excitation_wavelength: int = Field(..., title="Wavelength", ge=300, le=1000)
    excitation_wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Laser wavelength unit")
    excitation_power: float = Field(..., title="Laser power", le=2000)
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Laser power unit")
    # emission
    filter_wheel_index: int = Field(..., title="Filter wheel index")
    # dilation
    dilation: Optional[int] = Field(None, title="Dilation (pixels)")
    dilation_unit: SizeUnit = Field(SizeUnit.PX, title="Dilation unit")
    description: Optional[str] = Field(None, title="Description")


class CoordinateTransform(AindModel):
    """Generic base class for coordinate transform subtypes"""

    type: str = Field(..., title="transformation type")


class Scale3dTransform(CoordinateTransform):
    """Values to be vector-multiplied with a 3D position, equivalent to the diagonals of a 3x3 transform matrix.
    Represents voxel spacing if used as the first applied coordinate transform.
    """

    type: Literal["scale"] = "scale"
    scale: List[Decimal] = Field(..., title="3D scale parameters", min_length=3, max_length=3)


class Translation3dTransform(CoordinateTransform):
    """Values to be vector-added to a 3D position. Often needed to specify a Tile's origin."""

    type: Literal["translation"] = "translation"
    translation: List[Decimal] = Field(..., title="3D translation parameters", min_length=3, max_length=3)


class Rotation3dTransform(CoordinateTransform):
    """Values to be vector-added to a 3D position. Often needed to specify a Tile's origin."""

    type: Literal["rotation"] = "rotation"
    rotation: List[Decimal] = Field(..., title="3D rotation matrix values (3x3) ", min_length=9, max_length=9)


class Affine3dTransform(CoordinateTransform):
    """Values to be vector-added to a 3D position. Often needed to specify a Tile's origin."""

    type: Literal["affine"] = "affine"
    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )


class Tile(AindModel):
    """Description of an image tile"""

    coordinate_transformations: List[
        Union[
            Scale3dTransform,
            Translation3dTransform,
            Rotation3dTransform,
            Affine3dTransform,
        ]
    ] = Field(..., title="Tile coordinate transformations", discriminator="type")
    file_name: Optional[str] = Field(None, title="File name")


class AcquisitionTile(Tile):
    """Description of acquisition tile"""

    channel: Channel = Field(..., title="Channel")
    notes: Optional[str] = Field(None, title="Notes")
    imaging_angle: int = Field(0, title="Imaging angle")
    imaging_angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Imaging angle unit")
