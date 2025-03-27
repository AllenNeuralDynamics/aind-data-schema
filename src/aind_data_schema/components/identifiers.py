""" Schema for identifiers """

from typing import Optional
from pathlib import Path
from pydantic import Field
from aind_data_schema.base import DataModel, GenericModelType
from aind_data_schema_models.registries import Registry, _Orcid


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
    run_script: Optional[Path] = Field(default=None, title="Run script", description="Path to run script")

    language: Optional[str] = Field(default=None, title="Programming language", description="Programming language used")
    language_version: Optional[str] = Field(default=None, title="Programming language version")

    parameters: Optional[GenericModelType] = Field(
        default=None, title="Parameters", description="Parameters used in the code or script"
    )

    core_dependency: Optional[Software] = Field(
        default=None,
        title="Core dependency",
        description="For code with a core software package dependency, e.g. Bonsai",
    )
