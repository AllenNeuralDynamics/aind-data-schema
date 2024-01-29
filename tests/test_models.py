"""Tests classes with fixed Literal values match defaults"""

import unittest

from aind_data_schema.models.institutions import Institution
from aind_data_schema.models.manufacturers import Manufacturer
from aind_data_schema.models.platforms import Platform
from aind_data_schema.models.registry import Registry
from aind_data_schema.models.species import Species


class LiteralAndDefaultTests(unittest.TestCase):
    """Tests Literals match defaults in several classes"""

    def test_institution(self):
        """Test Literals match defaults"""

        for institution in Institution._ALL:
            model = institution()
            round_trip = model.model_validate_json(model.model_dump_json())
            self.assertIsNotNone(round_trip)

    def test_manufacturer(self):
        """Test Literals match defaults"""

        for manufacturer in Manufacturer._ALL:
            model = manufacturer()
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
