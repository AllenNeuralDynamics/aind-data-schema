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
    Microscope,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OlfactometerChannel,
    OlfactometerChannelType,
    ScanningStage,
)
from aind_data_schema.components.connections import Connection
from aind_data_schema.components.measurements import Calibration
from aind_data_schema.core.instrument import (
    DEVICES_REQUIRED,
    Instrument,
)
from examples.ephys_instrument import inst as ephys_instrument

computer_foo = Computer(name="foo")
computer_ASDF = Computer(name="ASDF")
computer_W10XXX000 = Computer(name="W10XXX000")

microscope = Microscope(
    name="Microscope A",
)

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
        source_device="Neuropixels basestation",
        source_port="123",
        target_device="Laser A",
    ),
    Connection(
        source_device="Neuropixels basestation",
        source_port="321",
        target_device="Probe A",
    ),
    Connection(
        source_device="Neuropixels basestation",
        source_port="234",
        target_device="Camera A",
    ),
    Connection(
        source_device="Neuropixels basestation",
        source_port="2354",
        target_device="Disc A",
    ),
    Connection(
        source_device="Neuropixels basestation",
        target_device="foo",
    ),
    Connection(
        source_device="cam",
        target_device="ASDF",
    ),
    Connection(
        source_device="Neuropixels basestation",
        target_device="foo",
    ),
    Connection(
        source_device="Camera A",
        target_device="ASDF",
    ),
    Connection(
        source_device="Olfactometer",
        target_device="W10XXX000",
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
        lens=Lens(name="Camera lens", manufacturer=Organization.OTHER, notes="Manufacturer unknown"),
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
            notes="Manufacturer unknown",
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
    line_shear_unit=SizeUnit.PX,
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
            notes="Manufacturer unknown",
        ),
        target=CameraTarget.BRAIN,
        relative_position=[AnatomicalRelative.SUPERIOR],
        lens=Lens(name="Lens A", manufacturer=Organization.OTHER, notes="Manufacturer unknown"),
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

        self.assertIsNotNone(ephys_instrument)

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
                        source_device="Olfactometer",
                        target_device="Laser A",
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
                    source_device="Olfactometer",
                    target_device="Laser A",
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
                        source_device="Not a real device",
                        target_device="Neuropixels basestation",
                    )
                ],
            )

        self.assertIn("Device name validation error: 'Not a real device'", str(context.exception))

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
                        target_device="Not a real device",
                        source_device="Neuropixels basestation",
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
        for modality_abbreviation, _ in DEVICES_REQUIRED.items():

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
                    microscope,
                ],
                calibrations=[],
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

        camera = Camera(
            name="Camera A",
            detector_type=DetectorType.CAMERA,
            manufacturer=Organization.OTHER,
            data_interface="USB",
            frame_rate=144,
            frame_rate_unit=FrequencyUnit.HZ,
            sensor_width=1,
            sensor_height=1,
            chroma="Color",
            notes="Manufacturer unknown",
        )

        # Create a matching CameraAssembly
        camera_assembly = CameraAssembly(
            name="Assembly A",
            camera=camera,
            target=CameraTarget.BRAIN,
            relative_position=[AnatomicalRelative.SUPERIOR],
            lens=Lens(name="Lens A", manufacturer=Organization.OTHER, notes="Manufacturer unknown"),
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
                camera_assembly,
                computer_ASDF,
            ],
            calibrations=[],
            connections=[
                Connection(
                    source_device="Camera A",
                    target_device="ASDF",
                )
            ],
        )
        self.assertIsNotNone(inst)

    def test_instrument_addition(self):
        """Test the __add__ method of Instrument"""

        # Create a copy of the ephys_instrument for testing
        inst1 = ephys_instrument.model_copy(deep=True)
        inst2 = ephys_instrument.model_copy(deep=True)

        # Test successful addition
        combined = inst1 + inst2

        # Verify the combined instrument has the expected properties
        self.assertEqual(combined.instrument_id, inst1.instrument_id)
        self.assertEqual(combined.location, inst1.location)
        self.assertEqual(combined.coordinate_system, inst1.coordinate_system)
        self.assertEqual(combined.temperature_control, inst1.temperature_control)

        # Check that modalities are combined and sorted (should be the same since we're adding identical instruments)
        self.assertEqual(len(combined.modalities), len(set(inst1.modalities + inst2.modalities)))

        # Check that components are combined
        self.assertEqual(len(combined.components), len(inst1.components) + len(inst2.components))

        # Check that connections are combined
        self.assertEqual(len(combined.connections), len(inst1.connections) + len(inst2.connections))

        # Check that calibrations are combined (if they exist)
        expected_calibrations_len = len(inst1.calibrations or []) + len(inst2.calibrations or [])
        actual_calibrations_len = len(combined.calibrations or [])
        self.assertEqual(actual_calibrations_len, expected_calibrations_len)

        # Test incompatible schema versions
        inst1_orig_schema_v = inst1.schema_version
        inst1.schema_version = "0.1.0"

        with self.assertRaises(ValueError) as context:
            inst1 + inst2
        self.assertIn("Cannot combine Instrument objects with different schema versions", str(context.exception))

        # Restore schema version for next tests
        inst1.schema_version = inst1_orig_schema_v

        # Test incompatible instrument IDs
        inst2.instrument_id = "different_instrument_id"
        with self.assertRaises(ValueError) as context:
            inst1 + inst2
        self.assertIn("Cannot combine Instrument objects that differ in key fields", str(context.exception))

        # Test incompatible locations
        inst2.instrument_id = inst1.instrument_id  # Reset to same
        inst2.location = "Different Location"
        with self.assertRaises(ValueError) as context:
            inst1 + inst2
        self.assertIn("Cannot combine Instrument objects that differ in key fields", str(context.exception))

        # Test notes combination
        inst2.location = inst1.location  # Reset to same
        inst1.notes = "First note"
        inst2.notes = "Second note"
        combined = inst1 + inst2
        self.assertIn("First note", combined.notes)
        self.assertIn("Second note", combined.notes)
        self.assertIn("\n", combined.notes)  # Should be joined with newline

        # Test notes combination with None values
        inst1.notes = "Only note"
        inst2.notes = None
        combined = inst1 + inst2
        self.assertEqual(combined.notes, "Only note")

        inst1.notes = None
        inst2.notes = "Only note"
        combined = inst1 + inst2
        self.assertEqual(combined.notes, "Only note")


class ConnectionTest(unittest.TestCase):
    """Test the Connection schema"""

    def test_connection(self):
        """Test the Connection schema"""

        connection = Connection(
            source_device="Neuropixels basestation",
            source_port="123",
            target_device="Laser A",
        )
        self.assertIsNotNone(connection)

        # Test that a simple connection with valid structure is created successfully
        simple_connection = Connection(
            source_device="Camera A",
            target_device="Invalid Target",
        )
        self.assertIsNotNone(simple_connection)

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
