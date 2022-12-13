""" tests for Subject """
import unittest
from aind_data_schema import Procedures


class BaseTests(unittest.TestCase):
    """tests for the base module"""

    def test_described_by(self):
        """test that described by works"""

        p = Procedures(subject_id="1234")

        self.assertEqual(
            p.describedBy,
            "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/procedures.py",
        )


if __name__ == "__main__":
    unittest.main()
