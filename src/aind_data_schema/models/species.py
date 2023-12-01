from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import BaseName, PIDName
from aind_data_schema.models.registry import NCBI


class _Species(PIDName):
    model_config = ConfigDict(frozen=True)


class CallithrixJacchus(_Species):
    name: Literal["Callithrix jacchus"] = "Callithrix jacchus"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["9483"] = "9483"


class HomoSapiens(_Species):
    name: Literal["Homo sapiens"] = "Homo sapiens"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["9606"] = "9606"


class MacacaMulatta(_Species):
    name: Literal["Macaca mulatta"] = "Macaca mulatta"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["9544"] = "9544"


class MusMusculus(_Species):
    name: Literal["Mus musculus"] = "Mus musculus"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["10090"] = "10090"


class Species:
    CALLITHRIX_JACCHUS = CallithrixJacchus()
    HOMO_SAPIENS = HomoSapiens()
    MACACA_MULATTA = MacacaMulatta()
    MUS_MUSCULUS = MusMusculus()
    ALL = tuple(_Species.__subclasses__())
    ONE_OF = Annotated[Union[ALL], Field(discriminator="name")]
