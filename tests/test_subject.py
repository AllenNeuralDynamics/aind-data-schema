""" tests for Subject """

import datetime
import unittest

import pydantic

from aind_data_schema.core.subject import Housing, LightCycle, MgiAlleleId, Subject, BreedingInfo
from aind_data_schema.models.species import Species
from aind_data_schema.models.institutions import Institution


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
            source=Institution.AIND,
            housing=Housing(
                light_cycle=LightCycle(
                    lights_on_time=now.time(),
                    lights_off_time=now.time(),
                ),
                cage_id="543",
            ),
            breeding_info=BreedingInfo(

            ),
            mgi_allele_ids=[MgiAlleleId(mgi_id="12345", allele_name="adsf")],
        )

        Subject.model_validate_json(s.model_dump_json())

        self.assertIsNotNone(s)

    def test_validators(self):
        """test validators"""

        now = datetime.datetime.now()

        with self.assertRaises(ValueError):
            Subject(
                species=Species.MUS_MUSCULUS,
                subject_id="1234",
                sex="Male",
                date_of_birth=now.date(),
                genotype="wt",
                source=Institution.AI,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=now.time(),
                        lights_off_time=now.time(),
                    ),
                    cage_id="543",
                ),
                
                mgi_allele_ids=[MgiAlleleId(mgi_id="12345", allele_name="adsf")],
            )
            
        with self.assertRaises(ValueError):
            Subject(
                species=Species.MUS_MUSCULUS,
                subject_id="1234",
                sex="Male",
                date_of_birth=now.date(),
                source=Institution.AIND,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=now.time(),
                        lights_off_time=now.time(),
                    ),
                    cage_id="543",
                ),
                mgi_allele_ids=[MgiAlleleId(mgi_id="12345", allele_name="adsf")],
            )


if __name__ == "__main__":
    unittest.main()
