""" tests for Subject """
import unittest
from pathlib import Path
from unittest.mock import patch

from aind_data_schema import Procedures


class BaseTests(unittest.TestCase):
    """tests for the base module"""

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

    def test_get_default_filename(self):
        """tests that default filename returns as expected"""

        p = Procedures.construct()
        expected_default_filename = "procedures.json"
        actual_default_filename = p._get_default_filename()
        self.assertEqual(expected_default_filename, actual_default_filename)

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_standard_file_no_prefix(self, mocked_file):
        """tests that standard file is named and written as expected with no prefix"""
        p = Procedures.construct()
        default_filename = p._get_default_filename()
        json_contents = p.json(indent=3)
        p.write_standard_file()

        mocked_file.assert_called_once_with(default_filename, "w")
        mocked_file.return_value.__enter__().write.assert_called_once_with(
            json_contents
        )

    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_write_standard_file_with_prefix(self, mocked_file):
        """tests that standard file is named and written as expected with prefix"""
        p = Procedures.construct()
        default_filename = p._get_default_filename()
        json_contents = p.json(indent=3)
        new_path = Path("foo") / "bar" / "aibs"
        p.write_standard_file(new_path)

        # It's expected that the file will be written to something like
        # foo/bar/aibs_procedure.json
        expected_file_path = str(new_path) + "_" + default_filename

        mocked_file.assert_called_once_with(expected_file_path, "w")
        mocked_file.return_value.__enter__().write.assert_called_once_with(
            json_contents
        )


if __name__ == "__main__":
    unittest.main()
