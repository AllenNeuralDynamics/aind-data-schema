""" test Imaging """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema import Acquisition, Instrument, Microscope


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            a = Acquisition()

        a = Acquisition(
            institution="AIND",
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            subject_id="1234",
            instrument_id="1234",
            session_end_time=datetime.datetime.now(),
            positions=[],
            lasers=[],
        )

        assert a is not None

        with self.assertRaises(ValidationError):
            i = Instrument()

        m = Microscope(
            manufacturer="LifeCanvas", type="smartSPIM", location="440"
        )

        i = Instrument(
            microscope=m, objectives=[], detectors=[], light_sources=[]
        )

        assert i is not None


if __name__ == "__main__":
    unittest.main()
