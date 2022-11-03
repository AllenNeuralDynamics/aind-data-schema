""" Schemas for Ophys Rigs"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class CameraName(Enum):
    """Camera name"""

    BODY_CAMERA = "Body Camera"
    EYE_CAMERA = "Eye Camera"
    FACE_CAMERA = "Face Camera"


class Camera(BaseModel):
    """Description of an ophys camera"""

    name: CameraName = Field(..., title="Camera Name")
    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
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


class DetectorManufacturer(Enum):
    """Detector manufacturer name"""

    HAMAMATSU = "Hamamatsu"
    PCOS = "PCOS"
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


class Detector(BaseModel):
    """Description of a generic detector"""

    name: Optional[str] = Field(
        None,
        description="Brief name to identify detector to match with session information",
        title="Name",
    )
    type: CameraType = Field(..., title="Camera Type")
    manufacturer: DetectorManufacturer = Field(
        ..., title="Detector Manufacturer"
    )
    model: str = Field(..., title="Model")
    serial_number: Optional[str] = Field(None, title="Serial number")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: Optional[Immersion] = Field(None, title="Immersion")


class DeviceType(Enum):
    """Device type name"""

    DIFFUSER = "Diffuser"
    GALVO = "Galvo"
    BEAM_EXPANDER = "Beam expander"
    LASER_COUPLER = "Laser coupler"
    PRISM = "Prism"
    OBJECTIVE = "Objective"
    SLIT = "Slit"
    OTHER = "Other"


class DeviceManufacturer(Enum):
    """Device manufacturer name"""

    THORLABS = "Thorlabs"
    OPTOTUNE = "Optotune"
    CAMBRIDGE_TECHNOLOGY = "Cambridge Technology"
    NIKON = "Nikon"
    EDMUND_OPTICS = "Edmund Optics"
    EALING = "Ealing"
    HAMAMATSU = "Hamamatsu"
    OTHER = "Other"


class Device(BaseModel):
    """Description of an ophys device"""

    type: DeviceType = Field(
        ...,
        description="Type of device. If Other please describe in Notes.",
        title="Type",
    )
    manufacturer: DeviceManufacturer = Field(..., title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    serial_number: Optional[str] = Field(None, title="Serial number")
    notes: Optional[str] = Field(None, title="Notes")


class FilterType(Enum):
    """Filter type name"""

    LONG_PASS = "Long pass"
    BAND_PASS = "Band pass"


class FilterManufacturer(Enum):
    """Filter manufacturer name"""

    CHROMA = "Chroma"
    SEMROCK = "Semrock"


class FilterSize(Enum):
    """Filter size value"""

    FILTER_SIZE_25 = 25
    FILTER_SIZE_32 = 32


class Filter(BaseModel):
    """Description of a filter"""

    type: FilterType = Field(..., title="Filter Type")
    manufacturer: FilterManufacturer = Field(..., title="Filter Manufacturer")
    model: str = Field(..., title="Model")
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


class Laser(BaseModel):
    """Description of a laser"""

    name: LaserName = Field(..., title="Laser Name")
    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    item_number: Optional[str] = Field(None, title="Item number")
    serial_number: str = Field(..., title="Serial number")
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


class Lens(BaseModel):
    """Description of a lens"""

    manufacturer: Optional[str] = Field(None, title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
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


class Patch(BaseModel):
    """Description of a patch"""

    name: PatchName = Field(..., title="Patch Name")
    manufacturer: Optional[str] = Field(None, title="Manufacturer")
    part_number: str = Field(..., title="model")
    serial_number: str = Field(..., title="Serial number")
    core_diameter: float = Field(..., title="Core diameter (um)")
    numerical_aperture: float = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(
        None, title="Photobleaching date"
    )


class OphysRig(BaseModel):
    """Description of an optical physiology rig"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/aind-data-schema/tree/main/src/aind_data_schema/ophys/ophys_rig.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field(
        "0.0.1",
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
    devices: Optional[List[Device]] = Field(
        None, title="Devices", unique_items=True
    )
    light_path_diagram: Optional[str] = Field(
        None,
        description="Path to diagram of the light path.",
        title="Light path diagram",
    )
    notes: Optional[str] = Field(None, title="Notes")
