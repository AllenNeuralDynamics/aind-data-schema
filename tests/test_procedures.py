""" test Procedures """

import unittest
import datetime
from pydantic import ValidationError

from aind_data_schema import Procedures
from aind_data_schema.procedures import (
    FiberImplant,
    OphysProbe,
    RetroOrbitalInjection,
    NanojectInjection,
)


class ProceduresTests(unittest.TestCase):
    """test Procedures"""

    def test_constructors(self):
        """test that we can construct things"""

        with self.assertRaises(ValidationError):
            p = Procedures()

        p = Procedures(subject_id="1234")

        assert p is not None

        now = datetime.datetime.now()

        p = Procedures(
            subject_id="12345",
            injections=[
                RetroOrbitalInjection(
                    start_date=now,
                    end_date=now,
                    experimenter_full_name="tom",
                    protocol_id="134",
                    injection_virus="abc",
                    injection_volume=1,
                    injection_eye="left",
                    injection_duration=1,
                ),
                NanojectInjection(
                    start_date=now,
                    end_date=now,
                    experimenter_full_name="betsy",
                    protocol_id="bca",
                    injection_virus="fds",
                    injection_duration=1,
                    injection_coordinate_ml=1,
                    injection_coordinate_ap=1,
                    injection_coordinate_depth=1,
                    injection_angle=1,
                    injection_volume=1,
                ),
            ],
            fiber_implants=[
                FiberImplant(
                    start_date=now,
                    end_date=now,
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
