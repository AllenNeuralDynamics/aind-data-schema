"""tests for Model"""

import unittest

import pydantic

from aind_data_schema.core.model import Model
from examples.model import m


class ModelTests(unittest.TestCase):
    """tests for model"""

    def test_constructors(self):
        """try building model"""

        with self.assertRaises(pydantic.ValidationError):
            Model()

        Model.model_validate_json(m.model_dump_json())

        self.assertIsNotNone(m)


if __name__ == "__main__":
    unittest.main()
