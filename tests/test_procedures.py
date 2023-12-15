""" test Procedures """

import unittest
from datetime import date

from pydantic import ValidationError

from aind_data_schema.core.procedures import (
    FiberImplant,
    ViralMaterial,
    NanojectInjection,
    OphysProbe,
    Procedures,
    RetroOrbitalInjection,
    SpecimenProcedure,
    TarsIds,
)
from aind_data_schema.models.devices import FiberProbe
from aind_data_schema.models.manufacturers import Manufacturer


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
                        ViralMaterial(
                            material_type="Virus",
                            name="AAV2-Flex-ChrimsonR",
                            tars_identifiers=TarsIds(
                                virus_TARS_id="AiV222",
                                plasmid_TARS_alias="AiP222",
                                prep_lot_number="VT222",
                            ),
                            titer=2300000000,
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
                        ViralMaterial(
                            material_type="Virus",
                            name="AAV2-Flex-ChrimsonR",
                            tars_identifiers=TarsIds(
                                virus_TARS_id="AiV222",
                                plasmid_TARS_alias="AiP222",
                                prep_lot_number="VT222",
                            ),
                            titer=2300000000,
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
                            ophys_probe=FiberProbe(
                                device_type="Fiber optic probe",
                                name="Probe A",
                                manufacturer=Manufacturer.DORIC,
                                model="8",
                                core_diameter=2,
                                numerical_aperture=1,
                                ferrule_material="Ceramic",
                                total_length=10,
                            ),
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

    def test_notes_other(self):
        """Test that the other/notes validation error works"""

        with self.assertRaises(ValidationError):
            SpecimenProcedure(
                specimen_id="1000",
                procedure_name="procedure name",
                procedure_type="Other - see notes",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenter_full_name="guy person",
                protocol_id="10",
                reagents=[],
                notes=None,
            )

    def test_coordinate_volume_validator(self):
        """Test validator for list lengths on NanojectInjection"""

        # Should be okay
        inj1 = NanojectInjection(
            start_date=date(2020, 10, 10),
            end_date=date(2020, 10, 10),
            experimenter_full_name="Betsy",
            protocol_id="abc",
            injection_coordinate_ml=1,
            injection_coordinate_ap=1,
            injection_angle=1,
            injection_coordinate_depth=[0, 1],
            injection_volume=[1, 2],
        )
        self.assertEqual(len(inj1.injection_coordinate_depth), len(inj1.injection_volume))

        # Different coord_depth and inj_vol list lengths should raise an error
        with self.assertRaises(ValidationError):
            NanojectInjection(
                start_date=date(2020, 10, 10),
                end_date=date(2020, 10, 10),
                experimenter_full_name="Betsy",
                protocol_id="abc",
                injection_coordinate_ml=1,
                injection_coordinate_ap=1,
                injection_angle=1,
                injection_coordinate_depth=[0.1],
                injection_volume=[1, 2],
            )


if __name__ == "__main__":
    unittest.main()
