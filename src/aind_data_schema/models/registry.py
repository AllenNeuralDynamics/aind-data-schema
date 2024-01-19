"""Common registries"""

from typing import Literal

from pydantic import ConfigDict

from aind_data_schema.models.pid_names import BaseName


class _Registry(BaseName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class Addgene(_Registry):
    """Addgene"""

    name: Literal["Addgene"] = "Addgene"
    abbreviation: Literal["ADDGENE"] = "ADDGENE"


class MouseGenomeInformatics(_Registry):
    """MouseGenomeInformatics"""

    name: Literal["Mouse Genome Informatics"] = "Mouse Genome Informatics"
    abbreviation: Literal["MGI"] = "MGI"


class ResearchOrganizationRegistry(_Registry):
    """ResearchOrganizationRegistry"""

    name: Literal["Research Organization Registry"] = "Research Organization Registry"
    abbreviation: Literal["ROR"] = "ROR"


class ResearchResourceIdentifiers(_Registry):
    """ResearchResourceIdentifiers"""

    name: Literal["Research Resource Identifiers"] = "Research Resource Identifiers"
    abbreviation: Literal["RRID"] = "RRID"


class NationalCenterForBiotechnologyInformation(_Registry):
    """NationalCenterForBiotechnologyInformation"""

    name: Literal["National Center for Biotechnology Information"] = "National Center for Biotechnology Information"
    abbreviation: Literal["NCBI"] = "NCBI"


class Registry:
    """Registry definitions"""

    ADDGENE = Addgene()
    ROR = ResearchOrganizationRegistry()
    MGI = MouseGenomeInformatics()
    NCBI = NationalCenterForBiotechnologyInformation()
    RRID = ResearchResourceIdentifiers()

    _ALL = tuple(_Registry.__subclasses__())
