""" Schema for identifiers """

from typing import Optional
from pathlib import Path
from pydantic_core import core_schema

from aind_data_schema_models.registries import Registry, _Orcid
from pydantic import Field, GetCoreSchemaHandler

from aind_data_schema.base import DataModel, GenericModelType


class AssetPath(Path):
    """Relative path to a file"""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.str_schema()


class Person(DataModel):
    """Person identifier"""

    name: str = Field(..., title="Person's name", description="First and last name OR anonymous ID")

    registry: _Orcid = Field(default_factory=lambda: Registry.ORCID, title="Registry")
    registry_identifier: Optional[str] = Field(default=None, title="ORCID ID")


class Software(DataModel):
    """Software package identifier"""

    name: str = Field(..., title="Software name", description="Name of the software package")
    version: Optional[str] = Field(
        default=None, title="Software version", description="Version of the software package"
    )


class Code(DataModel):
    """Code or script identifier"""

    url: str = Field(..., title="Code URL", description="Path to code repository")
    version: Optional[str] = Field(default=None, title="Code version")

    software: Optional[Software] = Field(default=None, title="Software", description="Software package")

    language: Optional[str] = Field(default=None, title="Programming language", description="Programming language used")
    language_version: Optional[str] = Field(default=None, title="Programming language version")

    parameters: Optional[GenericModelType] = Field(
        default=None, title="Parameters", description="Parameters used in the code or script"
    )
