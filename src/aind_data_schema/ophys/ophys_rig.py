""" Schemas for Ophys Rigs"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Literal, Optional, Set, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel, Constant
from aind_data_schema.device import (
    CameraAssembly,
    DAQDevice,
    DataInterface,
    Device,
    Disc,
    Filter,
    HarpDevice,
    Immersion,
    Laser,
    Lens,
    LightEmittingDiode,
    Monitor,
    Objective,
    Treadmill,
    Tube,
)


class DetectorType(Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class Cooling(Enum):
    """Cooling medium name"""

    AIR = "air"
    WATER = "water"


class Detector(Device):
    """Description of a generic detector"""

    detector_type: DetectorType = Field(..., title="Detector Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: Optional[Immersion] = Field(None, title="Immersion")


class Patch(Device):
    """Description of a patch cord"""

    core_diameter: float = Field(..., title="Core diameter (um)")
    numerical_aperture: float = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(None, title="Photobleaching date")


class OphysRig(AindCoreModel):
    """Description of an optical physiology rig"""

    schema_version: Constant("0.6.1", title="Schema version")
    rig_id: str = Field(..., description="room number_stim apparatus_version", title="Rig ID")
    temperature_control: Optional[bool] = Field(None, title="Temperature control")
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")
    patch_cords: Optional[List[Patch]] = Field(..., title="Patch cords")
    light_sources: List[Union[Laser, LightEmittingDiode]] = Field(..., title="Light sources")
    detectors: Optional[List[Detector]] = Field(None, title="Detectors")
    objectives: Optional[List[Objective]] = Field(None, title="Objectives")
    filters: Optional[List[Filter]] = Field(None, title="Filters")
    lenses: Optional[List[Lens]] = Field(None, title="Lenses")
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies")
    mouse_platform: Optional[Union[Tube, Treadmill, Disc]] = Field(None, title="Mouse platform")
    visual_monitors: Optional[List[Monitor]] = Field(None, title="Visual monitors")
    daqs: Optional[List[Union[DAQDevice, HarpDevice]]] = Field(None, title="Data acquisition devices")
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices")
    light_path_diagram: Optional[str] = Field(
        None,
        description="Path to diagram of the light path.",
        title="Light path diagram",
    )
    notes: Optional[str] = Field(None, title="Notes")
