""" tests for Subject """

import unittest

import pydantic
import datetime

from aind_data_schema import Subject, LightCycle


class SubjectTests(unittest.TestCase):
    """tests for subject"""

    def test_constructors(self):
        """try building Subjects"""

        with self.assertRaises(pydantic.ValidationError):
            s = Subject()

        now = datetime.datetime.now()

        lc = LightCycle(
            lights_on_time=now.time(), 
            lights_off_time=now.time()
        )

        s = Subject(
            species="Mus musculus",
            specimen_id="1234",
            sex="Male",
            date_of_birth=now.date(),
            genotype="wt",
            light_cycle=lc
        )

        assert s is not None


if __name__ == "__main__":
    unittest.main()
