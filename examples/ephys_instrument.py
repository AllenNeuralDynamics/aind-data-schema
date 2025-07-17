"""Generates an example JSON file for an ephys instrument"""

from datetime import date, datetime, timezone

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, SizeUnit
from aind_data_schema.components.coordinates import CoordinateSystemLibrary

from aind_data_schema.components.devices import (
    Camera,
    CameraAssembly,
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
    FiberPatchCord,
    ProbePort,
    Computer,
)
from aind_data_schema.components.measurements import Calibration
from aind_data_schema.components.connections import Connection
from aind_data_schema.core.instrument import Instrument
from aind_data_schema_models.units import PowerUnit
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.devices import CameraTarget

# Describes an instrument with running wheel, 2 behavior cameras, one Harp Behavior board,
# one dual-color laser module, one stick microscope, and 2 Neuropixels probes

computer_names = {
    "Behavior computer": "W10DT72941",
    "Ephys computer": "W10DT72942",
}
behavior_computer = Computer(name=computer_names["Behavior computer"])
ephys_computer = Computer(name=computer_names["Ephys computer"])

running_wheel = Disc(name="Running Wheel", radius=15)

digital_out0 = DAQChannel(channel_name="DO0", channel_type="Digital Output")

digital_out1 = DAQChannel(channel_name="DO1", channel_type="Digital Output")

analog_input = DAQChannel(channel_name="AI0", channel_type="Analog Input")

harp = HarpDevice(
    name="Harp Behavior",
    harp_device_type=HarpDeviceType.BEHAVIOR,
    core_version="2.1",
    channels=[digital_out0, digital_out1, analog_input],
    is_clock_generator=False,
)

connections = [
    Connection(
        source_device="Harp Behavior",
        source_port="DO0",
        target_device="Face Camera",
    ),
    Connection(
        source_device="Harp Behavior",
        source_port="DO1",
        target_device="Body Camera",
    ),
    Connection(
        source_device="Running Wheel",
        target_device="Harp Behavior",
        target_port="AI0",
    ),
    Connection(
        source_device="Harp Behavior",
        target_device=computer_names["Behavior computer"],
    ),
    Connection(
        source_device="Face Camera",
        target_device=computer_names["Behavior computer"],
    ),
    Connection(
        source_device="Body Camera",
        target_device=computer_names["Behavior computer"],
    ),
    Connection(
        source_device="Basestation Slot 3",
        target_device=computer_names["Ephys computer"],
    ),
    Connection(
        source_device="stick microscope 1",
        target_device=computer_names["Ephys computer"],
    ),
    Connection(
        source_device="stick microscope 2",
        target_device=computer_names["Ephys computer"],
    ),
    Connection(
        source_device="stick microscope 3",
        target_device=computer_names["Ephys computer"],
    ),
    Connection(
        source_device="stick microscope 4",
        target_device=computer_names["Ephys computer"],
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
    fiber=FiberPatchCord(
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
    cut_on_wavelength=850,
    wavelength_unit=SizeUnit.NM,
)

lens = Lens(
    name="Camera lens",
    manufacturer=Organization.EDMUND_OPTICS,
)

face_camera = Camera(
    name="Face Camera",
    detector_type="Camera",
    data_interface="USB",
    manufacturer=Organization.FLIR,
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
    location="323",
    instrument_id="EPHYS1",
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
        behavior_computer,
        ephys_computer,
    ],
    connections=connections,
    calibrations=[red_laser_calibration, blue_laser_calibration],
)

if __name__ == "__main__":
    serialized = inst.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="ephys")
