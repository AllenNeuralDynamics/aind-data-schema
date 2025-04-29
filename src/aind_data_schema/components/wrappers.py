from pathlib import PurePosixPath
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Any


class AssetPath(PurePosixPath):
    """Relative path to a file from the metadata root folder"""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, 
        _source_type: Any, 
        _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Defines the Pydantic core schema for AssetPath validation and serialization.
        
        Args:
            _source_type: The source type (unused in this implementation)
            _handler: The schema handler from Pydantic
            
        Returns:
            CoreSchema: The schema for AssetPath type
        """
        return core_schema.union_schema([
            # Handle strings
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls),
            ]),
            # Handle if an AssetPath is directly passed
            core_schema.is_instance_schema(cls),
        ])
