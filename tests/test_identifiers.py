"""Test identifier module"""

import unittest
from pydantic import ValidationError
from aind_data_schema.components.identifiers import Person, AssetPath


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


class TestAssetPath(unittest.TestCase):
    """Test AssetPath class"""

    def test_asset_path(self):
        """Test AssetPath with valid path"""
        asset_path = AssetPath("/path/to/file.txt")
        asset_path = AssetPath(Path("/path/to/file.txt"))
        self.assertEqual(str(asset_path), "/path/to/file.txt")

        asset_path = AssetPath(PureWindowsPath(r"path\to\file.txt"))
        self.assertEqual(str(asset_path), "path/to/file.txt")


if __name__ == "__main__":
    unittest.main()
