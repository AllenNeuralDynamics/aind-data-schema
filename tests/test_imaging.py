""" test Imaging """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema.imaging import acquisition as acq
from aind_data_schema.imaging import instrument as inst


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
                acq.Tile(
                    coordinate_transformations=[
                        acq.Scale3dTransform(scale=[1, 1, 1]),
                        acq.Translation3dTransform(translation=[1, 1, 1]),
                    ],
                    channel=acq.Channel(
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


if __name__ == "__main__":
    unittest.main()
