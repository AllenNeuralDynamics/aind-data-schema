""" test Imaging """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema.core import acquisition as acq
from aind_data_schema.core import instrument as inst
from aind_data_schema.core import mri_session as ms
from aind_data_schema.core.processing import Registration
from aind_data_schema.imaging import tile
from aind_data_schema.models.devices import Calibration, DAQChannel, DAQDevice
from aind_data_schema.models.manufacturers import Manufacturer
from aind_data_schema.models.units import PowerValue


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            acq.Acquisition()

        a = acq.Acquisition(
            experimenter_full_name=["alice"],
            session_start_time=datetime.datetime.now(),
            specimen_id="12345",
            subject_id="1234",
            instrument_id="1234",
            calibrations=[
                Calibration(
                    calibration_date=datetime.datetime.now(),
                    description="Laser power calibration",
                    device_name="Laser 1",
                    input={"power_setting": PowerValue(value=100.0, unit="percent")},
                    output={"power_measurement": PowerValue(value=50.0, unit="milliwatt")},
                ),
            ],
            session_end_time=datetime.datetime.now(),
            chamber_immersion=acq.Immersion(medium="PBS", refractive_index=1),
            tiles=[
                tile.AcquisitionTile(
                    coordinate_transformations=[
                        tile.Scale3dTransform(scale=[1, 1, 1]),
                        tile.Translation3dTransform(translation=[1, 1, 1]),
                    ],
                    channel=tile.Channel(
                        channel_name="488",
                        light_source_name="Ex_488",
                        filter_names=["Em_600"],
                        detector_name="PMT_1",
                        excitation_wavelength=488,
                        excitation_power=0.1,
                        filter_wheel_index=0,
                    ),
                )
            ],
            axes=[],
        )

        self.assertIsNotNone(a)

        with self.assertRaises(ValidationError):
            inst.Instrument()

        i = inst.Instrument(
            instrument_type="diSPIM",
            modification_date=datetime.datetime.now().date(),
            manufacturer=Manufacturer.LIFECANVAS,
            objectives=[],
            detectors=[],
            light_sources=[],
        )

        self.assertIsNotNone(i)

        with self.assertRaises(ValidationError) as e1:
            inst.Instrument(
                instrument_type="Other",
                modification_date=datetime.datetime(2020, 10, 10, 0, 0, 0).date(),
                manufacturer=Manufacturer.OTHER,
                objectives=[],
                detectors=[],
                light_sources=[],
            )

        expected_exception1 = (
            "1 validation error for Instrument\n"
            "notes\n"
            "  Value error, Notes cannot be empty if instrument_type is Other."
            " Describe the instrument_type in the notes field."
            " [type=value_error, input_value=None, input_type=NoneType]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/value_error"
        )
        self.assertEqual(expected_exception1, repr(e1.exception))

        with self.assertRaises(ValidationError) as e2:
            inst.Instrument(
                instrument_type="diSPIM",
                manufacturer=Manufacturer.OTHER,
                objectives=[],
                detectors=[],
                light_sources=[],
            )

        expected_exception2 = (
            "2 validation errors for Instrument\n"
            "modification_date\n"
            "  Field required [type=missing, input_value={'instrument_type': 'diSP...[],"
            " 'light_sources': []}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "notes\n"
            "  Value error, Notes cannot be empty if manufacturer is Other."
            " Describe the manufacturer in the notes field."
            " [type=value_error, input_value=None, input_type=NoneType]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/value_error"
        )
        self.assertEqual(expected_exception2, repr(e2.exception))

        with self.assertRaises(ValidationError):
            ms.MRIScan(
                scan_sequence_type="Other",
            )

        with self.assertRaises(ValidationError):
            ms.MRIScan(scan_sequence_type="Other", notes="")

        mri = ms.MriSession(
            experimenter_full_name=["Frank Frankson"],
            subject_id="1234",
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            protocol_id="doi_path",
            animal_weight_prior=22.1,
            animal_weight_post=21.9,
            mri_scanner=ms.Scanner(
                name="MRI scanner",
                scanner_location="UW SLU",
                magnetic_strength=7,
                magnetic_strength_unit="T",
            ),
            scans=[
                ms.MRIScan(
                    scan_type="3D Scan",
                    scan_sequence_type="RARE",
                    primary_scan=True,
                    axes=[
                        acq.Axis(
                            name="X",
                            dimension=2,
                            direction="Left_to_right",
                        ),
                        acq.Axis(
                            name="Y",
                            dimension=1,
                            direction="Anterior_to_posterior",
                        ),
                        acq.Axis(
                            name="Z",
                            dimension=0,
                            direction="Inferior_to_superior",
                        ),
                    ],
                    voxel_sizes=tile.Scale3dTransform(scale=[0.01, 0.01, 0.01]),
                    echo_time=2.2,
                    effective_echo_time=2.0,
                    repetition_time=1.2,
                    additional_scan_parameters={"number_averages": 3},
                )
            ],
        )

        assert mri is not None

    def test_axis(self):
        """test the axis class"""
        # test that a few work
        test_codes = ["RAS", "LSP", "RAI", "PAR"]
        for test_code in test_codes:
            a = acq.Acquisition(
                experimenter_full_name=["alice"],
                session_start_time=datetime.datetime.now(),
                specimen_id="12345",
                subject_id="1234",
                instrument_id="1234",
                calibrations=[
                    Calibration(
                        calibration_date=datetime.datetime.now(),
                        description="Laser power calibration",
                        device_name="Laser 1",
                        input={"power_setting": PowerValue(value=100.0, unit="percent")},
                        output={"power_measurement": PowerValue(value=50.0, unit="milliwatt")},
                    ),
                ],
                session_end_time=datetime.datetime.now(),
                chamber_immersion=acq.Immersion(medium="PBS", refractive_index=1),
                tiles=[
                    tile.AcquisitionTile(
                        coordinate_transformations=[
                            tile.Scale3dTransform(scale=[1, 1, 1]),
                            tile.Translation3dTransform(translation=[1, 1, 1]),
                        ],
                        channel=tile.Channel(
                            channel_name="488",
                            light_source_name="Ex_488",
                            filter_names=["Em_600"],
                            detector_name="PMT_1",
                            excitation_wavelength=488,
                            excitation_power=0.1,
                            filter_wheel_index=0,
                        ),
                    )
                ],
                axes=test_code,
            )
            self.assertEqual(3, len(a.axes))

    def test_registration(self):
        """test the tile models"""

        t = Registration(
            name="Image tile alignment",
            software_version="2.3",
            start_date_time=datetime.datetime.now(),
            end_date_time=datetime.datetime.now(),
            input_location="/some/path",
            output_location="/some/path",
            code_url="http://foo",
            parameters={},
            registration_type="Intra-channel",
            tiles=[
                tile.Tile(
                    coordinate_transformations=[
                        tile.Affine3dTransform(affine_transform=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
                    ]
                ),
                tile.Tile(
                    coordinate_transformations=[
                        tile.Translation3dTransform(translation=[0, 1, 2]),
                        tile.Rotation3dTransform(rotation=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
                        tile.Scale3dTransform(scale=[1, 2, 3]),
                    ]
                ),
            ],
        )

        self.assertIsNotNone(t)

    def test_validators(self):
        """test the validators"""

        with self.assertRaises(ValidationError) as e:
            inst.Instrument(
                instrument_id="exaSPIM1-1",
                instrument_type="exaSPIM",
                modification_date=datetime.date(2023, 10, 4),
                manufacturer=Manufacturer.CUSTOM,
                daqs=[
                    DAQDevice(
                        model="PCIe-6738",
                        data_interface="USB",
                        computer_name="Dev2",
                        manufacturer=Manufacturer.NATIONAL_INSTRUMENTS,
                        name="Dev2",
                        serial_number="Unknown",
                        channels=[
                            DAQChannel(
                                channel_name="3",
                                channel_type="Analog Output",
                                device_name="LAS-08308",
                                sample_rate=10000,
                            ),
                            DAQChannel(
                                channel_name="5",
                                channel_type="Analog Output",
                                device_name="539251",
                                sample_rate=10000,
                            ),
                            DAQChannel(
                                channel_name="4",
                                channel_type="Analog Output",
                                device_name="LAS-08309",
                                sample_rate=10000,
                            ),
                            DAQChannel(
                                channel_name="2",
                                channel_type="Analog Output",
                                device_name="stage-x",
                                sample_rate=10000,
                            ),
                            DAQChannel(
                                channel_name="0",
                                channel_type="Analog Output",
                                device_name="TL-1",
                                sample_rate=10000,
                            ),
                            DAQChannel(
                                channel_name="6",
                                channel_type="Analog Output",
                                device_name="LAS-08307",
                                sample_rate=10000,
                            ),
                        ],
                    )
                ],
            )
        expected_exception = (
            "2 validation errors for Instrument\n"
            "objectives\n"
            "  Field required [type=missing,"
            " input_value={'instrument_id': 'exaSPI...based_sampling=None)])]}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "daqs\n"
            "  Value error, Device name validation error: 'LAS-08308' is connected to '3' on 'Dev2',"
            " but this device is not part of the rig. [type=value_error,"
            " input_value=[DAQDevice(device_type='D..._based_sampling=None)])], input_type=list]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/value_error"
        )
        self.assertEqual(expected_exception, repr(e.exception))


if __name__ == "__main__":
    unittest.main()
