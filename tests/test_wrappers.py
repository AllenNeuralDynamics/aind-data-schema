"""Test wrappers module"""

import unittest
from pathlib import Path, PureWindowsPath

from aind_data_schema.components.wrappers import AssetPath


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
