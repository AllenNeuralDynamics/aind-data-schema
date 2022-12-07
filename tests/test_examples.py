import glob
import unittest
from pathlib import Path
import subprocess

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


class ExampleTests(unittest.TestCase):
    """tests for examples"""

    def test_examples(self):
        for example_file in glob.glob(f"{EXAMPLES_DIR}/*.py"):
            print(example_file)

            json_file = example_file.replace(".py", ".json")

            with open(json_file, "r") as f:
                target_data = f.read().replace("\r\n", "\n")

            cmd = f"python {example_file}"
            test_data = (
                subprocess.check_output(cmd, shell=True)
                .decode("utf-8")
                .replace("\r\n", "\n")
            )

            assert test_data == target_data


if __name__ == "__main__":
    unittest.main()
