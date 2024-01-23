""" tests for Subject """

import datetime
import unittest

import pydantic

from aind_data_schema.core.subject import Housing, LightCycle, Subject
from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.registry import Registry
from aind_data_schema.models.species import Species


class SubjectTests(unittest.TestCase):
    """tests for subject"""

    def test_constructors(self):
        """try building Subjects"""

        with self.assertRaises(pydantic.ValidationError):
            Subject()

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
            alleles=[PIDName(registry_identifier="12345", name="adsf", registry=Registry.MGI)],
        )

        Subject.model_validate_json(s.model_dump_json())

        self.assertIsNotNone(s)


if __name__ == "__main__":
    unittest.main()
