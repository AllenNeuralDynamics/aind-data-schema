import unittest
import json
import os

from argparse import Namespace
from pathlib import Path
from unittest.mock import patch, call, mock_open

from aind_data_schema import DataDescription, Procedures, Processing, Subject
from aind_data_schema.utils.json_writer import SchemaWriter

TEST_ARGS = ["--output", "some_test_dir"]

class JsonWriterTests(unittest.TestCase):
    """Tests for the Json Writer module"""

    def test_get_schemas(self):
        sw = SchemaWriter([])
        schema_gen = sw.get_schemas()

        for schema in schema_gen:
            filename = schema.default_filename()
            schema_contents = schema.schema_json(indent=3)
            self.assertIsNotNone(filename)
            self.assertIsNotNone(schema_contents)

    def test_parse_args(self):
        sw = SchemaWriter(TEST_ARGS)

        sw2 = SchemaWriter([])

        expected_output = "some_test_dir"

        self.assertEqual(expected_output, sw.configs.output)
        self.assertEqual(TEST_ARGS, sw.args)
        self.assertEqual(os.getcwd(), sw2.configs.output)

    @patch("builtins.open", new_callable=mock_open())
    def test_write_to_json(self, mock_json_file):
        """Tests that model is written to JSON"""
        sw = SchemaWriter(TEST_ARGS)
        sw.write_to_json()

        schema_gen = sw.get_schemas()
        calls = []
        for schema in schema_gen:
            filename = schema.default_filename()
            path = Path(os.getcwd()) / filename
            schema_contents = schema.schema_json(indent=3)
            calls.append(call(schema_contents))
        handle = mock_json_file()
        handle.write.assert_has_calls(calls, any_order=True)


if __name__ == "__main__":
    unittest.main()
