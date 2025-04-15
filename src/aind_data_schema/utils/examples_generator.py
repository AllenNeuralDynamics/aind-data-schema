"""script for re-generating all examples"""

import logging
import os
import runpy
from glob import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = CURRENT_DIR.parents[2]
EXAMPLES_DIR = ROOT_DIR / "examples"


class ExamplesGenerator:
    """Class to generate example files from .py files in examples directory"""

    def generate_all_examples(self):
        """Generate all examples in EXAMPLES_DIR in parallel"""

        logging.info(f"Running all examples in {EXAMPLES_DIR}")

        def run_example(example_file):  # pragma: no cover
            """ Run example file"""
            if "__init__" in example_file:
                return
            logging.info(f"Running {example_file}")
            try:
                runpy.run_path(path_name=example_file)
            except Exception as e:
                logging.info(f"Error running {example_file}: {e}")

        example_files = [f for f in glob(f"{EXAMPLES_DIR}/*.py") if "__init__" not in f]

        with ThreadPoolExecutor() as executor:
            executor.map(run_example, example_files)

    def generate_example(self, example_file):
        """Generate example from example_file"""

        logging.info(f"Running {example_file}")
        try:
            runpy.run_path(path_name=example_file)
        except Exception as e:
            logging.info(f"Error running {example_file}: {e}")


if __name__ == "__main__":
    """Run all examples in EXAMPLES_DIR"""
    ExamplesGenerator().generate_all_examples()
