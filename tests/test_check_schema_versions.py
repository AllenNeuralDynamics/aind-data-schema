"""Tests schema_version_check script"""

import os
import unittest
from pathlib import Path

from aind_data_schema.utils.schema_version_check import compare_versions, run_job

RESOURCE_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / "resources"
NEW_SCHEMA_DIR = RESOURCE_DIR / "schema_version_comparison" / "new_schemas"
NEW_SCHEMA_DIR2 = RESOURCE_DIR / "schema_version_comparison" / "new_schemas_bad_versions"
OLD_SCHEMA_DIR = RESOURCE_DIR / "schema_version_comparison" / "old_schemas"


class SchemaVersionTests(unittest.TestCase):
    """Tests the methods in schema_version_check module."""

    def test_compare_versions(self):
        """Test the compare_version method."""
        true_checks = [
            compare_versions("1.0.0", "0.13.4"),
            compare_versions("0.14.0", "0.13.4"),
            compare_versions("0.13.5", "0.13.4"),
            compare_versions("0.0.1", None),
            # If old schema_version is None of malformed, user can set the new
            # schema version to whatever they want
            compare_versions("0.7.1", None),
            compare_versions("0.0.1", "0.8"),
        ]

        for true_check in true_checks:
            self.assertEqual((True, None), true_check)

        # False checks
        self.assertEqual(
            (False, "Version not bumped correctly. New Version: 0.0.1. Old Version: 0.0.2"),
            compare_versions("0.0.1", "0.0.2"),
        )
        self.assertEqual(
            (False, "Version not bumped correctly. New Version: 0.3.2. Old Version: 0.2.1"),
            compare_versions("0.3.2", "0.2.1"),
        )
        self.assertEqual(
            (False, "Version not bumped correctly. New Version: 2.0.1. Old Version: 1.2.3"),
            compare_versions("2.0.1", "1.2.3"),
        )
        self.assertEqual(
            (False, "Version not bumped correctly. New Version: 0.0.1. Old Version: 0.0.3"),
            compare_versions("0.0.1", "0.0.3"),
        )
        self.assertEqual(
            (False, "Version not bumped correctly. New Version: 0.1.1. Old Version: 0.2.1"),
            compare_versions("0.1.1", "0.2.1"),
        )
        self.assertEqual(
            (False, "Version not bumped correctly. New Version: 1.0.2. Old Version: 2.1.4"),
            compare_versions("1.0.2", "2.1.4"),
        )
        self.assertEqual((False, "Malformed version: 1.0"), compare_versions("1.0", "2.1.4"))
        self.assertEqual((False, "Malformed version: .0.1"), compare_versions(".0.1", None))

    def test_run_job(self):
        """Tests the run_job method."""
        # Should run without any errors
        self.assertIsNone(run_job(new_schema_folder=str(NEW_SCHEMA_DIR), old_schema_folder=str(OLD_SCHEMA_DIR)))

        # Should raise an assertion
        expected_error_message = (
            "There were issues checking the schema versions: ["
            "'data_description_schema.json - Malformed version: 0.3', "
            "'subject_schema.json - Version not bumped correctly. "
            "New Version: 0.2.2. Old Version: 0.2.2']"
        )
        with self.assertRaises(AssertionError) as error:
            run_job(new_schema_folder=str(NEW_SCHEMA_DIR2), old_schema_folder=str(OLD_SCHEMA_DIR))
        self.assertEqual(str(error.exception), expected_error_message)


if __name__ == "__main__":
    unittest.main()
