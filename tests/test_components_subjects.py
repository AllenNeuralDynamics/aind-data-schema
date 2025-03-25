"""Tests for subjects details models"""

import unittest
from datetime import datetime
from aind_data_schema.components.subjects import MouseSubject, BreedingInfo, Housing, LightCycle, Sex
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.species import Species, Strain


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
                species=Species.MUS_MUSCULUS,
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

    def test_validate_genotype(self):
        """Test the genotype validator"""

        with self.assertRaises(ValueError) as context:
            MouseSubject(
                sex=Sex.MALE,
                date_of_birth=self.now.date(),
                strain=Strain.C57BL_6J,
                species=Species.MUS_MUSCULUS,
                source=Organization.AI,
                housing=Housing(
                    light_cycle=LightCycle(
                        lights_on_time=self.now.time(),
                        lights_off_time=self.now.time(),
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
        self.assertIn("Full genotype should be provided for mouse subjects", str(context.exception))

    def test_validate_species_strain(self):
        """Test the species and strain validator"""

        with self.assertRaises(ValueError) as context:
            MouseSubject(
                sex=Sex.MALE,
                date_of_birth=self.now.date(),
                strain=Strain.BALB_C,
                species=Species.HOMO_SAPIENS,
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
