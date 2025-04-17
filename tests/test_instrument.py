""" test Instrument """

import json
import unittest
from datetime import date

from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, PowerUnit, SizeUnit
from pydantic import ValidationError

from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.devices import (
    Camera,
    CameraAssembly,
    CameraTarget,
    Computer,
    DAQChannel,
    Detector,
    DetectorType,
    Device,
    DigitalMicromirrorDevice,
    Disc,
    EphysAssembly,
    EphysProbe,
    FiberPatchCord,
    Laser,
    LaserAssembly,
    Lens,
    LickSpout,
    LickSpoutAssembly,
    Manipulator,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OlfactometerChannel,
    OlfactometerChannelType,
    ScanningStage,
)
from aind_data_schema.components.measurements import Calibration
from aind_data_schema.core.instrument import (
    DEVICES_REQUIRED,
    Connection,
    ConnectionData,
    ConnectionDirection,
    Instrument,
)

computer_foo = Computer(name="foo")
computer_ASDF = Computer(name="ASDF")
computer_W10XXX000 = Computer(name="W10XXX000")

daqs = [
    NeuropixelsBasestation(
        name="Neuropixels basestation",
        basestation_firmware_version="1",
        bsc_firmware_version="2",
        slot=0,
        manufacturer=Organization.IMEC,
        ports=[],
        channels=[
            DAQChannel(
                channel_name="123",
                channel_type="Analog Output",
            ),
            DAQChannel(
                channel_name="321",
                channel_type="Analog Output",
            ),
            DAQChannel(
                channel_name="234",
                channel_type="Digital Output",
            ),
            DAQChannel(
                channel_name="2354",
                channel_type="Digital Output",
            ),
        ],
    )
]

