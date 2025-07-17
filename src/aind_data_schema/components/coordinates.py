"""Classes to define device positions, orientations, and coordinates"""

import math
from typing import List, Union

from aind_data_schema_models.atlas import AtlasName
from aind_data_schema_models.coordinates import AxisName, Direction, Origin
from aind_data_schema_models.units import AngleUnit, SizeUnit
from pydantic import Field

from aind_data_schema.base import DataModel, DiscriminatedList
from aind_data_schema.components.wrappers import AssetPath


class Axis(DataModel):
    """Linked direction and axis"""

    name: AxisName = Field(..., title="Axis")
    direction: Direction = Field(
        ...,
        title="Direction",
        description="Direction of positive values along the axis",
    )


class Scale(DataModel):
    """Scale"""

    scale: List[float] = Field(..., title="Scale parameters")

    def to_matrix(self) -> List[List[float]]:
        """Return the affine scale matrix for arbitrary sized lists

        Returns
        -------
        List[List[float]]
            Affine scale matrix
        """

        size = len(self.scale)
        scale_matrix = [[1.0 if i == j else 0.0 for j in range(size + 1)] for i in range(size + 1)]

        for i, value in enumerate(self.scale):
            scale_matrix[i][i] = value

        return scale_matrix


class Translation(DataModel):
    """Translation"""

    translation: List[float] = Field(..., title="Translation parameters")

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
        for i, value in enumerate(self.translation):
            translation_matrix[i][-1] = value

        return translation_matrix


class Rotation(DataModel):
    """Rotation

    Rotations are applied as Euler angles in order X/Y/Z

    Angles follow right-hand rule, with positive angles rotating counter-clockwise.
    """

    angles: List[float] = Field(
        ..., title="Angles and axes in 3D space", description="Right-hand rule, positive angles rotate CCW"
    )
    angles_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")

    def to_matrix(self) -> List[List[float]]:
        """Return the affine rotation matrix for arbitrary sized lists.

        Returns
        -------
        List[List[float]]
            Affine rotation matrix.
        """
        try:
            from scipy.spatial.transform import Rotation as R
        except ImportError:  # pragma: no cover
            raise ImportError(
                "Please run `pip install aind-data-schema[transforms]` to "
                "install necessary dependencies for Rotation.to_matrix"
            )

        # Prepare the angles and axes for scipy Rotation
        angles = [angle if self.angles_unit == AngleUnit.RAD else math.radians(angle) for angle in self.angles]

        # Create the rotation matrix
        order = "xyz"[: len(self.angles)]
        rotation = R.from_euler(order, angles)
        rotation_matrix = rotation.as_matrix().tolist()

        size = len(self.angles)
        rotation_matrix = [row + [0.0] for row in rotation_matrix] + [[0.0] * size + [1.0]]

        return rotation_matrix


class Affine(DataModel):
    """Definition of an affine transform 3x4 matrix"""

    affine_transform: List[List[float]] = Field(
        ...,
        title="Affine transform matrix",
    )

    def to_matrix(self) -> List[List[float]]:
        """Return the affine transform matrix

        Returns
        -------
        List[List[float]]
            Affine transform matrix
        """
        return self.affine_transform

    @classmethod
    def compose(cls, transform: List[Union[Translation, Rotation, Scale, "Affine"]]) -> "Affine":
        """Compose an affine transform matrix from a list of transforms

        Parameters
        ----------
        transform : List[Union[Translation, Rotation, Scale, Affine]]
            List of transforms

        Returns
        -------
        Affine
            Composed transform
        """
        try:
            import numpy as np
        except ImportError:  # pragma: no cover
            raise ImportError(
                "Please run `pip install aind-data-schema[transforms]` "
                "to install necessary dependencies for rotation support"
            )

        matrices = [t.to_matrix() for t in transform]

        # Check that all the transforms are the same size
        def get_shape(list_of_lists):
            """Get the shape of a list of lists"""
            len0 = len(list_of_lists)
            len1 = len(list_of_lists[0])

            # Check that all the lists are the same size
            if not all(len(lst) == len1 for lst in list_of_lists):  # pragma: no cover
                raise ValueError("Cannot get the shape of a non-rectangular list of lists")

            return (len0, len1)

        shape = get_shape(matrices[0])
        if not all(get_shape(matrix) == shape for matrix in matrices):
            raise ValueError("All transforms must be the same size")

        transform_matrix = matrices[0]

        for matrix in matrices[1:]:
            transform_matrix = np.matmul(transform_matrix, matrix).tolist()

        return Affine(affine_transform=transform_matrix)


