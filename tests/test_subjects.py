"""Tests for subjects details models"""

import unittest
from datetime import datetime

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.species import Species, Strain

from aind_data_schema.components.subjects import (
    Housing,
    HumanSubject,
    LightCycle,
    MouseSubject,
    NonHumanPrimateSubject,
    Sex,
    MatingStatus
)


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


class TestHumanSubject(unittest.TestCase):
    """Test the human subject model"""

    def test_validate_species_is_human(self):
        """Test the species validator"""

        with self.assertRaises(ValueError) as context:
            HumanSubject(
                sex=Sex.MALE,
                species=Species.HOUSE_MOUSE,
                year_of_birth=1962,
                source=Organization.UCSD
            )
        self.assertIn("HumanSubject species must be HUMAN", str(context.exception))


class TestNonHumanPrimateSubject(unittest.TestCase):
    """Test the non-human primate subject model"""

    def setUp(self):
        """Set up the tests"""
        self.now = datetime.now()

    def test_non_human_primate_without_date_of_birth(self):
        """Test creating NonHumanPrimateSubject without optional date_of_birth"""

        subject = NonHumanPrimateSubject(
            species=Species.RHESUS_MACAQUE,
            sex=Sex.MALE,
            year_of_birth=2019,
            mating_status=MatingStatus.UNMATED,
            source=Organization.JAX
        )

        self.assertEqual(subject.species, Species.RHESUS_MACAQUE)
        self.assertEqual(subject.sex, Sex.MALE)
        self.assertIsNone(subject.date_of_birth)
        self.assertEqual(subject.year_of_birth, 2019)
        self.assertEqual(subject.mating_status, MatingStatus.UNMATED)
        self.assertEqual(subject.source, Organization.JAX)

    def test_non_human_primate_mating_status_unknown(self):
        """Test NonHumanPrimateSubject with unknown mating status"""

        subject = NonHumanPrimateSubject(
            species=Species.RHESUS_MACAQUE,
            sex=Sex.FEMALE,
            year_of_birth=2021,
            mating_status=MatingStatus.UNKNOWN,
            source=Organization.AI
        )

        self.assertEqual(subject.mating_status, MatingStatus.UNKNOWN)

    def test_validate_date_year_consistency_valid(self):
        """Test that date_of_birth year matching year_of_birth is valid"""
        from datetime import date

        birth_date = date(2020, 5, 15)
        subject = NonHumanPrimateSubject(
            species=Species.RHESUS_MACAQUE,
            sex=Sex.FEMALE,
            date_of_birth=birth_date,
            year_of_birth=2020,  # Matching year
            mating_status=MatingStatus.MATED,
            source=Organization.UCSD
        )

        self.assertEqual(subject.date_of_birth, birth_date)
        self.assertEqual(subject.year_of_birth, 2020)

    def test_validate_date_year_consistency_invalid(self):
        """Test that mismatched date_of_birth year and year_of_birth raises ValueError"""
        from datetime import date

        with self.assertRaises(ValueError) as context:
            NonHumanPrimateSubject(
                species=Species.RHESUS_MACAQUE,
                sex=Sex.MALE,
                date_of_birth=date(2019, 8, 10),  # Year 2019
                year_of_birth=2020,  # Different year
                mating_status=MatingStatus.UNMATED,
                source=Organization.JAX
            )

        self.assertIn("Date of birth (2019) does not match year of birth (2020)", str(context.exception))

    def test_validate_date_year_consistency_no_date(self):
        """Test that validation passes when date_of_birth is None"""

        subject = NonHumanPrimateSubject(
            species=Species.RHESUS_MACAQUE,
            sex=Sex.FEMALE,
            date_of_birth=None,  # No date provided
            year_of_birth=2021,
            mating_status=MatingStatus.UNKNOWN,
            source=Organization.AI
        )

        self.assertIsNone(subject.date_of_birth)
        self.assertEqual(subject.year_of_birth, 2021)


if __name__ == "__main__":
    unittest.main()
