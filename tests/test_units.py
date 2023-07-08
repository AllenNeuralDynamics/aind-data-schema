"""Test utils.units"""

import unittest
from decimal import Decimal
from typing import TypeVar

from aind_data_schema.utils.units import Size, SizeValue, create_unit_with_value

ScalarType = TypeVar("ScalarType", Decimal, int)


class UnitsTests(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_units(self):
        """Tests creation of a SizeVal object"""

        self.assertIsNotNone(Size.MM)

        default = SizeValue(value=10.1)

        self.assertEqual(default, SizeValue(value=10.1, unit=Size.MM))

        ArbitraryValue = create_unit_with_value("ArbitraryValue", Decimal, Size, Size.IN)

        self.assertIsNotNone(ArbitraryValue(value=10, unit=Size.PX))


if __name__ == "__main__":
    unittest.main()
