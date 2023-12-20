"""Common registries"""

from typing import Literal

from pydantic import ConfigDict

from aind_data_schema.models.pid_names import BaseName


class _Registry(BaseName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class ResearchOrganizationRegistry(_Registry):
    """ResearchOrganizationRegistry"""

    name: Literal["Research Organization Registry"] = "Research Organization Registry"
    abbreviation: Literal["ROR"] = "ROR"


class NationalCenterForBiotechnologyInformation(_Registry):
    """NationalCenterForBiotechnologyInformation"""

    name: Literal["National Center for Biotechnology Information"] = "National Center for Biotechnology Information"
    abbreviation: Literal["NCBI"] = "NCBI"


class ResearchResourceIdentifiers(_Registry):
    """ResearchResourceIdentifiers"""

    name: Literal["Research Resource Identifiers"] = "Research Resource Identifiers"
    abbreviation: Literal["RRID"] = "RRID"


class Registry:
    """Registry definitions"""

    ROR = ResearchOrganizationRegistry()
    NCBI = NationalCenterForBiotechnologyInformation()
    RRID = ResearchResourceIdentifiers()

    _ALL = tuple(_Registry.__subclasses__())
