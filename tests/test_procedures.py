""" test Procedures """

import unittest

from aind_data_schema import Procedures
from pydantic import ValidationError


class ProceduresTests(unittest.TestCase):
    """test Procedures"""

    def test_constructors(self):
        with self.assertRaises(ValidationError):
            p = Procedures()

        p = Procedures(specimen_id="1234")


if __name__ == "__main__":
    unittest.main()
