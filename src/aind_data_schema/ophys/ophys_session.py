""" Schemas for Ophys Sessions. This is being deprecated after 2023-11-01."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field
from pydantic.typing import Annotated

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.imaging.tile import Channel
from aind_data_schema.procedures import TimeUnit
from aind_data_schema.session import Laser, LightEmittingDiode
from aind_data_schema.stimulus import StimulusEpoch
from aind_data_schema.utils.units import FrequencyUnit, PowerUnit, SizeUnit


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


class Patch(AindModel):
    """Description of a patch"""

    name: PatchCordName = Field(..., title="Name")
    output_power: Decimal = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(PowerUnit.UW, title="Output power unit")


class Camera(AindModel):
    """Description of camera recorded"""

    name: str = Field(..., title="Camera name (must match rig JSON)")


class OphysSession(AindCoreModel):
    """Description of an ophys session. This is being deprecated after 2023-11-01. Use Session class instead."""

    schema_version: str = Field(
        "0.2.12",
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
    light_sources: Optional[
        Annotated[
            List[Union[Laser, LightEmittingDiode]],
            Field(None, title="Light sources", unique_items=True, discriminator="device_type"),
        ]
    ]
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title="Cameras", unique_items=True)
    stimulus_epochs: Optional[List[StimulusEpoch]] = Field(None, title="Stimulus")
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
    fov_coordinate_ml: Decimal = Field(..., title="FOV coordinate ML")
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
    """Description of a two photon session. This is being deprecated after 2023-11-01."""

    fovs: List[FieldOfView] = Field(..., title="Fields of view", unique_items=True)


class StackChannel(Channel):
    """Description of a Channel used in a Stack"""

    start_depth: int = Field(..., title="Starting depth (um)")
    end_depth: int = Field(..., title="Ending depth (um)")
    depth_unit: SizeUnit = Field(SizeUnit.UM, title="Depth unit")


class Stack(OphysSession):
    """Description of a two photon stack"""

    channels: List[StackChannel] = Field(..., title="Channels")
    number_of_planes: int = Field(..., title="Number of planes")
    step_size: float = Field(..., title="Step size (um)")
    step_size_unit: SizeUnit = Field(SizeUnit.UM, title="Step size unit")
    number_of_plane_repeats_per_volume: int = Field(..., title="Number of repeats per volume")
    number_of_volume_repeats: int = Field(..., title="Number of volume repeats")
    fov_coordinate_ml: float = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: float = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(..., title="FOV reference", description="Reference for ML/AP coordinates")
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")
    magnification: Optional[str] = Field(None, title="Magnification")
    fov_scale_factor: float = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field("um/pixel", title="FOV scale factor unit")
    frame_rate: float = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    targeted_structure: Optional[str] = Field(None, title="Targeted structure")