class NonlinearTransform(DataModel):
    """Definition of a nonlinear transform"""

    path: AssetPath = Field(
        ..., title="Path to nonlinear transform file", description="Relative path from metadata json to file"
    )


TRANSFORM_TYPES = DiscriminatedList[Translation | Rotation | Scale | Affine]
TRANSFORM_TYPES_NONLINEAR = DiscriminatedList[Translation | Rotation | Scale | Affine | NonlinearTransform]


class CoordinateSystem(DataModel):
    """Definition of a coordinate system relative to a brain"""

    name: str = Field(..., title="Name")

    origin: Origin = Field(..., title="Origin", description="Defines the position of (0,0,0) in the coordinate system")
    axes: List[Axis] = Field(..., title="Axis names", description="Axis names and directions")
    axis_unit: SizeUnit = Field(..., title="Size unit")


class Atlas(CoordinateSystem):
    """Definition an atlas"""

    name: AtlasName = Field(..., title="Atlas name")
    version: str = Field(..., title="Atlas version")
    size: List[float] = Field(..., title="Size")
    size_unit: SizeUnit = Field(default=SizeUnit.PX, title="Size unit")
    resolution: List[float] = Field(..., title="Resolution")
    resolution_unit: SizeUnit = Field(..., title="Resolution unit")


class AtlasCoordinate(Translation):
    """A point in an Atlas"""

    coordinate_system: Atlas = Field(..., title="Atlas")


