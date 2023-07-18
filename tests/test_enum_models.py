"""Module to test custom Enums and Literals"""

import json
import unittest
from enum import Enum
from typing import Optional

from aind_data_schema.base import AindModel, EnumSubset, PIDName
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

            a: EnumSubset[TestEnum.FOO, TestEnum.BAR]
            b: Optional[EnumSubset[TestEnum.FOO, TestEnum.BAR]]

        # ensure we can generate the schema
        schema = TestThing.schema()

        self.assertEqual({"FOO", "BAR"}, set(schema["properties"]["a"]["enumNames"]))
        self.assertEqual({"FOO", "BAR"}, set(schema["properties"]["b"]["enumNames"]))
        self.assertFalse("b" in schema["required"])

        # now check that the json schema is good
        json_schema = TestThing.schema_json(indent=2)
        self.assertIsNotNone(json_schema)

    def test_model_enum_literals(self):
        """test that ModelEnumLiterals works"""

        class TestEnum(Enum):
            """temp enum"""

            FOO = PIDName(name="foo")
            BAR = PIDName(name="bar", abbreviation="b")

        class TestThing(AindModel):
            """temp model"""

            a: EnumSubset[TestEnum.FOO, TestEnum.BAR]
            b: Optional[EnumSubset[TestEnum.FOO, TestEnum.BAR]]

        # ensure we can generate the schema
        schema = TestThing.schema()

        self.assertEqual({"FOO", "BAR"}, set(schema["properties"]["a"]["enumNames"]))
        self.assertEqual({"FOO", "BAR"}, set(schema["properties"]["b"]["enumNames"]))
        self.assertFalse("b" in schema["required"])

        # now check that the json schema is good
        json_schema = TestThing.schema_json(indent=2)

        assert json_schema is not None

    def test_model_enum_literals_rehydrate(self):
        """Test ModelEnumLiterals"""

        class TestModel(AindModel):
            """Test class"""

            manufacturer: EnumSubset[Manufacturer.NEW_SCALE_TECHNOLOGIES]

        test_instance = TestModel(manufacturer=Manufacturer.NEW_SCALE_TECHNOLOGIES)

        test_json = json.loads(test_instance.json())

        # Test serialization/de-serialization
        test_instance2 = TestModel.parse_obj(test_json)
        self.assertEqual(test_instance, test_instance2)

    def test_edge_cases(self):
        """Tests that errors are raised if non-enums or mixed enums are used."""

        class TestEnum(Enum):
            """temp enum"""

            FOO = PIDName(name="foo")
            BAR = PIDName(name="bar", abbreviation="b")

        with self.assertRaises(Exception) as e1:

            class A(AindModel):
                """temp model"""

                a: EnumSubset[4, 5]

        with self.assertRaises(Exception) as e2:

            class B(AindModel):
                """temp model"""

                a: EnumSubset[TestEnum.FOO, Manufacturer.OTHER]

        expected_exception1 = """TypeError("Only Enums are allowed. <class 'int'>")"""
        expected_exception2 = """ValueError('All enums must be of the same class.')"""
        self.assertEqual(expected_exception1, repr(e1.exception))
        self.assertEqual(expected_exception2, repr(e2.exception))


if __name__ == "__main__":
    unittest.main()
