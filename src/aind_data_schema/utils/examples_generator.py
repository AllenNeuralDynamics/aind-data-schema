"""script for re-generating all examples"""

import runpy
from glob import glob
from pathlib import Path
import os

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = CURRENT_DIR.parents[2]
EXAMPLES_DIR = ROOT_DIR / "examples"

if __name__ == '__main__':

    print(f"Running all examples in {EXAMPLES_DIR}")
    for example_file in glob(f"{EXAMPLES_DIR}/*.py"):
        print(f"Running {example_file}")
        runpy.run_path(path_name=example_file)
