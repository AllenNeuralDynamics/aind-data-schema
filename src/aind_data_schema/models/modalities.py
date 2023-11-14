from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import BaseName


class Modality(BaseName):
    model_config = ConfigDict(frozen=True)


class BehaviorVideos(Modality):
    name: Literal["Behavior videos"] = "Behavior videos"
    abbreviation: Literal["behavior-videos"] = "behavior-videos"


class Confocal(Modality):
    name: Literal["Confocal microscopy"] = "Confocal microscopy"
    abbreviation: Literal["confocal"] = "confocal"


class Ecephys(Modality):
    name: Literal["Extracellular electrophysiology"] = "Extracellular electrophysiology"
    abbreviation: Literal["ecephys"] = "ecephys"


class Fmost(Modality):
    name: Literal[
        "Fluorescence micro-optical sectioning tomography"
    ] = "Fluorescence micro-optical sectioning tomography"
    abbreviation: Literal["fMOST"] = "fMOST"


class Icephys(Modality):
    name: Literal["Intracellular electrophysiology"] = "Intracellular electrophysiology"
    abbreviation: Literal["icephys"] = "icephys"


class Fib(Modality):
    name: Literal["Fiber photometry"] = "Fiber photometry"
    abbreviation: Literal["fib"] = "fib"


class Merfish(Modality):
    name: Literal[
        "Multiplexed error-robust fluorescence in situ hybridization"
    ] = "Multiplexed error-robust fluorescence in situ hybridization"
    abbreviation: Literal["merfish"] = "merfish"


class Mri(Modality):
    name: Literal["Magnetic resonance imaging"] = "Magnetic resonance imaging"
    abbreviation: Literal["MRI"] = "MRI"


class POphys(Modality):
    name: Literal["Planar optical physiology"] = "Planar optical physiology"
    abbreviation: Literal["ophys"] = "ophys"


class Slap(Modality):
    name: Literal["Scanned line projection imaging"] = "Scanned line projection imaging"
    abbreviation: Literal["slap"] = "slap"


class Spim(Modality):
    name: Literal["Selective plane illumination microscopy"] = "Selective plane illumination microscopy"
    abbreviation: Literal["SPIM"] = "SPIM"


class TrainedBehavior(Modality):
    name: Literal["Trained behavior"] = "Trained behavior"
    abbreviation: Literal["trained-behavior"] = "trained-behavior"


MODALITIES = Annotated[Union[tuple(Modality.__subclasses__())], Field(discriminator="name")]

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
