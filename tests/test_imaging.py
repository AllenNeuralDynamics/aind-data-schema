""" test Imaging """

import re
import unittest
from datetime import datetime, timezone

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import PowerUnit
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components import tile
from aind_data_schema.components.coordinates import (
    Affine3dTransform,
    Rotation3dTransform,
    Scale3dTransform,
    Translation3dTransform,
)
from aind_data_schema.components.devices import Calibration
from aind_data_schema.core import acquisition as acq
from aind_data_schema.core.processing import Registration
from aind_data_schema.core.instrument import Instrument
from aind_data_schema_models.modalities import Modality

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            acq.Acquisition()

        a = acq.Acquisition(
            experimenter_full_name=["alice"],
            session_start_time=datetime.now(tz=timezone.utc),
            specimen_id="12345",
            subject_id="1234",
            instrument_id="1234",
            calibrations=[
                Calibration(
                    calibration_date=datetime.now(tz=timezone.utc),
                    description="Laser power calibration",
                    device_name="Laser 1",
                    input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
                    output={
                        "power_measurement": 50.0,
                        "power_unit": PowerUnit.MW,
                    },
                ),
            ],
            session_end_time=datetime.now(tz=timezone.utc),
            chamber_immersion=acq.Immersion(medium="PBS", refractive_index=1),
            tiles=[
                tile.AcquisitionTile(
                    coordinate_transformations=[
                        Scale3dTransform(scale=[1, 1, 1]),
                        Translation3dTransform(translation=[1, 1, 1]),
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
            Instrument()

        i = Instrument(
            instrument_id="room_exaSPIM1-1_20231004",
            modalities=[Modality.SPIM],
            instrument_type="diSPIM",
            modification_date=datetime.now().date(),
            manufacturer=Organization.LIFECANVAS,
        )

        self.assertIsNotNone(i)

        # Instrument type Other requires notes
        with self.assertRaises(ValidationError) as e1:
            Instrument(
                instrument_id="room_exaSPIM1-1_20231004",
                modalities=[Modality.SPIM],
                instrument_type="Other",
                modification_date=datetime(2020, 10, 10, 0, 0, 0).date(),
                manufacturer=Organization.OTHER,
            )

        self.assertIn("instrument_id", repr(e1.exception))

        # Modality SPIM requirements components
        with self.assertRaises(ValidationError) as e2:
            Instrument(
                instrument_id="room_exaSPIM1-1_20231004",
                modalities=[Modality.SPIM],
                modification_date=datetime(2020, 10, 10, 0, 0, 0).date(),
                instrument_type="diSPIM",
                manufacturer=Organization.OTHER,
            )

        expected_exception2 = (
            "2 validation errors for Instrument\n"
            "modification_date\n"
            "  Field required [type=missing, input_value={'instrument_type': 'diSP...[],"
            " 'light_sources': []}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "notes\n"
            "  Value error, Notes cannot be empty if manufacturer is Other."
            " Describe the manufacturer in the notes field."
            " [type=value_error, input_value=None, input_type=NoneType]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )
        self.assertEqual(expected_exception2, repr(e2.exception))

    def test_axis(self):
        """test the axis class"""
        # test that a few work
        test_codes = ["RAS", "LSP", "RAI", "PAR"]
        for test_code in test_codes:
            a = acq.Acquisition(
                experimenter_full_name=["alice"],
                session_start_time=datetime.now(tz=timezone.utc),
                specimen_id="12345",
                subject_id="1234",
                instrument_id="1234",
                calibrations=[
                    Calibration(
                        calibration_date=datetime.now(tz=timezone.utc),
                        description="Laser power calibration",
                        device_name="Laser 1",
                        input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
                        output={
                            "power_measurement": 50.0,
                            "power_unit": PowerUnit.MW,
                        },
                    ),
                ],
                session_end_time=datetime.now(tz=timezone.utc),
                chamber_immersion=acq.Immersion(medium="PBS", refractive_index=1),
                tiles=[
                    tile.AcquisitionTile(
                        coordinate_transformations=[
                            Scale3dTransform(scale=[1, 1, 1]),
                            Translation3dTransform(translation=[1, 1, 1]),
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
            start_date_time=datetime.now(tz=timezone.utc),
            end_date_time=datetime.now(tz=timezone.utc),
            input_location="/some/path",
            output_location="/some/path",
            code_url="http://foo",
            parameters={},
            registration_type="Intra-channel",
            tiles=[
                tile.Tile(
                    coordinate_transformations=[
                        Affine3dTransform(affine_transform=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
                    ]
                ),
                tile.Tile(
                    coordinate_transformations=[
                        Translation3dTransform(translation=[0, 1, 2]),
                        Rotation3dTransform(rotation=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
                        Scale3dTransform(scale=[1, 2, 3]),
                    ]
                ),
            ],
        )

        self.assertIsNotNone(t)


if __name__ == "__main__":
    unittest.main()
