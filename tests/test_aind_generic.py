""" test round trip (de)serialization behavior of AindGeneric models"""

import unittest

from pydantic import BaseModel, Field

from aind_data_schema.base import AindGeneric, AindModel


class GenericContainer(AindModel):
    """Represents a generic container"""

    contains_model: AindGeneric
    contains_dict: AindGeneric


class Bar(BaseModel):
    """Represents a mock model"""

    bar: str = Field(default="bar")
    foo: int = Field(default=1)


class SubGenericContainer(GenericContainer):
    """Represents a subclass of GenericContainer where contains_model is typed to Bar"""

    contains_model: Bar


class AindGenericTests(unittest.TestCase):
    """tests device schemas"""

    def test_sub_generic_container_round_trip(self):
        """tests a round trip (de)serialization of the SubGenericContainer"""

        sub_generic_container = SubGenericContainer(
            contains_model=Bar(bar="baz", foo=2),
            contains_dict={"foodict": 1, "bardict": "bar"},
        )
        deserialized = SubGenericContainer.model_validate_json(sub_generic_container.model_dump_json())
        self.assertEqual(sub_generic_container, deserialized)

    def test_sub_generic_container_from_parent_round_trip(self):
        """tests a round trip (de)serialization of the SubGenericContainer from the parent"""
        sub_generic_container = SubGenericContainer(
            contains_model=Bar(bar="baz", foo=2),
            contains_dict={"foodict": 1, "bardict": "bar"},
        )
        deserialized_parent = GenericContainer.model_validate_json(sub_generic_container.model_dump_json())
        deserialized = SubGenericContainer.model_validate_json(deserialized_parent.model_dump_json())
        self.assertEqual(sub_generic_container, deserialized)

    def test_sub_container_from_container(self):
        """tests if a model created directly from GenericContainer can be deserialized from the SubGenericContainer"""

        sub_generic_container = SubGenericContainer(
            contains_model=Bar(bar="baz", foo=2),
            contains_dict={"foodict": 1, "bardict": "bar"},
        )
        parent_container = GenericContainer(
            contains_model=Bar(bar="baz", foo=2).model_dump(),
            contains_dict={"foodict": 1, "bardict": "bar"},
        )
        deserialized = SubGenericContainer.model_validate_json(parent_container.model_dump_json())
        self.assertEqual(sub_generic_container, deserialized)
