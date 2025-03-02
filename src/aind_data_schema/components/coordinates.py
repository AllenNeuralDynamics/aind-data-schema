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


class BrainOrigin(str, Enum):
    """Reference coordinate positions in a brain or atlas"""

    ATLAS_ORIGIN = "Atlas_origin"  # only exists in Atlases
    BREGMA = "Bregma"
    LAMBDA = "Lambda"


class AxisName(str, Enum):
    """Axis name"""

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


class AnatomicalRelative(str, Enum):
    """Relative positions in 3D space"""

    SUPERIOR = "Superior"
    INFERIOR = "Inferior"
    ANTERIOR = "Anterior"
    POSTERIOR = "Posterior"
    LEFT = "Left"
    RIGHT = "Right"
    MEDIAL = "Medial"
    LATERAL = "Lateral"


class RotationDirection(str, Enum):
    """Rotation direction"""

    CW = "Clockwise"
    CCW = "Counter-clockwise"


class FloatAxis(DataModel):
    """Float value and axis"""

    value: float = Field(..., title="Value")
    axis: AxisName = Field(..., title="Axis")


class Scale(DataModel):
    """Values to be vector-multiplied with a 3D position
    """

    scale: List[FloatAxis] = Field(..., title="Scale parameters", min_length=3, max_length=3)


class Position(DataModel):
    """Values to be vector-added to a 3D position"""

    position: List[FloatAxis] = Field(..., title="Position", min_length=3, max_length=3)


class RelativePosition(DataModel):
    """Relative position in 3D space"""

    position: List[AnatomicalRelative] = Field(..., title="Relative position")


class Rotation(DataModel):
    """Set of rotations in 3D space

    Defaults to MIS insertion conventions)

    1. The AP angle, rotating clockwise around ML
    2. The ML angle, rotating clockwise around AP
    3. The rotation angle, rotating counter-clockwise around the object's depth axis
    """

    angles: List[FloatAxis] = Field(..., title="Angles and axes in 3D space", min_length=3, max_length=3)
    rotation_direction: List[RotationDirection] = Field(
        ...,
        title="Rotation directions",
        description="Defined looking in the negative direction of the axis",
        min_length=3,
        max_length=3,
    )
    angles_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class AffineTransformMatrix(DataModel):
    """Definition of an affine transform 3x4 matrix"""

    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )


class CoordinateSpace(DataModel):
    """3D space relative to an animal's brain
    """

    name: str = Field(..., title="Space name")
    origin: BrainOrigin = Field(
        ...,
        title="Origin",
        description="Defines the position of (0,0,0) relative to the brain or atlas"
    )
    orientation: List[AnatomicalDirection] = Field(
        default=[AnatomicalDirection.PA, AnatomicalDirection.LR, AnatomicalDirection.IS],
        title="Axis orientation"
    )
    dimensions: Optional[List[FloatAxis]] = Field(default=None, title="Dimensions", min_length=3, max_length=3)
    resolution: Optional[List[FloatAxis]] = Field(default=None, title="Resolution", min_length=3, max_length=3)

    @model_validator("origin", mode="before")
    def validate_reference_coordinate(cls, v):
        if v['origin'] == BrainOrigin.ATLAS_ORIGIN and cls.__name__ == "CoordinateSpace":
            raise ValueError("CoordinateSpace objects cannot use the atlas origin, "
                             "you should use an anatomical landmark")
        return v


class AtlasSpace(CoordinateSpace):
    """3D space relative to an atlas

    The default Origin of an atlas is the anterior, left, superior corner

    The default orientation follows the right hand rule for AP/SI/LR
    """

    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")
    dimensions: List[FloatAxis] = Field(..., title="Dimensions", min_length=3, max_length=3)
    resolution: List[FloatAxis] = Field(..., title="Resolution", min_length=3, max_length=3)


class AtlasTransformed(AtlasSpace):
    """Transformation from one atlas to another"""

    transforms: List[
        Annotated[
            Union[Position, Rotation, Scale, AffineTransformMatrix, str], Field(discriminator="object_type")
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
    position: Position = Field(..., title="Coordinate in atlas space")
    position_unit: SizeUnit = Field(default=SizeUnit.UM, title="Position unit")

    angles: Optional[Rotation] = Field(default=None, title="Orientation in atlas space")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")


class InVivoCoordinate(DataModel):
    """A coordinate in a brain relative to a reference coordinate

    Angles can be optionally provided
    """

    position: Position = Field(..., title="Coordinates in in vivo space")
    position_unit: SizeUnit = Field(default=SizeUnit.UM, title="Position unit")

    angles: Optional[Rotation] = Field(default=None, title="Orientation in in vivo space")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")


class InVivoSurfaceCoordinate(DataModel):
    """A coordinate in a brain relative to a point on the brain surface, which is itself relative to a reference
    coordinate, usually on the skull

    Angles can be optionally provided
    """

    surface_position: Position = Field(..., title="Surface coordinates (AP/ML, optional SI)")
    surface_position_unit: SizeUnit = Field(default=SizeUnit.UM, title="Position unit")
    depth: Decimal = Field(..., title="Depth from brain surface")
    projection_axis: AxisName = Field(
        default=AxisName.DEPTH,
        title="Surface projection axis",
        description="Axis used to project surface_position onto the brain surface"
    )
    angles: Optional[Rotation] = Field(default=None, title="Orientation in in vivo space")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
