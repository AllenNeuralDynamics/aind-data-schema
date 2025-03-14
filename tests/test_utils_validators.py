""" Tests for compatibility check utilities """

import unittest
from aind_data_schema.utils.validators import subject_specimen_id_compatibility, _recurse_helper, recursive_axis_order_check
from aind_data_schema.components.coordinates import FloatAxis, AxisName, Coordinate


class TestCompatibilityCheck(unittest.TestCase):
    """Tests compatibility checks"""

    def test_subj_spec_valid(self):
        """Test subject_id specimen_id valid"""
        subject_id = "123456"
        specimen_id = "123456-valid"
        self.assertTrue(subject_specimen_id_compatibility(subject_id, specimen_id))

    def test_subj_spec_invalid(self):
        """Test invalid subject_id specimen_id"""
        subject_id = "123456"
        specimen_id = "invalid"
        self.assertFalse(subject_specimen_id_compatibility(subject_id, specimen_id))


class TestRecurseHelper(unittest.TestCase):
    """Tests for _recurse_helper function"""

    def setUp(self):
        """Set up test data"""
        self.system_name = "Bregma ARI"
        self.system_axes = [AxisName.AP, AxisName.ML, AxisName.SI]

    def test_recurse_helper_with_list(self):
        """Test _recurse_helper with a list of coordinates"""
        data = [
            Coordinate(
                system_name=self.system_name,
                position=[
                    FloatAxis(value=0.5, axis=AxisName.AP),
                    FloatAxis(value=1, axis=AxisName.ML),
                ],
            ),
            Coordinate(
                system_name=self.system_name,
                position=[
                    FloatAxis(value=0.5, axis=AxisName.AP),
                    FloatAxis(value=1, axis=AxisName.ML),
                ],
            ),
        ]
        try:
            _recurse_helper(data, self.system_name, self.system_axes)
        except ValueError:
            self.fail("_recurse_helper raised ValueError unexpectedly!")

    def test_recurse_helper_with_object(self):
        """Test _recurse_helper with a single coordinate object"""
        data = Coordinate(
            system_name=self.system_name,
            position=[
                FloatAxis(value=0.5, axis=AxisName.AP),
                FloatAxis(value=1, axis=AxisName.ML),
            ],
        )
        try:
            _recurse_helper(data, self.system_name, self.system_axes)
        except ValueError:
            self.fail("_recurse_helper raised ValueError unexpectedly!")

    def test_recurse_helper_with_invalid_axes(self):
        """Test _recurse_helper with invalid axes"""
        data = Coordinate(
            system_name=self.system_name,
            position=[
                FloatAxis(value=0.5, axis=AxisName.AP),
                FloatAxis(value=1, axis=AxisName.X),
            ],
        )
        with self.assertRaises(ValueError):
            _recurse_helper(data, self.system_name, self.system_axes)


class TestRecursiveAxisOrderCheck(unittest.TestCase):
    """Tests for recursive_axis_order_check function"""

    def setUp(self):
        """Set up test data"""
        self.system_name = "Bregma ARI"
        self.system_axes = [AxisName.AP, AxisName.ML, AxisName.SI]

    def test_recursive_axis_order_check_with_valid_data(self):
        """Test recursive_axis_order_check with valid data"""
        data = Coordinate(
            system_name=self.system_name,
            position=[
                FloatAxis(value=0.5, axis=AxisName.AP),
                FloatAxis(value=1, axis=AxisName.ML),
            ],
        )
        try:
            recursive_axis_order_check(data, self.system_name, self.system_axes)
        except ValueError:
            self.fail("recursive_axis_order_check raised ValueError unexpectedly!")

    def test_recursive_axis_order_check_with_invalid_system_name(self):
        """Test recursive_axis_order_check with invalid system name"""
        data = Coordinate(
            system_name="Invalid System",
            position=[
                FloatAxis(value=0.5, axis=AxisName.AP),
                FloatAxis(value=1, axis=AxisName.ML),
            ],
        )
        with self.assertRaises(ValueError):
            recursive_axis_order_check(data, self.system_name, self.system_axes)

    def test_recursive_axis_order_check_with_invalid_axes(self):
        """Test recursive_axis_order_check with invalid axes"""
        data = Coordinate(
            system_name=self.system_name,
            position=[
                FloatAxis(value=0.5, axis=AxisName.AP),
                FloatAxis(value=1, axis=AxisName.X),
            ],
        )
        with self.assertRaises(ValueError):
            recursive_axis_order_check(data, self.system_name, self.system_axes)

    def test_recursive_axis_order_check_with_empty_data(self):
        """Test recursive_axis_order_check with empty data"""
        data = None
        try:
            recursive_axis_order_check(data, self.system_name, self.system_axes)
        except ValueError:
            self.fail("recursive_axis_order_check raised ValueError unexpectedly!")

    def test_recursive_axis_order_check_with_list_of_coordinates(self):
        """Test recursive_axis_order_check with a list of coordinates"""
        data = [
            Coordinate(
                system_name=self.system_name,
                position=[
                    FloatAxis(value=0.5, axis=AxisName.AP),
                    FloatAxis(value=1, axis=AxisName.ML),
                ],
            ),
            Coordinate(
                system_name=self.system_name,
                position=[
                    FloatAxis(value=0.5, axis=AxisName.AP),
                    FloatAxis(value=1, axis=AxisName.ML),
                ],
            ),
        ]
        try:
            recursive_axis_order_check(data, self.system_name, self.system_axes)
        except ValueError:
            self.fail("recursive_axis_order_check raised ValueError unexpectedly!")


if __name__ == "__main__":
    unittest.main()
