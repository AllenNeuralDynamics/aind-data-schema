import unittest
from src.aind_data_schema.components.coordinates import (
    Scale,
    AxisName,
    FloatAxis,
    Translation,
    Rotation,
    RotationDirection,
)
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

    def test_to_matrix_custom_order(self):
        """Test to_matrix method with custom axis order"""
        scale_data = [
            FloatAxis(value=2.0, axis=AxisName.X),
            FloatAxis(value=3.0, axis=AxisName.Y),
            FloatAxis(value=4.0, axis=AxisName.Z),
        ]
        scale = Scale(scale=scale_data)
        custom_order = [AxisName.Z, AxisName.X, AxisName.Y]
        expected_matrix = [[4.0, 0.0, 0.0, 0.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 3.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(scale.to_matrix(axis_order=custom_order), expected_matrix)

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

    def test_to_matrix_custom_order(self):
        """Test to_matrix method with custom axis order"""
        translation_data = [
            FloatAxis(value=2.0, axis=AxisName.X),
            FloatAxis(value=3.0, axis=AxisName.Y),
            FloatAxis(value=4.0, axis=AxisName.Z),
        ]
        translation = Translation(translation=translation_data)
        custom_order = [AxisName.Z, AxisName.X, AxisName.Y]
        expected_matrix = [[1.0, 0.0, 0.0, 4.0], [0.0, 1.0, 0.0, 2.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
        self.assertEqual(translation.to_matrix(axis_order=custom_order), expected_matrix)

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
            rotation_direction=[RotationDirection.CCW, RotationDirection.CCW, RotationDirection.CCW],
        )
        expected_matrix = R.from_euler("xyz", [90, 45, 30], degrees=True).as_matrix().tolist()
        self.assertEqual(rotation.to_matrix(), expected_matrix)

    # def test_to_matrix_custom_order(self):
    #     """Test to_matrix method with custom axis order"""
    #     rotation_data = [
    #         FloatAxis(value=90.0, axis=AxisName.AP),
    #         FloatAxis(value=45.0, axis=AxisName.ML),
    #         FloatAxis(value=30.0, axis=AxisName.SI),
    #     ]
    #     rotation = Rotation(
    #         angles=rotation_data,
    #         order=[AxisName.SI, AxisName.AP, AxisName.ML],
    #         rotation_direction=[RotationDirection.CCW, RotationDirection.CCW, RotationDirection.CCW],
    #     )
    #     expected_matrix = R.from_euler("zxy", [30, 90, 45], degrees=True).as_matrix().tolist()
    #     self.assertEqual(
    #         rotation.to_matrix(axis_order=[AxisName.SI, AxisName.AP, AxisName.ML]), expected_matrix
    #     )

    # def test_to_matrix_mixed_directions(self):
    #     """Test to_matrix method with mixed rotation directions"""
    #     rotation_data = [
    #         FloatAxis(value=90.0, axis=AxisName.AP),
    #         FloatAxis(value=45.0, axis=AxisName.ML),
    #         FloatAxis(value=30.0, axis=AxisName.SI),
    #     ]
    #     rotation = Rotation(
    #         angles=rotation_data,
    #         order=[AxisName.AP, AxisName.ML, AxisName.SI],
    #         rotation_direction=[RotationDirection.CCW, RotationDirection.CW, RotationDirection.CCW],
    #     )
    #     expected_matrix = R.from_euler("x-yz", [90, 45, 30], degrees=True).as_matrix().tolist()
    #     self.assertEqual(rotation.to_matrix(), expected_matrix)

    # def test_to_matrix_partial_axes(self):
    #     """Test to_matrix method with partial axes"""
    #     rotation_data = [FloatAxis(value=90.0, axis=AxisName.AP), FloatAxis(value=45.0, axis=AxisName.ML)]
    #     rotation = Rotation(
    #         angles=rotation_data,
    #         order=[AxisName.AP, AxisName.ML],
    #         rotation_direction=[RotationDirection.CCW, RotationDirection.CCW],
    #     )
    #     expected_matrix = R.from_euler("xy", [90, 45], degrees=True).as_matrix().tolist()
    #     self.assertEqual(rotation.to_matrix(), expected_matrix)

    # def test_to_matrix_no_rotation(self):
    #     """Test to_matrix method with no rotation"""
    #     rotation_data = []
    #     rotation = Rotation(angles=rotation_data, order=[], rotation_direction=[])
    #     expected_matrix = R.from_euler("xyz", [0, 0, 0], degrees=True).as_matrix().tolist()
    #     self.assertEqual(rotation.to_matrix(), expected_matrix)


if __name__ == "__main__":
    unittest.main()
