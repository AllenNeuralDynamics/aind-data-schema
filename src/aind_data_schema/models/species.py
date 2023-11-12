from aind_data_schema.models.registry import NCBI
from aind_data_schema.models.pid_names import PIDName, BaseName
from pydantic import ConfigDict, Field
from typing import Literal, Union
from typing_extensions import Annotated


class Species(PIDName):
    model_config = ConfigDict(frozen=True)


class CallithrixJacchus(Species):
    name: Literal["Callithrix jacchus"] = "Callithrix jacchus"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["9483"] = "9483"


class HomoSapiens(Species):
    name: Literal["Homo sapiens"] = "Homo sapiens"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["9606"] = "9606"


class MacacaMulatta(Species):
    name: Literal["Macaca mulatta"] = "Macaca mulatta"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["9544"] = "9544"


class MusMusculus(Species):
    name: Literal["Mus musculus"] = "Mus musculus"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(NCBI, json_schema_extra={"const": True})
    registry_identifier: Literal["10090"] = "10090"


SPECIES = Annotated[Union[tuple(Species.__subclasses__())], Field(discriminator="name")]

CALLITHRIX_JACCHUS = CallithrixJacchus()
HOMO_SAPIENS = HomoSapiens()
MACACA_MULATTA = MacacaMulatta()
MUS_MUSCULUS = MusMusculus()
