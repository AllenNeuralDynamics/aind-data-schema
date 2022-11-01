""" test Procedures """

import unittest

from pydantic import ValidationError

from aind_data_schema import Procedures


class ProceduresTests(unittest.TestCase):
    """test Procedures"""

    def test_constructors(self):
        """test that we can construct things"""

        with self.assertRaises(ValidationError):
            p = Procedures()

        p = Procedures(specimen_id="1234")

        assert p is not None


if __name__ == "__main__":
    unittest.main()
