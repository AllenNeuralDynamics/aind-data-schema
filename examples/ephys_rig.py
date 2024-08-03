"""Generates an example JSON file for an ephys rig"""

from datetime import date, datetime, timezone

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.devices import (
    Calibration,
    Camera,
    CameraAssembly,
    CameraTarget,
    DAQChannel,
    Device,
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
    Patch,
    ProbePort,
)
from aind_data_schema.core.rig import Rig

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
    name="Laser_assemblyA",
    manipulator=Manipulator(
        name="Manipulator A", serial_number="SN2937", manufacturer=Organization.NEW_SCALE_TECHNOLOGIES
    ),
    lasers=[red_laser, blue_laser],
    collimator=Device(name="Collimator A", device_type="Collimator"),
    fiber=Patch(
        name="Bundle Branching Fiber-optic Patch Cord",
        manufacturer=Organization.DORIC,
        model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
        core_diameter=200,
        numerical_aperture=0.37,
    ),
)

probe_camera_1 = Camera(
    name="stick microscope 1",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=ephys_computer,
    frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Color",
)

probe_camera_2 = Camera(
    name="stick microscope 2",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=ephys_computer,
    frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Color",
)

probe_camera_3 = Camera(
    name="stick microscope 3",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=ephys_computer,
    frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Color",
)

probe_camera_4 = Camera(
    name="stick microscope 4",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=ephys_computer,
    frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Color",
)

stick_lens = Lens(name="Probe lens", manufacturer=Organization.EDMUND_OPTICS)

microscope_1 = CameraAssembly(
    name="Stick_assembly_1",
    camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS TO BE FILLED OUT
    camera=probe_camera_1,
    lens=stick_lens,
)

microscope_2 = CameraAssembly(
    name="Stick_assembly_2",
    camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS TO BE FILLED OUT
    camera=probe_camera_2,
    lens=stick_lens,
)

microscope_3 = CameraAssembly(
    name="Stick_assembly_3",
    camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS TO BE FILLED OUT
    camera=probe_camera_3,
    lens=stick_lens,
)

microscope_4 = CameraAssembly(
    name="Stick_assembly_4",
    camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS TO BE FILLED OUT
    camera=probe_camera_4,
    lens=stick_lens,
)

probeA = EphysProbe(name="Probe A", serial_number="9291019", probe_model="Neuropixels 1.0")

probeB = EphysProbe(name="Probe B", serial_number="9291020", probe_model="Neuropixels 1.0")

ephys_assemblyA = EphysAssembly(
    name="Ephys_assemblyA",
    manipulator=Manipulator(
        name="Manipulator 1", serial_number="SN2938", manufacturer=Organization.NEW_SCALE_TECHNOLOGIES
    ),
    probes=[probeA],
)

ephys_assemblyB = EphysAssembly(
    name="Ephys_assemblyB",
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
    frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Monochrome",
)

camassm1 = CameraAssembly(
    name="Face Camera Assembly",
    camera=face_camera,
    camera_target="Face side left",
    filter=filt,
    lens=lens,
)

body_camera = Camera(
    name="Body Camera",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=behavior_computer,
    frame_rate=50,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Monochrome",
)

camassm2 = CameraAssembly(
    name="Body Camera Assembly",
    camera=body_camera,
    camera_target="Body",
    filter=filt,
    lens=lens,
)

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default

red_laser_calibration = Calibration(
    calibration_date=datetime(2023, 10, 2, 10, 22, 13, tzinfo=timezone.utc),
    device_name="Red Laser",
    description="Laser power calibration",
    input={"power percent": [10, 20, 40]},
    output={"power mW": [1, 3, 6]},
)

blue_laser_calibration = Calibration(
    calibration_date=datetime(2023, 10, 2, 10, 22, 13, tzinfo=timezone.utc),
    device_name="Blue Laser",
    description="Laser power calibration",
    input={"power percent": [10, 20, 40]},
    output={"power mW": [1, 2, 7]},
)

rig = Rig(
    rig_id="323_EPHYS1_20231003",
    modification_date=date(2023, 10, 3),
    modalities=[Modality.ECEPHYS],
    ephys_assemblies=[ephys_assemblyA, ephys_assemblyB],
    cameras=[camassm1, camassm2],
    laser_assemblies=[laser_assembly],
    daqs=[basestation, harp],
    stick_microscopes=[microscope_1, microscope_2, microscope_3, microscope_4],
    mouse_platform=running_wheel,
    calibrations=[red_laser_calibration, blue_laser_calibration],
)
serialized = rig.model_dump_json()
deserialized = Rig.model_validate_json(serialized)
deserialized.write_standard_file(prefix="ephys")
