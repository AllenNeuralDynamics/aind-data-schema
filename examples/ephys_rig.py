"""Generates an example JSON file for an ephys rig"""

import datetime

from aind_data_schema.core.rig import Rig
from aind_data_schema.models.devices import (
    Calibration,
    Camera,
    CameraAssembly,
    DAQChannel,
    Disc,
    EphysAssembly,
    EphysProbe,
    Filter,
    HarpDevice,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    NeuropixelsBasestation,
    ProbePort,
    StickMicroscopeAssembly,
)
from aind_data_schema.models.harp_types import HarpDeviceType
from aind_data_schema.models.modalities import Modality
from aind_data_schema.models.organizations import Organization

# Describes a rig with running wheel, 2 behavior cameras, one Harp Behavior board,
# one dual-color laser module, one stick microscope, and 2 Neuropixels probes

behavior_computer = "W10DT72941"
ephys_computer = "W10DT72942"

running_wheel = Disc(name="Running Wheel", radius=15)

digital_out0 = DAQChannel(channel_name="DO0", device_name="Face Camera", channel_type="Digital Output")

digital_out1 = DAQChannel(channel_name="DO1", device_name="Body Camera", channel_type="Digital Output")

analog_input = DAQChannel(channel_name="AI0", device_name="Running Wheel", channel_type="Analog Input")

harp = HarpDevice(
    name="Harp Behavior",
    harp_device_type=HarpDeviceType.BEHAVIOR,
    core_version="2.1",
    computer_name=behavior_computer,
    channels=[digital_out0, digital_out1, analog_input],
    is_clock_generator=False,
)

port1 = ProbePort(index=1, probes=["Probe A"])

port2 = ProbePort(index=2, probes=["Probe B"])

basestation = NeuropixelsBasestation(
    name="Basestation Slot 3",
    basestation_firmware_version="2.019",
    bsc_firmware_version="2.199",
    slot=3,
    ports=[port1, port2],
    computer_name=ephys_computer,
)

red_laser = Laser(name="Red Laser", wavelength=473, manufacturer=Organization.OXXIUS)

blue_laser = Laser(name="Blue Laser", wavelength=638, manufacturer=Organization.OXXIUS)

laser_assembly = LaserAssembly(
    laser_assembly_name="Laser_assemblyA",
    manipulator=Manipulator(
        name="Manipulator A", serial_number="SN2937", manufacturer=Organization.NEW_SCALE_TECHNOLOGIES
    ),
    lasers=[red_laser, blue_laser],
)

probe_camera = Camera(
    name="Probe Camera",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=ephys_computer,
    max_frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Color",
)

stick_lens = Lens(name="Probe lens", manufacturer=Organization.EDMUND_OPTICS)

microscope = StickMicroscopeAssembly(
    scope_assembly_name="Stick_assembly",
    camera=probe_camera,
    lens=stick_lens,
)

probeA = EphysProbe(name="Probe A", serial_number="9291019", probe_model="Neuropixels 1.0")

probeB = EphysProbe(name="Probe B", serial_number="9291020", probe_model="Neuropixels 1.0")

ephys_assemblyA = EphysAssembly(
    ephys_assembly_name="Ephys_assemblyA",
    manipulator=Manipulator(
        name="Manipulator 1", serial_number="SN2938", manufacturer=Organization.NEW_SCALE_TECHNOLOGIES
    ),
    probes=[probeA],
)

ephys_assemblyB = EphysAssembly(
    ephys_assembly_name="Ephys_assemblyB",
    manipulator=Manipulator(
        name="Manipulator B", serial_number="SN2939", manufacturer=Organization.NEW_SCALE_TECHNOLOGIES
    ),
    probes=[probeB],
)

filt = Filter(
    name="LP filter",
    filter_type="Long pass",
    manufacturer=Organization.THORLABS,
    description="850 nm longpass filter",
)

lens = Lens(name="Camera lens", focal_length=15, manufacturer=Organization.EDMUND_OPTICS, max_aperture="f/2")

face_camera = Camera(
    name="Face Camera",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=behavior_computer,
    max_frame_rate=500,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Monochrome",
)

camassm1 = CameraAssembly(
    camera_assembly_name="Face Camera Assembly",
    camera=face_camera,
    camera_target="Face side",
    filter=filt,
    lens=lens,
)

body_camera = Camera(
    name="Body Camera",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=behavior_computer,
    max_frame_rate=500,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Monochrome",
)

camassm2 = CameraAssembly(
    camera_assembly_name="Body Camera Assembly",
    camera=body_camera,
    camera_target="Body",
    filter=filt,
    lens=lens,
)

red_laser_calibration = Calibration(
    calibration_date=datetime.datetime(2023, 10, 2, 10, 22, 13),
    device_name="Red Laser",
    description="Laser power calibration",
    input={"power percent": [10, 20, 40]},
    output={"power mW": [1, 3, 6]},
)

blue_laser_calibration = Calibration(
    calibration_date=datetime.datetime(2023, 10, 2, 10, 22, 13),
    device_name="Blue Laser",
    description="Laser power calibration",
    input={"power percent": [10, 20, 40]},
    output={"power mW": [1, 2, 7]},
)

rig = Rig(
    rig_id="323_EPHYS1",
    modification_date=datetime.date(2023, 10, 3),
    modalities=[Modality.ECEPHYS],
    ephys_assemblies=[ephys_assemblyA, ephys_assemblyB],
    cameras=[camassm1, camassm2],
    laser_assemblies=[laser_assembly],
    daqs=[basestation, harp],
    stick_microscopes=[microscope],
    mouse_platform=running_wheel,
    calibrations=[red_laser_calibration, blue_laser_calibration],
)

rig.write_standard_file(prefix="ephys")
