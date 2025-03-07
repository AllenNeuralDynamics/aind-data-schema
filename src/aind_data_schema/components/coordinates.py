"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
import math

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
    C1 = "C1"  # cervical vertebrae
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"
    C7 = "C7"


class RotationDirection(str, Enum):
    """Rotation direction"""

    CW = "Clockwise"
    CCW = "Counter-clockwise"


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

    def to_matrix(self, axis_order: Optional[List[AxisName]] = None) -> List[List[float]]:
        """Return the scale matrix for arbitrary sized lists

        Parameters
        ----------
        axis_order : Optional[List[AxisName]], optional
            Order of the axes, by default None

        Returns
        -------
        List[List[float]]
            Affine transform matrix
        """
        if axis_order is None:
            axis_order = [fa.axis for fa in self.scale]

        size = len(axis_order)
        scale_matrix = [[1.0 if i == j else 0.0 for j in range(size + 1)] for i in range(size + 1)]

        for scale_axis in self.scale:
            axis_index = axis_order.index(scale_axis.axis)
            scale_matrix[axis_index][axis_index] = scale_axis.value

        return scale_matrix


class Translation(DataModel):
    """Translation"""

    translation: List[FloatAxis] = Field(..., title="Translation parameters")

    def to_matrix(self, axis_order: Optional[List[AxisName]] = None) -> List[List[float]]:
        """Return the translation matrix for arbitrary sized lists.

        Parameters
        ----------
        axis_order : Optional[List[AxisName]], optional
            Order of the axes, by default None.

        Returns
        -------
        List[List[float]]
            Affine transform matrix.
        """

        if axis_order is None:
            axis_order = [fa.axis for fa in self.translation]

        size = len(axis_order)

        # Create (size + 1) x (size + 1) identity matrix
        translation_matrix = [[1.0 if i == j else 0.0 for j in range(size + 1)] for i in range(size + 1)]

        axis_to_value = {fa.axis: fa.value for fa in self.translation}

        # Populate the translation part (last column except for bottom-right corner)
        for i, axis in enumerate(axis_order):
            if axis in axis_to_value:
                translation_matrix[i][-1] = axis_to_value[axis]

        return translation_matrix


class Rotation(DataModel):
    """Rotation"""

    angles: List[FloatAxis] = Field(..., title="Angles and axes in 3D space")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
    order: List[AxisName] = Field(
        default=[AxisName.AP, AxisName.ML, AxisName.SI], title="Rotation order", description="Order of rotation axes"
    )
    rotation_direction: List[RotationDirection] = Field(
        ...,
        title="Rotation directions",
        description="CCW for right-hand rule. Defined looking in the negative direction of the axis",
    )

    def to_matrix(self, axis_order: Optional[List[AxisName]] = None) -> List[List[float]]:
        """Return the rotation matrix for arbitrary axis orders and directions.

        Parameters
        ----------
        axis_order : Optional[List[AxisName]], optional
            Order of the axes, by default None.

        Returns
        -------
        List[List[float]]
            Rotation matrix.
        """
        if axis_order is None:
            axis_order = [fa.axis for fa in self.angles]

        if not self.angles:
            return []

        size = len(axis_order)

        # Create identity matrix of appropriate size
        rotation_matrix = [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]

        # Map angles and directions to their axes
        axis_to_angle = {fa.axis: fa.value for fa in self.angles}
        axis_to_direction = {axis: direction for axis, direction in zip(self.order, self.rotation_direction)}

        # Helper to generate a rotation matrix for a given axis
        def axis_rotation_matrix(axis: AxisName, angle: float, direction: RotationDirection) -> List[List[float]]:
            sign = 1 if direction == RotationDirection.CCW else -1
            theta = math.radians(angle) * sign

            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            if axis == AxisName.X:  # Rotate around x-axis
                return [[1, 0, 0], [0, cos_theta, -sin_theta], [0, sin_theta, cos_theta]]
            elif axis == AxisName.Y:  # Rotate around y-axis
                return [[cos_theta, 0, sin_theta], [0, 1, 0], [-sin_theta, 0, cos_theta]]
            elif axis == AxisName.Z:  # Rotate around z-axis
                return [[cos_theta, -sin_theta, 0], [sin_theta, cos_theta, 0], [0, 0, 1]]

        # Apply rotations in the specified order
        for axis in self.order:
            if axis in axis_to_angle and axis in axis_to_direction:
                angle = axis_to_angle[axis]
                direction = axis_to_direction[axis]
                R = axis_rotation_matrix(axis, angle, direction)

                # Matrix multiplication: rotation_matrix = rotation_matrix @ R
                rotation_matrix = [
                    [sum(rotation_matrix[i][k] * R[k][j] for k in range(3)) for j in range(3)] for i in range(3)
                ]

        # Reorder axes if necessary
        axis_index = {axis: i for i, axis in enumerate([AxisName.AP, AxisName.ML, AxisName.SI])}
        permuted_indices = [axis_index[axis] for axis in axis_order]

        return [[rotation_matrix[i][j] for j in permuted_indices] for i in permuted_indices]


