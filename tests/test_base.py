""" tests for Subject """
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from aind_data_schema.core.subject import Subject


class BaseTests(unittest.TestCase):
    """tests for the base module"""

    def test_described_by(self):
        """test that described by works"""

        s = Subject.model_construct()

        self.assertEqual(
            "https://raw.githubusercontent.com/AllenNeuralDynamics/"
            "aind-data-schema/main/src/aind_data_schema/core/subject.py",
            s.describedBy,
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_write_standard_file(self, mock_open: MagicMock):
        """Tests writer with suffix and output directory defined"""

        s = Subject.model_construct()
        s.write_standard_file(output_directory=Path("dir"), suffix=".foo.bar")
        mock_open.assert_has_calls([call(Path("dir/subject.foo.bar"), "w")])
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
