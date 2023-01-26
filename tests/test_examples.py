""" testing examples """

import glob
import importlib.util
import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


class ExampleTests(unittest.TestCase):
    """tests for examples"""

    def test_examples(self):
        """run through each example, compare to rendered json"""

        for example_file in glob.glob(f"{EXAMPLES_DIR}/*.py"):
            logging.debug(f"testing {example_file}")

            json_file = example_file.replace(".py", ".json")

            with open(json_file, "r") as f:
                target_data = f.read().replace("\r\n", "\n")

            spec = importlib.util.spec_from_file_location("test_module", example_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules["test_module"] = module

            with patch("builtins.open", new_callable=mock_open) as mocked_file:
                spec.loader.exec_module(module)
                h = mocked_file.return_value.__enter__()
                h.write.assert_called_once_with(target_data)


if __name__ == "__main__":
    unittest.main()
