"""Module for Modality definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.base import Constant
from aind_data_schema.models.pid_names import BaseName


class _Modality(BaseName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class BehaviorVideos(_Modality):
    """BehaviorVideos"""

    name: Constant("Behavior videos")
    abbreviation: Constant("behavior-videos")


class Confocal(_Modality):
    """Confocal"""

    name: Constant("Confocal microscopy")
    abbreviation: Constant("confocal")


class Ecephys(_Modality):
    """Ecephys"""

    name: Constant("Extracellular electrophysiology")
    abbreviation: Constant("ecephys")


class Fmost(_Modality):
    """Fmost"""

    name: Literal[
        "Fluorescence micro-optical sectioning tomography"
    ] = "Fluorescence micro-optical sectioning tomography"
    abbreviation: Constant("fMOST")


class Icephys(_Modality):
    """Icephys"""

    name: Constant("Intracellular electrophysiology")
    abbreviation: Constant("icephys")


class Fib(_Modality):
    """Fib"""

    name: Constant("Fiber photometry")
    abbreviation: Constant("fib")


class Merfish(_Modality):
    """Merfish"""

    name: Literal[
        "Multiplexed error-robust fluorescence in situ hybridization"
    ] = "Multiplexed error-robust fluorescence in situ hybridization"
    abbreviation: Constant("merfish")


class Mri(_Modality):
    """Mri"""

    name: Constant("Magnetic resonance imaging")
    abbreviation: Constant("MRI")


class POphys(_Modality):
    """POphys"""

    name: Constant("Planar optical physiology")
    abbreviation: Constant("ophys")


class Slap(_Modality):
    """Slap"""

    name: Constant("Scanned line projection imaging")
    abbreviation: Constant("slap")


class Spim(_Modality):
    """Spim"""

    name: Constant("Selective plane illumination microscopy")
    abbreviation: Constant("SPIM")


class TrainedBehavior(_Modality):
    """TrainedBehavior"""

    name: Constant("Trained behavior")
    abbreviation: Constant("trained-behavior")


class Modality:
    """Modality classes"""

    BEHAVIOR_VIDEOS = BehaviorVideos()
    CONFOCAL = Confocal()
    ECEPHYS = Ecephys()
    FMOST = Fmost()
    ICEPHYS = Icephys()
    FIB = Fib()
    MERFISH = Merfish()
    MRI = Mri()
    POPHYS = POphys()
    SLAP = Slap()
    SPIM = Spim()
    TRAINED_BEHAVIOR = TrainedBehavior()
    ALL = tuple(_Modality.__subclasses__())
    ONE_OF = Annotated[Union[ALL], Field(discriminator="name")]
