"""Tests rig session compatibility check"""

import json
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization

import aind_data_schema.components.devices as d
import aind_data_schema.core.rig as r
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
    Software,
)
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import (
    CcfCoords,
    Coordinates3d,
    DetectorConfig,
    DomeModule,
    FiberConnectionConfig,
    FiberModule,
    LaserConfig,
    ManipulatorModule,
    Session,
    StimulusEpoch,
    StimulusModality,
    Stream,
    VisualStimulation,
)
from aind_data_schema.utils.compatibility_check import RigSessionCompatibility

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"
EPHYS_RIG_JSON = EXAMPLES_DIR / "ephys_rig.json"
EPHYS_SESSION_JSON = EXAMPLES_DIR / "ephys_session.json"

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

probe_camera = Camera(
    name="Probe Camera",
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

microscope = CameraAssembly(
    name="Stick_assembly",
    camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS TO BE FILLED OUT
    camera=probe_camera,
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

ephys_rig = Rig(
    rig_id="323_EPHYS1_20231003",
    modification_date=date(2023, 10, 3),
    modalities=[Modality.ECEPHYS],
    ephys_assemblies=[ephys_assemblyA, ephys_assemblyB],
    cameras=[camassm1, camassm2],
    laser_assemblies=[laser_assembly],
    daqs=[basestation, harp],
    stick_microscopes=[microscope],
    mouse_platform=running_wheel,
    calibrations=[red_laser_calibration, blue_laser_calibration],
)

ephys_session = Session(
    experimenter_full_name=["Max Quibble", "Finn Tickle"],
    subject_id="664484",
    session_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0, tzinfo=timezone.utc),
    session_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
    session_type="Receptive field mapping",
    iacuc_protocol="2109",
    rig_id="323_EPHYS2-RF_2023-04-24_01",
    active_mouse_platform=False,
    mouse_platform_name="mouse platform",
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_name="Visual Stimulation",
            stimulus_modalities=[StimulusModality.VISUAL],
            stimulus_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stimulus_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=10, second=0, tzinfo=timezone.utc),
            software=[
                Software(
                    name="Bonsai",
                    version="2.7",
                    url="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                )
            ],
            stimulus_parameters=[
                VisualStimulation(
                    stimulus_name="Static Gratings",
                    stimulus_parameters={
                        "grating_orientations": [0, 45, 90, 135],
                        "grating_orientation_unit": "degrees",
                        "grating_spatial_frequencies": [0.02, 0.04, 0.08, 0.16, 0.32],
                        "grating_spatial_frequency_unit": "cycles/degree",
                    },
                )
            ],
        ),
        StimulusEpoch(
            stimulus_name="Visual Stimulation",
            stimulus_modalities=[StimulusModality.VISUAL],
            stimulus_start_time=datetime(year=2023, month=4, day=25, hour=3, minute=10, second=0, tzinfo=timezone.utc),
            stimulus_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
            software=[
                Software(
                    name="Bonsai",
                    version="2.7",
                    url="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                )
            ],
            stimulus_parameters=[
                VisualStimulation(
                    stimulus_name="Flashes",
                    stimulus_parameters={
                        "flash_interval": 5.0,
                        "flash_interval_unit": "seconds",
                        "flash_duration": 0.5,
                        "flash_duration_unit": "seconds",
                    },
                )
            ],
        ),
    ],
    data_streams=[
        Stream(
            stream_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stream_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
            stream_modalities=[Modality.ECEPHYS],
            daq_names=["Basestation"],
            camera_names=["some_camera_name"],
            stick_microscopes=[
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 1",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="did not record angles, did not calibrate.",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 2",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 3",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 4",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
            ],
            ephys_modules=[
                ManipulatorModule(
                    targeted_ccf_coordinates=[
                        CcfCoords(ml=8150, ap=3250, dv=7800),
                    ],
                    assembly_name="ephys module 1",
                    arc_angle=5.2,
                    module_angle=8,
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording"
                        " with a sudden shift in signals. Lots of motion. Maybe some implant motion."
                    ),
                ),
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=25,
                    module_angle=-22,
                    targeted_ccf_coordinates=[CcfCoords(ml=6637.28, ap=4265.02, dv=10707.35)],
                    assembly_name="ephys module 2",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
                    primary_targeted_structure="LC",
                    manipulator_coordinates=Coordinates3d(x=9015, y=7144, z=13262),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Trouble penetrating. Lots of compression, needed to move probe. Small amount of surface"
                        " bleeding/bruising. Initial Target: X;10070.3\tY:7476.6"
                    ),
                ),
            ],
        ),
        Stream(
            stream_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0, tzinfo=timezone.utc),
            stream_end_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stream_modalities=[Modality.ECEPHYS],
            notes="664484_2023-04-24_20-06-37; Surface Finding",
            daq_names=["Basestation"],
            stick_microscopes=[
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 1",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="did not record angles, did not calibrate.",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 2",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 3",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 4",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
            ],
            manipulator_modules=[
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=5.2,
                    module_angle=8,
                    targeted_ccf_coordinates=[CcfCoords(ml=8150, ap=3250, dv=7800)],
                    assembly_name="ephys module 1",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording"
                        " with a sudden shift in signals. Lots of motion. Maybe some implant motion."
                    ),
                ),
            ],
            ephys_modules=[
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=5.2,
                    module_angle=8,
                    targeted_ccf_coordinates=[CcfCoords(ml=8150, ap=3250, dv=7800)],
                    assembly_name="ephys module 1",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording"
                        " with a sudden shift in signals. Lots of motion. Maybe some implant motion."
                    ),
                ),
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=25,
                    module_angle=-22,
                    targeted_ccf_coordinates=[CcfCoords(ml=6637.28, ap=4265.02, dv=10707.35)],
                    assembly_name="ephys module 2",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
                    primary_targeted_structure="LC",
                    manipulator_coordinates=Coordinates3d(x=9015, y=7144, z=13262),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Trouble penetrating. Lots of compression, needed to move probe. Small amount of surface"
                        " bleeding/bruising. Initial Target: X;10070.3\tY:7476.6"
                    ),
                ),
            ],
        ),
    ],
)


