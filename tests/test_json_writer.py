import unittest
import json

from pathlib import Path
from unittest.mock import patch

from aind_data_schema import DataDescription, Procedures, Processing, Subject
from aind_data_schema.utils.json_writer import SchemaWriter

TEST_PATH = Path("fake_path") / "aind"

class JsonWriterTests(unittest.TestCase):
    """Tests for the Json Writer module"""

    def test_schema_filename(self):
        """Tests that filename is returned in expected format"""

        test_models = [
            (DataDescription, "data_description.json"),
            (Procedures, "procedures.json"),
            (Processing, "processing.json"),
            (Subject, "subject.json"),
        ]

        for model, expected_filename in test_models:
            actual_filename = SchemaWriter.schema_filename(model)
            self.assertEqual(expected_filename, actual_filename)

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_to_json(self, mock_json_file):
        """Tests that model is written to JSON"""
        s = SchemaWriter.write_to_json(Subject, TEST_PATH)
        s_filename = SchemaWriter.schema_filename(Subject)
        expected_path = str(TEST_PATH) + s_filename

        mock_json_file.assert_called_once_with(expected_path, "w")


if __name__ == "__main__":
    unittest.main()
