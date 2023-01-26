""" test Imaging """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema.imaging import acquisition as acq
from aind_data_schema.imaging import instrument as inst
from aind_data_schema.imaging import tile
from aind_data_schema.processing import Stitching


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            a = acq.Acquisition()

        a = acq.Acquisition(
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            subject_id="1234",
            instrument_id="1234",
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
                        laser_wavelength=488,
                        laser_power=0.1,
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
            type="smartSPIM",
            location="440",
            manufacturer="LifeCanvas",
            objectives=[],
            detectors=[],
            light_sources=[],
        )

        assert i is not None

    def test_axis(self):
        """test the axis class"""
        # test that a few work
        test_codes = ["RAS", "LSP", "RAI", "PAR"]
        for test_code in test_codes:
            axes = acq.Axis.from_direction_code(test_code)
            assert len(axes) == 3

    def test_stitching(self):
        """test the tile models"""

        t = Stitching(
            name="Image tile stitching",
            version="1.0",
            start_date_time=datetime.datetime.now(),
            end_date_time=datetime.datetime.now(),
            input_location="/some/path",
            output_location="/some/path",
            code_url="http://foo",
            parameters={},
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
