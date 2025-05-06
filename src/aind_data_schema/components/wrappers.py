""" Wrappers for Pydantic types."""

from pathlib import PurePosixPath
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class AssetPath(PurePosixPath):
    """Relative path to a file from the metadata root folder"""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Generate JSON schema for AssetPath."""
        json_schema = handler(core_schema)
        json_schema.update(
            {
                "type": "string",
                "format": "uri-reference",
                "description": cls.__doc__,
            }
        )
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Generate core schema for AssetPath."""
        return core_schema.union_schema(
            [
                # Handle str -> AssetPath
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(cls),
                    ]
                ),
                # Handle AssetPath directly
                core_schema.is_instance_schema(cls),
            ],
            # Add a serializer: convert AssetPath -> str
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: str(value), return_schema=core_schema.str_schema()
            ),
        )