connections = [
    Connection(
        device_names=["Laser A", "Neuropixels basestation"],
        connection_data={
            "Neuropixels basestation": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="123",
            ),
            "Laser A": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Probe A", "Neuropixels basestation"],
        connection_data={
            "Neuropixels basestation": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="321",
            ),
            "Probe A": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Camera A", "Neuropixels basestation"],
        connection_data={
            "Neuropixels basestation": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="234",
            ),
            "Camera A": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Disc A", "Neuropixels basestation"],
        connection_data={
            "Neuropixels basestation": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="2354",
            ),
            "Disc A": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Neuropixels basestation", "foo"],
        connection_data={
            "Neuropixels basestation": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "foo": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["cam", "ASDF"],
        connection_data={
            "cam": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "ASDF": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Neuropixels basestation", "foo"],
        connection_data={
            "Neuropixels basestation": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "foo": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Camera A", "ASDF"],
        connection_data={
            "Camera A": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "ASDF": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Olfactometer", "W10XXX000"],
        connection_data={
            "Olfactometer": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "W10XXX000": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
]

ems = [
    EphysAssembly(
        probes=[EphysProbe(probe_model="Neuropixels 1.0", name="Probe A")],
        manipulator=Manipulator(
            name="Probe manipulator",
            manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
            serial_number="4321",
        ),
        name="Ephys_assemblyA",
    )
]

laser = Laser(
    manufacturer=Organization.HAMAMATSU,
    serial_number="1234",
    name="Laser A",
    wavelength=488,
)

lms = [
    LaserAssembly(
        lasers=[
            Laser(
                manufacturer=Organization.HAMAMATSU,
                serial_number="1234",
                name="Laser A",
                wavelength=488,
            ),
        ],
        manipulator=Manipulator(
            name="Laser manipulator",
            manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
            serial_number="1234",
        ),
        name="Laser_assembly",
        collimator=Device(name="Collimator A"),
        fiber=FiberPatchCord(
            name="Bundle Branching Fiber-optic Patch Cord",
            manufacturer=Organization.DORIC,
            model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
            core_diameter=200,
            numerical_aperture=0.37,
        ),
    )
]
cameras = [
    CameraAssembly(
        name="cam",
        target=CameraTarget.FACE,
        relative_position=[AnatomicalRelative.ANTERIOR, AnatomicalRelative.INFERIOR],
        lens=Lens(name="Camera lens", manufacturer=Organization.OTHER),
        camera=Camera(
            name="Camera A",
            detector_type=DetectorType.CAMERA,
            manufacturer=Organization.OTHER,
            data_interface="USB",
            frame_rate=144,
            frame_rate_unit=FrequencyUnit.HZ,
            sensor_width=1,
            sensor_height=1,
            chroma="Color",
        ),
    )
]
scan_stage = ScanningStage(
    name="Sample stage Z",
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Detection axis",
    stage_axis_name="Z",
    travel=50,
)

# Example of a DigitalMicromirrorDevice
dmd = DigitalMicromirrorDevice(
    name="Example DMD",
    max_dmd_patterns=1024,
    double_bounce_design=True,
    invert_pixel_values=False,
    motion_padding_x=10,
    motion_padding_y=10,
    padding_unit=SizeUnit.PX,
    pixel_size=13.68,
    pixel_size_unit=SizeUnit.UM,
    start_phase=0.5,
    dmd_flip=True,
    dmd_curtain=[0.1, 0.2, 0.3],
    dmd_curtain_unit=SizeUnit.PX,
    line_shear=[1, 2, 3],
    line_shear_units=SizeUnit.PX,
)

stick_microscopes = [
    CameraAssembly(
        name="Assembly A",
        camera=Camera(
            name="Camera A",
            detector_type=DetectorType.CAMERA,
            manufacturer=Organization.OTHER,
            data_interface="USB",
            frame_rate=144,
            frame_rate_unit=FrequencyUnit.HZ,
            sensor_width=1,
            sensor_height=1,
            chroma="Color",
        ),
        target=CameraTarget.BRAIN,
        relative_position=[AnatomicalRelative.SUPERIOR],
        lens=Lens(name="Lens A", manufacturer=Organization.OTHER),
    )
]
light_sources = [
    Laser(
        manufacturer=Organization.HAMAMATSU,
        serial_number="1234",
        name="Laser A",
        wavelength=488,
    )
]
detectors = [
    Detector(
        name="FLIR CMOS for Green Channel",
        serial_number="21396991",
        manufacturer=Organization.FLIR,
        model="BFS-U3-20S40M",
        detector_type=DetectorType.CAMERA,
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
    )
]
patch_cords = [
    FiberPatchCord(
        name="Bundle Branching Fiber-optic Patch Cord",
        manufacturer=Organization.DORIC,
        model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
        core_diameter=200,
        numerical_aperture=0.37,
    )
]
objectives = [
    Objective(
        name="TLX Objective 1",
        numerical_aperture=0.2,
        magnification=3.6,
        manufacturer=Organization.LIFECANVAS,
        immersion="multi",
        notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
    )
]
stimulus_devices = [
    Olfactometer(
        name="Olfactometer",
        manufacturer=Organization.CHAMPALIMAUD,
        model="1234",
        serial_number="213456",
        hardware_version="1",
        is_clock_generator=False,
        channels=[
            OlfactometerChannel(
                channel_index=0,
                channel_type=OlfactometerChannelType.CARRIER,
                flow_capacity=100,
            ),
            OlfactometerChannel(
                channel_index=1,
                channel_type=OlfactometerChannelType.ODOR,
                flow_capacity=100,
            ),
        ],
    ),
    LickSpoutAssembly(
        name="Lick spout assembly",
        lick_spouts=[
            LickSpout(
                name="Left spout",
                spout_diameter=1.2,
                solenoid_valve=Device(name="Solenoid Left"),
                lick_sensor=Device(
                    name="Lick-o-meter Left",
                ),
            ),
            LickSpout(
                name="Right spout",
                spout_diameter=1.2,
                solenoid_valve=Device(name="Solenoid Right"),
                lick_sensor=Device(
                    name="Lick-o-meter Right",
                ),
            ),
        ],
    ),
]
calibration = Calibration(
    calibration_date=date(2020, 10, 10),
    device_name="Laser A",
    description="Laser power calibration",
    input=[10, 40, 80],
    input_unit=PowerUnit.PERCENT,
    output=[2, 6, 10],
    output_unit=PowerUnit.MW,
)


class InstrumentTests(unittest.TestCase):
    """test instrument schemas"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(ValidationError):
            Instrument()

        inst = Instrument(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            modalities=[Modality.ECEPHYS, Modality.FIB],
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            components=[
                *daqs,
                *cameras,
                *stick_microscopes,
                *light_sources,
                *lms,
                laser,
                *ems,
                *detectors,
                *patch_cords,
                *stimulus_devices,
                scan_stage,
                Disc(name="Disc A", radius=1),
                computer_ASDF,
                computer_foo,
                computer_W10XXX000,
            ],
            connections=connections,
            calibrations=[
                Calibration(
                    calibration_date=date(2020, 10, 10),
                    device_name="Laser A",
                    description="Laser power calibration",
                    input=[10, 40, 80],
                    input_unit=PowerUnit.PERCENT,
                    output=[2, 6, 10],
                    output_unit=PowerUnit.MW,
                )
            ],
        )
        self.assertIsNotNone(inst)

    def test_other_camera_target(self):
        """Test that the camera_target being set to Other throws a validation error without notes"""

        camera_no_target = cameras[0].model_copy()
        camera_no_target.target = CameraTarget.OTHER

        with self.assertRaises(ValidationError):
            Instrument(
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
                components=[
                    *daqs,
                    camera_no_target,
                    *stick_microscopes,
                    *light_sources,
                    *lms,
                    *ems,
                    *detectors,
                    *patch_cords,
                    *stimulus_devices,
                    Disc(name="Disc A", radius=1),
                ],
                calibrations=[
                    Calibration(
                        calibration_date=date(2020, 10, 10),
                        device_name="Laser A",
                        description="Laser power calibration",
                        input=[10, 40, 80],
                        input_unit=PowerUnit.PERCENT,
                        output=[2, 6, 10],
                        output_unit=PowerUnit.MW,
                    )
                ],
                connections=[
                    Connection(
                        device_names=["Olfactometer", "Laser A"],
                    )
                ],
            )

        inst = Instrument(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            modalities=[Modality.ECEPHYS, Modality.FIB],
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            components=[
                *daqs,
                camera_no_target,
                *stick_microscopes,
                *light_sources,
                *lms,
                *ems,
                *detectors,
                *patch_cords,
                *stimulus_devices,
                Disc(name="Disc A", radius=1),
            ],
            calibrations=[
                Calibration(
                    calibration_date=date(2020, 10, 10),
                    device_name="Laser A",
                    description="Laser power calibration",
                    input=[10, 40, 80],
                    input_unit=PowerUnit.PERCENT,
                    output=[2, 6, 10],
                    output_unit=PowerUnit.MW,
                )
            ],
            connections=[
                Connection(
                    device_names=["Olfactometer", "Laser A"],
                )
            ],
            notes="Camera target is Other",
        )
        self.assertIsNotNone(inst)

    def test_missing_connections(self):
        """Validation error when connections are missing"""
        with self.assertRaises(ValueError) as context:
            Instrument(
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
                components=[
                    *daqs,
                    *cameras,
                    *stick_microscopes,
                    *light_sources,
                    *lms,
                    *ems,
                    *detectors,
                    *patch_cords,
                    *stimulus_devices,
                    Disc(name="Disc A", radius=1),
                    dmd,
                ],
                calibrations=[
                    Calibration(
                        calibration_date=date(2020, 10, 10),
                        device_name="Laser A",
                        description="Laser power calibration",
                        input=[10, 40, 80],
                        input_unit=PowerUnit.PERCENT,
                        output=[2, 6, 10],
                        output_unit=PowerUnit.MW,
                    )
                ],
                connections=[
                    Connection(
                        device_names=["Not a real device"],
                    )
                ],
            )

        self.assertIn("Device name validation error: 'Not a real device'", str(context.exception))

    def test_validator_modality_device_missing(self):
        """Test that the modality -> device validator throws validation errors when devices are missing"""

        # Mapping is a dictionary of Modality -> List[Device groups]
        for modality_abbreviation, _ in DEVICES_REQUIRED.items():
            with self.assertRaises(ValidationError):
                Instrument(
                    modalities=[Modality.from_abbreviation(modality_abbreviation)],
                    instrument_id="123_EPHYS1-OPTO_20220101",
                    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
                    modification_date=date(2020, 10, 10),
                    components=[],
                    calibrations=[],
                )

    def test_validator_modality_device_present(self):
        """Test that the modality -> device validator does not throw validation errors when devices are present"""

        # Mapping is a dictionary of Modality -> List[Device groups]
        for modality_abbreviation, device_groups in DEVICES_REQUIRED.items():

            inst = Instrument(
                modalities=[Modality.from_abbreviation(modality_abbreviation)],
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
                components=[
                    *daqs,
                    *cameras,
                    *stick_microscopes,
                    *light_sources,
                    *lms,
                    *ems,
                    *detectors,
                    *patch_cords,
                    *stimulus_devices,
                    *objectives,
                    laser,
                    dmd,
                    scan_stage,
                ],
                calibrations=[],
            )
            self.assertIsNotNone(inst)

    def test_validator_notes(self):
        """Test the notes validator"""

        # Test when manufacturer is OTHER and notes are empty
        with self.assertRaises(ValidationError):
            Instrument(
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
                modalities=[Modality.ECEPHYS],
                components=[*daqs, *ems],
                manufacturer=Organization.OTHER,
                notes=None,
            )

        # Test when notes are provided for manufacturer OTHER
        inst = Instrument(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            modalities=[Modality.ECEPHYS],
            components=[*daqs, *ems],
            manufacturer=Organization.OTHER,
            notes="This is a custom manufacturer.",
        )
        self.assertIsNotNone(inst)

    def test_serialize_modalities(self):
        """Tests that modalities serializer can handle different types"""
        expected_modalities = [{"name": "Extracellular electrophysiology", "abbreviation": "ecephys"}]
        # Case 1: Modality is a class instance
        instrument_instance_modality = Instrument.model_construct(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modalities={Modality.ECEPHYS},  # Example with a valid Modality instance
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
        )
        instrument_json = instrument_instance_modality.model_dump_json()
        instrument_data = json.loads(instrument_json)
        self.assertEqual(instrument_data["modalities"], expected_modalities)

        # Case 2: Modality is a dictionary when Instrument is constructed from JSON
        instrument_dict_modality = Instrument.model_construct(**instrument_data)
        instrument_dict_json = instrument_dict_modality.model_dump_json()
        instrument_dict_data = json.loads(instrument_dict_json)
        self.assertEqual(instrument_dict_data["modalities"], expected_modalities)

    def test_coordinate_validator(self):
        """Test the coordinate_validator function"""

        # Create a matching CameraAssembly
        camera = CameraAssembly(
            name="Assembly A",
            camera=Camera(
                name="Camera A",
                detector_type=DetectorType.CAMERA,
                manufacturer=Organization.OTHER,
                data_interface="USB",
                frame_rate=144,
                frame_rate_unit=FrequencyUnit.HZ,
                sensor_width=1,
                sensor_height=1,
                chroma="Color",
            ),
            target=CameraTarget.BRAIN,
            relative_position=[AnatomicalRelative.SUPERIOR],
            lens=Lens(name="Lens A", manufacturer=Organization.OTHER),
        )

        inst = Instrument(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            modalities=[Modality.ECEPHYS, Modality.FIB],
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,  # order is AP, ML, SI
            components=[
                *daqs,
                *cameras,
                *stick_microscopes,
                *light_sources,
                *lms,
                laser,
                *ems,
                *detectors,
                *patch_cords,
                *stimulus_devices,
                scan_stage,
                Disc(name="Disc A", radius=1),
                camera,
                computer_ASDF,
            ],
            calibrations=[],
            connections=[
                Connection(
                    device_names=["Camera A", "ASDF"],
                    connection_data={
                        "Camera A": ConnectionData(
                            direction=ConnectionDirection.SEND,
                        ),
                        "ASDF": ConnectionData(
                            direction=ConnectionDirection.RECEIVE,
                        ),
                    },
                )
            ],
        )
        self.assertIsNotNone(inst)


class ConnectionTest(unittest.TestCase):
    """Test the Connection schema"""

    def test_connection(self):
        """Test the Connection schema"""

        connection = Connection(
            device_names=["Laser A", "Neuropixels basestation"],
            connection_data={
                "Neuropixels basestation": ConnectionData(
                    direction=ConnectionDirection.SEND,
                    port="123",
                ),
                "Laser A": ConnectionData(
                    direction=ConnectionDirection.RECEIVE,
                ),
            },
        )
        self.assertIsNotNone(connection)

        with self.assertRaises(ValidationError) as context:
            Connection(
                device_names=["Camera A", "Neuropixels basestation"],
                connection_data={
                    "Neuropixels basestation": ConnectionData(
                        direction=ConnectionDirection.SEND,
                        port="123",
                    ),
                    "Laser A": ConnectionData(
                        direction=ConnectionDirection.RECEIVE,
                    ),
                    "Camera A": ConnectionData(
                        direction=ConnectionDirection.RECEIVE,
                    ),
                },
            )

        self.assertIn("Connection data key 'Laser A' does not exist", str(context.exception))

    def test_validate_modalities_sorting(self):
        """Test that validate_modalities sorts modalities by their name"""

        # Create unsorted modalities
        unsorted_modalities = [
            Modality.FIB,
            Modality.ECEPHYS,
            Modality.BEHAVIOR_VIDEOS,
        ]

        # Expected sorted modalities
        expected_sorted_modalities = [
            Modality.BEHAVIOR_VIDEOS.abbreviation,
            Modality.ECEPHYS.abbreviation,
            Modality.FIB.abbreviation,
        ]

        # Create an instrument with unsorted modalities
        inst = Instrument(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            modalities=unsorted_modalities,
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            components=[
                *daqs,
                *cameras,
                *stick_microscopes,
                *light_sources,
                *lms,
                laser,
                *ems,
                *detectors,
                *patch_cords,
                *stimulus_devices,
                scan_stage,
                Disc(name="Disc A", radius=1),
                computer_ASDF,
                computer_foo,
                computer_W10XXX000,
            ],
            connections=connections,
            calibrations=[],
        )

        inst_modality_abbr = [modality.abbreviation for modality in inst.modalities]
        # Validate that the modalities are sorted
        self.assertEqual(inst_modality_abbr, expected_sorted_modalities)


if __name__ == "__main__":
    unittest.main()
