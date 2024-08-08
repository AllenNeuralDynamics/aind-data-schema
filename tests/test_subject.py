""" tests for Subject """

import datetime
import unittest

import pydantic
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.species import Species

from aind_data_schema.core.subject import BreedingInfo, Housing, LightCycle, Subject


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
            source=Organization.AI,
            housing=Housing(
                light_cycle=LightCycle(
                    lights_on_time=now.time(),
                    lights_off_time=now.time(),
                ),
                cage_id="543",
            ),
            breeding_info=BreedingInfo(
                breeding_group="Emx1-IRES-Cre(ND)",
                maternal_id="546543",
                maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
                paternal_id="232323",
                paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
            ),
            alleles=[PIDName(registry_identifier="12345", name="adsf", registry=Registry.MGI)],
        )

        Subject.model_validate_json(s.model_dump_json())

        self.assertIsNotNone(s)

    def test_validators(self):
        """test validators"""

        now = datetime.datetime.now()

        # missing BreedingInfo when source is AI
        with self.assertRaises(ValueError):
            Subject(
                species=Species.MUS_MUSCULUS,
                subject_id="1234",
                sex="Male",
                date_of_birth=now.date(),
                genotype="wt",
                source=Organization.AI,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=now.time(),
                        lights_off_time=now.time(),
                    ),
                    cage_id="543",
                ),
                alleles=[PIDName(registry_identifier="12345", name="adsf", registry=Registry.MGI)],
            )

        with self.assertRaises(ValueError):
            Subject(
                species=Species.MUS_MUSCULUS,
                subject_id="1234",
                sex="Male",
                date_of_birth=now.date(),
                source=Organization.AI,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=now.time(),
                        lights_off_time=now.time(),
                    ),
                    cage_id="543",
                ),
                alleles=[PIDName(registry_identifier="12345", name="adsf", registry=Registry.MGI)],
            )


if __name__ == "__main__":
    unittest.main()
