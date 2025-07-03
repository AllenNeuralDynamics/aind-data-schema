"""Tests for subjects details models"""

import unittest
from datetime import datetime

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.species import Species, Strain

from aind_data_schema.components.subjects import Housing, LightCycle, MouseSubject, Sex


class TestMouseSubject(unittest.TestCase):
    """Test the mouse subject model"""

    def setUp(self):
        """Set up the tests"""
        self.now = datetime.now()

    def test_validate_inhouse_breeding_info(self):
        """Test the inhouse breeding info validator"""

        with self.assertRaises(ValueError) as context:
            MouseSubject(
                sex=Sex.MALE,
                date_of_birth=self.now.date(),
                strain=Strain.C57BL_6J,
                species=Species.HOUSE_MOUSE,
                genotype="wt",
                source=Organization.AI,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=self.now.time(),
                        lights_off_time=self.now.time(),
                    ),
                    cage_id="543",
                ),
                alleles=[PIDName(registry_identifier="12345", name="adsf", registry=Registry.MGI)],
            )
        self.assertIn("Breeding info should be provided for subjects bred in house", str(context.exception))

    def test_validate_species_strain(self):
        """Test the species and strain validator"""

        with self.assertRaises(ValueError) as context:
            MouseSubject(
                sex=Sex.MALE,
                date_of_birth=self.now.date(),
                strain=Strain.BALB_C,
                species=Species.HUMAN,
                genotype="wt",
                source=Organization.JAX,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=self.now.time(),
                        lights_off_time=self.now.time(),
                    ),
                    cage_id="543",
                ),
                alleles=[PIDName(registry_identifier="12345", name="adsf", registry=Registry.MGI)],
            )
        self.assertIn("The animal species and it's strain's species do not match", str(context.exception))


if __name__ == "__main__":
    unittest.main()
