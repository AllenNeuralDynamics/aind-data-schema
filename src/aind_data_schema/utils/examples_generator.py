"""script for re-generating all examples"""

import os
import runpy
from glob import glob
from pathlib import Path

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = CURRENT_DIR.parents[2]
EXAMPLES_DIR = ROOT_DIR / "examples"


class ExamplesGenerator:
    """Class to generate example files from .py files in examples directory"""

    def generate_all_examples(self):
        """Generate all examples in EXAMPLES_DIR"""

        print(f"Running all examples in {EXAMPLES_DIR}")
        for example_file in glob(f"{EXAMPLES_DIR}/*.py"):
            print(f"Running {example_file}")
            runpy.run_path(path_name=example_file)

    def generate_example(self, example_file):
        """Generate example from example_file"""

        print(f"Running {example_file}")
        try:
            runpy.run_path(path_name=example_file)
        except Exception as e:
            print(f"Error running {example_file}: {e}")


if __name__ == "__main__":
    """Run all examples in EXAMPLES_DIR"""
    ExamplesGenerator().generate_all_examples()
