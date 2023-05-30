"""Test utils.units"""

import unittest
from typing import TypeVar

from aind_data_schema.utils.units import Size, SizeValue

ScalarType = TypeVar("ScalarType", float, int)


class UnitsTests(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_units(self):
        """Tests creation of a SizeVal object"""

        self.assertIsNotNone(Size.MM)

        default = SizeValue(value=10.1)
        # testVal = SizeValue(value=10.1, unit=Size.MM)

        self.assertEqual(default, SizeValue(value=10.1, unit=Size.MM))
        # self.assertEqual(default, testVal)


if __name__ == "__main__":
    unittest.main()
