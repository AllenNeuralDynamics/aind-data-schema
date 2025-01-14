"""Test identifier module"""

import unittest
from pydantic import ValidationError
from aind_data_schema.components.identifiers import Experimenter


class TestExperimenter(unittest.TestCase):
    """Test Experimenter class"""

    def test_experimenter_with_full_name(self):
        """Test Experimenter with first and last name"""
        experimenter = Experimenter(name="John Doe", registry_identifier="0000-0001-2345-6789")
        self.assertEqual(experimenter.name, "John Doe")
        self.assertEqual(experimenter.registry_identifier, "0000-0001-2345-6789")

    def test_experimenter_missing_required_fields(self):
        """Test Experimenter missing required fields"""
        with self.assertRaises(ValidationError):
            Experimenter()


if __name__ == "__main__":
    unittest.main()
