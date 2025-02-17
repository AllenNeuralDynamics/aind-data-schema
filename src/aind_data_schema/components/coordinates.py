"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field
from typing_extensions import Annotated

from aind_data_schema.base import DataModel


class AtlasName(str, Enum):
    """Atlas name"""

    CCF = "CCF"
    CUSTOM = "Custom"


class ReferenceCoordinate(str, Enum):
    """Reference coordinate position"""

    BREGMA = "Bregma"
    LAMBDA = "Lambda"


class AxisName(str, Enum):
    """Image axis name"""

    X = "X"
    Y = "Y"
    Z = "Z"
    AP = "AP"
    ML = "ML"
    SI = "SI"
    DEPTH = "Depth"


class AnatomicalDirection(str, Enum):
    """Anatomical direction name"""

    LR = "Left_to_right"
    RL = "Right_to_left"
    AP = "Anterior_to_posterior"
    PA = "Posterior_to_anterior"
    IS = "Inferior_to_superior"
    SI = "Superior_to_inferior"
    OTHER = "Other"


class RotationDirection(str, Enum):
    """Rotation direction"""

    CW = "Clockwise"
    CCW = "Counter-clockwise"


class Scale3dTransform(DataModel):
    """Values to be vector-multiplied with a 3D position, equivalent to the diagonals of a 3x3 transform matrix.
    Represents voxel spacing if used as the first applied coordinate transform.
    """

    data_type: Literal["scale"] = "scale"
    scale: List[Decimal] = Field(..., title="3D scale parameters", min_length=3, max_length=3)


# TODO: rename "Translation"
class Translation3dTransform(DataModel):
    """Values to be vector-added to a 3D position. Often needed to specify a device or tile's origin."""

    data_type: Literal["translation"] = "translation"
    translation: List[Decimal] = Field(..., title="3D translation parameters", min_length=3, max_length=3)


# TODO: rename "Rotatoin"
class Rotation3dTransform(DataModel):
    """Values to be vector-added to a 3D position. Often needed to specify a device or tile's origin."""

    data_type: Literal["rotation"] = "rotation"
    rotation: List[Decimal] = Field(..., title="3D rotation matrix values (3x3) ", min_length=9, max_length=9)


# TODO: rename "etc"
class Affine3dTransform(DataModel):
    """Values to be vector-added to a 3D position. Often needed to specify a Tile's origin."""

    data_type: Literal["affine"] = "affine"
    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )


class Vector2(DataModel):
    """XY vector"""

    x: Decimal = Field(..., title="X")
    y: Decimal = Field(..., title="Y")
    unit: SizeUnit = Field(..., title="Vector unit")


class Vector3(DataModel):
    """XYZ vector"""

    x: Decimal = Field(..., title="X")
    y: Decimal = Field(..., title="Y")
    z: Decimal = Field(..., title="Z")
    unit: SizeUnit = Field(..., title="Vector unit")


class CoordinateSpace(DataModel):
    """3D space definition
    """

    data_type: Literal["space"] = "space"
    name: str = Field(..., title="Space name")
    dimensions: Vector3 = Field(..., title="Dimensions")
    resolution: Vector3 = Field(..., title="Resolution")
    reference_coordinate: Vector3 = Field(default_factory=lambda: Vector3(x=0, y=0, z=0, unit=SizeUnit.PX),
                                          title="Reference coordinate")
    orientation: List[AnatomicalDirection] = Field(
        default=[AnatomicalDirection.AP, AnatomicalDirection.SI, AnatomicalDirection.LR], title="Atlas orientation"
    )


class AtlasSpace(CoordinateSpace):
    """Atlas definition

    The default Origin of an atlas is the anterior, left, superior corner

    The default orientation follows the right hand rule for AP/SI/LR
    """

    data_type: Literal["atlas_space"] = "atlas_space"
    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")


class AtlasTransformed(AtlasSpace):
    """Transformation from one atlas to another"""

    data_type: Literal["atlas_transformed"] = "atlas_transformed"
    transforms: List[
        Annotated[
            Union[Translation3dTransform, Rotation3dTransform, Scale3dTransform, str], Field(discriminator="type")
        ]
    ] = Field(
        ...,
        title="Transformations from in vivo to atlas space",
        description="Non-linear transformations should be stored in a relative file path",
    )


class Angles(DataModel):
    """Set of rotations in 3D space

    By default, angles are defined by three rotations:
        1. The AP angle, rotating clockwise around ML
        2. The ML angle, rotating clockwise around AP
        3. The rotation angle, rotating clockwise around the object's depth axis
    """

    angles: Vector3 = Field(..., title="Angles in 3D space")
    rotation_axes: List[AxisName] = Field(default=[AxisName.ML, AxisName.AP, AxisName.DEPTH], title="Rotation axes")
    rotation_direction: List[RotationDirection] = Field(
        default=[RotationDirection.CW, RotationDirection.CW, RotationDirection.CW], title="Rotation directions"
    )
    angles_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class AtlasCoordinate(DataModel):
    """A coordinate in an atlas, can be relative to the atlas origin or a standard reference coordinate

    Angles can be optionally provided
    """

    atlas: Annotated[Union[AtlasSpace, AtlasTransformed], Field(title="Atlas definition", discriminator="data_type")]
    coordinates: Vector3 = Field(..., title="Coordinate in atlas space")
    reference_coordinate: Vector3 = Field(default_factory=lambda: Vector3(x=0, y=0, z=0, unit=SizeUnit.PX),
                                          title="Reference coordinate")
    angles: Optional[Angles] = Field(default=None, title="Orientation in atlas space")


class InVivoCoordinate(DataModel):
    """A coordinate in a brain relative to a reference coordinate on the skull"""

    coordinates: Vector3 = Field(..., title="Coordinates in in vivo space")
    reference_coordinate: ReferenceCoordinate = Field(..., title="Reference coordinate")
    angles: Optional[Angles] = Field(default=None, title="Orientation in in vivo space")


class InVivoSurfaceCoordinate(DataModel):
    """A coordinate in a brain relative to a point on the brain surface, which is itself relative to a reference
    coordinate on the skull"""

    surface_coordinates: Vector2 = Field(..., title="Surface coordinates (AP/ML)")
    depth: Decimal = Field(..., title="Depth from surface")
    projection_axis: AxisName = Field(AxisName.SI, title="Axis used to project AP/ML coordinate onto surface")
    reference_coordinate: ReferenceCoordinate = Field(..., title="Reference coordinate")
    angles: Optional[Angles] = Field(default=None, title="Orientation in in vivo space")
