""" ephys rig schemas """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field

from ..base import AindCoreModel, AindModel
from ..device import DAQ, Device


class HarpDeviceName(Enum):
    """Harp device name"""

    BEHAVIOR = "Behavior"
    CAMERA_CONTROLLER = "Camera Controller"
    LOAD_CELLS = "Load Cells"
    SOUND_BOARD = "Sound Board"
    TIMESTAMP_GENERATOR = "Timestamp Generator"
    INPUT_EXPANDER = "Input Expander"


class HarpDevice(Device):
    """Describes a Harp device"""

    name: HarpDeviceName = Field(..., title="Name")
    device_version: str = Field(..., title="Device version")


class CameraName(Enum):
    """Camera name"""

    BODY_CAMERA = "Body Camera"
    EYE_CAMERA = "Eye Camera"
    FACE_CAMERA = "Face Camera"


class Camera(Device):
    """Description of camera"""

    name: CameraName = Field(..., title="Name")
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


class MousePlatform(Device):
    """Description of a mouse platform"""

    surface_material: Optional[str] = Field(None, title="Surface material")


class Disc(MousePlatform):
    """Description of a running disc"""

    platform_type: str = Field("Disc", title="Platform type", const=True)
    radius: float = Field(..., title="Radius (cm)", units="cm", ge=0)
    date_surface_replaced: Optional[datetime] = Field(
        None, title="Date surface replaced"
    )


class Tube(MousePlatform):
    """Description of a tube platform"""

    platform_type: str = Field("Tube", title="Platform type", const=True)
    diameter: float = Field(..., title="Diameter (cm)", units="cm", ge=0)


class Treadmill(MousePlatform):
    """Descrsiption of treadmill platform"""

    platform_type: str = Field("Treadmill", title="Platform type", const=True)


class AngleName(Enum):
    """Euler angle name"""

    XY = "XY"
    XZ = "XZ"
    YZ = "YZ"


class ManipulatorAngle(AindModel):
    """Description of manipulator angle"""

    name: AngleName = Field(..., title="AngleName")
    value: float = Field(..., title="Value (deg)", units="deg")


class Manipulator(Device):
    """Description of manipulator"""

    manipulator_angles: List[ManipulatorAngle] = Field(
        ..., title="Manipulator angles", unique_items=True
    )


class LaserName(Enum):
    """Laser name"""

    LASER_A = "Laser A"
    LASER_B = "Laser B"
    LASER_C = "Laser C"
    LASER_D = "Laser D"


class LaserModule(Device):
    """Description of lasers used in ephys recordings"""

    name: LaserName = Field(..., title="Laser Name")
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
    laser_manipulator: Manipulator = Field(..., title="Manipulator")


class Monitor(Device):
    """Description of a visual monitor"""

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


class ProbeModel(Enum):
    """Probe model name"""

    NP1 = "Neuropixels 1.0"
    NP_UHD_FIXED = "Neuropixels UHD (Fixed)"
    NP_UHD_SWITCHABLE = "Neuropixels UHD (Switchable)"
    NP2_SINGLE_SHANK = "Neuropixels 2.0 (Single Shank)"
    NP2_MULTI_SHANK = "Neuropixels 2.0 (Multi Shank)"
    NP2_QUAD_BASE = "Neuropixels 2.0 (Quad Base)"
    NP_OPTO_DEMONSTRATOR = "Neuropixels Opto (Demonstrator)"
    MI_ULED_PROBE = "Michigan uLED Probe (Version 1)"
    MP_PHOTONIC_V1 = "MPI Photonic Probe (Version 1)"


class EphysProbe(Device):
    """Description of an ephys probe"""

    name: ProbeName = Field(..., title="Name")
    model: ProbeModel = Field(..., title="Model")
    probe_manipulator: Manipulator = Field(..., title="Manipulator")
    calibration_data: str = Field(
        ..., title="Calibration data", description="Path to calibration data"
    )
    calibration_date: Optional[datetime] = Field(
        None, title="Calibration date"
    )


class EphysRig(AindCoreModel):
    """Description of an ephys rig"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/ephys_rig.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field(
        "0.4.2", description="schema version", title="Version", const=True
    )
    rig_id: str = Field(
        ..., description="room_stim apparatus_version", title="Rig ID"
    )
    probes: Optional[List[EphysProbe]] = Field(
        None, title="Ephys probes", unique_items=True
    )
    cameras: Optional[List[Camera]] = Field(
        None, title="Cameras", unique_items=True
    )
    lasers: Optional[List[LaserModule]] = Field(
        None, title="Lasers", unique_items=True
    )
    visual_monitors: Optional[List[Monitor]] = Field(
        None, title="Visual monitor", unique_items=True
    )
    mouse_platform: Optional[MousePlatform] = Field(
        None, title="Mouse platform"
    )
    harp_devices: Optional[List[HarpDevice]] = Field(
        None, title="Harp devices"
    )
    daq: Optional[DAQ] = Field(None, title="DAQ")
