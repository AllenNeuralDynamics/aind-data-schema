"""Tests schema_version_bump module"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from semver import Version

from aind_data_schema.core.session import Session
from aind_data_schema.core.subject import Subject
from aind_data_schema.utils.json_writer import SchemaWriter
from aind_data_schema.utils.schema_version_bump import SchemaVersionHandler


class SchemaVersionTests(unittest.TestCase):
    """Tests the methods in the SchemaVersionHandler class."""

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
    @patch("pathlib.Path.exists")
    def test_get_list_of_models_that_changed(self, mock_exists: MagicMock, mock_json_load: MagicMock, _: MagicMock):
        """Tests get_list_of_models_that_changed method."""
        mock_json_load.side_effect = self.mock_open_values
        mock_exists.return_value = True

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        models_that_changed = handler._get_list_of_models_that_changed()
        self.assertTrue(Session in models_that_changed)
        self.assertTrue(Subject in models_that_changed)

    def test_get_list_of_incremented_versions(self):
        """Tests get_list_of_incremented_versions method"""

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        old_subject_version = Subject.model_fields["schema_version"].default
        new_subject_version = str(Version.parse(old_subject_version).bump_patch())
        old_session_version = Session.model_fields["schema_version"].default
        new_session_version = str(Version.parse(old_session_version).bump_patch())
        # Pycharm raises a warning about types that we can ignore
        # noinspection PyTypeChecker
        model_map = handler._get_incremented_versions_map([Subject, Session])
        expected_model_map = {Subject: new_subject_version, Session: new_session_version}
        self.assertEqual(expected_model_map, model_map)

    @patch("builtins.open")
    def test_write_new_file(self, mock_open: MagicMock):
        """ "Tests write_new_file method"""

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        file_contents = [b"Hello World!", b"Goodbye?"]
        file_path = "output_dir"
        handler._write_new_file(file_contents, file_path)
        mock_open.assert_called_once_with(file_path, "wb")
        mock_open.return_value.__enter__().write.assert_has_calls([call(file_contents[0]), call(file_contents[1])])

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._write_new_file")
    def test_update_files(self, mock_write: MagicMock):
        """Tests the update_files method"""
        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        old_subject_version = Subject.model_fields["schema_version"].default
        new_subject_version = str(Version.parse(old_subject_version).bump_patch())
        old_session_version = Session.model_fields["schema_version"].default
        new_session_version = str(Version.parse(old_session_version).bump_patch())
        # Pycharm raises a warning about types that we can ignore
        # noinspection PyTypeChecker
        handler._update_files({Subject: new_subject_version, Session: new_session_version})

        expected_line_change0 = (
            f'    schema_version: Literal["{new_subject_version}"] = Field("{new_subject_version}")\n'
        )
        expected_line_change1 = (
            f'    schema_version: Literal["{new_session_version}"] = Field("{new_session_version}")\n'
        )

        mock_write_args0 = mock_write.mock_calls[0].args
        mock_write_args1 = mock_write.mock_calls[1].args
        self.assertTrue("subject.py" in str(mock_write_args0[1]))
        self.assertTrue(expected_line_change0.encode() in mock_write_args0[0])
        self.assertTrue("session.py" in str(mock_write_args1[1]))
        self.assertTrue(expected_line_change1.encode() in mock_write_args1[0])

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._get_list_of_models_that_changed")
    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._update_files")
    def test_run_job(self, mock_update_files: MagicMock, mock_get_list_of_models: MagicMock):
        """Tests run_job method"""

        old_subject_version = Subject.model_fields["schema_version"].default
        new_subject_version = str(Version.parse(old_subject_version).bump_patch())
        old_session_version = Session.model_fields["schema_version"].default
        new_session_version = str(Version.parse(old_session_version).bump_patch())
        mock_get_list_of_models.return_value = [Subject, Session]
        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        handler.run_job()
        mock_update_files.assert_called_once_with({Subject: new_subject_version, Session: new_session_version})


if __name__ == "__main__":
    unittest.main()
