"""Tests schema_version_bump module"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from semver import Version

from aind_data_schema.core.session import Session
from aind_data_schema.core.subject import Subject
from aind_data_schema.core.rig import Rig
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

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._get_schema_json")
    def test_get_list_of_incremented_versions(self, mock_get_schema: MagicMock):
        """Tests get_list_of_incremented_versions method"""

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        old_subject_version = Subject.model_fields["schema_version"].default
        new_subject_version = str(Version.parse(old_subject_version).bump_patch())
        old_session_version = Session.model_fields["schema_version"].default
        new_session_version = str(Version.parse(old_session_version).bump_patch())

        def side_effect(model):
            """Side effect for mock_get_schema"""
            if model == Subject:
                return {"properties": {"schema_version": {"default": old_subject_version}}}
            elif model == Session:
                return {"properties": {"schema_version": {"default": old_session_version}}}

        mock_get_schema.side_effect = side_effect

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

    @patch("builtins.open")
    @patch("json.load")
    @patch("pathlib.Path.exists")
    def test_get_schema_json(self, mock_exists: MagicMock, mock_json_load: MagicMock, mock_open: MagicMock):
        """Tests _get_schema_json method"""
        handler = SchemaVersionHandler(json_schemas_location=Path("."))

        mock_exists.return_value = True
        mock_json_load.return_value = {"properties": {"schema_version": {"default": "1.0.0"}}}

        model = MagicMock()
        model.default_filename.return_value = "test_model.json"

        schema_json = handler._get_schema_json(model)
        self.assertEqual(schema_json, {"properties": {"schema_version": {"default": "1.0.0"}}})

        mock_open.assert_called_once_with(Path("./test_model_schema.json"), "r")
        mock_json_load.assert_called_once()

    @patch("pathlib.Path.exists")
    def test_get_schema_json_file_not_found(self, mock_exists: MagicMock):
        """Tests _get_schema_json method when file is not found"""
        handler = SchemaVersionHandler(json_schemas_location=Path("."))

        mock_exists.return_value = False

        model = MagicMock()
        model.default_filename.return_value = "test_model.json"

        with self.assertRaises(FileNotFoundError):
            handler._get_schema_json(model)

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._get_schema_json")
    def test_get_incremented_versions_map_exception(self, mock_get_schema: MagicMock):
        """Test that missing schema_version field raises an error"""
        handler = SchemaVersionHandler(json_schemas_location=Path("."))

        mock_get_schema.return_value = {}

        with self.assertRaises(ValueError):
            handler._get_incremented_versions_map([Subject])

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._get_schema_json")
    def test_get_incremented_versions_map_skip(self, mock_get_schema: MagicMock):
        """Test that missing schema_version field raises an error"""
        handler = SchemaVersionHandler(json_schemas_location=Path("."))

        mock_get_schema.return_value = {"properties": {"schema_version": {"default": "0.0.0"}}}

        empty_map = handler._get_incremented_versions_map([Subject])
        self.assertEqual(empty_map, {})

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._write_new_file")
    def test_update_files(self, mock_write: MagicMock):
        """Tests the update_files method"""
        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        old_subject_version = Subject.model_fields["schema_version"].default
        new_subject_version = str(Version.parse(old_subject_version).bump_patch())
        old_session_version = Session.model_fields["schema_version"].default
        new_session_version = str(Version.parse(old_session_version).bump_patch())
        old_rig_version = Rig.model_fields["schema_version"].default
        new_rig_version = str(Version.parse(old_rig_version).bump_minor())
        # Pycharm raises a warning about types that we can ignore
        # noinspection PyTypeChecker
        handler._update_files({Subject: new_subject_version, Session: new_session_version, Rig: new_rig_version})

        expected_line_change0 = (
            f'schema_version: SkipValidation[Literal["{new_subject_version}"]] = Field(default="{new_subject_version}")'
        )
        expected_line_change1 = (
            f'schema_version: SkipValidation[Literal["{new_session_version}"]] = Field(default="{new_session_version}")'
        )

        mock_write_args0 = mock_write.mock_calls[0].args
        mock_write_args1 = mock_write.mock_calls[1].args
        self.assertTrue(expected_line_change0 in str(mock_write_args0[0]))
        self.assertTrue("subject.py" in str(mock_write_args0[1]))
        self.assertTrue(expected_line_change1 in str(mock_write_args1[0]))
        self.assertTrue("session.py" in str(mock_write_args1[1]))

    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._get_schema_json")
    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._get_list_of_models_that_changed")
    @patch("aind_data_schema.utils.schema_version_bump.SchemaVersionHandler._update_files")
    def test_run_job(
        self, mock_update_files: MagicMock, mock_get_list_of_models: MagicMock, mock_get_schema: MagicMock
    ):
        """Tests run_job method"""

        old_subject_version = Subject.model_fields["schema_version"].default
        new_subject_version = str(Version.parse(old_subject_version).bump_patch())
        old_session_version = Session.model_fields["schema_version"].default
        new_session_version = str(Version.parse(old_session_version).bump_patch())

        mock_get_list_of_models.return_value = [Subject, Session]

        def side_effect(model):
            """Return values for get_schema_json"""
            if model == Subject:
                return {"properties": {"schema_version": {"default": old_subject_version}}}
            elif model == Session:
                return {"properties": {"schema_version": {"default": old_session_version}}}

        mock_get_schema.side_effect = side_effect

        handler = SchemaVersionHandler(json_schemas_location=Path("."))
        handler.run_job()
        mock_update_files.assert_called_once_with({Subject: new_subject_version, Session: new_session_version})


if __name__ == "__main__":
    unittest.main()