class AffineTransformMatrix(DataModel):
    """Definition of an affine transform 3x4 matrix"""

    affine_transform: List[Decimal] = Field(
        ..., title="Affine transform matrix values (top 3x4 matrix)", min_length=12, max_length=12
    )

    def compose(self, transform: List[Union[Translation, Rotation, Scale]]) -> "AffineTransformMatrix":
        """Compose an affine transform matrix from a list of transforms

        Parameters
        ----------
        transform : List[Union[Translation, Rotation, Scale]]
            List of transforms

        Returns
        -------
        AffineTransformMatrix
            Composed transform
        """
        # Create an empty 4x4 matrix with 1s on the diagonal
        transform_matrix = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]

        for t in transform:
            transform_matrix = t.to_matrix() @ transform_matrix

        return AffineTransformMatrix(affine_transform=[Decimal(v) for row in transform_matrix for v in row])


class NonlinearTransform(DataModel):
    """Definition of a nonlinear transform"""

    path: str = Field(..., title="Path to nonlinear transform file")


class Transform(DataModel):
    """Affine and non-linear transformations"""

    transform: List[
        Annotated[
            Union[Translation, Rotation, Scale, AffineTransformMatrix, NonlinearTransform],
            Field(discriminator="object_type"),
        ]
    ] = Field(
        ...,
        title="Group of transformations",
        description="Non-linear transformations should be stored in a relative file path",
    )


class CoordinateSystem(DataModel):
    """Definition of a coordinate system relative to a brain"""

    name: str = Field(..., title="Space name")
    origin: Origin = Field(
        ..., title="Origin", description="Defines the position of (0,0,0) relative to the brain or atlas"
    )
    axes: List[Axis] = Field(..., title="Axis names", description="Axis names and directions")
    axes_unit: SizeUnit = Field(..., title="Axis unit")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")

    size: Optional[List[FloatAxis]] = Field(
        default=None,
        title="Size",
        description="Size of the coordinate system in the same unit as the axes",
    )
    resolution: Optional[List[FloatAxis]] = Field(
        default=None,
        title="Resolution",
        description="Resolution of the coordinate system when axes_unit is Pixels",
    )


class Atlas(CoordinateSystem):
    """Definition an atlas"""

    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")
    size: List[FloatAxis] = Field(..., title="Size")  # type: ignore
    resolution: List[FloatAxis] = Field(..., title="Resolution")  # type: ignore


class CoordinateTransform(DataModel):
    """Transformation from one CoordinateSystem to another"""

    input: CoordinateSystem = Field(..., title="Input coordinate system")
    output: CoordinateSystem = Field(..., title="Output coordinate system")
    transform: Transform = Field(..., title="Transformation from input to output coordinate system")


class RelativePosition(DataModel):
    """Relative position in a coordinate system"""

    position: List[AnatomicalRelative] = Field(..., title="Relative position")


class Coordinate(DataModel):
    """A coordinate in a brain (CoordinateSpace) or atlas (AtlasSpace)

    Angles can be optionally provided
    """

    position: List[FloatAxis] = Field(..., title="Coordinates in in vivo space")
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
