import unittest
from src.aind_data_schema.components.coordinates import (
    Scale,
    AxisName,
    FloatAxis,
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

""" Tests for the coordinates module """


class TestScale(unittest.TestCase):
    """Tests for the Scale class"""

    def test_to_matrix_default_order(self):
        """Test to_matrix method with default axis order"""
        scale_data = [
            FloatAxis(value=2.0, axis=AxisName.X),
            FloatAxis(value=3.0, axis=AxisName.Y),
            FloatAxis(value=4.0, axis=AxisName.Z),
        ]
        scale = Scale(scale=scale_data)
        expected_matrix = [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(scale.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        scale_data = [FloatAxis(value=2.0, axis=AxisName.X), FloatAxis(value=3.0, axis=AxisName.Y)]
        scale = Scale(scale=scale_data)
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
        translation_data = [
            FloatAxis(value=2.0, axis=AxisName.X),
            FloatAxis(value=3.0, axis=AxisName.Y),
            FloatAxis(value=4.0, axis=AxisName.Z),
        ]
        translation = Translation(translation=translation_data)
        expected_matrix = [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 3.0], [0.0, 0.0, 1.0, 4.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(translation.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        translation_data = [FloatAxis(value=2.0, axis=AxisName.X), FloatAxis(value=3.0, axis=AxisName.Y)]
        translation = Translation(translation=translation_data)
        expected_matrix = [[1.0, 0.0, 2.0], [0.0, 1.0, 3.0], [0.0, 0.0, 1.0]]
        self.assertEqual(translation.to_matrix(), expected_matrix)


class TestRotation(unittest.TestCase):
    """Tests for the Rotation class"""

    def test_to_matrix_default_order(self):
        """Test to_matrix method with default axis order"""
        rotation_data = [
            FloatAxis(value=90.0, axis=AxisName.AP),
            FloatAxis(value=45.0, axis=AxisName.ML),
            FloatAxis(value=30.0, axis=AxisName.SI),
        ]
        rotation = Rotation(
            angles=rotation_data,
            order=[AxisName.AP, AxisName.ML, AxisName.SI],
        )
        expected_matrix = R.from_euler("xyz", [90, 45, 30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.maxDiff = None
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_negative_directions(self):
        """Test to_matrix method with inverted rotation directions"""
        rotation_data = [
            FloatAxis(value=-90.0, axis=AxisName.AP),
            FloatAxis(value=-45.0, axis=AxisName.ML),
            FloatAxis(value=-30.0, axis=AxisName.SI),
        ]
        rotation = Rotation(
            angles=rotation_data,
            order=[AxisName.AP, AxisName.ML, AxisName.SI],
        )
        expected_matrix = R.from_euler("xyz", [-90, -45, -30], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_partial_axes(self):
        """Test to_matrix method with partial axes"""
        rotation_data = [FloatAxis(value=90.0, axis=AxisName.AP), FloatAxis(value=45.0, axis=AxisName.ML)]
        rotation = Rotation(
            angles=rotation_data,
            order=[AxisName.AP, AxisName.ML],
        )
        expected_matrix = R.from_euler("xy", [90, 45], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    def test_to_matrix_no_rotation(self):
        """Test to_matrix method with no rotation"""
        rotation_data = [
            FloatAxis(value=0, axis=AxisName.AP),
            FloatAxis(value=0, axis=AxisName.ML),
            FloatAxis(value=0, axis=AxisName.SI),
        ]
        rotation = Rotation(
            angles=rotation_data,
            order=[AxisName.AP, AxisName.ML, AxisName.SI],
        )
        expected_matrix = R.from_euler("xyz", [0, 0, 0], degrees=True).as_matrix().tolist()
        expected_matrix = [row + [0.0] for row in expected_matrix] + [[0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(rotation.to_matrix(), expected_matrix)


class TestAffineTransformMatrix(unittest.TestCase):
    """Tests for the AffineTransformMatrix class"""

    def test_compose_with_translation(self):
        """Test compose method with translation"""
        translation_data = [
            FloatAxis(value=2.0, axis=AxisName.X),
            FloatAxis(value=3.0, axis=AxisName.Y),
            FloatAxis(value=4.0, axis=AxisName.Z),
        ]
        translation = Translation(translation=translation_data)
        affine_transform = AffineTransformMatrix(affine_transform=[])
        composed_transform = affine_transform.compose([translation])
        expected_matrix = [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 3.0], [0.0, 0.0, 1.0, 4.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_rotation(self):
        """Test compose method with rotation"""
        rotation_data = [
            FloatAxis(value=90.0, axis=AxisName.X),
            FloatAxis(value=45.0, axis=AxisName.Y),
            FloatAxis(value=30.0, axis=AxisName.Z),
        ]
        rotation = Rotation(
            angles=rotation_data,
            order=[AxisName.X, AxisName.Y, AxisName.Z],
        )
        composed_transform = AffineTransformMatrix.compose([rotation])
        self.assertEqual(composed_transform.affine_transform, rotation.to_matrix())

    def test_compose_with_scale(self):
        """Test compose method with scale"""
        scale_data = [
            FloatAxis(value=2.0, axis=AxisName.X),
            FloatAxis(value=3.0, axis=AxisName.Y),
            FloatAxis(value=4.0, axis=AxisName.Z),
        ]
        scale = Scale(scale=scale_data)
        affine_transform = AffineTransformMatrix(affine_transform=[])
        composed_transform = affine_transform.compose([scale])
        expected_matrix = [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(composed_transform.affine_transform, expected_matrix)

    def test_compose_with_multiple_transforms(self):
        """Test compose method with multiple transforms"""
        translation = Translation(
            translation=[
                FloatAxis(value=2.0, axis=AxisName.X),
                FloatAxis(value=3.0, axis=AxisName.Y),
                FloatAxis(value=4.0, axis=AxisName.Z),
            ]
        )
        rotation = Rotation(
            angles=[
                FloatAxis(value=90.0, axis=AxisName.X),
                FloatAxis(value=45.0, axis=AxisName.Y),
                FloatAxis(value=30.0, axis=AxisName.Z),
            ],
            order=[AxisName.X, AxisName.Y, AxisName.Z],
        )
        scale = Scale(
            scale=[
                FloatAxis(value=2.0, axis=AxisName.X),
                FloatAxis(value=3.0, axis=AxisName.Y),
                FloatAxis(value=4.0, axis=AxisName.Z),
            ]
        )
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
        self.size = [
            FloatAxis(value=10.0, axis=AxisName.X),
            FloatAxis(value=20.0, axis=AxisName.Y),
            FloatAxis(value=30.0, axis=AxisName.Z),
        ]
        self.resolution = [
            FloatAxis(value=0.1, axis=AxisName.X),
            FloatAxis(value=0.2, axis=AxisName.Y),
            FloatAxis(value=0.3, axis=AxisName.Z),
        ]

    def test_validate_atlas_valid(self):
        """Test validate_atlas method with valid data"""

        axes = self.axes
        size = self.size
        resolution = self.resolution

        atlas = Atlas(
            name=AtlasName.CCF,
            version="1.0",
            size=size,
            size_unit=SizeUnit.MM,
            resolution=resolution,
            resolution_unit=SizeUnit.MM,
            axes=axes,
            origin=Origin.BREGMA,
        )
        self.assertIsNotNone(atlas)

    def test_validate_atlas_invalid_size_axis(self):
        """Test validate_atlas method with invalid size axis"""

        axes = self.axes
        size = self.size
        resolution = self.resolution

        size[0].axis = AxisName.Y.value
        size[1].axis = AxisName.X.value

        with self.assertRaises(ValueError) as context:
            Atlas(
                name=AtlasName.CCF,
                version="1.0",
                size=size,
                size_unit=SizeUnit.MM,
                resolution=resolution,
                resolution_unit=SizeUnit.MM,
                axes=axes,
                origin=Origin.BREGMA,
            )
        self.assertIn("Size axis Y does not match the axis name X", str(context.exception))

    def test_validate_atlas_invalid_resolution_axis(self):
        """Test validate_atlas method with invalid resolution axis"""

        axes = self.axes
        size = self.size
        resolution = self.resolution

        resolution[0].axis = AxisName.Y.value
        resolution[1].axis = AxisName.X.value

        with self.assertRaises(ValueError) as context:
            Atlas(
                name=AtlasName.CCF,
                version="1.0",
                size=size,
                size_unit=SizeUnit.MM,
                resolution=resolution,
                resolution_unit=SizeUnit.MM,
                axes=axes,
                origin=Origin.BREGMA,
            )
        self.assertIn("Resolution axis Y does not match the axis name X", str(context.exception))


if __name__ == "__main__":
    unittest.main()
