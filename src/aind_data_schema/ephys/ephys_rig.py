""" ephys rig schemas """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class HarpDevice(Enum):
    """list of harp device names"""

    BEHAVIOR = "Behavior"
    WEAR_BASESTATION = "WEAR basestation"
    CAMERA_TRIGGER_CONTROL = "Camera trigger control"
    LED_ARRAY_INTERFACE = "LED array interface"
    ANALOG_INPUT = "Analog input"
    MULTI_PWM_GENERATOR = "Multi PWM generator"
    CLOCK_SYNCHRONIZER = "Clock synchronizer"


class CameraName(Enum):
    """list of camera names"""

    BODY_CAMERA = "Body Camera"
    EYE_CAMERA = "Eye Camera"
    FACE_CAMERA = "Face Camera"


class Camera(BaseModel):
    """description of generic camera"""

    name: CameraName = Field(..., title="Name")
    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
    position_x: float = Field(..., title="Position X")
    position_y: float = Field(..., title="Position Y")
    position_z: float = Field(..., title="Position Z")
    angle_pitch: float = Field(..., title="Angle pitch (deg)", units="deg")
    angle_yaw: float = Field(..., title="Angle yaw (deg)", units="deg")
    angle_roll: float = Field(..., title="Angle roll (deg)", units="deg")
    recording_software: Optional[str] = Field(None, title="Recording software")
    recording_software_version: Optional[str] = Field(
        None, title="Recording software version"
    )


class Surface(Enum):
    """TODO"""

    NONE = "none"
    FOAM = "foam"


class Disc(BaseModel):
    """basic running disc information"""

    radius: float = Field(..., title="Radius (cm)", units="cm")
    surface: Optional[Surface] = Field(None, title="Surface")
    date_surface_replaced: Optional[datetime] = Field(
        None, title="Date surface replaced"
    )


class LaserName(Enum):
    """TODO"""

    LASER_A = "Laser A"
    LASER_B = "Laser B"


class Laser(BaseModel):
    """description of lasers used in ephys recordings"""

    name: LaserName = Field(..., title="Name")
    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
    wavelength: Optional[int] = Field(
        None, title="Wavelength (nm)", units="nm"
    )
    maximum_power: Optional[float] = Field(
        None, title="Maximum power (mW)", units="mW"
    )
    coupling_efficiency: Optional[float] = Field(
        None, title="Coupling efficiency (percent)", units="percent"
    )
    calibration_data: Optional[str] = Field(
        None, description="path to calibration data", title="Calibration data"
    )
    calibration_date: Optional[datetime] = Field(
        None, title="Calibration date"
    )


class Monitor(BaseModel):
    """description of a physical display"""

    manufacturer: str = Field(..., title="Manufacturer")
    model: str = Field(..., title="Model")
    serial_number: str = Field(..., title="Serial number")
    refresh_rate: int = Field(..., title="Refresh rate (Hz)", units="Hz")
    width: int = Field(..., title="Width (pixels)", units="pixels")
    height: int = Field(..., title="Height (pixels)", units="pixels")
    viewing_distance: float = Field(
        ..., title="Viewing distance (cm)", units="cm"
    )
    position_x: float = Field(..., title="Position X")
    position_y: float = Field(..., title="Position Y")
    position_z: float = Field(..., title="Position Z")
    angle_pitch: float = Field(..., title="Angle pitch (deg)", units="deg")
    angle_yaw: float = Field(..., title="Angle yaw (deg)", units="deg")
    angle_roll: float = Field(..., title="Angle roll (deg)", units="deg")
    contrast: int = Field(
        ...,
        description="Monitor's contrast setting",
        title="Contrast (percent)",
        units="percent",
    )
    brightness: int = Field(
        ..., description="Monitor's brightness setting", title="Brightness"
    )


class ProbeName(Enum):
    """TODO"""

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


class Probe(BaseModel):
    """description of a probe"""

    name: ProbeName = Field(..., title="Name")
    type: str = Field(..., title="Type")
    serial_number: str = Field(..., title="Serial number")


class Devices(BaseModel):
    """all of the devices in the rig"""

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
    """description of an ephys rig"""

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
