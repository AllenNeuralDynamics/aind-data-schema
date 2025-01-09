"""Test identifier module"""
import unittest
from pydantic import ValidationError
from aind_data_schema.components.identifiers import Experimenter


class TestExperimenter(unittest.TestCase):
    """Test Experimenter class"""

    def test_experimenter_with_full_name(self):
        """Test Experimenter with first and last name"""
        experimenter = Experimenter(
            first_name="John",
            last_name="Doe",
            registry_identifier="0000-0001-2345-6789"
        )
        self.assertEqual(experimenter.first_name, "John")
        self.assertEqual(experimenter.last_name, "Doe")
        self.assertEqual(experimenter.registry_identifier, "0000-0001-2345-6789")

    def test_experimenter_with_anonymous_id(self):
        """Test Experimenter with anonymous ID"""
        experimenter = Experimenter(
            anonymous_id="anon123"
        )
        self.assertEqual(experimenter.anonymous_id, "anon123")

    def test_experimenter_missing_required_fields(self):
        """Test Experimenter missing required fields"""
        with self.assertRaises(ValidationError):
            Experimenter()

    def test_experimenter_missing_last_name(self):
        """Test Experimenter missing last name"""
        with self.assertRaises(ValidationError):
            Experimenter(
                first_name="John"
            )

    def test_experimenter_missing_first_name(self):
        """Test Experimenter missing first name"""
        with self.assertRaises(ValidationError):
            Experimenter(
                last_name="Doe"
            )


if __name__ == '__main__':
    unittest.main()
