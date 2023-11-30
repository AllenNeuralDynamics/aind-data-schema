"""Test utils.units"""

import unittest
from decimal import Decimal
from typing import TypeVar

from aind_data_schema.models.units import SizeUnit, SizeValue, create_unit_with_value

ScalarType = TypeVar("ScalarType", Decimal, int)


class UnitsTests(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_units(self):
        """Tests creation of a SizeVal object"""

        self.assertIsNotNone(SizeUnit.MM)

        default = SizeValue(value=10.1)

        self.assertEqual(default, SizeValue(value=10.1, unit=SizeUnit.MM))

        ArbitraryValue = create_unit_with_value("ArbitraryValue", Decimal, SizeUnit, SizeUnit.IN)

        self.assertIsNotNone(ArbitraryValue(value=10, unit=SizeUnit.PX))


if __name__ == "__main__":
    unittest.main()
