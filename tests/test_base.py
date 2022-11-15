""" tests for Subject """
import unittest
from aind_data_schema.base import AindSchema


class TestSchema(AindSchema):
    foo: str


class BaseTests(unittest.TestCase):
    def test_described_by(self):
        s = TestSchema(foo="bar")
        self.assertEqual(
            s.describedBy,
            "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/tests/test_base.py",
        )


if __name__ == "__main__":
    unittest.main()
