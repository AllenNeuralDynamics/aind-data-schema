"""Test identifier module"""

import unittest
from pydantic import ValidationError
from aind_data_schema.components.identifiers import Investigator


class TestInvestigator(unittest.TestCase):
    """Test Investigator class"""

    def test_investigator_with_full_name(self):
        """Test Investigator with first and last name"""
        investigator = Investigator(name="John Doe", registry_identifier="0000-0001-2345-6789")
        self.assertIsNotNone(investigator)
        self.assertEqual(investigator.name, "John Doe")
        self.assertEqual(investigator.registry_identifier, "0000-0001-2345-6789")

    def test_investigator_missing_fields(self):
        """Test Investigator missing required fields"""
        with self.assertRaises(ValidationError):
            Investigator()


if __name__ == "__main__":
    unittest.main()
