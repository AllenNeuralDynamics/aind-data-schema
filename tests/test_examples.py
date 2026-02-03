""" testing examples """

import json
import os
import unittest
from pathlib import Path

from aind_data_schema.utils.examples_generator import ExamplesGenerator

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


class ExampleTests(unittest.TestCase):  # pragma: no cover
    """tests for examples"""

    @classmethod
    def setUpClass(cls):
        """Build the examples"""

        # Move to the examples directory
        os.chdir(EXAMPLES_DIR)
        # Remove all .json files in the examples directory
        for file in os.listdir(EXAMPLES_DIR):
            if file.endswith(".json") and not file.startswith("__"):
                os.remove(EXAMPLES_DIR / file)
        ExamplesGenerator().generate_all_examples()
        # Return to the original directory
        os.chdir(Path(__file__).parents[1])

    def test_examples_generated(self):
        """Test that each example file generates valid JSON."""
        # Get all json files in the examples directory
        example_files = [f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".py") and not f.startswith("__")]
        example_files = [f.replace(".py", ".json") for f in example_files]

        for example_file in example_files:
            example_path = EXAMPLES_DIR / example_file
            with self.subTest(example_file=example_file):
                # Check if the file exists
                self.assertTrue(example_path.exists(), f"{example_file} was not generated.")

                # Validate the JSON content
                with open(example_path, "r") as f:
                    json_data = json.load(f)
                self.assertIsInstance(json_data, dict, f"{example_file} does not contain valid JSON.")


if __name__ == "__main__":
    unittest.main()
