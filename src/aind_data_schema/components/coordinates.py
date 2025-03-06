"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field
from typing_extensions import Annotated

from aind_data_schema.base import DataModel


class AtlasName(str, Enum):
    """Atlas name"""

    CCF = "CCF"
    CUSTOM = "Custom"


class Origin(str, Enum):
    """Origin positions in a brain or atlas"""

    ORIGIN = "Origin"  # only exists in Atlases / Images
    BREGMA = "Bregma"
    LAMBDA = "Lambda"
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"
    C7 = "C7"


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
    """Linked value and axis"""

    value: float = Field(..., title="Value")
    axis: AxisName = Field(..., title="Axis")


class Axis(DataModel):
    """Linked direction and axis"""

    name: AxisName = Field(..., title="Axis")
    direction: AnatomicalDirection = Field(..., title="Direction")


class Scale(DataModel):
    """Scale"""

    scale: List[FloatAxis] = Field(..., title="Scale parameters")


class Translation(DataModel):
    """Translation"""

    translation: List[FloatAxis] = Field(..., title="Translation parameters")


class Rotation(DataModel):
    """Rotation"""

    angles: List[FloatAxis] = Field(..., title="Angles and axes in 3D space")
    order: List[AxisName] = Field(
        default=[AxisName.AP, AxisName.ML, AxisName.SI],
        title="Rotation order",
        description="Order of rotation axes"
    )
    rotation_direction: List[RotationDirection] = Field(
        ...,
        title="Rotation directions",
        description="CCW for right-hand rule. Defined looking in the negative direction of the axis",
    )


class AffineTransformMatrix(DataModel):
    """Definition of an affine transform 3x4 matrix"""

    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )


class Point(DataModel):
    """Point in a coordinate system """

    position: List[FloatAxis] = Field(..., title="Position")


class RelativePosition(DataModel):
    """Relative position in a coordinate system"""

    position: List[AnatomicalRelative] = Field(..., title="Relative position")


class CoordinateSystem(DataModel):
    """Definition of a coordinate system relative to a brain
    """

    name: str = Field(..., title="Space name")
    origin: Origin = Field(
        ...,
        title="Origin",
        description="Defines the position of (0,0,0) relative to the brain or atlas"
    )
    axes: List[Axis] = Field(..., title="Axis names", description="Axis names and directions")
    axes_unit: SizeUnit = Field(..., title="Axis unit")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")


class Atlas(CoordinateSystem):
    """Definition an atlas
    """

    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")
    dimensions: List[FloatAxis] = Field(..., title="Dimensions")
    resolution: List[FloatAxis] = Field(..., title="Resolution")


class Transform(DataModel):
    """Affine and non-linear transformations"""
    trasnform: List[
        Annotated[
            Union[Translation, Rotation, Scale, AffineTransformMatrix, str], Field(discriminator="object_type")
        ]
    ] = Field(
        ...,
        title="Transformations from in vivo to atlas space",
        description="Non-linear transformations should be stored in a relative file path",
    )


class CoordinateTransform(DataModel):
    """Transformation from one CoordinateSystem to another"""
    input: CoordinateSystem = Field(..., title="Input coordinate system")
    output: CoordinateSystem = Field(..., title="Output coordinate system")
    transform: Transform = Field(..., title="Transformation from input to output coordinate system")


class Coordinate(DataModel):
    """A coordinate in a brain (CoordinateSpace) or atlas (AtlasSpace)

    Angles can be optionally provided
    """

    position: Point = Field(..., title="Coordinates in in vivo space")
    angles: Optional[Rotation] = Field(default=None, title="Orientation in in vivo space")


class SurfaceCoordinate(Coordinate):
    """A coordinate relative to a point on the brain surface, which is itself relative to the CoordinateSpace origin

    Angles can be optionally provided
    """

    depth: Decimal = Field(..., title="Depth from brain surface")
    projection_axis: AxisName = Field(
        default=AxisName.DEPTH,
        title="Surface projection axis",
        description="Axis used to project the surface position onto the brain surface, defaults to the depth axis",
    )
