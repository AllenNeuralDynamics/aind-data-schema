""" ephys rig schemas """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal

from pydantic import Field, root_validator

from ..base import AindCoreModel, AindModel
from ..device import (AngleUnit, Camera, CameraAssembly, DAQDevice, DataInterface, Device, Laser, Manufacturer,
                      RelativePosition, SizeUnit)


class Size2d(AindModel):
    """2D size of an object"""

    width: int = Field(..., title="Width")
    height: int = Field(..., title="Height")
    unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")


class Orientation3d(AindModel):
    """3D orientation of an object"""

    pitch: float = Field(..., title="Angle pitch", ge=0, le=360)
    yaw: float = Field(..., title="Angle yaw", ge=0, le=360)
    roll: float = Field(..., title="Angle roll", ge=0, le=360)
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class ModuleOrientation2d(AindModel):
    """2D module orientation of an object"""

    arc_angle: float = Field(..., title="Arc angle")
    module_angle: float = Field(..., title="Module angle")
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class ModuleOrientation3d(AindModel):
    """3D module orientation of an object"""

    arc_angle: float = Field(..., title="Arc angle")
    module_angle: float = Field(..., title="Module angle")
    rotation_angle: float = Field(..., title="Rotation angle")
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class Coordinates3d(AindModel):
    """Coordinates in a 3D grid"""

    x: float = Field(..., title="Position X")
    y: float = Field(..., title="Position Y")
    z: float = Field(..., title="Position Z")
    unit: SizeUnit = Field(SizeUnit.UM, title="Position unit")


class HarpDeviceType(Enum):
    """Harp device type"""

    BEHAVIOR = "Behavior"
    CAMERA_CONTROLLER = "Camera Controller"
    LOAD_CELLS = "Load Cells"
    SOUND_BOARD = "Sound Board"
    TIMESTAMP_GENERATOR = "Timestamp Generator"
    INPUT_EXPANDER = "Input Expander"


class HarpDevice(DAQDevice):
    """DAQ that uses the Harp protocol for synchronization and data transmission"""

    # required fields
    harp_device_type: HarpDeviceType = Field(..., title="Type of Harp device")
    harp_device_version: str = Field(..., title="Device version")

    # fixed values
    manufacturer: Manufacturer = Manufacturer.OEPS
    data_interface: DataInterface = Field("USB", const=True)


class ProbePort(AindModel):
    """Port for a probe connection"""

    index: int = Field(..., title="Zero-based port index")
    probes: List[str] = Field(..., title="Names of probes connected to this port")


class NeuropixelsBasestation(DAQDevice):
    """PXI-based Neuropixels DAQ"""

    # required fields
    basestation_firmware_version: str = Field(..., title="Basestation firmware version")
    bsc_firmware_version: str = Field(..., title="Basestation connect board firmware")
    slot: int = Field(..., title="Slot number for this basestation")
    ports: List[ProbePort] = Field(..., title="Basestation ports")

    # fixed values
    data_interface: DataInterface = Field("PXI", const=True)
    manufacturer: Manufacturer = Manufacturer.IMEC


class OpenEphysAcquisitionBoard(DAQDevice):
    """Multichannel electrophysiology DAQ"""

    # required fields
    ports: List[ProbePort] = Field(..., title="Acquisition board ports")

    # fixed values
    data_interface: DataInterface = Field("USB", const=True)
    manufacturer: Manufacturer = Manufacturer.OEPS


class MousePlatform(Device):
    """Description of a mouse platform"""

    surface_material: Optional[str] = Field(None, title="Surface material")
    date_surface_replaced: Optional[datetime] = Field(None, title="Date surface replaced")


class Disc(MousePlatform):
    """Description of a running disc"""

    platform_type: str = Field("Disc", title="Platform type", const=True)
    radius: float = Field(..., title="Radius (cm)", units="cm", ge=0)
    radius_unit: SizeUnit = Field(SizeUnit.CM, title="radius unit")


class Tube(MousePlatform):
    """Description of a tube platform"""

    platform_type: str = Field("Tube", title="Platform type", const=True)
    diameter: float = Field(..., title="Diameter", ge=0)
    diameter_unit: SizeUnit = Field(SizeUnit.CM, title="Diameter unit")


class Treadmill(MousePlatform):
    """Description of treadmill platform"""

    platform_type: str = Field("Treadmill", title="Platform type", const=True)
    treadmill_width: float = Field(..., title="Width of treadmill (mm)", units="mm")
    width_unit: SizeUnit = Field(SizeUnit.CM, title="Width unit")


class DomeModule(AindModel):
    """Movable module that is mounted on the ephys dome insertion system"""

    # required fields
    arc_angle: float = Field(..., title="Arc Angle", units="degrees")
    module_angle: float = Field(..., title="Module Angle", units="degrees")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")

    # optional fields
    rotation_angle: Optional[float] = Field(0.0, title="Rotation Angle", units="degrees")
    coordinate_transform: Optional[str] = Field(
        None, title="Transform from local manipulator axes to rig", description="Path to coordinate transform"
    )
    calibration_date: Optional[datetime] = Field(None, title="Data on which coordinate transform was last calibrated")


