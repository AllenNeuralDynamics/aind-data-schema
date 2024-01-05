"""Module for Institution definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.registry import Registry, ResearchOrganizationRegistry


class _Institution(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class AllenInstitute(_Institution):
    """AllenInstitute"""

    name: Literal["Allen Institute"] = "Allen Institute"
    abbreviation: Literal["AI"] = "AI"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03cpe7c52"] = "03cpe7c52"


class AllenInstituteForBrainScience(_Institution):
    """AllenInstituteForBrainScience"""

    name: Literal["Allen Institute for Brain Science"] = "Allen Institute for Brain Science"
    abbreviation: Literal["AIBS"] = "AIBS"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00dcv1019"] = "00dcv1019"


class AllenInstituteForNeuralDynamics(_Institution):
    """AllenInstituteForNeuralDynamics"""

    name: Literal["Allen Institute for Neural Dynamics"] = "Allen Institute for Neural Dynamics"
    abbreviation: Literal["AIND"] = "AIND"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["04szwah67"] = "04szwah67"


class ColumbiaUniversity(_Institution):
    """ColumbiaUniversity"""

    name: Literal["Columbia University"] = "Columbia University"
    abbreviation: Literal["Columbia"] = "Columbia"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00hj8s172"] = "00hj8s172"


class JacksonLaboratory(_Institution):
    """JacksonLaboratory"""

    name: Literal["Jackson Laboratory"] = "Jackson Laboratory"
    abbreviation: Literal["JAX"] = "JAX"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["021sy4w91"] = "021sy4w91"


class HuazhongUniversityOfScienceAndTechnology(_Institution):
    """HuazhongUniversityOfScienceAndTechnology"""

    name: Literal["Huazhong University of Science and Technology"] = "Huazhong University of Science and Technology"
    abbreviation: Literal["HUST"] = "HUST"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00p991c53"] = "00p991c53"


class NationalInstituteOfNeurologicalDisordersAndStroke(_Institution):
    """NationalInstituteOfNeurologicalDisordersAndStroke"""

    name: Literal[
        "National Institute of Neurological Disorders and Stroke"
    ] = "National Institute of Neurological Disorders and Stroke"
    abbreviation: Literal["NINDS"] = "NINDS"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01s5ya894"] = "01s5ya894"


class NewYorkUniversity(_Institution):
    """NewYorkUniversity"""

    name: Literal["New York University"] = "New York University"
    abbreviation: Literal["NYU"] = "NYU"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["0190ak572"] = "0190ak572"


class SimonsFoundation(_Institution):
    """SimonsFoundation"""

    name: Literal["Simons Foundation"] = "Simons Foundation"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01cmst727"] = "01cmst727"


class Institution:
    """Institution definitions"""

    AI = AllenInstitute()
    AIBS = AllenInstituteForBrainScience()
    AIND = AllenInstituteForNeuralDynamics()
    COLUMBIA = ColumbiaUniversity()
    JAX = JacksonLaboratory()
    HUST = HuazhongUniversityOfScienceAndTechnology()
    NINDS = NationalInstituteOfNeurologicalDisordersAndStroke()
    NYU = NewYorkUniversity()
    SIMONS = SimonsFoundation()
    _ALL = tuple(_Institution.__subclasses__())
    ONE_OF = Annotated[Union[_ALL], Field(discriminator="name")]

    _abbreviation_map = {m().abbreviation: m() for m in _ALL}
    _name_map = {m().name: m() for m in _ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get class from abbreviation"""
        return cls._abbreviation_map[abbreviation]

    @classmethod
    def from_name(cls, name: str):
        """Get class from abbreviation"""
        return cls._name_map[name]

    @property
    def name_map(self) -> dict:
        """Dictionary of mapping from name to object"""
        return self._name_map
