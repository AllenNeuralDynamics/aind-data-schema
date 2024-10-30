"""Tests methods in utils.docdb module"""

import json
import os
import unittest
from pathlib import Path

from aind_data_schema.utils.docdb import is_dict_corrupt

TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
TEST_UTILS_DIR = TEST_DIR / "resources" / "utils"


class TestDocdbUtils(unittest.TestCase):
    """Class to test methods in utils.docdb module."""

    def test_is_dict_corrupt(self):
        """Tests is_dict_corrupt method"""
        good_contents = [
            {"a": 1, "b": {"c": 2, "d": 3}},
            {"a": 1, "b": {"c": 2, "d": 3}, "e": ["f", "g"]},
            {"a": 1, "b": {"c": 2, "d": 3}, "e": ["f.valid", "g"]},
            {"a": 1, "b": {"c": {"d": 2}, "e": 3}},
            {"a": 1, "b": [{"c": 2}, {"d": 3}], "e": 4},
        ]
        bad_contents = [
            {"a.1": 1, "b": {"c": 2, "d": 3}},
            {"a": 1, "b": {"c": 2, "$d": 3}},
            {"a": 1, "b": {"c": {"d": 2}, "$e": 3}},
            {"a": 1, "b": {"c": 2, "d": 3, "e.csv": 4}},
            {"a": 1, "b": [{"c": 2}, {"d.csv": 3}], "e": 4},
        ]
        invalid_types = [
            json.dumps({"a": 1, "b": {"c": 2, "d": 3}}),
            [{"a": 1}, {"b": {"c": 2, "d": 3}}],
            1,
            None,
        ]
        for contents in good_contents:
            with self.subTest(contents=contents):
                self.assertFalse(is_dict_corrupt(contents))
        for contents in bad_contents:
            with self.subTest(contents=contents):
                self.assertTrue(is_dict_corrupt(contents))
        for contents in invalid_types:
            with self.subTest(contents=contents):
                self.assertTrue(is_dict_corrupt(contents))


if __name__ == "__main__":
    unittest.main()
