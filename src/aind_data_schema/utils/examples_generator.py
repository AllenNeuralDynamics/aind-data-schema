"""script for re-generating all examples"""

import logging
import os
import subprocess
from glob import glob
from pathlib import Path

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = CURRENT_DIR.parents[2]
EXAMPLES_DIR = ROOT_DIR / "examples"


class ExamplesGenerator:
    """Class to generate example files from .py files in examples directory"""

    def generate_all_examples(self):
        """Generate all examples in EXAMPLES_DIR"""

        logging.info(f"Running all examples in {EXAMPLES_DIR}")
        for example_file in glob(str(EXAMPLES_DIR / "*.py")):
            if Path(example_file).name == "__init__.py":
                continue
            self.generate_example(example_file)

    def generate_example(self, example_file):
        """Generate example from example_file"""

        logging.info(f"Running {example_file}")
        try:
            subprocess.run(["python", example_file], check=True)
        except subprocess.CalledProcessError as e:
            logging.info(f"Error running {example_file}: {e}")


if __name__ == "__main__":
    """Run all examples in EXAMPLES_DIR"""
    ExamplesGenerator().generate_all_examples()
