""" Schema for identifiers """

from typing import Optional
from pydantic import Field
from aind_data_schema.base import DataModel, GenericModelType
from aind_data_schema_models.registries import Registry, _Orcid


class Person(DataModel):
    """Person identifier"""

    name: str = Field(..., title="Person's name", description="First and last name OR anonymous ID")

    registry: _Orcid = Field(default_factory=lambda: Registry.ORCID, title="Registry")
    registry_identifier: Optional[str] = Field(default=None, title="ORCID ID")


class Software(DataModel):
    """Software identifier"""

    url: str = Field(..., title="Software URL", description="Path to code repository")
    name: Optional[str] = Field(default=None, title="Software name", description="Name of the software used")
    version: Optional[str] = Field(default=None, title="Software version", description="Version of the software used")
    parameters: Optional[GenericModelType] = Field(
        default=None, title="Parameters", description="Parameters used in the software"
    )
