"""Tests schema_version_bump script"""

import os
import unittest
from pathlib import Path

from aind_data_schema.utils.schema_version_bump import bump_version, run_job

RESOURCE_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / "resources"
NEW_SCHEMA_DIR = RESOURCE_DIR / "schema_version_bump" / "new_schemas"

class SchemaVersionTests(unittest.TestCase):
    """Tests the methods in schema_version_bump module."""

    def test_bump_versions(self):
        """Test the bump_version method."""
        self.assertEqual("1.0.1", bump_version("1.0.0"))

    def test_run_job(self):
        """Tests the run_job method."""
        # Should run without any errors
        self.assertIsNone(
            run_job(
                new_schema_folder=str(NEW_SCHEMA_DIR)
            )
        )

if __name__ == "__main__":
    unittest.main()
