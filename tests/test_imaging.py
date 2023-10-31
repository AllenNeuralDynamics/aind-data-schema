""" test Imaging """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema.device import Calibration
from aind_data_schema.imaging import acquisition as acq
from aind_data_schema.imaging import instrument as inst
from aind_data_schema.imaging import mri_session as ms
from aind_data_schema.imaging import tile
from aind_data_schema.manufacturers import Manufacturer
from aind_data_schema.processing import Registration
from aind_data_schema.utils.units import PowerValue


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            a = acq.Acquisition()

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

        assert a is not None

        with self.assertRaises(ValidationError):
            i = inst.Instrument()

        i = inst.Instrument(
            instrument_type="diSPIM",
            modification_date=datetime.datetime.now(),
            manufacturer=Manufacturer.LIFECANVAS,
            objectives=[],
            detectors=[],
            light_sources=[],
        )

        assert i is not None

        with self.assertRaises(ValidationError):
            i = inst.Instrument(
                instrument_type="Other",
                manufacturer=Manufacturer.OTHER,
                objectives=[],
                detectors=[],
                light_sources=[],
            )

        with self.assertRaises(ValidationError):
            i = inst.Instrument(
                instrument_type="diSPIM",
                manufacturer=Manufacturer.OTHER,
                objectives=[],
                detectors=[],
                light_sources=[],
            )

        with self.assertRaises(ValidationError):
            mri = ms.MRIScan(
                scan_sequence_type="Other",
            )

        with self.assertRaises(ValidationError):
            mri = ms.MRIScan(scan_sequence_type="Other", notes="")

        mri = ms.MriSession(
            experimenter_full_name=["Frank Frankson"],
            subject_id=1234,
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            protocol_id="doi_path",
            animal_weight_prior=22.1,
            animal_weight_post=21.9,
            mri_scanner=ms.Scanner(
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
            axes = acq.Axis.from_direction_code(test_code)
            assert len(axes) == 3

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

        assert t is not None


if __name__ == "__main__":
    unittest.main()