class CoordinateSystemLibrary:
    """Library of common coordinate systems

    Convention is to use the following naming scheme:

    <<ORIGIN>_<POS_X_DIR><POS_Y_DIR><POS_Z_DIR> etc

    ORIGIN is the origin in the world, Bregma, "front
    """

    # Standard coordinates
    BREGMA_ARI = CoordinateSystem(
        name="BREGMA_ARI",
        origin=Origin.BREGMA,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.AP, direction=Direction.PA),
            Axis(name=AxisName.ML, direction=Direction.LR),
            Axis(name=AxisName.SI, direction=Direction.SI),
        ],
    )
    BREGMA_RAS = CoordinateSystem(
        name="BREGMA_RAS",
        origin=Origin.BREGMA,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.ML, direction=Direction.LR),
            Axis(name=AxisName.AP, direction=Direction.PA),
            Axis(name=AxisName.SI, direction=Direction.IS),
        ],
    )

    # Standard surface coordinates (with depth)
    BREGMA_ARID = CoordinateSystem(
        name="BREGMA_ARID",
        origin=Origin.BREGMA,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.AP, direction=Direction.PA),
            Axis(name=AxisName.ML, direction=Direction.LR),
            Axis(name=AxisName.SI, direction=Direction.SI),
            Axis(name=AxisName.DEPTH, direction=Direction.UD),
        ],
    )
    BREGMA_RASD = CoordinateSystem(
        name="BREGMA_RASD",
        origin=Origin.BREGMA,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.ML, direction=Direction.LR),
            Axis(name=AxisName.AP, direction=Direction.PA),
            Axis(name=AxisName.SI, direction=Direction.IS),
            Axis(name=AxisName.DEPTH, direction=Direction.UD),
        ],
    )

    # Arena
    ARENA_RBT = CoordinateSystem(
        name="ARENA_RBT",
        origin=Origin.ARENA_CENTER,
        axis_unit=SizeUnit.CM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.FB),
            Axis(name=AxisName.Z, direction=Direction.DU),
        ],
    )

    SIPE_CAMERA_RBF = CoordinateSystem(
        name="SIPE_CAMERA_RBF",
        origin=Origin.FRONT_CENTER,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.UD),
            Axis(name=AxisName.Z, direction=Direction.BF),
        ],
    )

    SIPE_MONITOR_RTF = CoordinateSystem(
        name="SIPE_MONITOR_RTF",
        origin=Origin.FRONT_CENTER,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.DU),
            Axis(name=AxisName.Z, direction=Direction.BF),
        ],
    )

    SIPE_SPEAKER_LTF = CoordinateSystem(
        name="SIPE_SPEAKER_LTF",
        origin=Origin.FRONT_CENTER,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.RL),
            Axis(name=AxisName.Y, direction=Direction.DU),
            Axis(name=AxisName.Z, direction=Direction.FB),
        ],
    )

    MPM_MANIP_RFB = CoordinateSystem(
        name="MPM_MANIP_RFB",
        origin=Origin.TIP,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.BF),
            Axis(name=AxisName.Z, direction=Direction.UD),
        ],
    )

    PINPOINT_PROBE_RSAB = CoordinateSystem(
        name="PINPOINT_PROBE_RSAB",
        origin=Origin.TIP,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.IS),
            Axis(name=AxisName.Z, direction=Direction.PA),
            Axis(name=AxisName.DEPTH, direction=Direction.UD),
        ],
    )

    SPIM_IJK = CoordinateSystem(
        name="SPIM_IJK",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.PX,
        axes=[
            Axis(name=AxisName.X, direction=Direction.POS),
            Axis(name=AxisName.Y, direction=Direction.POS),
            Axis(name=AxisName.Z, direction=Direction.POS),
        ],
    )

    SPIM_RPI = CoordinateSystem(
        name="SPIM_RPI",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.AP),
            Axis(name=AxisName.Z, direction=Direction.SI),
        ],
    )

    SPIM_LPS = CoordinateSystem(
        name="SPIM_LPS",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.RL),
            Axis(name=AxisName.Y, direction=Direction.AP),
            Axis(name=AxisName.Z, direction=Direction.IS),
        ],
    )

    MRI_LPS = CoordinateSystem(
        name="MRI_LPS",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.MM,
        axes=[
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.AP),
            Axis(name=AxisName.Z, direction=Direction.IS),
        ],
    )

    IMAGE_XYZ = CoordinateSystem(
        name="IMAGE_XYZ",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.PX,
        axes=[
            Axis(name=AxisName.X, direction=Direction.POS),
            Axis(name=AxisName.Y, direction=Direction.POS),
            Axis(name=AxisName.Z, direction=Direction.POS),
        ],
    )


class AtlasLibrary:
    """Library of common atlases"""

    CCFv3_10um = Atlas(
        name=AtlasName.CCF,
        version="3",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.UM,
        axes=[
            Axis(name=AxisName.AP, direction=Direction.AP),
            Axis(name=AxisName.SI, direction=Direction.SI),
            Axis(name=AxisName.ML, direction=Direction.LR),
        ],
        size=[1320, 800, 1140],
        resolution=[10, 10, 10],
        resolution_unit=SizeUnit.UM,
    )

    CCFv3_25um = Atlas(
        name=AtlasName.CCF,
        version="3",
        origin=Origin.ORIGIN,
        axis_unit=SizeUnit.UM,
        axes=[
            Axis(name=AxisName.AP, direction=Direction.AP),
            Axis(name=AxisName.SI, direction=Direction.SI),
            Axis(name=AxisName.ML, direction=Direction.LR),
        ],
        size=[528, 320, 456],
        resolution=[25, 25, 25],
        resolution_unit=SizeUnit.UM,
    )
