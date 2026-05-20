"""Tests for the coordinates module"""

import unittest

import numpy as np
from aind_data_schema_models.atlas import AtlasName
from aind_data_schema_models.units import SizeUnit
from scipy.spatial.transform import Rotation as R

from aind_data_schema.components.coordinates import (
    Affine,
    Atlas,
    Axis,
    AxisName,
    CoordinateSystem,
    Direction,
    Handedness,
    Origin,
    Rotation,
    RotationDirection,
    RotationPivot,
    Scale,
    TransformFrame,
    Translation,
)


class TestScale(unittest.TestCase):
    """Tests for the Scale class"""

    def test_to_matrix_default_order(self):
        """Test to_matrix method with default axis order"""
        scale = Scale(scale=[2, 3, 4])
        expected_matrix = [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(scale.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        scale = Scale(scale=[2, 3])
        expected_matrix = [
            [2.0, 0.0, 0.0],
            [0.0, 3.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        self.assertEqual(scale.to_matrix(), expected_matrix)


class TestTranslation(unittest.TestCase):
    """Tests for the Translation class"""

    def test_to_matrix_default_order(self):
        """Test to_matrix method with default axis order"""
        translation = Translation(translation=[2, 3, 4])
        expected_matrix = [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 3.0], [0.0, 0.0, 1.0, 4.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(translation.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        translation = Translation(translation=[2, 3])
        expected_matrix = [[1.0, 0.0, 2.0], [0.0, 1.0, 3.0], [0.0, 0.0, 1.0]]
        self.assertEqual(translation.to_matrix(), expected_matrix)


class TestRotation(unittest.TestCase):
    """Tests for the Rotation class"""

    def test_to_matrix_default_order(self):
        """Test to_matrix method with default axis order"""

        rotation = Rotation(
            angles=[90, 45, 30],
        )
        expected_matrix = R.from_euler("xyz", [90, 45, 30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.maxDiff = None
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_negative_directions(self):
        """Test to_matrix method with inverted rotation directions"""

        rotation = Rotation(
            angles=[-90, -45, -30],
        )
        expected_matrix = R.from_euler("xyz", [-90, -45, -30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        rotation = Rotation(
            angles=[90, 45],
        )
        expected_matrix = R.from_euler("xy", [90, 45], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_no_rotation(self):
        """Test to_matrix method with no rotation"""

        rotation = Rotation(
            angles=[
                0,
                0,
                0,
            ],
        )
        expected_matrix = R.from_euler("xyz", [0, 0, 0], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)


class TestAffineWithAffineTransforms(unittest.TestCase):
    """Additional tests for the Affine class with Affine transforms"""

    def test_compose_with_single_affine(self):
        """Test compose method with a single Affine transform"""
        affine = Affine(
            affine_transform=[[1.0, 0.0, 0.0, 5.0], [0.0, 1.0, 0.0, 6.0], [0.0, 0.0, 1.0, 7.0], [0.0, 0.0, 0.0, 1.0]]
        )
        composed_transform = Affine.compose([affine])
        self.assertEqual(composed_transform.affine_transform, affine.affine_transform)

    def test_compose_with_single_translation(self):
        """Test compose method with a single Translation"""
        translation = Translation(translation=[2, 3, 4])
        composed_transform = Affine.compose([translation])
        expected_matrix = translation.to_matrix()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_single_rotation(self):
        """Test compose method with a single Rotation"""
        rotation = Rotation(angles=[90, 45, 30])
        composed_transform = Affine.compose([rotation])
        expected_matrix = rotation.to_matrix()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_single_scale(self):
        """Test compose method with a single Scale"""
        scale = Scale(scale=[2, 3, 4])
        composed_transform = Affine.compose([scale])
        expected_matrix = scale.to_matrix()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_affine_and_translation(self):
        """Test compose method with an Affine transform and a Translation"""
        affine = Affine(
            affine_transform=[[1.0, 0.0, 0.0, 5.0], [0.0, 1.0, 0.0, 6.0], [0.0, 0.0, 1.0, 7.0], [0.0, 0.0, 0.0, 1.0]]
        )
        translation = Translation(translation=[2, 3, 4])
        composed_transform = Affine.compose([affine, translation])
        expected_matrix = np.matmul(affine.affine_transform, translation.to_matrix()).tolist()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_affine_and_rotation(self):
        """Test compose method with an Affine transform and a Rotation"""
        affine = Affine(
            affine_transform=[[1.0, 0.0, 0.0, 5.0], [0.0, 1.0, 0.0, 6.0], [0.0, 0.0, 1.0, 7.0], [0.0, 0.0, 0.0, 1.0]]
        )
        rotation = Rotation(angles=[90, 45, 30])
        composed_transform = Affine.compose([affine, rotation])
        expected_matrix = np.matmul(affine.affine_transform, rotation.to_matrix()).tolist()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_affine_and_scale(self):
        """Test compose method with an Affine transform and a Scale"""
        affine = Affine(
            affine_transform=[[1.0, 0.0, 0.0, 5.0], [0.0, 1.0, 0.0, 6.0], [0.0, 0.0, 1.0, 7.0], [0.0, 0.0, 0.0, 1.0]]
        )
        scale = Scale(scale=[2, 3, 4])
        composed_transform = Affine.compose([affine, scale])
        expected_matrix = np.matmul(affine.affine_transform, scale.to_matrix()).tolist()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_multiple_affine_transforms(self):
        """Test compose method with multiple Affine transforms"""
        affine1 = Affine(
            affine_transform=[[1.0, 0.0, 0.0, 5.0], [0.0, 1.0, 0.0, 6.0], [0.0, 0.0, 1.0, 7.0], [0.0, 0.0, 0.0, 1.0]]
        )
        affine2 = Affine(
            affine_transform=[[2.0, 0.0, 0.0, 1.0], [0.0, 2.0, 0.0, 2.0], [0.0, 0.0, 2.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
        )
        composed_transform = Affine.compose([affine1, affine2])
        expected_matrix = np.matmul(affine1.affine_transform, affine2.affine_transform).tolist()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)


class TestTranslationFrame(unittest.TestCase):
    """Tests for Translation frame field"""

    def test_default_frame_is_extrinsic(self):
        t = Translation(translation=[1, 2, 3])
        self.assertEqual(t.frame, TransformFrame.EXTRINSIC)

    def test_intrinsic_frame(self):
        t = Translation(translation=[1, 2, 3], frame=TransformFrame.INTRINSIC)
        self.assertEqual(t.frame, TransformFrame.INTRINSIC)

    def test_matrix_unaffected_by_frame(self):
        t_ext = Translation(translation=[1, 2, 3], frame=TransformFrame.EXTRINSIC)
        t_int = Translation(translation=[1, 2, 3], frame=TransformFrame.INTRINSIC)
        self.assertEqual(t_ext.to_matrix(), t_int.to_matrix())


class TestRotationNewFields(unittest.TestCase):
    """Tests for new Rotation fields"""

    def test_default_fields(self):
        r = Rotation(angles=[45, 0, 0])
        self.assertEqual(r.frame, TransformFrame.EXTRINSIC)
        self.assertEqual(r.rotation_direction, RotationDirection.RIGHT_HAND)
        self.assertEqual(r.pivot, RotationPivot.GLOBAL_ORIGIN)
        self.assertEqual(r.axis_order, "xyz")

    def test_custom_axis_order(self):
        r = Rotation(angles=[45, 30, 15], axis_order="zyx")
        self.assertEqual(r.axis_order, "zyx")
        expected = R.from_euler("zyx", [45, 30, 15], degrees=True).as_matrix().tolist()
        expected = [row + [0.0] for row in expected] + [[0.0, 0.0, 0.0, 1.0]]
        self.maxDiff = None
        self.assertEqual(r.to_matrix(), expected)

    def test_axis_order_normalized_to_lowercase(self):
        r = Rotation(angles=[45, 0, 0], axis_order="XYZ")
        self.assertEqual(r.axis_order, "xyz")

    def test_invalid_axis_order_raises(self):
        with self.assertRaises(Exception):
            Rotation(angles=[45, 0, 0], axis_order="abc")

    def test_left_hand_rule_negates_angles(self):
        angles = [30, 45, 60]
        r_right = Rotation(angles=angles, rotation_direction=RotationDirection.RIGHT_HAND)
        r_left = Rotation(angles=angles, rotation_direction=RotationDirection.LEFT_HAND)
        expected_left = R.from_euler("xyz", [-30, -45, -60], degrees=True).as_matrix().tolist()
        expected_left = [row + [0.0] for row in expected_left] + [[0.0, 0.0, 0.0, 1.0]]
        self.maxDiff = None
        self.assertNotEqual(r_right.to_matrix(), r_left.to_matrix())
        self.assertEqual(r_left.to_matrix(), expected_left)

    def test_intrinsic_frame(self):
        angles = [30, 45, 60]
        r_ext = Rotation(angles=angles, frame=TransformFrame.EXTRINSIC)
        r_int = Rotation(angles=angles, frame=TransformFrame.INTRINSIC)
        expected_ext = R.from_euler("xyz", angles, degrees=True).as_matrix().tolist()
        expected_int = R.from_euler("XYZ", angles, degrees=True).as_matrix().tolist()
        expected_ext = [row + [0.0] for row in expected_ext] + [[0.0, 0.0, 0.0, 1.0]]
        expected_int = [row + [0.0] for row in expected_int] + [[0.0, 0.0, 0.0, 1.0]]
        self.maxDiff = None
        self.assertEqual(r_ext.to_matrix(), expected_ext)
        self.assertEqual(r_int.to_matrix(), expected_int)

    def test_pivot_field_stored(self):
        r = Rotation(angles=[0, 0, 90], pivot=RotationPivot.LOCAL_ORIGIN)
        self.assertEqual(r.pivot, RotationPivot.LOCAL_ORIGIN)


class TestCoordinateSystemHandedness(unittest.TestCase):
    """Tests for CoordinateSystem handedness field"""

    def test_default_handedness_is_none(self):
        cs = CoordinateSystem(
            name="TEST",
            origin=Origin.BREGMA,
            axis_unit=SizeUnit.MM,
            axes=[
                Axis(name=AxisName.AP, direction=Direction.PA),
                Axis(name=AxisName.ML, direction=Direction.LR),
                Axis(name=AxisName.SI, direction=Direction.SI),
            ],
        )
        self.assertIsNone(cs.handedness)

    def test_right_handedness(self):
        cs = CoordinateSystem(
            name="TEST_R",
            origin=Origin.BREGMA,
            axis_unit=SizeUnit.MM,
            handedness=Handedness.RIGHT,
            axes=[
                Axis(name=AxisName.AP, direction=Direction.PA),
                Axis(name=AxisName.ML, direction=Direction.LR),
                Axis(name=AxisName.SI, direction=Direction.SI),
            ],
        )
        self.assertEqual(cs.handedness, Handedness.RIGHT)

    def test_left_handedness(self):
        cs = CoordinateSystem(
            name="TEST_L",
            origin=Origin.BREGMA,
            axis_unit=SizeUnit.MM,
            handedness=Handedness.LEFT,
            axes=[
                Axis(name=AxisName.AP, direction=Direction.PA),
                Axis(name=AxisName.ML, direction=Direction.LR),
                Axis(name=AxisName.SI, direction=Direction.SI),
            ],
        )
        self.assertEqual(cs.handedness, Handedness.LEFT)

    def test_compose_with_affine_and_other_transforms(self):
        """Test compose method with an Affine transform and other transforms"""
        affine = Affine(
            affine_transform=[[1.0, 0.0, 0.0, 5.0], [0.0, 1.0, 0.0, 6.0], [0.0, 0.0, 1.0, 7.0], [0.0, 0.0, 0.0, 1.0]]
        )
        translation = Translation(translation=[2, 3, 4])
        rotation = Rotation(angles=[90, 45, 30])
        scale = Scale(scale=[2, 3, 4])
        composed_transform = Affine.compose([affine, translation, rotation, scale])
        expected_matrix = np.matmul(
            affine.affine_transform,
            np.matmul(translation.to_matrix(), np.matmul(rotation.to_matrix(), scale.to_matrix())),
        ).tolist()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_invalid_sizes(self):
        """Raise error when composing matrices of different sizes"""
        translation = Translation(translation=[2, 3, 4])
        rotation = Rotation(
            angles=[90, 45, 30],
        )
        scale = Scale(scale=[2, 3])
        affine_transform = Affine(affine_transform=[])
        with self.assertRaises(ValueError) as context:
            affine_transform.compose([rotation, translation, scale])
        self.assertIn("All transforms must be the same size", str(context.exception))


class TestMultiplyMatrix(unittest.TestCase):
    """Tests for the multiply_matrix function"""

    def test_multiply_identity_matrix(self):
        """Test multiplying with identity matrix"""
        matrix1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        matrix2 = [[5, 6, 7], [8, 9, 10], [11, 12, 13]]
        expected_result = [[5, 6, 7], [8, 9, 10], [11, 12, 13]]
        self.assertEqual(np.matmul(matrix1, matrix2).tolist(), expected_result)

    def test_multiply_zero_matrix(self):
        """Test multiplying with zero matrix"""
        matrix1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        matrix2 = [[5, 6, 7], [8, 9, 10], [11, 12, 13]]
        expected_result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(np.matmul(matrix1, matrix2).tolist(), expected_result)

    def test_multiply_non_square_matrix(self):
        """Test multiplying non-square matrices"""
        matrix1 = [[1, 2, 3], [4, 5, 6]]
        matrix2 = [[7, 8], [9, 10], [11, 12]]
        expected_result = [[58, 64], [139, 154]]
        self.assertEqual(np.matmul(matrix1, matrix2).tolist(), expected_result)

    def test_multiply_varied_size(self):
        """Test multiplying incompatible matrices"""
        matrix1 = [[1, 2], [3, 4]]
        matrix2 = [[5, 6, 7], [8, 9, 10]]
        expected_result = [[21, 24, 27], [47, 54, 61]]
        self.assertEqual(np.matmul(matrix1, matrix2).tolist(), expected_result)


class TestAtlas(unittest.TestCase):
    """Tests for the Atlas class"""

    def setUp(self):
        """Set up pieces to use for testing"""
        self.axes = [
            Axis(name=AxisName.X, direction=Direction.LR),
            Axis(name=AxisName.Y, direction=Direction.AP),
            Axis(name=AxisName.Z, direction=Direction.SI),
        ]
        self.size = [10, 20, 30]
        self.resolution = [0.1, 0.1, 0.1]

    def test_validate_atlas_valid(self):
        """Test validate_atlas method with valid data"""

        axes = self.axes
        size = self.size
        resolution = self.resolution

        atlas = Atlas(
            name=AtlasName.CCF,
            version="1.0",
            axis_unit=SizeUnit.UM,
            size=size,
            size_unit=SizeUnit.MM,
            resolution=resolution,
            resolution_unit=SizeUnit.MM,
            axes=axes,
            origin=Origin.BREGMA,
        )
        self.assertIsNotNone(atlas)


if __name__ == "__main__":
    unittest.main()
