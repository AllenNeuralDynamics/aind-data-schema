"""Schema for identifiers"""

from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from aind_data_schema_models.registries import Registry
from pydantic import Field

from aind_data_schema.base import DataModel, DiscriminatedList, GenericModel


class Database(str, Enum):
    """Database platforms that can host data assets"""

    CODEOCEAN = "Code Ocean"
    DANDI = "DANDI"


DatabaseIdentifiers = Dict[Database, List[str]]


class DataAsset(DataModel):
    """Description of a single data asset"""

    url: str = Field(..., title="Asset location", description="URL pointing to the data asset")


class CombinedData(DataModel):
    """Description of a group of data assets"""

    assets: List[DataAsset] = Field(..., title="Data assets", min_length=1)
    name: Optional[str] = Field(default=None, title="Name")
    database_identifier: Optional[DatabaseIdentifiers] = Field(
        default=None,
        title="Database identifier",
        description="ID or link to the Combined Data asset, if materialized.",
    )
    description: Optional[str] = Field(
        default=None, title="Description", description="Intention or approach used to select group of assets"
    )


class Person(DataModel):
    """Person identifier"""

    name: str = Field(..., title="Person's name", description="First and last name OR anonymous ID")

    registry: Registry = Field(default=Registry.ORCID, title="Registry")
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

    url: str = Field(..., title="Code URL", description="URL to code repository")
    name: Optional[str] = Field(default=None, title="Name")
    version: Optional[str] = Field(default=None, title="Code version")

    container: Optional[Container] = Field(default=None, title="Container")
    run_script: Optional[Path] = Field(default=None, title="Run script", description="Path to run script")

    language: Optional[str] = Field(default=None, title="Programming language", description="Programming language used")
    language_version: Optional[str] = Field(default=None, title="Programming language version")

    input_data: Optional[DiscriminatedList[DataAsset | CombinedData]] = Field(
        default=None, title="Input data", description="Input data used in the code or script"
    )
    parameters: Optional[GenericModel] = Field(
        default=None, title="Parameters", description="Parameters used in the code or script"
    )

    core_dependency: Optional[Software] = Field(
        default=None,
        title="Core dependency",
        description="For code with a core software package dependency, e.g. Bonsai",
    )
