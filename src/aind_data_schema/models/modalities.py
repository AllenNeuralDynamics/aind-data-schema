"""Module for Modality definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import BaseName


class _Modality(BaseName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class BehaviorVideos(_Modality):
    """BehaviorVideos"""

    name: Literal["Behavior videos"] = "Behavior videos"
    abbreviation: Literal["behavior-videos"] = "behavior-videos"


class Confocal(_Modality):
    """Confocal"""

    name: Literal["Confocal microscopy"] = "Confocal microscopy"
    abbreviation: Literal["confocal"] = "confocal"


class Ecephys(_Modality):
    """Ecephys"""

    name: Literal["Extracellular electrophysiology"] = "Extracellular electrophysiology"
    abbreviation: Literal["ecephys"] = "ecephys"


class Fmost(_Modality):
    """Fmost"""

    name: Literal[
        "Fluorescence micro-optical sectioning tomography"
    ] = "Fluorescence micro-optical sectioning tomography"
    abbreviation: Literal["fMOST"] = "fMOST"


class Icephys(_Modality):
    """Icephys"""

    name: Literal["Intracellular electrophysiology"] = "Intracellular electrophysiology"
    abbreviation: Literal["icephys"] = "icephys"


class Fib(_Modality):
    """Fib"""

    name: Literal["Fiber photometry"] = "Fiber photometry"
    abbreviation: Literal["fib"] = "fib"


class Merfish(_Modality):
    """Merfish"""

    name: Literal[
        "Multiplexed error-robust fluorescence in situ hybridization"
    ] = "Multiplexed error-robust fluorescence in situ hybridization"
    abbreviation: Literal["merfish"] = "merfish"


class Mri(_Modality):
    """Mri"""

    name: Literal["Magnetic resonance imaging"] = "Magnetic resonance imaging"
    abbreviation: Literal["MRI"] = "MRI"


class POphys(_Modality):
    """POphys"""

    name: Literal["Planar optical physiology"] = "Planar optical physiology"
    abbreviation: Literal["ophys"] = "ophys"


class Slap(_Modality):
    """Slap"""

    name: Literal["Scanned line projection imaging"] = "Scanned line projection imaging"
    abbreviation: Literal["slap"] = "slap"


class Spim(_Modality):
    """Spim"""

    name: Literal["Selective plane illumination microscopy"] = "Selective plane illumination microscopy"
    abbreviation: Literal["SPIM"] = "SPIM"


class TrainedBehavior(_Modality):
    """TrainedBehavior"""

    name: Literal["Trained behavior"] = "Trained behavior"
    abbreviation: Literal["trained-behavior"] = "trained-behavior"


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
    _ALL = tuple(_Modality.__subclasses__())
    ONE_OF = Annotated[Union[_ALL], Field(discriminator="name")]

    _abbreviation_map = {m().abbreviation: m() for m in _ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get class from abbreviation"""
        return cls._abbreviation_map[abbreviation]
