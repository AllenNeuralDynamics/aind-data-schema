""" test DataDescription """

import unittest
from pydantic import ValidationError
from aind_data_schema import Acquisition, Instrument, Microscope
import datetime


class ImagingTests(unittest.TestCase):
    """test imaging schemas """

    def test_constructors(self):
        with self.assertRaises(ValidationError):
            a = Acquisition()

        a = Acquisition(institution='AIND',
            experimenter_full_name='alice',
            session_start_time=datetime.datetime.now(),
            specimen_id='1234',
            instrument_id='1234',
            session_end_time=datetime.datetime.now(),
            positions=[],
            lasers=[]
            )

        with self.assertRaises(ValidationError):
            i = Instrument()

        m = Microscope(
            manufacturer='LifeCanvas',
            type='smartSPIM',
            location='440'
        )

        i = Instrument(
            microscope=m,
            objectives=[],
            detectors=[],
            light_sources=[]
        )

if __name__ == "__main__":
    unittest.main()
