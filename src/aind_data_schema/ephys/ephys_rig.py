""" ephys rig schemas """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class HarpDevice(Enum):
    """Harp device name"""

    BEHAVIOR = "Behavior"
    CAMERA_CONTROLLER = "Camera Controller"
    LOAD_CELLS = "Load Cells"
    SOUND_BOARD = "Sound Board"
    TIMESTAMP_GENERATOR = "Timestamp Generator"
    INPUT_EXPANDER = "Input Expander"


class CameraName(Enum):
    """Camera name"""

    BODY_CAMERA = "Body Camera"
    EYE_CAMERA = "Eye Camera"
    FACE_CAMERA = "Face Camera"


class Camera(BaseModel):
    """Description of camera"""

    name: CameraName = Field(..., title="Name")
    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
    position_x: float = Field(..., title="Position X")
    position_y: float = Field(..., title="Position Y")
    position_z: float = Field(..., title="Position Z")
    angle_pitch: float = Field(
        ..., title="Angle pitch (deg)", units="deg", ge=0, le=360
    )
    angle_yaw: float = Field(
        ..., title="Angle yaw (deg)", units="deg", ge=0, le=360
    )
    angle_roll: float = Field(
        ..., title="Angle roll (deg)", units="deg", ge=0, le=360
    )
    recording_software: Optional[str] = Field(None, title="Recording software")
    recording_software_version: Optional[str] = Field(
        None, title="Recording software version"
    )


class Surface(Enum):
    """Running disc surface name"""

    NONE = "none"
    FOAM = "foam"


class Disc(BaseModel):
    """Description of a running disc"""

    radius: float = Field(..., title="Radius (cm)", units="cm", ge=0)
    surface: Optional[Surface] = Field(None, title="Surface")
    date_surface_replaced: Optional[datetime] = Field(
        None, title="Date surface replaced"
    )


class LaserName(Enum):
    """Laser name"""

    LASER_A = "Laser A"
    LASER_B = "Laser B"


class Laser(BaseModel):
    """Description of lasers used in ephys recordings"""

    name: LaserName = Field(..., title="Laser Name")
    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
    wavelength: Optional[int] = Field(
        None, title="Wavelength (nm)", units="nm", ge=300, le=1000
    )
    maximum_power: Optional[float] = Field(
        None, title="Maximum power (mW)", units="mW"
    )
    coupling_efficiency: Optional[float] = Field(
        None,
        title="Coupling efficiency (percent)",
        units="percent",
        ge=0,
        le=100,
    )
    calibration_data: Optional[str] = Field(
        None, description="path to calibration data", title="Calibration data"
    )
    calibration_date: Optional[datetime] = Field(
        None, title="Calibration date"
    )


class Monitor(BaseModel):
    """Description of a visual monitor"""

    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
    refresh_rate: int = Field(
        ..., title="Refresh rate (Hz)", units="Hz", ge=60
    )
    width: int = Field(..., title="Width (pixels)", units="pixels")
    height: int = Field(..., title="Height (pixels)", units="pixels")
    viewing_distance: float = Field(
        ..., title="Viewing distance (cm)", units="cm"
    )
    position_x: float = Field(..., title="Position X")
    position_y: float = Field(..., title="Position Y")
    position_z: float = Field(..., title="Position Z")
    angle_pitch: float = Field(
        ..., title="Angle pitch (deg)", units="deg", ge=0, le=360
    )
    angle_yaw: float = Field(
        ..., title="Angle yaw (deg)", units="deg", ge=0, le=360
    )
    angle_roll: float = Field(
        ..., title="Angle roll (deg)", units="deg", ge=0, le=360
    )
    contrast: int = Field(
        ...,
        description="Monitor's contrast setting",
        title="Contrast (percent)",
        units="percent",
        ge=0,
        le=100,
    )
    brightness: int = Field(
        ...,
        description="Monitor's brightness setting",
        title="Brightness",
        ge=0,
        le=100,
    )


class ProbeName(Enum):
    """Probe name"""

    PROBE_A = "Probe A"
    PROBE_B = "Probe B"
    PROBE_C = "Probe C"
    PROBE_D = "Probe D"
    PROBE_E = "Probe E"
    PROBE_F = "Probe F"
    PROBE_G = "Probe G"
    PROBE_H = "Probe H"
    PROBE_I = "Probe I"
    PROBE_J = "Probe J"


class ProbeType(Enum):
    """Probe type name"""

    NP1 = "Neuropixels 1.0"
    NP_UHD_FIXED = "Neuropixels UHD (Fixed)"
    NP_UHD_SWITCHABLE = "Neuropixels UHD (Switchable)"
    NP2_SINGLE_SHANK = "Neuropixels 2.0 (Single Shank)"
    NP2_MULTI_SHANK = "Neuropixels 2.0 (Multi Shank)"
    NP2_QUAD_BASE = "Neuropixels 2.0 (Quad Base)"
    NP_OPTO_DEMONSTRATOR = "Neuropixels Opto (Demonstrator)"
    MI_ULED_PROBE = "Michigan uLED Probe (Version 1)"
    MP_PHOTONIC_V1 = "MPI Photonic Probe (Version 1)"


class Probe(BaseModel):
    """Description of an ephys probe"""

    name: ProbeName = Field(..., title="Name")
    type: ProbeType = Field(..., title="Type")
    serial_number: str = Field(..., title="Serial number")


class Devices(BaseModel):
    """All of the devices in the rig"""

    probes: Optional[List[Probe]] = Field(
        None, title="Probes", unique_items=True
    )
    cameras: Optional[List[Camera]] = Field(
        None, title="Cameras", unique_items=True
    )
    lasers: Optional[List[Laser]] = Field(
        None, title="Lasers", unique_items=True
    )
    visual_monitors: Optional[List[Monitor]] = Field(
        None, title="Visual monitor", unique_items=True
    )
    running_disc: Optional[Disc] = Field(None, title="Running disc")
    harp_devices: Optional[List[HarpDevice]] = None


class EphysRig(BaseModel):
    """Description of an ephys rig"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/ephys_rig.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field(
        "0.2.0", description="schema version", title="Version", const=True
    )
    rig_id: str = Field(
        ..., description="room_stim apparatus_version", title="Rig ID"
    )
    devices: Devices