class Manipulator(Device):
    """Manipulator used on a dome module"""

    manufacturer: Literal[Manufacturer.NEW_SCALE_TECHNOLOGIES.value]


class StickMicroscope(DomeModule):
    """Stick microscope used to monitor probes during insertion"""

    camera: Camera = Field(..., title="Camera for this module")


class LaserModule(DomeModule):
    """Module for optogenetic stimulation"""

    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: List[Laser] = Field(..., title="Lasers connected to this module")


class Monitor(Device):
    """Visual display"""

    # required fields
    manufacturer: Literal[Manufacturer.LG.value]
    refresh_rate: int = Field(..., title="Refresh rate (Hz)", units="Hz", ge=60)
    width: int = Field(..., title="Width (pixels)", units="pixels")
    height: int = Field(..., title="Height (pixels)", units="pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    viewing_distance: float = Field(..., title="Viewing distance (cm)", units="cm")
    viewing_distance_unit: SizeUnit = Field(SizeUnit.CM, title="Viewing distance unit")

    # optional fields
    contrast: Optional[int] = Field(
        ...,
        description="Monitor's contrast setting",
        title="Contrast",
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


class HeadstageModel(Enum):
    """Headstage model name"""

    RHD_16_CH = "Intan RHD 16-channel"
    RHD_32_CH = "Intan RHD 32-channel"
    RHD_64_CH = "Intan RHD 64-channel"


class EphysProbe(Device):
    """Named probe used in an ephys experiment"""

    # required fields
    probe_model: ProbeModel = Field(..., title="Probe model")

    # optional fields
    lasers: Optional[List[Laser]] = Field(None, title="Lasers connected to this probe")
    headstage: Optional[HeadstageModel] = Field(None, title="Headstage for this probe")


class EphysModule(DomeModule):
    """Module for electrophysiological recording"""

    manipulator: Manipulator = Field(..., title="Manipulator")
    probes: List[EphysProbe] = Field(..., title="Probes that are held by this module")


class EphysRig(AindCoreModel):
    """Description of an ephys rig"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/ephys_rig.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field("0.5.2", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    ephys_modules: Optional[List[EphysModule]] = Field(None, title="Ephys probes", unique_items=True)
    stick_microscopes: Optional[List[StickMicroscope]] = Field(None, title="Stick microscopes")
    laser_modules: Optional[List[LaserModule]] = Field(None, title="Laser modules", unique_items=True)
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    visual_monitors: Optional[List[Monitor]] = Field(None, title="Visual monitors", unique_items=True)
    mouse_platform: Optional[Union[Tube, Treadmill, Disc]] = Field(None, title="Mouse platform")
    daqs: Optional[List[Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice]]] = Field(
        None, title="Data acquisition devices"
    )

    @root_validator
    def validate_device_names(cls, values):
        """validate that all DAQ channels are connected to devices that
        actually exist
        """

        cameras = values.get("cameras")
        ephys_modules = values.get("ephys_modules")
        laser_modules = values.get("laser_modules")
        mouse_platform = values.get("mouse_platform")
        daqs = values.get("daqs")

        if daqs is None:
            return values

        device_names = [None]

        if cameras is not None:
            device_names += [c.camera.name for c in cameras]

        if ephys_modules is not None:
            device_names += [probe.name for ephys_module in ephys_modules for probe in ephys_module.probes]

        if laser_modules is not None:
            device_names += [laser.name for laser_module in laser_modules for laser in laser_module.lasers]

        if mouse_platform is not None:
            device_names += [mouse_platform.name]

        for daq in daqs:
            if daq.channels is not None:
                for channel in daq.channels:
                    if channel.device_name not in device_names:
                        raise ValueError(
                            f"Device name validation error: '{channel.device_name}' "
                            + f"is connected to '{channel.channel_name}' on '{daq.name}', but "
                            + "this device is not part of the rig."
                        )

        return values

    @root_validator
    def validate_probe_names(cls, values):
        """validate that all DAQ probe ports are connected to probes that
        actually exist
        """

        ephys_modules = values.get("ephys_modules")
        daqs = values.get("daqs")

        if daqs is None or ephys_modules is None:
            return values

        probe_names = [probe.name for ephys_module in ephys_modules for probe in ephys_module.probes]

        for daq in daqs:
            try:
                daq.ports
            except AttributeError:
                pass
            else:
                if daq.ports is not None:
                    for port in daq.ports:
                        for probe in port.probes:
                            if probe not in probe_names:
                                raise ValueError(
                                    f"Probe name validation error: '{probe}' "
                                    + f"is connected to '{daq.name}' port '{port.index}', but "
                                    + "this probe is not part of the rig."
                                )

        return values
