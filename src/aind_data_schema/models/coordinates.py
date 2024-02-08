"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional

from pydantic import Field

from aind_data_schema.base import AindModel
from aind_data_schema.models.units import AngleUnit, SizeUnit


class CcfVersion(str, Enum):
    """CCF version"""

    CCFv3 = "CCFv3"


class Origin(str, Enum):
    """Coordinate reference origin point"""

    BREGMA = "Bregma"
    LAMBDA = "Lambda"
    OTHER = "Other (see Notes)"


class AxisName(str, Enum):
    """Image axis name"""

    X = "X"
    Y = "Y"
    Z = "Z"


class Direction(str, Enum):
    """Anatomical direction name"""

    LR = "Left_to_right"
    RL = "Right_to_left"
    AP = "Anterior_to_posterior"
    PA = "Posterior_to_anterior"
    IS = "Inferior_to_superior"
    SI = "Superior_to_inferior"
    OTHER = "Other (see Notes)"


class Size2d(AindModel):
    """2D size of an object"""

    width: int = Field(..., title="Width")
    height: int = Field(..., title="Height")
    unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")


class Size3d(AindModel):
    """3D size of an object"""

    width: int = Field(..., title="Width")
    length: int = Field(..., title="Length")
    height: int = Field(..., title="Height")
    unit: SizeUnit = Field(SizeUnit.M, title="Size unit")


class Orientation3d(AindModel):
    """3D orientation of an object"""

    pitch: Decimal = Field(..., title="Angle pitch", ge=0, le=360)
    yaw: Decimal = Field(..., title="Angle yaw", ge=0, le=360)
    roll: Decimal = Field(..., title="Angle roll", ge=0, le=360)
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class ModuleOrientation2d(AindModel):
    """2D module orientation of an object"""

    arc_angle: Decimal = Field(..., title="Arc angle")
    module_angle: Decimal = Field(..., title="Module angle")
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class ModuleOrientation3d(AindModel):
    """3D module orientation of an object"""

    arc_angle: Decimal = Field(..., title="Arc angle")
    module_angle: Decimal = Field(..., title="Module angle")
    rotation_angle: Decimal = Field(..., title="Rotation angle")
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class Coordinates3d(AindModel):
    """Coordinates in a 3D grid"""

    x: Decimal = Field(..., title="Position X")
    y: Decimal = Field(..., title="Position Y")
    z: Decimal = Field(..., title="Position Z")
    unit: SizeUnit = Field(SizeUnit.UM, title="Position unit")


class CcfCoords(AindModel):
    """Coordinates in CCF template space"""

    ml: Decimal = Field(..., title="ML")
    ap: Decimal = Field(..., title="AP")
    dv: Decimal = Field(..., title="DV")
    unit: SizeUnit = Field(SizeUnit.UM, title="Coordinate unit")
    ccf_version: CcfVersion = Field(CcfVersion.CCFv3, title="CCF version")


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
    """Values to be vector-added to a 3D position."""

    type: Literal["translation"] = "translation"
    translation: List[Decimal] = Field(..., title="3D translation parameters", min_length=3, max_length=3)


class Rotation3dTransform(CoordinateTransform):
    """Values to be vector-added to a 3D position."""

    type: Literal["rotation"] = "rotation"
    rotation: List[Decimal] = Field(..., title="3D rotation matrix values (3x3) ", min_length=9, max_length=9)


class Affine3dTransform(CoordinateTransform):
    """Values to be vector-added to a 3D position."""

    type: Literal["affine"] = "affine"
    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )


class Axis(AindModel):
    """Description of an axis"""

    name: AxisName = Field(..., title="Axis")
    direction: str = Field(..., title="Direction as the value of axis increases.")


class AnatomicalAxis(Axis):
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


class RelativePosition(AindModel):
    """Position and rotation of a device in a rig or instrument"""

    device_position: Translation3dTransform = Field(..., title="Device position")
    position_unit: SizeUnit = Field(SizeUnit.MM, title="Position unit")
    device_rotation: Rotation3dTransform = Field(..., title="Device rotation")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")
    device_reference_point: str = Field(
        ..., title="Device reference point",
        description="Reference point on device for position information"
        )
    device_axes: List[Axis] = Field(..., title="Device axes", min_length=3, max_length=3)
    notes: Optional[str] = Field(None, title="Notes")
