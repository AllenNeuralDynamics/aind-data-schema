""" Schemas for Ophys Rigs"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field
from ..base import AindCoreModel

from ..device import DeviceBase, DataInterface, Camera, Laser, Filter, Lens


class CameraType(Enum):
    """Camera type name"""

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


class Detector(DeviceBase):
    """Description of a generic detector"""

    name: Optional[str] = Field(
        None,
        description="Brief name to identify detector to match with session information",
        title="Name",
    )
    type: CameraType = Field(..., title="Camera Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: Optional[Immersion] = Field(None, title="Immersion")



class PatchName(Enum):
    """Patch name"""

    PATCH_CORD_A = "Patch Cord A"
    PATCH_CORD_B = "Patch Cord B"
    PATCH_CORD_C = "Patch Cord C"


class Patch(DeviceBase):
    """Description of a patch"""

    name: PatchName = Field(..., title="Patch Name")
    core_diameter: float = Field(..., title="Core diameter (um)")
    numerical_aperture: float = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(
        None, title="Photobleaching date"
    )


class OphysRig(AindCoreModel):
    """Description of an optical physiology rig"""

    schema_version: str = Field(
        "0.2.0",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    rig_id: str = Field(
        ..., description="room number_stim apparatus_version", title="Rig ID"
    )
    rig_location: Optional[str] = Field(None, title="Rig location")
    temperature_control: Optional[bool] = Field(
        None, title="Temperature control"
    )
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")
    patch_cords: List[Patch] = Field(
        ..., title="Patch cords", unique_items=True
    )
    cameras: Optional[List[Camera]] = Field(
        None, title="Cameras", unique_items=True
    )
    lasers: List[Laser] = Field(..., title="Lasers", unique_items=True)
    detectors: Optional[List[Detector]] = Field(
        None, title="Detectors", unique_items=True
    )
    filters: Optional[List[Filter]] = Field(
        None, title="Filters", unique_items=True
    )
    lenses: Optional[List[Lens]] = Field(
        None, title="Lenses", unique_items=True
    )
    additional_devices: Optional[List[DeviceBase]] = Field(
        None, title="Additional devices", unique_items=True
    )
    light_path_diagram: Optional[str] = Field(
        None,
        description="Path to diagram of the light path.",
        title="Light path diagram",
    )
    notes: Optional[str] = Field(None, title="Notes")
