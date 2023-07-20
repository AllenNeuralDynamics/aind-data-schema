""" Schemas for Ophys Sessions """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.device import FrequencyUnit, PowerUnit, SizeUnit
from aind_data_schema.procedures import TimeUnit
from aind_data_schema.stimulus import StimulusPresentation


class FiberName(Enum):
    """Fiber name"""

    FIBER_A = "Fiber A"
    FIBER_B = "Fiber B"
    FIBER_C = "Fiber C"
    FIBER_D = "Fiber D"
    FIBER_E = "Fiber E"


class PatchCordName(Enum):
    """Patch cord name"""

    PATCH_CORD_A = "Patch Cord A"
    PATCH_CORD_B = "Patch Cord B"
    PATCH_CORD_C = "Patch Cord C"
    PATCH_CORD_D = "Patch Cord D"


class Coupling(AindModel):
    """Description of fiber coupling"""

    fiber_name: FiberName = Field(..., title="Fiber name")
    patch_cord_name: PatchCordName = Field(..., title="Patch cord name")


class TriggerType(Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class Detector(AindModel):
    """Description of detector"""

    name: str = Field(..., title="Name")
    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")


class LaserName(Enum):
    """Laser name"""

    LASER_A = "Laser A"
    LASER_B = "Laser B"
    LASER_C = "Laser C"
    LASER_D = "Laser D"
    LASER_E = "Laser E"


class Laser(AindModel):
    """Description of a laser"""

    name: LaserName = Field(..., title="Name")
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class LightEmittingDiode(AindModel):
    """Description of a LED"""

    name: str = Field(..., title="Name")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class Patch(AindModel):
    """Description of a patch"""

    name: PatchCordName = Field(..., title="Name")
    output_power: Decimal = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(PowerUnit.UW, title="Output power unit")


class Camera(AindModel):
    """Description of camera recorded"""

    name: str = Field(..., title="Camera name (must match rig JSON)")


class OphysSession(AindCoreModel):
    """Description of an ophys session"""

    schema_version: str = Field(
        "0.2.3",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: Optional[datetime] = Field(None, title="Session end time")
    subject_id: int = Field(..., title="Subject ID")
    session_type: str = Field(..., title="Session type")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    light_sources: List[Union[Laser, LightEmittingDiode]] = Field(..., title="Light source", unique_items=True)
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title="Cameras", unique_items=True)
    stimulus_presentations: Optional[List[StimulusPresentation]] = Field(None, title="Stimulus")
    notes: Optional[str] = None


class FiberPhotometrySession(OphysSession):
    """Description of a fiber photometry session"""

    patch_cords: List[Patch] = Field(..., title="Patch cords", unique_items=True)
    coupling_array: List[Coupling] = Field(..., title="Coupling array", unique_items=True)


class FieldOfView(AindModel):
    """Description of an imaging field of view"""

    index: int = Field(..., title="Index")
    imaging_depth: int = Field(..., title="Imaging depth (um)")
    imaging_depth_unit: SizeUnit = Field(SizeUnit.UM, title="Imaging depth unit")
    targeted_structure: str = Field(..., title="Targeted structure")
    fov_coordinate_ml: Decimal = Field(..., title="FOV coodinate ML")
    fov_coordinate_ap: Decimal = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(..., title="FOV reference", description="Reference for ML/AP coordinates")
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")
    magnification: str = Field(..., title="Magnification")
    fov_scale_factor: Decimal = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field("um/pixel", title="FOV scale factor unit")
    frame_rate: Decimal = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")


class TwoPhotonOphysSession(OphysSession):
    """Description of a two photon session"""

    fovs: List[FieldOfView] = Field(..., title="Fields of view", unique_items=True)
