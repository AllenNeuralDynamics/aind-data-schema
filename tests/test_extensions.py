from typing import Any, Literal
import unittest

from pydantic import BaseModel, ConfigDict, Field
from aind_data_schema.base import AindCoreModel, AindGenericType
from aind_data_schema.core.quality_control import QualityControl


class ExtensionTests(unittest.TestCase):
    """tests for examples"""

    def test_extension(self):
        """run through each example, compare to rendered json"""

        # Ensure that an extension can be added to the QualityControl object
        class Extension(BaseModel):
            """Extension for QualityControl"""

            ext_field: str = Field(..., title="Example")

        class Parent(AindCoreModel):
            """Parent class"""
            describedBy: Literal["url"] = Field(default="url")
            schema_version: Literal["1.2.1"] = Field(default="1.2.1")

            example: str = Field(..., title="Example")
            extensions: Extension = Field(default=None, title="Extensions")

        ext = Extension(ext_field="ext_field")

        parent = Parent(
            example="example",
            extensions=ext
        )
        print(parent.model_dump_json())

        data = parent.model_dump()
        parent = Parent(**data)
        print(parent.extensions)
        print(parent.model_dump_json())

        self.assertIsNotNone(parent)


if __name__ == "__main__":
    unittest.main()