""" generic base class with supporting validators and fields for basic AIND schema """

from typing import Final

from pydantic import BaseModel, ConfigDict, Extra, Field


class AindModel(BaseModel):
    """BaseModel that disallows extra fields"""

    model_config = ConfigDict(extra=Extra.forbid, use_enum_values=True)


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    _DEFAULT_FILE_EXTENSION = ".json"
    _DESCRIBED_BY_BASE_URL: Final = "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/"

    describedBy: str = Field(..., json_schema_extra={"const": True})
    schema_version: str = Field(
        ..., pattern=r"^\d+.\d+.\d+$", description="schema version", title="Version", frozen=True
    )

    @classmethod
    def default_file_extension(cls) -> str:
        """Public method to retrieve protected _DEFAULT_FILE_EXTENSION"""
        return cls._DEFAULT_FILE_EXTENSION
