""" Schemas for Ophys Rigs"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field

from ..base import AindCoreModel
from ..device import Device


class CameraName(Enum):
    """Camera name"""

    BODY_CAMERA = "Body Camera"
    EYE_CAMERA = "Eye Camera"
    FACE_CAMERA = "Face Camera"


class Camera(Device):
    """Description of an ophys camera"""

    name: CameraName = Field(..., title="Camera Name")
    position_x: float = Field(..., title="Position X")
    position_y: float = Field(..., title="Position Y")
    position_z: float = Field(..., title="Position Z")
    angle_pitch: float = Field(..., title="Angle pitch (deg)")
    angle_yaw: float = Field(..., title="Angle yaw (deg)")
    angle_roll: float = Field(..., title="Angle roll (deg)")
    recording_software: Optional[str] = Field(None, title="Recording software")
    recording_software_version: Optional[str] = Field(
        None, title="Recording software version"
    )


class CameraType(Enum):
    """Camera type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class DataInterface(Enum):
    """Data interface name"""

    USB = "USB"
    CAMERALINK = "CameraLink"
    COAX = "Coax"
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

    name: Optional[str] = Field(
        None,
        description="Brief name to identify detector to match with session information",
        title="Name",
    )
    type: CameraType = Field(..., title="Camera Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: Optional[Immersion] = Field(None, title="Immersion")


class FilterType(Enum):
    """Filter type name"""

    LONG_PASS = "Long pass"
    BAND_PASS = "Band pass"


class FilterSize(Enum):
    """Filter size value"""

    FILTER_SIZE_25 = 25
    FILTER_SIZE_32 = 32


class Filter(Device):
    """Description of a filter"""

    type: FilterType = Field(..., title="Filter Type")
    size: Optional[FilterSize] = Field(None, title="Size (mm)")
    cut_off_frequency: Optional[int] = Field(None, title="Cut off frequency")
    cut_on_frequency: Optional[int] = Field(None, title="Cut on frequency")
    description: Optional[str] = Field(
        None, description="Where/how filter is being used", title="Description"
    )


class LaserName(Enum):
    """Laser name"""

    LASER_A = "Laser A"
    LASER_B = "Laser B"
    LASER_C = "Laser C"
    LASER_D = "Laser D"
    LASER_E = "Laser E"


class Coupling(Enum):
    """Coupling type name"""

    FREE_SPACE = "Free-space"
    SMF = "SMF"
    MMF = "MMF"
    OTHER = "other"


class Laser(Device):
    """Description of a laser"""

    name: LaserName = Field(..., title="Laser Name")
    item_number: Optional[str] = Field(None, title="Item number")
    wavelength: int = Field(..., title="Wavelength (nm)")
    maximum_power: float = Field(..., title="Maximum power (mW)")
    coupling: Optional[Coupling] = Field(None, title="Coupling")
    coupling_efficiency: Optional[float] = Field(
        None, title="Coupling efficiency (percent)"
    )
    calibration_data: Optional[str] = Field(
        None, description="path to calibration data", title="Calibration data"
    )
    calibration_date: Optional[datetime] = Field(
        None, title="Calibration date"
    )


class LensSize(Enum):
    """Lens size value"""

    LENS_SIZE_1 = 1
    LENS_SIZE_2 = 2


class Lens(Device):
    """Description of a lens"""

    focal_length: Optional[float] = Field(None, title="Focal length (mm)")
    size: Optional[LensSize] = Field(None, title="Size (inches)")
    optimized_wavelength_range: Optional[str] = Field(
        None, title="Optimized wavelength range (nm)"
    )
    notes: Optional[str] = Field(None, title="Notes")


class PatchName(Enum):
    """Patch name"""

    PATCH_CORD_A = "Patch Cord A"
    PATCH_CORD_B = "Patch Cord B"
    PATCH_CORD_C = "Patch Cord C"


class Patch(Device):
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
    additional_devices: Optional[List[Device]] = Field(
        None, title="Additional devices", unique_items=True
    )
    light_path_diagram: Optional[str] = Field(
        None,
        description="Path to diagram of the light path.",
        title="Light path diagram",
    )
    notes: Optional[str] = Field(None, title="Notes")
