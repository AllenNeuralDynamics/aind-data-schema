""" Schema for identifiers """

from typing import Optional

from aind_data_schema_models.registries import Registry, _Orcid
from pydantic import Field

from aind_data_schema.base import DataModel, GenericModelType


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


class Container(DataModel):
    """Code container identifier, e.g. Docker"""

    container_type: str = Field(..., title="Type", description="Type of container, e.g. Docker, Singularity")
    tag: str = Field(..., title="Tag", description="Tag of the container, e.g. version number")
    uri: str = Field(..., title="URI", description="URI of the container, e.g. Docker Hub URL")


class Code(DataModel):
    """Code or script identifier"""

    url: str = Field(..., title="Code URL", description="Path to code repository")
    version: Optional[str] = Field(default=None, title="Code version")

    software: Optional[Software] = Field(default=None, title="Software", description="Software package")
    container: Optional[Container] = Field(default=None, title="Container")

    language: Optional[str] = Field(default=None, title="Programming language", description="Programming language used")
    language_version: Optional[str] = Field(default=None, title="Programming language version")

    parameters: Optional[GenericModelType] = Field(
        default=None, title="Parameters", description="Parameters used in the code or script"
    )
