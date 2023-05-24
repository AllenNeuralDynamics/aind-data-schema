"""Test aind_utils"""

import unittest

from aind_data_schema.utils.aind_utils import aind_core_models, get_classes


class UtilsTests(unittest.TestCase):
    """Tests for aind_utils methods"""

    def test_get_schemas(self):
        """Tests get schemas method"""
        schema_gen = aind_core_models()

        for schema in schema_gen:
            filename = schema.default_filename()
            schema_filename = filename.replace(".json", "_schema.json")
            schema_contents = schema.schema_json(indent=3)
            self.assertIsNotNone(schema_filename)
            self.assertIsNotNone(schema_contents)

    def test_get_classes(self):
        """Tests get classes method"""
        self.assertEqual(list(get_classes()), list(get_classes(__name__)))


if __name__ == "__main__":
    unittest.main()
