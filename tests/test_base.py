""" tests for Subject """
import unittest

from aind_data_schema.core.subject import Subject


class BaseTests(unittest.TestCase):
    """tests for the base module"""

    def test_described_by(self):
        """test that described by works"""

        s = Subject.model_construct()

        self.assertEqual(
            "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/subject.py",
            s.describedBy,
        )


if __name__ == "__main__":
    unittest.main()
