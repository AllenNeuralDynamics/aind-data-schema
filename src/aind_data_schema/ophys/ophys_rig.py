""" Schemas for Ophys Rigs"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import Field

from ..base import AindCoreModel
from ..device import Camera, DataInterface, Device, Filter, Laser, Lens


class DetectorType(Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class Cooling(Enum):
    """Cooling medium name"""

    AIR = "air"
    WATER = "water"


class Immersion(Enum):
    """Immersion medium name"""

    AIR = "air"
    WATER = "water"
    OIL = "oil"


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

    schema_version: str = Field(
        "0.2.0",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    rig_id: str = Field(..., description="room number_stim apparatus_version", title="Rig ID")
    rig_location: Optional[str] = Field(None, title="Rig location")
    temperature_control: Optional[bool] = Field(None, title="Temperature control")
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")
    patch_cords: List[Patch] = Field(..., title="Patch cords", unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title="Cameras", unique_items=True)
    lasers: List[Laser] = Field(..., title="Lasers", unique_items=True)
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    filters: Optional[List[Filter]] = Field(None, title="Filters", unique_items=True)
    lenses: Optional[List[Lens]] = Field(None, title="Lenses", unique_items=True)
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    light_path_diagram: Optional[str] = Field(
        None,
        description="Path to diagram of the light path.",
        title="Light path diagram",
    )
    notes: Optional[str] = Field(None, title="Notes")
