""" test processing """

import unittest

import pydantic

from aind_data_schema import Processing


class ProcessingTest(unittest.TestCase):
    """tests for processing schema"""

    def test_constructors(self):
        """test creation"""

        with self.assertRaises(pydantic.ValidationError):
            p = Processing()

        p = Processing(data_processes=[])

        assert p is not None


if __name__ == "__main__":
    unittest.main()
