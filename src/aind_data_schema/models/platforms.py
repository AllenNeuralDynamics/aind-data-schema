"""Module for Platform definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.base import Constant
from aind_data_schema.models.pid_names import BaseName


class _Platform(BaseName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class Behavior(_Platform):
    """Behavior"""

    name: Constant("Behavior platform")
    abbreviation: Constant("behavior")


class Confocal(_Platform):
    """Confocal"""

    name: Constant("Confocal microscopy platform")
    abbreviation: Constant("confocal")


class Ecephys(_Platform):
    """Ecephys"""

    name: Constant("Electrophysiology platform")
    abbreviation: Constant("ecephys")


class ExaSpim(_Platform):
    """ExaSpim"""

    name: Constant("ExaSPIM platform")
    abbreviation: Constant("exaSPIM")


class Fip(_Platform):
    """Fip"""

    name: Literal[
        "Frame-projected independent-fiber photometry platform"
    ] = "Frame-projected independent-fiber photometry platform"
    abbreviation: Constant("FIP")


class Hcr(_Platform):
    """Hcr"""

    name: Constant("Hybridization chain reaction platform")
    abbreviation: Constant("HCR")


class Hsfp(_Platform):
    """Hsfp"""

    name: Constant("Hyperspectral fiber photometry platform")
    abbreviation: Constant("HSFP")


class MesoSpim(_Platform):
    """MesoSpim"""

    name: Constant("MesoSPIM platform")
    abbreviation: Constant("mesoSPIM")


class Merfish(_Platform):
    """Merfish"""

    name: Constant("MERFISH platform")
    abbreviation: Constant("MERFISH")


class Mri(_Platform):
    """Mri"""

    name: Constant("Magnetic resonance imaging platform")
    abbreviation: Constant("MRI")


class MultiplaneOphys(_Platform):
    """MulitplaneOphys"""

    name: Constant("Multiplane optical physiology platform")
    abbreviation: Constant("multiplane-ophys")


class SingleplaneOphys(_Platform):
    """SingleplaneOphys"""

    name: Constant("Single-plane optical physiology platform")
    abbreviation: Constant("single-plane-ophys")


class Slap2(_Platform):
    """Slap2"""

    name: Constant("SLAP2 platform")
    abbreviation: Constant("SLAP2")


class SmartSpim(_Platform):
    """SmartSpim"""

    name: Constant("SmartSPIM platform")
    abbreviation: Constant("SmartSPIM")


class Platform:
    """Platform classes"""

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
        """Get platform from abbreviation"""
        return cls._abbreviation_map[abbreviation]
