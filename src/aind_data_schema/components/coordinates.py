"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field, model_validator
from typing_extensions import Annotated

from aind_data_schema.base import DataModel


class AtlasName(str, Enum):
    """Atlas name"""

    CCF = "CCF"
    CUSTOM = "Custom"


class ReferenceCoordinate(str, Enum):
    """Reference coordinate position"""

    ORIGIN = "Origin"  # only exists in Atlases
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


class Scaling(DataModel):
    """Values to be vector-multiplied with a 3D position, equivalent to the diagonals of a 3x3 transform matrix.
    Represents voxel spacing if used as the first applied coordinate transform.
    """

    scale: Vector3 = Field(..., title="Scale parameters", min_length=3, max_length=3)


class Translation(DataModel):
    """Values to be vector-added to a 3D position. Often needed to specify a device or tile's origin."""

    translation: Vector3 = Field(..., title="Translatino parameters", min_length=3, max_length=3)


class Rotation(DataModel):
    """Set of rotations in 3D space

    Defaults to MIS insertion conventions)

    1. The AP angle, rotating clockwise around ML
    2. The ML angle, rotating clockwise around AP
    3. The rotation angle, rotating counter-clockwise around the object's depth axis
    """

    angles: Vector3 = Field(..., title="Angles in 3D space")
    rotation_axes: List[AxisName] = Field(default=[AxisName.ML, AxisName.AP, AxisName.DEPTH], title="Rotation axes")
    rotation_direction: List[RotationDirection] = Field(
        default=[RotationDirection.CW, RotationDirection.CW, RotationDirection.CW], title="Rotation directions"
    )
    angles_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class AffineTransform(DataModel):
    """Values to be vector-added to a 3D position. Often needed to specify a Tile's origin."""

    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )


class CoordinateSpace(DataModel):
    """3D space relative to an animal's brain
    """

    name: str = Field(..., title="Space name")
    reference_coordinate: ReferenceCoordinate = Field(
        ...,
        title="Reference coordinate",
        description="Defines the position of (0,0,0) in the space"
    )
    orientation: List[AnatomicalDirection] = Field(
        default=[AnatomicalDirection.PA, AnatomicalDirection.LR, AnatomicalDirection.IS],
        title="Axis orientation"
    )
    dimensions: Optional[Vector3] = Field(default=None, title="Dimensions")
    resolution: Optional[Vector3] = Field(default=None, title="Resolution")

    @model_validator("reference_coordinate", mode="before")
    def validate_reference_coordinate(cls, v):
        if v['reference_coordinate'] == ReferenceCoordinate.ORIGIN and cls.__name__ == "CoordinateSpace":
            raise ValueError("CoordinateSpace objects cannot have an origin reference coordinate, you should use an anatomical landmark")
        return v


class AtlasSpace(CoordinateSpace):
    """3D space relative to an atlas

    The default Origin of an atlas is the anterior, left, superior corner

    The default orientation follows the right hand rule for AP/SI/LR
    """

    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")
    dimensions: Vector3 = Field(..., title="Dimensions")
    resolution: Vector3 = Field(..., title="Resolution")


class AtlasTransformed(AtlasSpace):
    """Transformation from one atlas to another"""

    transforms: List[
        Annotated[
            Union[Translation, Rotation, Scaling, str], Field(discriminator="object_type")
        ]
    ] = Field(
        ...,
        title="Transformations from in vivo to atlas space",
        description="Non-linear transformations should be stored in a relative file path",
    )


class AtlasCoordinate(DataModel):
    """A coordinate in an atlas, can be relative to the atlas origin or a standard reference coordinate

    Angles can be optionally provided
    """

    atlas: Annotated[Union[AtlasSpace, AtlasTransformed], Field(title="Atlas definition", discriminator="object_type")]
    coordinates: Vector3 = Field(..., title="Coordinate in atlas space")
    angles: Optional[Rotation] = Field(default=None, title="Orientation in atlas space")


class InVivoCoordinate(DataModel):
    """A coordinate in a brain relative to a reference coordinate

    Angles can be optionally provided
    """

    space: CoordinateSpace = Field(..., title="In vivo space definition")
    coordinates: Vector3 = Field(..., title="Coordinates in in vivo space")

    angles: Optional[Rotation] = Field(default=None, title="Orientation in in vivo space")


class InVivoSurfaceCoordinate(DataModel):
    """A coordinate in a brain relative to a point on the brain surface, which is itself relative to a reference
    coordinate on the skull

    Angles can be optionally provided
    """

    space: CoordinateSpace = Field(..., title="In vivo space definition")
    surface_coordinates: Vector2 = Field(..., title="Surface coordinates (AP/ML)")
    depth: Decimal = Field(..., title="Depth from surface")
    projection_axis: AxisName = Field(default=AxisName.DEPTH, title="Surface projection axis", description="Axis used to project AP/ML coordinate onto surface")

    angles: Optional[Rotation] = Field(default=None, title="Orientation in in vivo space")
