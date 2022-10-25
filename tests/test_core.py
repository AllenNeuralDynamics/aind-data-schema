""" example unit test file """

import unittest

import jsonschema
import pydantic

import aind_data_schema


class ExampleTest(unittest.TestCase):
    """an example test"""

    def test_example(self):
        """always returns true"""

        print(aind_data_schema)
        print(pydantic)
        print(jsonschema)
        assert True


if __name__ == "__main__":
    unittest.main()
