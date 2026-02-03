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

    def generate_all_examples(self, output_directory=None):
        """Generate all examples in EXAMPLES_DIR
        
        Parameters
        ----------
        output_directory : str or Path, optional
            Directory where generated JSON files should be written.
            If None, defaults to the same directory as the example script.
        """

        logging.info(f"Running all examples in {EXAMPLES_DIR}")
        for example_file in glob(str(EXAMPLES_DIR / "*.py")):
            if Path(example_file).name == "__init__.py":
                continue
            self.generate_example(example_file, output_directory)

    def generate_example(self, example_file, output_directory=None):
        """Generate example from example_file
        
        Parameters
        ----------
        example_file : str or Path
            Path to the example .py file to run
        output_directory : str or Path, optional
            Directory where generated JSON files should be written.
            If None, defaults to the same directory as the example script.
        """

        logging.info(f"Running {example_file}")
        try:
            cmd = ["python", example_file]
            if output_directory is not None:
                cmd.extend(["--output-dir", str(output_directory)])
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            logging.info(f"Error running {example_file}: {e}")


if __name__ == "__main__":
    """Run all examples in EXAMPLES_DIR"""
    ExamplesGenerator().generate_all_examples()
