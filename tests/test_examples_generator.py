"""Module to test the examples_generator.py script"""

import unittest
from unittest.mock import patch

from aind_data_schema.utils.examples_generator import ExamplesGenerator
from unittest.mock import MagicMock


class ExamplesGeneratorTest(unittest.TestCase):
    """Tests for ExamplesGenerator methods"""

    @patch('aind_data_schema.utils.examples_generator.glob')
    @patch('aind_data_schema.utils.examples_generator.runpy.run_path')
    def test_generate_all_examples(self, mock_run_path, mock_glob):
        """Test generate_all_examples method"""
        mock_glob.return_value = ['example1.py', 'example2.py']
        generator = ExamplesGenerator()
        generator.generate_all_examples()
        self.assertEqual(mock_run_path.call_count, 2)
        mock_run_path.assert_any_call(path_name='example1.py')
        mock_run_path.assert_any_call(path_name='example2.py')

    @patch('aind_data_schema.utils.examples_generator.runpy.run_path')
    def test_generate_example_success(self, mock_run_path):
        """Test generate_example method when example runs successfully"""
        generator = ExamplesGenerator()
        generator.generate_example('example1.py')
        mock_run_path.assert_called_once_with(path_name='example1.py')

    @patch('aind_data_schema.utils.examples_generator.runpy.run_path')
    def test_generate_example_failure(self, mock_run_path):
        """Test generate_example method when example raises an exception"""
        mock_run_path.side_effect = Exception('Test exception')
        generator = ExamplesGenerator()
        with self.assertLogs(level='INFO') as log:
            generator.generate_example('example1.py')
            self.assertIn('Error running example1.py: Test exception', log.output[-1])


if __name__ == "__main__":
    unittest.main()