""" tests for Subject """
import unittest
from aind_data_schema.base import AindSchema


class TestSchema(AindSchema):
    """a made up schema"""

    foo: str


class BaseTests(unittest.TestCase):
    """tests for the base module"""

    def test_described_by(self):
        """test that described by works"""

        s = TestSchema(foo="bar")
        self.assertEqual(
            s.describedBy,
            "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/tests/test_base.py",
        )


if __name__ == "__main__":
    unittest.main()
