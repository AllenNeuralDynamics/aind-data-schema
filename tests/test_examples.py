""" testing examples """

import json
import os
import unittest
import tempfile
import shutil
from pathlib import Path

from aind_data_schema.utils.examples_generator import ExamplesGenerator

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


class ExampleTests(unittest.TestCase):  # pragma: no cover
    """tests for examples"""

    @classmethod
    def setUpClass(cls):
        """Build the examples in a temporary directory"""
        cls.temp_dir = tempfile.mkdtemp()
        cls.temp_path = Path(cls.temp_dir)
        ExamplesGenerator().generate_all_examples(output_directory=cls.temp_path)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory"""
        if hasattr(cls, 'temp_dir') and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_examples_generated(self):
        """Test that each example file generates valid JSON."""
        example_files = [f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".py") and not f.startswith("__")]
        example_files = [f.replace(".py", ".json") for f in example_files]

        for example_file in example_files:
            example_path = self.temp_path / example_file
            with self.subTest(example_file=example_file):
                self.assertTrue(example_path.exists(), f"{example_file} was not generated.")

                with open(example_path, "r") as f:
                    json_data = json.load(f)
                self.assertIsInstance(json_data, dict, f"{example_file} does not contain valid JSON.")


if __name__ == "__main__":
    unittest.main()
