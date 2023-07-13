"""Module to test custom Enums and Literals"""

import json
import unittest

from pydantic import BaseModel

from aind_data_schema.base import ModelEnumLiterals
from aind_data_schema.device import Manufacturer


class TestEnumLiterals(unittest.TestCase):
    """Test Enum Literals methods"""

    def test_model_enum_literals(self):
        """Test ModelEnumLiterals"""

        class TestModel(BaseModel):
            """Test class"""

            manufacturers: ModelEnumLiterals([Manufacturer.NEW_SCALE_TECHNOLOGIES])

        test_instance = TestModel(manufacturers=Manufacturer.NEW_SCALE_TECHNOLOGIES)

        # Test serialization/de-serialization
        test_instance2 = TestModel.parse_obj(json.loads(test_instance.json()))
        self.assertEqual(test_instance, test_instance2)


if __name__ == "__main__":
    unittest.main()
