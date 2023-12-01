"""Module for species definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.base import Constant
from aind_data_schema.models.pid_names import BaseName, PIDName
from aind_data_schema.models.registry import NCBI


class _Species(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class CallithrixJacchus(_Species):
    """CallithrixJacchus"""

    name: Constant("Callithrix jacchus")
    abbreviation: Constant(None)
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Constant("9483")


class HomoSapiens(_Species):
    """HomoSapiens"""

    name: Constant("Homo sapiens")
    abbreviation: Constant(None)
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Constant("9606")


class MacacaMulatta(_Species):
    """MacacaMulatta"""

    name: Constant("Macaca mulatta")
    abbreviation: Constant(None)
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Constant("9544")


class MusMusculus(_Species):
    """MusMusculus"""

    name: Constant("Mus musculus")
    abbreviation: Constant(None)
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Constant("10090")


class Species:
    """Species classes"""

    CALLITHRIX_JACCHUS = CallithrixJacchus()
    HOMO_SAPIENS = HomoSapiens()
    MACACA_MULATTA = MacacaMulatta()
    MUS_MUSCULUS = MusMusculus()
    ALL = tuple(_Species.__subclasses__())
    ONE_OF = Annotated[Union[ALL], Field(discriminator="name")]
