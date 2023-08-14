""" test Procedures """

import unittest
from datetime import date

from pydantic import ValidationError

from aind_data_schema import Procedures
from aind_data_schema.procedures import (
    FiberImplant,
    InjectionMaterial,
    NanojectInjection,
    OphysProbe,
    RetroOrbitalInjection,
)


class ProceduresTests(unittest.TestCase):
    """test Procedures"""

    def test_required_field_validation_check(self):
        """Tests that validation error is thrown if subject_id is not set."""
        with self.assertRaises(ValidationError):
            Procedures()

        p = Procedures(subject_id="12345")
        self.assertEqual("12345", p.subject_id)

    def test_injection_material_check(self):
        """Tests validation on the presence of injections materials"""

        start_date = date.fromisoformat("2020-10-10")
        end_date = date.fromisoformat("2020-10-11")

        with self.assertRaises(ValidationError):
            Procedures(
                subject_id="12345",
                subject_procedures=[
                    RetroOrbitalInjection(
                        start_date=start_date,
                        end_date=end_date,
                        experimenter_full_name="tom",
                        protocol_id="134",
                        injection_materials=[],  # An empty list is invalid
                        injection_volume=1,
                        injection_eye="Left",
                        injection_duration=1,
                        recovery_time=10,
                    ),
                ],
            )

        p = Procedures(
            subject_id="12345",
            subject_procedures=[
                RetroOrbitalInjection(
                    start_date=start_date,
                    end_date=end_date,
                    experimenter_full_name="tom",
                    protocol_id="134",
                    injection_materials=[
                        InjectionMaterial(
                            name="abc",
                            titer="5.46E13",
                            prep_lot_number="CT323",
                        )
                    ],
                    injection_volume=1,
                    injection_eye="Left",
                    injection_duration=1,
                    recovery_time=10,
                ),
                NanojectInjection(
                    start_date=start_date,
                    end_date=end_date,
                    experimenter_full_name="betsy",
                    protocol_id="bca",
                    injection_materials=[
                        InjectionMaterial(
                            name="abc",
                            titer="5.46E13",
                            prep_lot_number="CT323",
                        )
                    ],
                    injection_duration=1,
                    injection_coordinate_ml=1,
                    injection_coordinate_ap=1,
                    injection_coordinate_depth=[1],
                    injection_coordinate_reference="Bregma",
                    bregma_to_lambda_distance=4.1,
                    injection_angle=1,
                    injection_volume=[1],
                    recovery_time=10,
                    targeted_structure="VISp6",
                ),
                FiberImplant(
                    start_date=start_date,
                    end_date=end_date,
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
                            stereotactic_coordinate_reference="Bregma",
                            bregma_to_lambda_distance=4.1,
                            angle=10,
                        )
                    ],
                ),
            ],
        )

        self.assertEqual(3, len(p.subject_procedures))


if __name__ == "__main__":
    unittest.main()
