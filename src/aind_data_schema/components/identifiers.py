"""Schema for identifiers"""

from enum import Enum
from pathlib import Path
from typing import Annotated, Dict, List, Optional, Union

from aind_data_schema_models.registries import Registry, _Orcid
from pydantic import Field

from aind_data_schema.base import DataModel, GenericModelType


class ExternalPlatforms(str, Enum):
    """External Platforms of Data Assets."""

    CODEOCEAN = "Code Ocean"


ExternalLinks = Dict[ExternalPlatforms, List[str]]


class DataAsset(DataModel):
    """Description of a single data asset"""

    url: str = Field(..., title="Asset location", description="URL pointing to the data asset")


class CombinedData(DataModel):
    """Description of a group of data assets"""

    assets: List[DataAsset] = Field(..., title="Data assets", min_items=1)
    name: Optional[str] = Field(default=None, title="Name")
    external_links: ExternalLinks = Field(
        default=dict(), title="External Links", description="Links to the Combined Data asset, if materialized."
    )
    description: Optional[str] = Field(
        default=None, title="Description", description="Intention or approach used to select group of assets"
    )


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

    url: str = Field(..., title="Code URL", description="URL to code repository")
    name: Optional[str] = Field(default=None, title="Name")
    version: Optional[str] = Field(default=None, title="Code version")
    run_script: Optional[Path] = Field(default=None, title="Run script", description="Path to run script")

    language: Optional[str] = Field(default=None, title="Programming language", description="Programming language used")
    language_version: Optional[str] = Field(default=None, title="Programming language version")

    input_data: Optional[List[Annotated[Union[DataAsset, CombinedData], Field(discriminator="object_type")]]] = Field(
        default=None, title="Input data", description="Input data used in the code or script"
    )
    parameters: Optional[GenericModelType] = Field(
        default=None, title="Parameters", description="Parameters used in the code or script"
    )

    core_dependency: Optional[Software] = Field(
        default=None,
        title="Core dependency",
        description="For code with a core software package dependency, e.g. Bonsai",
    )
