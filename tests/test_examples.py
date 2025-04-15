""" testing examples """

import json
import os
import unittest
from pathlib import Path
from aind_data_schema.utils.examples_generator import ExamplesGenerator


EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


class ExampleTests(unittest.TestCase):
    """tests for examples"""

    def setUpClass():
        """Build the examples"""

        # Move to the examples directory
        os.chdir(EXAMPLES_DIR)
        ExamplesGenerator().generate_all_examples()
        # Return to the original directory
        os.chdir(Path(__file__).parents[1])

    def test_examples_generated(self):
        """Test that each example file generates valid JSON."""
        example_files = ["processing.json", "procedures.json"]
        for example_file in example_files:
            example_path = EXAMPLES_DIR / example_file
            with self.subTest(example_file=example_file):
                # Check if the file exists
                self.assertTrue(example_path.exists(), f"{example_file} was not generated.")

                # Validate the JSON content
                try:
                    with open(example_path, "r") as f:
                        json_data = json.load(f)
                    self.assertIsInstance(json_data, dict, f"{example_file} does not contain valid JSON.")
                except json.JSONDecodeError as e:
                    self.fail(f"{example_file} contains invalid JSON: {e}")


if __name__ == "__main__":
    unittest.main()
