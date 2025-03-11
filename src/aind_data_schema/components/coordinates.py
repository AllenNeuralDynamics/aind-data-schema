"""Classes to define device positions, orientations, and coordinates"""

from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
import math

from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field, model_validator
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


class Direction(str, Enum):
    """Local and anatomical directions"""

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
    direction: Direction = Field(
        ..., title="Direction", description="Use Other for device-defined axes, such as on manipulators"
    )


class Scale(DataModel):
    """Scale"""

    scale: List[FloatAxis] = Field(..., title="Scale parameters")

    def to_matrix(self) -> List[List[float]]:
        """Return the affine scale matrix for arbitrary sized lists

        Returns
        -------
        List[List[float]]
            Affine scale matrix
        """

        size = len(self.scale)
        scale_matrix = [[1.0 if i == j else 0.0 for j in range(size + 1)] for i in range(size + 1)]

        for i, fa in enumerate(self.scale):
            scale_matrix[i][i] = fa.value

        return scale_matrix


class Translation(DataModel):
    """Translation"""

    translation: List[FloatAxis] = Field(..., title="Translation parameters")

    def to_matrix(self) -> List[List[float]]:
        """Return the affine translation matrix for arbitrary sized lists.

        Returns
        -------
        List[List[float]]
            Affine transform matrix.
        """

        size = len(self.translation)

        # Create (size + 1) x (size + 1) identity matrix
        translation_matrix = [[1.0 if i == j else 0.0 for j in range(size + 1)] for i in range(size + 1)]

        # Populate the translation part (last column except for bottom-right corner)
        for i, fa in enumerate(self.translation):
            translation_matrix[i][-1] = fa.value

        return translation_matrix


class Rotation(DataModel):
    """Rotation"""

    angles: List[FloatAxis] = Field(..., title="Angles and axes in 3D space")
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
    order: List[AxisName] = Field(..., title="Rotation order", description="Order of rotation axes")
    rotation_direction: List[RotationDirection] = Field(
        ...,
        title="Rotation directions",
        description="CCW for right-hand rule. Defined looking in the negative direction of the axis",
    )

    def to_matrix(self) -> List[List[float]]:
        """Return the affine rotation matrix for arbtirary sized lists.

        Returns
        -------
        List[List[float]]
            Affine rotation matrix.
        """
        try:
            from scipy.spatial.transform import Rotation as R
        except ImportError:
            raise ImportError(
                "Please run `pip install aind-data-schema[transforms]` to install necessary dependencies for Rotation.to_matrix"
            )

        if not self.angles:
            return []

        # Map angles and directions to their axes
        axis_to_angle = {fa.axis: fa.value for fa in self.angles}
        axis_to_direction = {axis: direction for axis, direction in zip(self.order, self.rotation_direction)}

        # Prepare the angles and axes for scipy Rotation
        angles = []
        axes = ""
        for fa in self.angles:
            if fa.axis in axis_to_angle and fa.axis in axis_to_direction:
                # Get the angle, convert if needed
                axis = fa.axis
                angle = axis_to_angle[axis]
                if self.angles_unit == AngleUnit.DEG:
                    angle = math.radians(angle)

                # Switch sign for CCW rotations
                sign = 1 if axis_to_direction[axis] == RotationDirection.CW else -1
                angles.append(angle * sign)

                # Get the axis order
                index = self.order.index(axis)
                axes += "xyz"[index]

        # Create the rotation matrix
        rotation = R.from_euler(axes, angles)
        rotation_matrix = rotation.as_matrix().tolist()

        size = len(self.angles)
        rotation_matrix = [row + [0.0] for row in rotation_matrix] + [[0.0] * size + [1.0]]

        return rotation_matrix

    @model_validator(mode="after")
    def validate_matched_axes(cls, values):
        """Validate that the axis names match the angles"""

        angles = values.angles
        order = values.order

        if len(angles) != len(order):
            raise ValueError("Number of angles must match the number of axes in the order")

        for angle, axis in zip(angles, order):
            if angle.axis != axis:
                raise ValueError("Angle axis must match the order of rotation axes")

        return values


class AffineTransformMatrix(DataModel):
    """Definition of an affine transform 3x4 matrix"""

    affine_transform: List[List[float]] = Field(
        ...,
        title="Affine transform matrix",
    )

    @classmethod
    def compose(cls, transform: List[Union[Translation, Rotation, Scale]]) -> "AffineTransformMatrix":
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
        try:
            import numpy as np
        except ImportError:
            raise ImportError(
                "Please run `pip install aind-data-schema[transforms]` to install necessary dependencies for rotation support"
            )

        matrices = [t.to_matrix() for t in transform]

        # Check that all the transforms are the same size
        size = len(matrices[0])
        if not all(len(matrix) == size for matrix in matrices):
            raise ValueError("All transforms must be the same size")

        transform_matrix = matrices[0]

        for matrix in matrices[1:]:
            transform_matrix = np.matmul(transform_matrix, matrix).tolist()

        return AffineTransformMatrix(affine_transform=transform_matrix)


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
        title="Transforms",
    )


class CoordinateSystem(DataModel):
    """Definition of a coordinate system relative to a brain"""

    name: str = Field(..., title="Space name")
    origin: Origin = Field(
        ..., title="Origin", description="Defines the position of (0,0,0) relative to the brain or atlas"
    )
    axes: List[Axis] = Field(..., title="Axis names", description="Axis names and directions")

    size: Optional[List[FloatAxis]] = Field(
        default=None,
        title="Size",
        description="Size of the coordinate system in the same unit as the axes",
    )
    size_unit: Optional[SizeUnit] = Field(default=None, title="Size unit")
    resolution: Optional[List[FloatAxis]] = Field(
        default=None,
        title="Resolution",
        description="Resolution of the coordinate system when axes_unit is Pixels",
    )
    resolution_unit: Optional[SizeUnit] = Field(default=None, title="Resolution unit")


class Atlas(CoordinateSystem):
    """Definition an atlas"""

    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")
    size: List[FloatAxis] = Field(..., title="Size")
    size_unit: SizeUnit = Field(..., title="Size unit")
    resolution: List[FloatAxis] = Field(..., title="Resolution")
    resolution_unit: SizeUnit = Field(..., title="Resolution unit")

    @model_validator(mode="after")
    def validate_atlas(cls, values):
        """ Ensure that all FloatAxis axis names match the axes names in order """

        axes = [axis.name for axis in values.axes]
        for i, fa in enumerate(values.size):
            if fa.axis != axes[i]:
                raise ValueError(f"Size axis {fa.axis} does not match the axis name {axes[i]}")
        for i, fa in enumerate(values.resolution):
            if fa.axis != axes[i]:
                raise ValueError(f"Resolution axis {fa.axis} does not match the axis name {axes[i]}")

        return values


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
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")


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


ORDERED_AXIS_TYPES = [Translation, Rotation, Scale, Coordinate, SurfaceCoordinate]
