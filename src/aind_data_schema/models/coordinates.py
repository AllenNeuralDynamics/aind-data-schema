"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import Field

from aind_data_schema.base import AindModel
from aind_data_schema.models.units import AngleUnit, SizeUnit


class CcfVersion(str, Enum):
    """CCF version"""

    CCFv3 = "CCFv3"


class RelativePosition(AindModel):
    """Set of 6 values describing relative position on a rig"""

    pitch: Optional[Decimal] = Field(None, title="Angle pitch (deg)", ge=0, le=360)
    yaw: Optional[Decimal] = Field(None, title="Angle yaw (deg)", ge=0, le=360)
    roll: Optional[Decimal] = Field(None, title="Angle roll (deg)", ge=0, le=360)
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")

    x: Optional[Decimal] = Field(None, title="Position X (mm)")
    y: Optional[Decimal] = Field(None, title="Position Y (mm)")
    z: Optional[Decimal] = Field(None, title="Position Z (mm)")
    position_unit: SizeUnit = Field(SizeUnit.MM, title="Position unit")

    coordinate_system: Optional[str] = Field(None, title="Description of the coordinate system used")


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
