"""Module to test custom Enums and Literals"""

import json
import unittest

from enum import Enum

from aind_data_schema.base import ModelEnumLiterals, EnumLiterals, PIDName, AindModel
from aind_data_schema.device import Manufacturer


class TestEnumLiterals(unittest.TestCase):
    """Test Enum Literals methods"""

    def test_enum_literals(self):
        """test that EnumLiterals works"""

        class TestEnum(Enum):
            """temp enum"""

            FOO = "foo"
            BAR = "bar"

        class TestThing(AindModel):
            """temp model"""

            a: EnumLiterals([TestEnum.FOO, TestEnum.BAR])
            b: EnumLiterals([TestEnum.FOO, TestEnum.BAR], optional=True)

        # ensure we can generate the schema
        schema = TestThing.schema()

        assert set(schema["properties"]["a"]["enumNames"]) == {"foo", "bar"}
        assert set(schema["properties"]["b"]["enumNames"]) == {"foo", "bar"}
        assert "b" not in schema["required"]

        # now check that the json schema is good
        json_schema = TestThing.schema_json(indent=2)

        assert json_schema is not None

    def test_model_enum_literals(self):
        """test that ModelEnumLiterals works"""

        class TestEnum(Enum):
            """temp enum"""

            FOO = PIDName(name="foo")
            BAR = PIDName(name="bar", abbreviation="b")

        class TestThing(AindModel):
            """temp model"""

            a: ModelEnumLiterals([TestEnum.FOO, TestEnum.BAR])
            b: ModelEnumLiterals([TestEnum.FOO, TestEnum.BAR], optional=True)

        # ensure we can generate the schema
        schema = TestThing.schema()

        assert set(schema["properties"]["a"]["enumNames"]) == {"foo", "bar"}
        assert set(schema["properties"]["b"]["enumNames"]) == {"foo", "bar"}
        assert "b" not in schema["required"]

        # now check that the json schema is good
        json_schema = TestThing.schema_json(indent=2)

        assert json_schema is not None

    def test_model_enum_literals_rehydrate(self):
        """Test ModelEnumLiterals"""

        class TestModel(AindModel):
            """Test class"""

            manufacturer: ModelEnumLiterals([Manufacturer.NEW_SCALE_TECHNOLOGIES])

        test_instance = TestModel(manufacturer=Manufacturer.NEW_SCALE_TECHNOLOGIES)

        test_json = json.loads(test_instance.json())

        # Test serialization/de-serialization
        test_instance2 = TestModel.parse_obj(test_json)
        self.assertEqual(test_instance, test_instance2)


if __name__ == "__main__":
    unittest.main()
