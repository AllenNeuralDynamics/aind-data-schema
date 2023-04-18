"""Module to test json_writer classes."""

import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from aind_data_schema.utils.json_writer import SchemaWriter


class SchemaWriterTests(unittest.TestCase):
    """Tests for SchemaWriter methods"""

    TEST_ARGS = ["--output", "some_test_dir"]

    def test_get_schemas(self):
        """Tests get schemas method"""
        sw = SchemaWriter([])
        schema_gen = sw._get_schemas()

        for schema in schema_gen:
            filename = schema.default_filename()
            schema_filename = filename.replace(".json", "_schema.json")
            schema_contents = schema.schema_json(indent=3)
            self.assertIsNotNone(schema_filename)
            self.assertIsNotNone(schema_contents)

    def test_parse_args(self):
        """Tests arguments are parsed correctly."""
        sw = SchemaWriter(self.TEST_ARGS)

        sw2 = SchemaWriter([])

        expected_output = "some_test_dir"

        self.assertEqual(expected_output, sw.configs.output)
        self.assertEqual(self.TEST_ARGS, sw.args)
        self.assertEqual(os.getcwd(), sw2.configs.output)

    @patch("builtins.open", new_callable=mock_open())
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_write_to_json(self, mock_mkdir: MagicMock, mock_path_exists: MagicMock, mock_file: MagicMock):
        """Tests that model is written to JSON"""
        mock_path_exists.return_value = False
        sw = SchemaWriter(self.TEST_ARGS)
        schema_list = list(sw._get_schemas())
        mock_path_exists.side_effect = [False] + [True for _ in schema_list[:-1]]
        sw.write_to_json()
        file_handle = mock_file.return_value.__enter__.return_value
        schema_gen = sw._get_schemas()
        open_calls = []
        write_calls = []
        for schema in schema_gen:
            filename = schema.default_filename()
            schema_filename = filename.replace(".json", "_schema.json")
            path = Path("some_test_dir") / schema_filename
            schema_contents = schema.schema_json(indent=3)
            open_calls.append(call(path, "w"))
            write_calls.append(call(schema_contents))
        mock_mkdir.assert_called_once_with(Path("some_test_dir"), 511)
        mock_file.assert_has_calls(open_calls, any_order=True)
        file_handle.write.assert_has_calls(write_calls, any_order=True)

    @patch("builtins.open", new_callable=mock_open())
    @patch("os.path.exists")
    @patch("os.mkdir")
    def test_write_to_json_version_number(
        self, mock_mkdir: MagicMock, mock_path_exists: MagicMock, mock_file: MagicMock
    ):
        """Tests that model is written to JSON with version directory"""
        mock_path_exists.return_value = False
        sys_args = ["--output", "some_test_dir", "--attach-version"]
        sw = SchemaWriter(sys_args)
        sw.write_to_json()
        file_handle = mock_file.return_value.__enter__.return_value
        schema_list = list(sw._get_schemas())
        mock_path_exists.side_effect = [False] + [True for _ in schema_list[:-1]]
        schema_gen = sw._get_schemas()
        open_calls = []
        write_calls = []
        mkdir_calls = []
        for schema in schema_gen:
            filename = schema.default_filename()
            schema_filename = filename.replace(".json", "_schema.json")
            model_directory_name = schema_filename.replace("_schema.json", "")
            path = Path("some_test_dir") / model_directory_name / schema.construct().schema_version / schema_filename
            schema_contents = schema.schema_json(indent=3)
            mkdir_calls.append(call("some_test_dir", 511))
            mkdir_calls.append(call(str(path.parent.parent), 511))
            mkdir_calls.append(call(path.parent, 511))

            open_calls.append(call(path, "w"))
            write_calls.append(call(schema_contents))
        mock_mkdir.assert_has_calls(
            calls=mkdir_calls,
            any_order=True,
        )
        mock_file.assert_has_calls(open_calls, any_order=True)
        file_handle.write.assert_has_calls(write_calls, any_order=True)


if __name__ == "__main__":
    unittest.main()