class TestRigSessionCompatibility(unittest.TestCase):
    """Tests RigSessionCompatibility class"""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class by reading in json files"""

        def read_json(filepath: Path) -> dict:
            """Small util method"""
            with open(filepath, "r") as f:
                contents = json.load(f)
            return contents

        cls.example_ephys_rig = Rig.model_validate_json(json.dumps(read_json(EPHYS_RIG_JSON)))
        cls.example_ephys_session = Session.model_validate_json(json.dumps(read_json(EPHYS_SESSION_JSON)))
        cls.ophys_rig = r.Rig(
            rig_id="428_FIP1_20231003",
            modification_date=date(2023, 10, 3),
            modalities=[Modality.FIB],
            cameras=[
                d.CameraAssembly(
                    name="BehaviorVideography_FaceSide",
                    camera_target=d.CameraTarget.FACE_SIDE_LEFT,
                    camera=d.Camera(
                        name="Side face camera",
                        detector_type="Camera",
                        serial_number="TBD",
                        manufacturer=d.Organization.AILIPU,
                        model="ELP-USBFHD05MT-KL170IR",
                        notes="The light intensity sensor was removed; IR illumination is constantly on",
                        data_interface="USB",
                        computer_name="W10DTJK7N0M3",
                        frame_rate=120,
                        sensor_width=640,
                        sensor_height=480,
                        chroma="Color",
                        cooling="Air",
                        bin_mode="Additive",
                        recording_software=d.Software(name="Bonsai", version="2.5"),
                    ),
                    lens=d.Lens(
                        name="Xenocam 1",
                        model="XC0922LENS",
                        serial_number="unknown",
                        manufacturer=d.Organization.OTHER,
                        max_aperture="f/1.4",
                        notes='Focal Length 9-22mm 1/3" IR F1.4',
                    ),
                ),
                d.CameraAssembly(
                    name="BehaviorVideography_FaceBottom",
                    camera_target=d.CameraTarget.FACE_BOTTOM,
                    camera=d.Camera(
                        name="Bottom face Camera",
                        detector_type="Camera",
                        serial_number="TBD",
                        manufacturer=d.Organization.AILIPU,
                        model="ELP-USBFHD05MT-KL170IR",
                        notes="The light intensity sensor was removed; IR illumination is constantly on",
                        data_interface="USB",
                        computer_name="W10DTJK7N0M3",
                        frame_rate=120,
                        sensor_width=640,
                        sensor_height=480,
                        chroma="Color",
                        cooling="Air",
                        bin_mode="Additive",
                        recording_software=d.Software(name="Bonsai", version="2.5"),
                    ),
                    lens=d.Lens(
                        name="Xenocam 2",
                        model="XC0922LENS",
                        serial_number="unknown",
                        manufacturer=d.Organization.OTHER,
                        max_aperture="f/1.4",
                        notes='Focal Length 9-22mm 1/3" IR F1.4',
                    ),
                ),
            ],
            patch_cords=[
                d.Patch(
                    name="Bundle Branching Fiber-optic Patch Cord",
                    manufacturer=d.Organization.DORIC,
                    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                    core_diameter=200,
                    numerical_aperture=0.37,
                )
            ],
            light_sources=[
                d.LightEmittingDiode(
                    name="470nm LED",
                    manufacturer=d.Organization.THORLABS,
                    model="M470F3",
                    wavelength=470,
                ),
                d.LightEmittingDiode(
                    name="415nm LED",
                    manufacturer=d.Organization.THORLABS,
                    model="M415F3",
                    wavelength=415,
                ),
                d.LightEmittingDiode(
                    name="565nm LED",
                    manufacturer=d.Organization.THORLABS,
                    model="M565F3",
                    wavelength=565,
                ),
            ],
            detectors=[
                d.Detector(
                    name="Green CMOS",
                    serial_number="21396991",
                    manufacturer=d.Organization.FLIR,
                    model="BFS-U3-20S40M",
                    detector_type="Camera",
                    data_interface="USB",
                    cooling="Air",
                    immersion="air",
                    bin_width=4,
                    bin_height=4,
                    bin_mode="Additive",
                    crop_width=200,
                    crop_height=200,
                    gain=2,
                    chroma="Monochrome",
                    bit_depth=16,
                ),
                d.Detector(
                    name="Red CMOS",
                    serial_number="21396991",
                    manufacturer=d.Organization.FLIR,
                    model="BFS-U3-20S40M",
                    detector_type="Camera",
                    data_interface="USB",
                    cooling="Air",
                    immersion="air",
                    bin_width=4,
                    bin_height=4,
                    bin_mode="Additive",
                    crop_width=200,
                    crop_height=200,
                    gain=2,
                    chroma="Monochrome",
                    bit_depth=16,
                ),
            ],
            objectives=[
                d.Objective(
                    name="Objective",
                    serial_number="128022336",
                    manufacturer=d.Organization.NIKON,
                    model="CFI Plan Apochromat Lambda D 10x",
                    numerical_aperture=0.45,
                    magnification=10,
                    immersion="air",
                )
            ],
            filters=[
                d.Filter(
                    name="Green emission filter",
                    manufacturer=d.Organization.SEMROCK,
                    model="FF01-520/35-25",
                    filter_type="Band pass",
                    center_wavelength=520,
                    diameter=25,
                ),
                d.Filter(
                    name="Red emission filter",
                    manufacturer=d.Organization.SEMROCK,
                    model="FF01-600/37-25",
                    filter_type="Band pass",
                    center_wavelength=600,
                    diameter=25,
                ),
                d.Filter(
                    name="Emission Dichroic",
                    model="FF562-Di03-25x36",
                    manufacturer=d.Organization.SEMROCK,
                    filter_type="Dichroic",
                    height=25,
                    width=36,
                    cut_off_wavelength=562,
                ),
                d.Filter(
                    name="dual-edge standard epi-fluorescence dichroic beamsplitter",
                    model="FF493/574-Di01-25x36",
                    manufacturer=d.Organization.SEMROCK,
                    notes="493/574 nm BrightLine dual-edge standard epi-fluorescence dichroic beamsplitter",
                    filter_type="Multiband",
                    width=36,
                    height=24,
                ),
                d.Filter(
                    name="Excitation filter 410nm",
                    manufacturer=d.Organization.THORLABS,
                    model="FB410-10",
                    filter_type="Band pass",
                    diameter=25,
                    center_wavelength=410,
                ),
                d.Filter(
                    name="Excitation filter 470nm",
                    manufacturer=d.Organization.THORLABS,
                    model="FB470-10",
                    filter_type="Band pass",
                    center_wavelength=470,
                    diameter=25,
                ),
                d.Filter(
                    name="Excitation filter 560nm",
                    manufacturer=d.Organization.THORLABS,
                    model="FB560-10",
                    filter_type="Band pass",
                    diameter=25,
                    center_wavelength=560,
                ),
                d.Filter(
                    name="450 Dichroic Longpass Filter",
                    manufacturer=d.Organization.EDMUND_OPTICS,
                    model="#69-898",
                    filter_type="Dichroic",
                    cut_off_wavelength=450,
                    width=35.6,
                    height=25.2,
                ),
                d.Filter(
                    name="500 Dichroic Longpass Filter",
                    manufacturer=d.Organization.EDMUND_OPTICS,
                    model="#69-899",
                    filter_type="Dichroic",
                    cut_off_wavelength=500,
                    width=35.6,
                    height=23.2,
                ),
            ],
            lenses=[
                d.Lens(
                    manufacturer=d.Organization.THORLABS,
                    model="AC254-080-A-ML",
                    name="Image focusing lens",
                    focal_length=80,
                    size=1,
                )
            ],
            daqs=[
                d.HarpDevice(
                    name="Harp Behavior",
                    harp_device_type=d.HarpDeviceType.BEHAVIOR,
                    core_version="2.1",
                    computer_name="behavior_computer",
                    is_clock_generator=False,
                    channels=[
                        d.DAQChannel(channel_name="DO0", device_name="Solenoid Left", channel_type="Digital Output"),
                        d.DAQChannel(channel_name="DO1", device_name="Solenoid Right", channel_type="Digital Output"),
                        d.DAQChannel(
                            channel_name="DI0", device_name="Janelia_Lick_Detector Left", channel_type="Digital Input"
                        ),
                        d.DAQChannel(
                            channel_name="DI1", device_name="Janelia_Lick_Detector Right", channel_type="Digital Input"
                        ),
                        d.DAQChannel(channel_name="DI3", device_name="Photometry Clock", channel_type="Digital Input"),
                    ],
                )
            ],
            mouse_platform=d.Disc(name="mouse_disc", radius=8.5),
            stimulus_devices=[
                d.RewardDelivery(
                    reward_spouts=[
                        d.RewardSpout(
                            name="Left spout",
                            side=d.SpoutSide.LEFT,
                            spout_diameter=1.2,
                            solenoid_valve=d.Device(device_type="Solenoid", name="Solenoid Left"),
                            lick_sensor=d.Device(
                                name="Janelia_Lick_Detector Left",
                                device_type="Lick detector",
                                manufacturer=d.Organization.JANELIA,
                            ),
                            lick_sensor_type=d.LickSensorType("Capacitive"),
                        ),
                        d.RewardSpout(
                            name="Right spout",
                            side=d.SpoutSide.RIGHT,
                            spout_diameter=1.2,
                            solenoid_valve=d.Device(device_type="Solenoid", name="Solenoid Right"),
                            lick_sensor=d.Device(
                                name="Janelia_Lick_Detector Right",
                                device_type="Lick detector",
                                manufacturer=d.Organization.JANELIA,
                            ),
                            lick_sensor_type=d.LickSensorType("Capacitive"),
                        ),
                    ],
                ),
            ],
            additional_devices=[d.Device(device_type="Photometry Clock", name="Photometry Clock")],
            calibrations=[
                d.Calibration(
                    calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
                    device_name="470nm LED",
                    description="LED calibration",
                    input={"Power setting": [1, 2, 3]},
                    output={"Power mW": [5, 10, 13]},
                )
            ],
        )
        cls.ophys_session = Session(
            experimenter_full_name=["John Doe"],
            session_start_time=datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc),
            session_end_time=datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc),
            subject_id="652567",
            session_type="Parameter Testing",
            iacuc_protocol="2115",
            rig_id="ophys_rig",
            mouse_platform_name="Disc",
            active_mouse_platform=False,
            data_streams=[
                Stream(
                    stream_start_time=datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc),
                    stream_end_time=datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc),
                    stream_modalities=[Modality.FIB],
                    light_sources=[
                        LaserConfig(
                            name="Laser A",
                            wavelength=405,
                            wavelength_unit="nanometer",
                            excitation_power=10,
                            excitation_power_unit="milliwatt",
                        ),
                        LaserConfig(
                            name="Laser B",
                            wavelength=473,
                            wavelength_unit="nanometer",
                            excitation_power=7,
                            excitation_power_unit="milliwatt",
                        ),
                    ],
                    detectors=[DetectorConfig(name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal")],
                    fiber_modules=[
                        FiberModule(
                            assembly_name="Fiber Module A",
                            arc_angle=30,
                            module_angle=180,
                            primary_targeted_structure="Structure A",
                            manipulator_coordinates=Coordinates3d(x=30.5, y=70, z=180),
                        )
                    ],
                    fiber_connections=[
                        FiberConnectionConfig(
                            patch_cord_name="Patch Cord A",
                            patch_cord_output_power=40,
                            output_power_unit="microwatt",
                            fiber_name="Fiber A",
                        ),
                        FiberConnectionConfig(
                            patch_cord_name="Patch Cord B",
                            patch_cord_output_power=43,
                            output_power_unit="microwatt",
                            fiber_name="Fiber B",
                        ),
                    ],
                    notes="Internal trigger. GRAB-DA2m shows signal. Unclear about GRAB-rAC",
                )
            ],
            stimulus_epochs=[
                StimulusEpoch(
                    stimulus_start_time=datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc),
                    stimulus_end_time=datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc),
                    stimulus_name="Some Stimulus Name",
                    stimulus_modalities=[StimulusModality.AUDITORY],
                    stimulus_device_names=["Stimulus Device A", "Stimulus Device B"],
                )
            ],
        )

    def test_run_compatibility_check(self):
        """Tests compatibility check"""
        expected_error = "Rig ID in session 323_EPHYS2-RF_2023-04-24_01 does not match the rig's 323_EPHYS1_20231003."
        with self.assertRaises(ValueError) as context:
            RigSessionCompatibility(rig=ephys_rig, session=ephys_session).run_compatibility_check()
        self.assertIn(expected_error, str(context.exception))

        with self.assertRaises(ValueError):
            RigSessionCompatibility(rig=self.ophys_rig, session=self.ophys_session).run_compatibility_check()

    def test_check_examples_compatibility(self):
        """Tests that examples are compatible"""
        # check that ephys session and rig are synced
        example_ephys_check = RigSessionCompatibility(rig=self.example_ephys_rig, session=self.example_ephys_session)
        self.assertIsNone(example_ephys_check.run_compatibility_check())


if __name__ == "__main__":
    unittest.main()
