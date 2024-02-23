"""Tests schema_version_bump script"""

import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from aind_data_schema.base import AindCoreModel
from aind_data_schema.utils.json_writer import SchemaWriter
from aind_data_schema.core.subject import Subject
from aind_data_schema.core.session import Session

from aind_data_schema.utils.schema_version_bump import bump_version, run_job, \
    SchemaVersionHandler

RESOURCE_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / "resources"
NEW_SCHEMA_DIR = RESOURCE_DIR / "schema_version_bump" / "main_branch_schemas"


class SchemaVersionTests(unittest.TestCase):
    """Tests the methods in schema_version_bump module."""

    @classmethod
    def setUpClass(cls):
        """Load json files before running tests."""
        mock_open_return_values = []
        for core_model in SchemaWriter.get_schemas():
            contents = core_model.model_json_schema()
            if core_model in [Session, Subject]:
                contents["description"] = "I HAVE CHANGED!"
            mock_open_return_values.append(contents)
        cls.mock_open_values = mock_open_return_values

    @patch("builtins.open")
    @patch("json.load")
    def test_get_list_of_models_that_changed(self, mock_json_load: MagicMock, _: MagicMock):
        mock_json_load.side_effect = self.mock_open_values

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        models_that_changed = handler.get_list_of_models_that_changed()
        self.assertTrue(Session in models_that_changed)
        self.assertTrue(Subject in models_that_changed)

    def test_get_list_of_incremented_versions(self):

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        model_map = handler.get_incremented_versions_map([Subject, Session])
        print(model_map)

    @patch("builtins.open")
    def test_update_files(self, _: MagicMock):
        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        handler.update_files({Subject: "0.5.6", Session: "0.1.9"})


if __name__ == "__main__":
    unittest.main()
