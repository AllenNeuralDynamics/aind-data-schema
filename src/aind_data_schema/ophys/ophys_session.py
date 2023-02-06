""" Schemas for Ophys Sessions """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field

from ..base import AindCoreModel, AindModel
from ..device import PowerUnit, SizeUnit


class FiberName(Enum):
    """Fiber name"""

    LASER_A = "Laser A"
    LASER_B = "Laser B"
    LASER_C = "Laser C"
    LASER_D = "Laser D"
    LASER_E = "Laser E"


class PatchCordName(Enum):
    """Patch cord name"""

    PATCH_CORD_A = "Patch Cord A"
    PATCH_CORD_B = "Patch Cord B"
    PATCH_CORD_C = "Patch Cord C"


class Coupling(AindModel):
    """Description of fiber coupling"""

    fiber_name: FiberName = Field(..., title="Fiber name")
    patch_cord_name: PatchCordName = Field(..., title="Patch cord name")


class Detector(AindModel):
    """Description of detector"""

    name: str = Field(..., title="Name")
    exposure_time: float = Field(..., title="Exposure time (ms)")


class LaserName(Enum):
    """Laser name"""

    Laser_A = "Laser A"
    Laser_B = "Laser B"
    Laser_C = "Laser C"
    Laser_D = "Laser D"
    Laser_E = "Laser E"


class Laser(AindModel):
    """Description of a laser"""

    name: LaserName = Field(..., title="Name")
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[float] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class Patch(AindModel):
    """Description of a patch"""

    name: PatchCordName = Field(..., title="Name")
    output_power: float = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(PowerUnit.UW, title="Output power unit")

class FiberPhotometrySession(OphysSession):
    """Description of a fiber photometry session"""

    patch_cords: List[Patch] = Field(..., title="Patch cords", unique_items=True)
    coupling_array: List[Coupling] = Field(..., title="Coupling array", unique_items=True)


class FieldOfView(AindCoreModel):
    """Description of an imaging field of view"""

    index: int = Field(..., title="Index")
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")


class TwoPhotonSession(OphysSession):
    """Description of a two photon session"""

    number_of_planes: int = Field(..., title="Number of planes")
    frame_rate: float = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: 




class OphysSession(AindCoreModel):
    """Description of an ophys session"""

    schema_version: str = Field(
        "0.0.2",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    subject_id: int = Field(..., title="Subject ID")
    session_type: str = Field(..., title="Session type")
    stimulus_protocol_id: Optional[str] = Field(None, title="Stimulus protocol ID")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    lasers: List[Laser] = Field(..., title="Lasers", unique_items=True)
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    notes: Optional[str] = None


