"""Module to test the examples_generator.py script"""

import json
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch
from aind_data_schema.utils.examples_generator import ExamplesGenerator

class ExamplesGeneratorTest(unittest.TestCase):
    """Tests for ExamplesGenerator methods"""

    @patch("AindCoreModel.write_standard_file()")
    def test_generate_all_files(self):
        ExamplesGenerator().generate_all_examples()
