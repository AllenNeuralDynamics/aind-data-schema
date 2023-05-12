""" tests for Subject """

import datetime
import unittest

import pydantic

from aind_data_schema import Subject
from aind_data_schema.subject import Housing, LightCycle, MgiAlleleId, Species


class SubjectTests(unittest.TestCase):
    """tests for subject"""

    def test_constructors(self):
        """try building Subjects"""

        with self.assertRaises(pydantic.ValidationError):
            s = Subject()

        now = datetime.datetime.now()

        s = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="1234",
            sex="Male",
            date_of_birth=now.date(),
            genotype="wt",
            housing=Housing(
                light_cycle=LightCycle(
                    lights_on_time=now.time(),
                    lights_off_time=now.time(),
                ),
                cage_id="543",
            ),
            mgi_allele_ids=[MgiAlleleId(mgi_id="12345", allele_name="adsf")],
        )

        assert s is not None


if __name__ == "__main__":
    unittest.main()
