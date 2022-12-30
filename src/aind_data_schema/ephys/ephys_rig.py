""" ephys rig schemas """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from ..device import DeviceBase, DAQ, Camera, CameraAssembly, RelativePosition, Laser
from ..base import AindCoreModel, AindModel


class HarpDeviceType(Enum):
    """Harp device name"""

    BEHAVIOR = "Behavior"
    CAMERA_CONTROLLER = "Camera Controller"
    LOAD_CELLS = "Load Cells"
    SOUND_BOARD = "Sound Board"
    TIMESTAMP_GENERATOR = "Timestamp Generator"
    INPUT_EXPANDER = "Input Expander"


class HarpDevice(DAQ):
    """Describes a Harp device"""

    device_type: HarpDeviceType = Field(..., title="Type of Harp device")
    device_version: str = Field(..., title="Device version")
    daq_manufacturer: str = Field("OEPS", title="Harp device manufacturer", const=True)


class ProbePort(AindModel):
    """Port for a probe connection"""

    index: int = Field(..., title="Port index")
    probes: List[str] = Field(..., title="Names of probes connected to this port")


class NeuropixelsBasestation(DAQ):
    """Describes a Neuropixels basestation"""

    basestation_firmware: str = Field(..., title="Basestation firmware version")
    bsc_firmware: str = Field(..., title="Basestation connect board firmware")
    slot: int = Field(..., title="Slot number for this basestation")
    ports: List[ProbePort] = Field(..., title="Basestation ports")
    daq_manufacturer: str = Field("IMEC", title="Basestation device manufacturer", const=True)


class OpenEphysAcquisitionBoard(DAQ):
    """Describes an Open Ephys Acquisition Board"""

    ports: List[ProbePort] = Field(..., title="Acquisition board ports")


class MousePlatform(DeviceBase):
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
    """Description of treadmill platform"""

    platform_type: str = Field("Treadmill", title="Platform type", const=True)


class DomeModule(AindModel):
    """A module that is mounted on the ephys dome insertion system"""

    arc_angle: float = Field(..., title="Arc Angle", units="degrees")
    module_angle: float = Field(..., title="Module Angle", units="degrees")
    rotation_angle: Optional[float] = Field(0.0, title="Rotatle Angle", units="degrees")
    coordinate_transform: Optional[str] = Field(
        None,
        title="Transform from local manipulator axes to rig", 
        description="Path to coordinate transform"
    )
    calibration_date: Optional[datetime] = Field(
        None, 
        title="Data on which coordinate transform was last calibrated"
    )


class StickMicroscope(DomeModule):
    """Description of a stick microscope used to monitor probes during insertion"""

    camera: Camera = Field(..., title="Camera on this module")
    

class ManipulatorManufacturer(Enum):
    """Manipulator manufacturer"""

    NEW_SCALE_TECHNOLOGIES = "New Scale Technologies"


class MonitorManufacturer(Enum):
    """Monitor manufacturer"""

    LG = "LG"


class Manipulator(DeviceBase):
    """Description of manipulator"""
    
    manipulator_manufacturer: ManipulatorManufacturer = Field(..., title="Manipulator manufacturer")


class LaserModule(DomeModule):
    """Description of lasers used in ephys recordings"""

    laser_module_name: str = Field(..., title="Laser module name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: List[Laser] = Field(..., title="Lasers connected to this module")


class Monitor(DeviceBase):
    """Description of a visual monitor"""

    monitor_manufacturer: MonitorManufacturer = Field(..., title="Monitor manufacturer")
    refresh_rate: int = Field(
        ..., title="Refresh rate (Hz)", units="Hz", ge=60
    )
    width: int = Field(..., title="Width (pixels)", units="pixels")
    height: int = Field(..., title="Height (pixels)", units="pixels")
    viewing_distance: float = Field(
        ..., title="Viewing distance (cm)", units="cm"
    )
    contrast: Optional[int] = Field(
        ...,
        description="Monitor's contrast setting",
        title="Contrast (percent)",
        units="percent",
        ge=0,
        le=100,
    )
    brightness: Optional[int] = Field(
        ...,
        description="Monitor's brightness setting",
        title="Brightness",
        ge=0,
        le=100,
    )
    position: Optional[RelativePosition] = Field(None, title="Relative position of the monitor")


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


class EphysProbe(DeviceBase, DomeModule):
    """Description of an ephys probe"""

    probe_name: str = Field(..., title="Name")
    probe_model: ProbeModel = Field(..., title="Probe model")
    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: Optional[List[Laser]] = Field(None, title="Lasers connected to this probe")


class EphysRig(AindCoreModel):
    """Description of an ephys rig"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/ephys_rig.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field(
        "0.5.0", description="schema version", title="Version", const=True
    )
    rig_id: str = Field(
        ..., description="room_stim apparatus_version", title="Rig ID"
    )
    probes: Optional[List[EphysProbe]] = Field(
        None, title="Ephys probes", unique_items=True
    )
    cameras: Optional[List[CameraAssembly]] = Field(
        None, title="Camera assemblies", unique_items=True
    )
    lasers: Optional[List[LaserModule]] = Field(
        None, title="Laser modules", unique_items=True
    )
    visual_monitors: Optional[List[Monitor]] = Field(
        None, title="Visual monitors", unique_items=True
    )
    mouse_platform: Optional[Union[Tube,Treadmill,Disc]] = Field(
        None, title="Mouse platform"
    )
    daqs: Optional[List[DAQ]] = Field(
        None, title="DAQs"
    )
    stick_microscopes: Optional[List[StickMicroscope]] = Field(
        None, title="Stick microscopes"
    )
