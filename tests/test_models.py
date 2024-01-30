"""Tests classes with fixed Literal values match defaults"""

import unittest

from aind_data_schema.models.harp_types import HarpDeviceType
from aind_data_schema.models.organizations import Organization
from aind_data_schema.models.platforms import Platform
from aind_data_schema.models.registry import Registry
from aind_data_schema.models.species import Species


class LiteralAndDefaultTests(unittest.TestCase):
    """Tests Literals match defaults in several classes"""

    def test_organations(self):
        """Test Literals match defaults"""

        for organization in Organization._ALL:
            model = organization()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)

    def test_harp(self):
        """Test Literals match defaults"""

        for harp in HarpDeviceType._ALL:
            model = harp()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)

    def test_registry(self):
        """Test Literals match defaults"""

        for registry in Registry._ALL:
            model = registry()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)

    def test_platforms(self):
        """Test Literals match defaults"""

        for platform in Platform._ALL:
            model = platform()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)

    def test_species(self):
        """Test Literals match defaults"""

        for species in Species._ALL:
            model = species()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)


if __name__ == "__main__":
    unittest.main()
