"""Module to test the examples_generator.py script"""

import unittest
from unittest.mock import patch

from aind_data_schema.utils.examples_generator import ExamplesGenerator


class ExamplesGeneratorTest(unittest.TestCase):
    """Tests for ExamplesGenerator methods"""

    @patch("aind_data_schema.base.DataCoreModel.write_standard_file")
    def test_generate_all_files(self, mocked_run_path):
        """Test generate_all_examples method"""

        ExamplesGenerator().generate_all_examples()
        
        # Assert that mock path was called at least once
        self.assertCalledOnce(mocked_run_path)

    @patch("aind_data_schema.base.DataCoreModel.write_standard_file")
    def test_generate_example(self, mocked_run_path):
        """Test generate_example method"""

        ExamplesGenerator().generate_example("fake/path/to/example.py")

        self.assertCalledOnce(mocked_run_path)
