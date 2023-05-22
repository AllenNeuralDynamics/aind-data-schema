"""Test utils.units"""

import unittest
from typing import TypeVar

from aind_data_schema.utils.units import GenericValues, SizeVal, Units

ScalarType = TypeVar("ScalarType", float, int)


class UnitsTests(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_units(self):
        """Tests creation of a SizeVal object"""
        
        self.assertIsNotNone(Units.Size.MM)

        default = SizeVal(value=10.1)
        testType = GenericValues.SizeValue[ScalarType, Units.SizeType]
        testVal = testType(value=10.1, unit=Units.Size.MM)

        self.assertEqual(default, SizeVal(value=10.1, unit=Units.Size.MM))
        self.assertEqual(default, testVal)


if __name__ == "__main__":
    unittest.main()
