"""Test identifier module"""

import unittest
from pydantic import ValidationError
from aind_data_schema.components.identifiers import Person


class Testexperimenter(unittest.TestCase):
    """Test experimenter class"""

    def test_experimenter_with_full_name(self):
        """Test experimenter with first and last name"""
        experimenter = Person(name="John Doe", registry_identifier="0000-0001-2345-6789")
        self.assertIsNotNone(experimenter)
        self.assertEqual(experimenter.name, "John Doe")
        self.assertEqual(experimenter.registry_identifier, "0000-0001-2345-6789")

    def test_experimenter_missing_fields(self):
        """Test experimenter missing required fields"""
        with self.assertRaises(ValidationError):
            Person()


if __name__ == "__main__":
    unittest.main()
