from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import BaseName


class _Platform(BaseName):
    model_config = ConfigDict(frozen=True)


class Behavior(_Platform):
    name: Literal["Behavior platform"] = "Behavior platform"
    abbreviation: Literal["behavior"] = "behavior"


class Confocal(_Platform):
    name: Literal["Confocal microscopy platform"] = "Confocal microscopy platform"
    abbreviation: Literal["confocal"] = "confocal"


class Ecephys(_Platform):
    name: Literal["Electrophysiology platform"] = "Electrophysiology platform"
    abbreviation: Literal["ecephys"] = "ecephys"


class ExaSpim(_Platform):
    name: Literal["ExaSPIM platform"] = "ExaSPIM platform"
    abbreviation: Literal["exaSPIM"] = "exaSPIM"


class Fip(_Platform):
    name: Literal[
        "Frame-projected independent-fiber photometry platform"
    ] = "Frame-projected independent-fiber photometry platform"
    abbreviation: Literal["FIP"] = "FIP"


class Hcr(_Platform):
    name: Literal["Hybridization chain reaction platform"] = "Hybridization chain reaction platform"
    abbreviation: Literal["HCR"] = "HCR"


class Hsfp(_Platform):
    name: Literal["Hyperspectral fiber photometry platform"] = "Hyperspectral fiber photometry platform"
    abbreviation: Literal["HSFP"] = "HSFP"


class MesoSpim(_Platform):
    name: Literal["MesoSPIM platform"] = "MesoSPIM platform"
    abbreviation: Literal["mesoSPIM"] = "mesoSPIM"


class Merfish(_Platform):
    name: Literal["MERFISH platform"] = "MERFISH platform"
    abbreviation: Literal["MERFISH"] = "MERFISH"


class Mri(_Platform):
    name: Literal["Magnetic resonance imaging platform"] = "Magnetic resonance imaging platform"
    abbreviation: Literal["MRI"] = "MRI"


class MultiplaneOphys(_Platform):
    name: Literal["Multiplane optical physiology platform"] = "Multiplane optical physiology platform"
    abbreviation: Literal["multiplane-ophys"] = "multiplane-ophys"


class SingleplaneOphys(_Platform):
    name: Literal["Single-plane optical physiology platform"] = "Single-plane optical physiology platform"
    abbreviation: Literal["single-plane-ophys"] = "single-plane-ophys"


class Slap2(_Platform):
    name: Literal["SLAP2 platform"] = "SLAP2 platform"
    abbreviation: Literal["SLAP2"] = "SLAP2"


class SmartSpim(_Platform):
    name: Literal["SmartSPIM platform"] = "SmartSPIM platform"
    abbreviation: Literal["SmartSPIM"] = "SmartSPIM"


class Platform:
    BEHAVIOR = Behavior()
    CONFOCAL = Confocal()
    ECEPHYS = Ecephys()
    EXASPIM = ExaSpim()
    FIP = Fip()
    HCR = Hcr()
    HSFP = Hsfp()
    MESOSPIM = MesoSpim()
    MERFISH = Merfish()
    MRI = Mri()
    MULTIPLANE_OPHYS = MultiplaneOphys()
    SINGLE_PLANE_OPHYS = SingleplaneOphys()
    SLAP2 = Slap2()
    SMARTSPIM = SmartSpim()
    ALL = tuple(_Platform.__subclasses__())
    ONE_OF = Annotated[Union[ALL], Field(discriminator="name")]

    _abbreviation_map = {p().abbreviation: p() for p in ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        return cls._abbreviation_map[abbreviation]

