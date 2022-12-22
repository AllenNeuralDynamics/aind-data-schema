""" test Imaging """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema import Acquisition, Instrument
from aind_data_schema.imaging.acquisition import Axis


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            a = Acquisition()

        a = Acquisition(
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            subject_id="1234",
            instrument_id="1234",
            session_end_time=datetime.datetime.now(),
            tiles=[],
            axes=[],
        )

        assert a is not None

        with self.assertRaises(ValidationError):
            i = Instrument()

        i = Instrument(
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
            axes = Axis.from_direction_code(test_code)
            assert len(axes) == 3


if __name__ == "__main__":
    unittest.main()
