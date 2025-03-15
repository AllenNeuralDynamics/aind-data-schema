""" Tests for the coordinates module """

import unittest
from aind_data_schema.components.coordinates import (
    Scale,
    AxisName,
    Translation,
    Rotation,
    AffineTransformMatrix,
    Axis,
    Direction,
    AtlasName,
    Atlas,
    Origin,
)
from aind_data_schema_models.units import SizeUnit
import numpy as np
from scipy.spatial.transform import Rotation as R


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
            order=[0, 1, 2],
        )
        expected_matrix = R.from_euler("xyz", [90, 45, 30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.maxDiff = None
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_negative_directions(self):
        """Test to_matrix method with inverted rotation directions"""

        rotation = Rotation(
            angles=[-90, -45, -30],
            order=[0, 1, 2],
        )
        expected_matrix = R.from_euler("xyz", [-90, -45, -30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        rotation = Rotation(
            angles=[90, 45],
            order=[0, 1],
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
            order=[0, 1, 2],
        )
        expected_matrix = R.from_euler("xyz", [0, 0, 0], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_error_invalid_order(self):
        """Test error with invalid order"""
        with self.assertRaises(ValueError) as context:
            Rotation(
                angles=[90, 45, 30],
                order=[0, 1],
            )

        self.assertIn("Number of angles must match the number of axes in the order", str(context.exception))


class TestAffineTransformMatrix(unittest.TestCase):
    """Tests for the AffineTransformMatrix class"""

    def test_compose_with_translation(self):
        """Test compose method with translation"""

        translation = Translation(translation=[2, 3, 4])
        affine_transform = AffineTransformMatrix(affine_transform=[])
        composed_transform = affine_transform.compose([translation])
        expected_matrix = [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 3.0], [0.0, 0.0, 1.0, 4.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_rotation(self):
        """Test compose method with rotation"""

        rotation = Rotation(
            angles=[90, 45, 30],
            order=[0, 1, 2],
        )
        composed_transform = AffineTransformMatrix.compose([rotation])
        self.assertEqual(composed_transform.affine_transform, rotation.to_matrix())

    def test_compose_with_scale(self):
        """Test compose method with scale"""

        scale = Scale(scale=[2, 3, 4])
        affine_transform = AffineTransformMatrix(affine_transform=[])
        composed_transform = affine_transform.compose([scale])
        expected_matrix = [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_multiple_transforms(self):
        """Test compose method with multiple transforms"""
        translation = Translation(translation=[2, 3, 4])
        rotation = Rotation(
            angles=[90, 45, 30],
            order=[0, 1, 2],
        )
        scale = Scale(scale=[2, 3, 4])
        affine_transform = AffineTransformMatrix(affine_transform=[])
        composed_transform = affine_transform.compose([rotation, translation, scale])
        expected_matrix = R.from_euler("xyz", [90, 45, 30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        expected_matrix = np.matmul(
            expected_matrix, [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 3.0], [0.0, 0.0, 1.0, 4.0], [0.0, 0.0, 0.0, 1.0]]
        ).tolist()
        expected_matrix = np.matmul(
            expected_matrix, [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        ).tolist()
        self.assertEqual(composed_transform.affine_transform, expected_matrix)
    
    def test_compose_invalid_sizes(self):
        """ Raise error when composing matrices of different sizes """
        translation = Translation(translation=[2, 3, 4])
        rotation = Rotation(
            angles=[90, 45, 30],
            order=[0, 1, 2],
        )
        scale = Scale(scale=[2, 3])
        affine_transform = AffineTransformMatrix(affine_transform=[])
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
