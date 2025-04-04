"""Wrapper classes for various types of data"""

from pathlib import PurePosixPath
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler


class AssetPath(PurePosixPath):
    """Relative path to a file from the metadata root folder"""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        """Correctly serialize/deserialize for pydantic"""
        return core_schema.str_schema()
