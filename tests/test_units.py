"""Test utils.units"""

import unittest

from aind_data_schema.utils.units import Units, GenericValues
from aind_data_schema.utils.units import SizeVal
from typing import TypeVar

ScalarType = TypeVar("ScalarType", float, int)


class UnitsTests(unittest.TestCase):
    """Class for testing Utils.Units"""

    def test_units(self):
        self.assertIsNotNone(Units.Size.MM)

        default = SizeVal(value=10.1)
        testType = GenericValues.SizeValue[ScalarType, Units.SizeType]
        testVal = testType(value=10.1, unit=Units.Size.M)

        self.assertEqual(default, SizeVal(value=10.1, unit=Units.Size.M))
        self.assertEqual(default, testVal)


if __name__ == "__main__":
    unittest.main()
