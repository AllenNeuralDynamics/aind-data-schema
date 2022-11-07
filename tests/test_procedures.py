""" test Procedures """

import unittest
import datetime
from pydantic import ValidationError

from aind_data_schema import Procedures
from aind_data_schema.procedures import FiberImplant, OphysProbe


class ProceduresTests(unittest.TestCase):
    """test Procedures"""

    def test_constructors(self):
        """test that we can construct things"""

        with self.assertRaises(ValidationError):
            p = Procedures()

        p = Procedures(subject_id="1234")

        assert p is not None

        p = Procedures(
            subject_id="12345",
            fiber_implants=[
                FiberImplant(
                    date=datetime.datetime.now(),
                    experimenter_full_name="Betsy",
                    protocol_id="dx.doi.org/120.123/fkjd",
                    probes=[
                        OphysProbe(
                            name="Probe A",
                            manufacturer="Tom",
                            part_number="8",
                            core_diameter=2,
                            numerical_aperture=1,
                            targeted_structure="MOp",
                            stereotactic_coordinate_ap=1,
                            stereotactic_coordinate_dv=2,
                            stereotactic_coordinate_ml=3,
                            angle=10,
                        )
                    ],
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
