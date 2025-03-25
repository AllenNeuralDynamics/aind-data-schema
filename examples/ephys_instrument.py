"""Generates an example JSON file for an ephys instrument"""

from datetime import date, datetime, timezone

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, SizeUnit
from aind_data_schema.components.coordinates import (
    AnatomicalRelative,
    CoordinateSystemLibrary,
)

from aind_data_schema.components.devices import (
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
    PatchCord,
    ProbePort,
)
from aind_data_schema.components.measurements import Calibration
from aind_data_schema.core.instrument import Instrument, Connection, ConnectionData, ConnectionDirection
from aind_data_schema_models.units import PowerUnit

# Describes an instrument with running wheel, 2 behavior cameras, one Harp Behavior board,
# one dual-color laser module, one stick microscope, and 2 Neuropixels probes

behavior_computer = "W10DT72941"
ephys_computer = "W10DT72942"

running_wheel = Disc(name="Running Wheel", radius=15)

digital_out0 = DAQChannel(channel_name="DO0", channel_type="Digital Output")

digital_out1 = DAQChannel(channel_name="DO1", channel_type="Digital Output")

analog_input = DAQChannel(channel_name="AI0", channel_type="Analog Input")

harp = HarpDevice(
    name="Harp Behavior",
    harp_device_type=HarpDeviceType.BEHAVIOR,
    core_version="2.1",
    computer_name=behavior_computer,
    channels=[digital_out0, digital_out1, analog_input],
    is_clock_generator=False,
)

connections = [
    Connection(
        device_names=["Harp Behavior", "Face Camera"],
        connection_data={
            "Harp Behavior": ConnectionData(channel="DO0", direction=ConnectionDirection.SEND),
            "Face Camera": ConnectionData(direction=ConnectionDirection.RECEIVE),
        },
    ),
    Connection(
        device_names=["Harp Behavior", "Body Camera"],
        connection_data={
            "Harp Behavior": ConnectionData(channel="DO1", direction=ConnectionDirection.SEND),
            "Body Camera": ConnectionData(direction=ConnectionDirection.RECEIVE),
        },
    ),
    Connection(
        device_names=["Harp Behavior", "Running Wheel"],
        connection_data={
            "Harp Behavior": ConnectionData(channel="AI0", direction=ConnectionDirection.RECEIVE),
            "Running Wheel": ConnectionData(direction=ConnectionDirection.SEND),
        },
    ),
]

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
    collimator=Device(name="Collimator A"),
    fiber=PatchCord(
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
    frame_rate_unit=FrequencyUnit.HZ,
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
    frame_rate_unit=FrequencyUnit.HZ,
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
    frame_rate_unit=FrequencyUnit.HZ,
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
    frame_rate_unit=FrequencyUnit.HZ,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Color",
)

stick_lens = Lens(name="Probe lens", manufacturer=Organization.EDMUND_OPTICS)

microscope_1 = CameraAssembly(
    name="Stick_assembly_1",
    target=CameraTarget.BRAIN,
    relative_position=[AnatomicalRelative.SUPERIOR],
    camera=probe_camera_1,
    lens=stick_lens,
)

microscope_2 = CameraAssembly(
    name="Stick_assembly_2",
    target=CameraTarget.BRAIN,
    relative_position=[AnatomicalRelative.SUPERIOR],
    camera=probe_camera_2,
    lens=stick_lens,
)

microscope_3 = CameraAssembly(
    name="Stick_assembly_3",
    target=CameraTarget.BRAIN,
    relative_position=[AnatomicalRelative.SUPERIOR],
    camera=probe_camera_3,
    lens=stick_lens,
)

microscope_4 = CameraAssembly(
    name="Stick_assembly_4",
    target=CameraTarget.BRAIN,
    relative_position=[AnatomicalRelative.SUPERIOR],
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

lens = Lens(
    name="Camera lens",
    focal_length=15,
    focal_length_unit=SizeUnit.MM,
    manufacturer=Organization.EDMUND_OPTICS,
    max_aperture="f/2",
)

face_camera = Camera(
    name="Face Camera",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
    computer_name=behavior_computer,
    frame_rate=50,
    frame_rate_unit=FrequencyUnit.HZ,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Monochrome",
)

camassm1 = CameraAssembly(
    name="Face Camera Assembly",
    camera=face_camera,
    target=CameraTarget.FACE,
    relative_position=[AnatomicalRelative.LEFT],
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
    frame_rate_unit=FrequencyUnit.HZ,
    sensor_width=1080,
    sensor_height=570,
    sensor_format="1/2.9",
    sensor_format_unit="inches",
    chroma="Monochrome",
)

camassm2 = CameraAssembly(
    name="Body Camera Assembly",
    target=CameraTarget.BODY,
    relative_position=[AnatomicalRelative.SUPERIOR],
    camera=body_camera,
    filter=filt,
    lens=lens,
)

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default

red_laser_calibration = Calibration(
    calibration_date=datetime(2023, 10, 2, 10, 22, 13, tzinfo=timezone.utc),
    device_name="Red Laser",
    description="Laser power calibration",
    input=[10, 20, 40],
    input_unit=PowerUnit.PERCENT,
    output=[1, 3, 6],
    output_unit=PowerUnit.MW,
)

blue_laser_calibration = Calibration(
    calibration_date=datetime(2023, 10, 2, 10, 22, 13, tzinfo=timezone.utc),
    device_name="Blue Laser",
    description="Laser power calibration",
    input=[10, 20, 40],
    input_unit=PowerUnit.PERCENT,
    output=[1, 2, 7],
    output_unit=PowerUnit.MW,
)

inst = Instrument(
    instrument_id="323_EPHYS1_20231003",
    modification_date=date(2023, 10, 3),
    modalities=[Modality.ECEPHYS],
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    components=[
        ephys_assemblyA,
        ephys_assemblyB,
        camassm1,
        camassm2,
        laser_assembly,
        basestation,
        harp,
        microscope_1,
        microscope_2,
        microscope_3,
        microscope_4,
        running_wheel,
    ],
    connections=connections,
    calibrations=[red_laser_calibration, blue_laser_calibration],
)
serialized = inst.model_dump_json()
deserialized = Instrument.model_validate_json(serialized)
deserialized.write_standard_file(prefix="ephys")
