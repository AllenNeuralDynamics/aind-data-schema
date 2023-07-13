""" tests for Subject """
import unittest
from pathlib import Path
from unittest.mock import patch

from aind_data_schema import Procedures, Processing, RawDataDescription, Subject
from aind_data_schema.base import AindCoreModel


class BaseTests(unittest.TestCase):
    """tests for the base module"""

    def test_schema_version_check(self):
        """test schema version"""
        with self.assertRaises(Exception):
            AindCoreModel(schema_version="123", describedBy="test")
        a = AindCoreModel(schema_version="1.2.3", describedBy="test")
        self.assertEqual("1.2.3", a.schema_version)

    def test_described_by(self):
        """test that described by works"""

        p = Procedures(subject_id="1234")

        self.assertEqual(
            p.describedBy,
            (
                "https://raw.githubusercontent.com/AllenNeuralDynamics/"
                "aind-data-schema/main/src/aind_data_schema/procedures.py"
            ),
        )

    @patch("logging.Logger.error")
    def test_default_filename(self, mock_log):
        """tests that default filename returns as expected"""

        test_models = [
            (RawDataDescription, "data_description.json"),
            (Procedures, "procedures.json"),
            (Subject, "subject.json"),
            (Processing, "processing.json"),
        ]
        for model, expected_name in test_models:
            actual_name = model.default_filename()
            self.assertEqual(expected_name, actual_name)

        with self.assertRaises(IndexError):
            AindCoreModel.default_filename()
        mock_log.assert_called_with(
            "Unable to find direct AindCoreModel subclass for" " <class 'aind_data_schema.base.AindCoreModel'>"
        )

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_standard_file_no_prefix(self, mock_open):
        """tests that standard file is named and written as expected with no prefix"""
        p = Procedures.construct()
        default_filename = p.default_filename()
        json_contents = p.json(indent=3)
        p.write_standard_file()

        mock_open.assert_called_once_with(default_filename, "w")
        mock_open.return_value.__enter__().write.assert_called_once_with(json_contents)

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_standard_file_with_prefix(self, mock_open):
        """tests that standard file is named and written as expected with filename prefix"""
        p = Procedures.construct()
        default_filename = p.default_filename()
        json_contents = p.json(indent=3)
        prefix = "aibs"
        p.write_standard_file(prefix=prefix)

        # It's expected that the file will be written to something like
        # aibs_procedure.json
        expected_file_path = str(prefix) + "_" + default_filename

        mock_open.assert_called_once_with(expected_file_path, "w")
        mock_open.return_value.__enter__().write.assert_called_once_with(json_contents)

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_standard_file_with_output_directory(self, mock_open):
        """tests that standard file is named and written as expected with designated output directory"""
        p = Procedures.construct()
        default_filename = p.default_filename()
        json_contents = p.json(indent=3)
        new_path = Path("foo") / "bar"
        p.write_standard_file(output_directory=new_path)

        # It's expected that the file will be written to something like
        # foo/bar/procedure.json
        expected_file_path = new_path / default_filename

        mock_open.assert_called_once_with(expected_file_path, "w")
        mock_open.return_value.__enter__().write.assert_called_once_with(json_contents)

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_standard_file_with_output_directory_and_prefix(self, mock_open):
        """tests that standard file is named and written as expected
        with designated output directory and filename prefix"""
        p = Procedures.construct()
        default_filename = p.default_filename()
        json_contents = p.json(indent=3)
        new_path = Path("foo") / "bar"
        prefix = "aibs"
        p.write_standard_file(output_directory=new_path, prefix=prefix)

        # It's expected that the file will be written to something like
        # foo/bar/aibs_procedure.json
        expected_file_path = new_path / (prefix + "_" + default_filename)

        mock_open.assert_called_once_with(expected_file_path, "w")
        mock_open.return_value.__enter__().write.assert_called_once_with(json_contents)


if __name__ == "__main__":
    unittest.main()
