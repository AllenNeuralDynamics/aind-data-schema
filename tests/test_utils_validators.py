""" Tests for compatibility check utilities """

import unittest
from aind_data_schema.utils.validators import (
    subject_specimen_id_compatibility,
    _recurse_helper,
    recursive_coord_system_check,
)
from aind_data_schema.components.coordinates import Coordinate


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
        self.system_name = "BREGMA_ARI"

    def test_recurse_helper_with_list(self):
        """Test _recurse_helper with a list of coordinates"""
        data = [
            Coordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
            Coordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
        ]
        try:
            _recurse_helper(data, self.system_name)
        except ValueError:
            self.fail("_recurse_helper raised ValueError unexpectedly!")

    def test_recurse_helper_with_object(self):
        """Test _recurse_helper with a single coordinate object"""
        data = Coordinate(
            system_name=self.system_name,
            position=[0.5, 1],
        )
        try:
            _recurse_helper(data, self.system_name)
        except ValueError:
            self.fail("_recurse_helper raised ValueError unexpectedly!")


class TestRecursiveAxisOrderCheck(unittest.TestCase):
    """Tests for recursive_axis_order_check function"""

    def setUp(self):
        """Set up test data"""
        self.system_name = "BREGMA_ARI"

    def test_recursive_axis_order_check_with_valid_data(self):
        """Test recursive_axis_order_check with valid data"""
        data = Coordinate(
            system_name=self.system_name,
            position=[0.5, 1],
        )
        try:
            recursive_coord_system_check(data, self.system_name)
        except ValueError:
            self.fail("recursive_axis_order_check raised ValueError unexpectedly!")

    def test_recursive_axis_order_check_with_invalid_system_name(self):
        """Test recursive_axis_order_check with invalid system name"""
        data = Coordinate(
            system_name="Invalid System",
            position=[0.5, 1],
        )
        with self.assertRaises(ValueError):
            recursive_coord_system_check(data, self.system_name)

    def test_recursive_axis_order_check_with_empty_data(self):
        """Test recursive_axis_order_check with empty data"""
        data = None
        try:
            recursive_coord_system_check(data, self.system_name)
        except ValueError:
            self.fail("recursive_axis_order_check raised ValueError unexpectedly!")

    def test_recursive_axis_order_check_with_list_of_coordinates(self):
        """Test recursive_axis_order_check with a list of coordinates"""
        data = [
            Coordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
            Coordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
        ]
        try:
            recursive_coord_system_check(data, self.system_name)
        except ValueError:
            self.fail("recursive_axis_order_check raised ValueError unexpectedly!")


if __name__ == "__main__":
    unittest.main()
