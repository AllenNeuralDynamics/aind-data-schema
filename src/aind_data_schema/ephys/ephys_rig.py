""" ephys rig schemas """

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import Field, root_validator

from aind_data_schema.base import AindCoreModel, AindModel, EnumSubset
from aind_data_schema.device import (
    Camera,
    CameraAssembly,
    DAQDevice,
    DataInterface,
    Device,
    Disc,
    HarpDevice,
    Laser,
    Lens,
    Manufacturer,
    Monitor,
    Treadmill,
    Tube,
)


class ProbePort(AindModel):
    """Port for a probe connection"""

    index: int = Field(..., title="One-based port index")
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
    manufacturer: Manufacturer = Field(Manufacturer.IMEC, const=True)


class OpenEphysAcquisitionBoard(DAQDevice):
    """Multichannel electrophysiology DAQ"""

    # required fields
    ports: List[ProbePort] = Field(..., title="Acquisition board ports")

    # fixed values
    data_interface: DataInterface = Field("USB", const=True)
    manufacturer: Manufacturer = Manufacturer.OEPS


class Manipulator(Device):
    """Manipulator used on a dome module"""

    manufacturer: EnumSubset[Manufacturer.NEW_SCALE_TECHNOLOGIES]


class StickMicroscopeAssembly(AindModel):
    """Stick microscope used to monitor probes during insertion"""

    scope_assembly_name: str = Field(..., title="Scope assembly name")
    camera: Camera = Field(..., title="Camera for this module")
    lens: Lens = Field(..., title="Lens for this module")


class LaserAssembly(AindModel):
    """Assembly for optogenetic stimulation"""

    laser_assembly_name: str = Field(..., title="Laser assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: List[Laser] = Field(..., title="Lasers connected to this module")


class ProbeModel(Enum):
    """Probe model name"""

    MI_ULED_PROBE = "Michigan uLED Probe (Version 1)"
    MP_PHOTONIC_V1 = "MPI Photonic Probe (Version 1)"
    NP_OPTO_DEMONSTRATOR = "Neuropixels Opto (Demonstrator)"
    NP_UHD_FIXED = "Neuropixels UHD (Fixed)"
    NP_UHD_SWITCHABLE = "Neuropixels UHD (Switchable)"
    NP1 = "Neuropixels 1.0"
    NP2_SINGLE_SHANK = "Neuropixels 2.0 (Single Shank)"
    NP2_MULTI_SHANK = "Neuropixels 2.0 (Multi Shank)"
    NP2_QUAD_BASE = "Neuropixels 2.0 (Quad Base)"


class HeadstageModel(Enum):
    """Headstage model name"""

    RHD_16_CH = "Intan RHD 16-channel"
    RHD_32_CH = "Intan RHD 32-channel"
    RHD_64_CH = "Intan RHD 64-channel"


class Headstage(Device):
    """Headstage used with an ephys probe"""

    headstage_model: Optional[HeadstageModel] = Field(None, title="Headstage model")


class EphysProbe(Device):
    """Named probe used in an ephys experiment"""

    # required fields
    probe_model: ProbeModel = Field(..., title="Probe model")

    # optional fields
    lasers: Optional[List[Laser]] = Field(None, title="Lasers connected to this probe")
    headstage: Optional[Headstage] = Field(None, title="Headstage for this probe")


class EphysAssembly(AindModel):
    """Module for electrophysiological recording"""

    ephys_assembly_name: str = Field(..., title="Ephys assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    probes: List[EphysProbe] = Field(..., title="Probes that are held by this module")


class EphysRig(AindCoreModel):
    """Description of an ephys rig"""

    schema_version: str = Field("0.7.5", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    ephys_assemblies: Optional[List[EphysAssembly]] = Field(None, title="Ephys probes", unique_items=True)
    stick_microscopes: Optional[List[StickMicroscopeAssembly]] = Field(None, title="Stick microscopes")
    laser_assemblies: Optional[List[LaserAssembly]] = Field(None, title="Laser modules", unique_items=True)
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    visual_monitors: Optional[List[Monitor]] = Field(None, title="Visual monitors", unique_items=True)
    mouse_platform: Optional[Union[Tube, Treadmill, Disc]] = Field(None, title="Mouse platform")
    daqs: Optional[List[Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice]]] = Field(
        None, title="Data acquisition devices"
    )
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")

    @root_validator
    def validate_device_names(cls, values):
        """validate that all DAQ channels are connected to devices that
        actually exist
        """

        cameras = values.get("cameras")
        ephys_assemblies = values.get("ephys_assemblies")
        laser_assemblies = values.get("laser_assemblies")
        mouse_platform = values.get("mouse_platform")
        daqs = values.get("daqs")

        if daqs is None:
            return values

        device_names = [None]

        if cameras is not None:
            device_names += [c.camera.name for c in cameras]

        if ephys_assemblies is not None:
            device_names += [probe.name for ephys_assembly in ephys_assemblies for probe in ephys_assembly.probes]

        if laser_assemblies is not None:
            device_names += [laser.name for laser_assembly in laser_assemblies for laser in laser_assembly.lasers]

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

        ephys_assemblies = values.get("ephys_assemblies")
        daqs = values.get("daqs")

        if daqs is None or ephys_assemblies is None:
            return values

        probe_names = [probe.name for ephys_assembly in ephys_assemblies for probe in ephys_assembly.probes]

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
