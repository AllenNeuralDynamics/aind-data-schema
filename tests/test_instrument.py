""" test Rig """

from decimal import Decimal
import json
import unittest
from datetime import date, datetime

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit
from pydantic import ValidationError
from pydantic_core import PydanticSerializationError

from aind_data_schema.components.devices import (
    Calibration,
    Camera,
    CameraAssembly,
    CameraTarget,
    ChannelType,
    DAQChannel,
    Detector,
    DetectorType,
    Device,
    Disc,
    EphysAssembly,
    EphysProbe,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    NeuropixelsBasestation,
    Olfactometer,
    OlfactometerChannel,
    Patch,
)
from aind_data_schema.core.instrument import Instrument

daqs = [
    NeuropixelsBasestation(
        name="Neuropixels basestation",
        basestation_firmware_version="1",
        bsc_firmware_version="2",
        slot=0,
        manufacturer=Organization.IMEC,
        ports=[],
        computer_name="foo",
        channels=[
            DAQChannel(
                channel_name="123",
                device_name="Laser A",
                channel_type="Analog Output",
            ),
            DAQChannel(
                channel_name="321",
                device_name="Probe A",
                channel_type="Analog Output",
            ),
            DAQChannel(
                channel_name="234",
                device_name="Camera A",
                channel_type="Digital Output",
            ),
            DAQChannel(
                channel_name="2354",
                device_name="Disc A",
                channel_type="Digital Output",
            ),
        ],
    )
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
        fiber=Patch(
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
        camera_target="Face bottom",
        lens=Lens(name="Camera lens", manufacturer=Organization.OTHER),
        camera=Camera(
            name="Camera A",
            detector_type=DetectorType.CAMERA,
            manufacturer=Organization.OTHER,
            data_interface="USB",
            computer_name="ASDF",
            frame_rate=144,
            frame_rate_unit=FrequencyUnit.HZ,
            sensor_width=1,
            sensor_height=1,
            chroma="Color",
        ),
    )
]
stick_microscopes = [
    CameraAssembly(
        name="Assembly A",
        camera=Camera(
            name="Camera A",
            detector_type=DetectorType.CAMERA,
            manufacturer=Organization.OTHER,
            data_interface="USB",
            computer_name="ASDF",
            frame_rate=144,
            frame_rate_unit=FrequencyUnit.HZ,
            sensor_width=1,
            sensor_height=1,
            chroma="Color",
        ),
        camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS A VALUE
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
    Patch(
        name="Bundle Branching Fiber-optic Patch Cord",
        manufacturer=Organization.DORIC,
        model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
        core_diameter=200,
        numerical_aperture=0.37,
    )
]
stimulus_devices = [
    Olfactometer(
        name="Olfactometer",
        manufacturer=Organization.CHAMPALIMAUD,
        model="1234",
        harp_device_type="1234",
        serial_number="213456",
        hardware_version="1",
        is_clock_generator=False,
        computer_name="W10XXX000",
        channels=[
            OlfactometerChannel(
                channel_index=0,
                channel_type=ChannelType.CARRIER,
                flow_capacity=100,
            ),
            OlfactometerChannel(
                channel_index=1,
                channel_type=ChannelType.ODOR,
                flow_capacity=100,
            ),
        ],
    )
]
calibration = Calibration(
    calibration_date=date(2020, 10, 10),
    device_name="Laser A",
    description="Laser power calibration",
    input={"power percent": [10, 40, 80]},
    output={"power mW": [2, 6, 10]},
)


class RigTests(unittest.TestCase):
    """test rig schemas"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(ValidationError):
            Instrument()

        inst = Instrument(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            modalities=[Modality.ECEPHYS, Modality.FIB],
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
            ],
            mouse_platform=Disc(name="Disc A", radius=1),
            calibrations=[
                Calibration(
                    calibration_date=date(2020, 10, 10),
                    device_name="Laser A",
                    description="Laser power calibration",
                    input={"power percent": [10, 40, 80]},
                    output={"power mW": [2, 6, 10]},
                )
            ],
        )

        assert rig is not None

    def test_validator(self):
        """Test the rig file validators"""
        neuropixels_base = NeuropixelsBasestation(
            name="Basestation",
            basestation_firmware_version="1",
            bsc_firmware_version="2",
            slot=0,
            manufacturer=Organization.IMEC,
            ports=[],
            computer_name="foo",
            channels=[
                DAQChannel(
                    channel_name="123",
                    device_name="Laser A",
                    channel_type="Analog Output",
                ),
                DAQChannel(
                    channel_name="321",
                    device_name="Probe A",
                    channel_type="Analog Output",
                ),
                DAQChannel(
                    channel_name="234",
                    device_name="Camera A",
                    channel_type="Digital Output",
                ),
                DAQChannel(
                    channel_name="2354",
                    device_name="Disc A",
                    channel_type="Digital Output",
                ),
            ],
        )

        # A Rig model with ECEPHYS in the modality list requires
        # ephys_assemblies and stick microscopes
        with self.assertRaises(ValidationError):
            Instrument(
                modalities=[
                    Modality.ECEPHYS,
                    Modality.SLAP,
                    Modality.FIB,
                    Modality.BEHAVIOR_VIDEOS,
                    Modality.POPHYS,
                    Modality.BEHAVIOR,
                ],
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                components=[
                    neuropixels_base,
                ],
                calibrations=[
                    Calibration(
                        calibration_date=date(2020, 10, 10),
                        device_name="Laser A",
                        description="Laser power calibration",
                        input={"power percent": [10, 40, 80]},
                        output={"power mW": [2, 6, 10]},
                    )
                ],
                mouse_platform=Disc(name="Disc A", radius=1),
            )

        with self.assertRaises(ValidationError):
            daqs = [
                NeuropixelsBasestation(
                    name="Basestation",
                    basestation_firmware_version="1",
                    bsc_firmware_version="2",
                    slot=0,
                    manufacturer=Organization.IMEC,
                    ports=[],
                    computer_name="foo",
                    channels=[
                        DAQChannel(
                            channel_name="123",
                            device_name="Laser A",
                            channel_type="Analog Output",
                        ),
                        DAQChannel(
                            channel_name="321",
                            device_name="Probe A",
                            channel_type="Analog Output",
                        ),
                        DAQChannel(
                            channel_name="234",
                            device_name="Camera A",
                            channel_type="Digital Output",
                        ),
                        DAQChannel(
                            channel_name="2354",
                            device_name="Disc A",
                            channel_type="Digital Output",
                        ),
                    ],
                )
            ]

            Instrument(
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=datetime.now(),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                components=[*daqs],
            )

        with self.assertRaises(ValueError):
            Instrument(
                instrument_id="1234",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
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
                ],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[
                    Calibration(
                        calibration_date=date(2020, 10, 10),
                        device_name="Laser A",
                        description="Laser power calibration",
                        input={"power percent": [10, 40, 80]},
                        output={"power mW": [2, 6, 10]},
                    )
                ],
            )

        # Tests that validators catch empty lists without KeyErrors
        with self.assertRaises(ValidationError):
            Instrument(
                instrument_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                components=[],
                mouse_platform=Disc(name="Disc A", radius=Decimal(1.0)),
                calibrations=[],
            )

        # What is this testing?
        with self.assertRaises(ValidationError):
            Instrument(
                instrument_id="123_EPHYS-OPTO_20200101",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
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
                ],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[
                    Calibration(
                        calibration_date=date(2020, 10, 10),
                        device_name="Laser A",
                        description="Laser power calibration",
                        input={"power percent": [10, 40, 80]},
                        output={"power mW": [2, 6, 10]},
                    )
                ],
            )

    def test_instrument_id_validator(self):
        """Tests that instrument_id validator works as expected"""

        with self.assertRaises(ValidationError):
            Instrument(
                instrument_id="123",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
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
                ],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[calibration],
            )
        with self.assertRaises(ValidationError):
            Instrument(
                instrument_id="123_EPHYS-OPTO_2020-01-01",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
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
                ],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[calibration],
            )

    def test_serialize_modalities(self):
        """Tests that modalities serializer can handle different types"""
        expected_modalities = [{"name": "Extracellular electrophysiology", "abbreviation": "ecephys"}]
        # Case 1: Modality is a class instance
        instrument_instance_modality = Instrument.model_construct(
            instrument_id="123_EPHYS1-OPTO_20220101",
            modalities={Modality.ECEPHYS},  # Example with a valid Modality instance
        )
        instrument_json = instrument_instance_modality.model_dump_json()
        instrument_data = json.loads(instrument_json)
        self.assertEqual(instrument_data["modalities"], expected_modalities)

        # Case 2: Modality is a dictionary when Rig is constructed from JSON
        instrument_dict_modality = Instrument.model_construct(**instrument_data)
        instrument_dict_json = instrument_dict_modality.model_dump_json()
        instrument_dict_data = json.loads(instrument_dict_json)
        self.assertEqual(instrument_dict_data["modalities"], expected_modalities)

        # Case 3: Modality is an unknown type
        with self.assertRaises(PydanticSerializationError) as context:
            instrument_unknown_modality = Instrument.model_construct(modalities={"UnknownModality"})

            instrument_unknown_modality.model_dump_json()
        self.assertIn("Error calling function `serialize_modalities`", str(context.exception))


if __name__ == "__main__":
    unittest.main()
