""" generic base class with supporting validators and fields for basic AIND schema """

from typing import Optional, Literal, Any, ClassVar, Final, Dict, Type
import inspect

from pydantic import BaseModel, Extra, Field, model_validator, field_validator, FieldValidationInfo, computed_field
import sys
#_DESCRIBED_BY_BASE_URL: Final = "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/"


class AindModel(BaseModel, extra=Extra.forbid):
    """BaseModel that disallows extra fields"""


class BaseName(AindModel):
    """A simple model associating a name with an abbreviation"""

    name: str = Field(..., title="Name")
    abbreviation: Optional[str] = Field(None, title="Abbreviation")


# class Registry:
#     """
#     Class to store common registries for use in PIDNames
#     """
#
#     ROR = BaseName(name="Research Organization Registry", abbreviation="ROR")
#     NCBI = BaseName(name="National Center for Biotechnology Information", abbreviation="NCBI")
#     RRID = BaseName(name="Research Resource Identifiers", abbreviation="RRID")


class PIDName(BaseName):
    """
    Model for associate a name with a persistent identifier (PID),
    the registry for that PID, and abbreviation for that registry
    """

    registry: Optional[BaseName] = Field(None, title="Registry")
    registry_identifier: Optional[str] = Field(None, title="Registry identifier")


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    _DEFAULT_FILE_EXTENSION = ".json"
    _DESCRIBED_BY_BASE_URL: Final = "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/"

    describedBy: str = Field(..., json_schema_extra={"const": True})
    schema_version: str = Field(..., pattern=r"^\d+.\d+.\d+$", description="schema version", title="Version", frozen=True)

    @classmethod
    def default_file_extension(cls) -> str:
        """Public method to retrieve protected _DEFAULT_FILE_EXTENSION"""
        return cls._DEFAULT_FILE_EXTENSION
