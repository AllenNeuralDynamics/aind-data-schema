"""Module for Institution definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.base import Constant
from aind_data_schema.models.pid_names import BaseName, PIDName
from aind_data_schema.models.registry import ROR


class _Institution(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class AllenInstitute(_Institution):
    """AllenInstitute"""

    name: Constant("Allen Institute")
    abbreviation: Constant("AI")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("03cpe7c52")


class AllenInstituteForBrainScience(_Institution):
    """AllenInstituteForBrainScience"""

    name: Constant("Allen Institute for Brain Science")
    abbreviation: Constant("AIBS")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("00dcv1019")


class AllenInstituteForNeuralDynamics(_Institution):
    """AllenInstituteForNeuralDynamics"""

    name: Constant("Allen Institute for Neural Dynamics")
    abbreviation: Constant("AIND")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("04szwah67")


class ColumbiaUniversity(_Institution):
    """ColumbiaUniversity"""

    name: Constant("Columbia University")
    abbreviation: Constant("Columbia")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("00hj8s172")


class JacksonLaboratory(_Institution):
    """JacksonLaboratory"""

    name: Constant("Jackson Laboratory")
    abbreviation: Constant("JAX")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("021sy4w91")


class HuazhongUniversityOfScienceAndTechnology(_Institution):
    """HuazhongUniversityOfScienceAndTechnology"""

    name: Constant("Huazhong University of Science and Technology")
    abbreviation: Constant("HUST")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("00p991c53")


class NationalInstituteOfNeurologicalDisordersAndStroke(_Institution):
    """NationalInstituteOfNeurologicalDisordersAndStroke"""

    name: Constant("National Institute of Neurological Disorders and Stroke")
    abbreviation: Constant("NINDS")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("01s5ya894")


class NewYorkUniversity(_Institution):
    """NewYorkUniversity"""

    name: Constant("New York University")
    abbreviation: Constant("NYU")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("0190ak572")


class SimonsFoundation(_Institution):
    """SimonsFoundation"""

    name: Constant("Simons Foundation")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("01cmst727")


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
    ALL = tuple(_Institution.__subclasses__())
    ONE_OF = Annotated[Union[ALL], Field(discriminator="name")]
