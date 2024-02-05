""" test Procedures """
import re
import unittest
from datetime import date

from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.core.procedures import (
    FiberImplant,
    IntraperitonealInjection,
    NanojectInjection,
    NonViralMaterial,
    OphysProbe,
    Procedures,
    RetroOrbitalInjection,
    SpecimenProcedure,
    Surgery,
    TarsVirusIdentifiers,
    ViralMaterial,
)
from aind_data_schema.models.devices import FiberProbe
from aind_data_schema.models.organizations import Organization

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


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

        with self.assertRaises(ValidationError):
            Procedures(
                subject_id="12345",
                subject_procedures=[
                    Surgery(
                        start_date=start_date,
                        experimenter_full_name="tom",
                        procedures=[
                            RetroOrbitalInjection(
                                start_date=start_date,
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
                ],
            )

        p = Procedures(
            subject_id="12345",
            subject_procedures=[
                Surgery(
                    start_date=start_date,
                    experimenter_full_name="tom",
                    iacuc_protocol="234",
                    procedures=[
                        RetroOrbitalInjection(
                            protocol_id="134",
                            injection_materials=[
                                ViralMaterial(
                                    material_type="Virus",
                                    name="AAV2-Flex-ChrimsonR",
                                    tars_identifiers=TarsVirusIdentifiers(
                                        virus_tars_id="AiV222",
                                        plasmid_tars_alias="AiP222",
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
                        IntraperitonealInjection(
                            protocol_id="234",
                            injection_materials=[
                                NonViralMaterial(
                                    material_type="Reagent",
                                    name="drug_xyz",
                                    source=Organization.AI,
                                    lot_number="12345",
                                    concentration=1,
                                )
                            ],
                            injection_volume=1,
                        ),
                        NanojectInjection(
                            protocol_id="bca",
                            injection_materials=[
                                ViralMaterial(
                                    material_type="Virus",
                                    name="AAV2-Flex-ChrimsonR",
                                    tars_identifiers=TarsVirusIdentifiers(
                                        virus_tars_id="AiV222",
                                        plasmid_tars_alias="AiP222",
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
                            protocol_id="dx.doi.org/120.123/fkjd",
                            probes=[
                                OphysProbe(
                                    ophys_probe=FiberProbe(
                                        device_type="Fiber optic probe",
                                        name="Probe A",
                                        manufacturer=Organization.DORIC,
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
            ],
        )

        self.assertEqual(1, len(p.subject_procedures))
        self.assertEqual(p, Procedures.model_validate_json(p.model_dump_json()))

    maxDiff = None

    def test_validate_procedure_type(self):
        """Test that the procedure type validation error works"""

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Other - see notes",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenter_full_name="guy person",
                protocol_id="10",
                reagents=[],
                notes=None,
            )
        expected_exception = (
            "1 validation error for SpecimenProcedure\n"
            "  Assertion failed, notes cannot be empty if procedure_type is Other."
            " Describe the procedure in the notes field. [type=assertion_error, "
            "input_value={'specimen_id': '1000', '...nts': [], 'notes': None}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/assertion_error"
        )
        self.assertEqual(expected_exception, repr(e.exception))

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Immunolabeling",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenter_full_name="guy person",
                protocol_id="10",
                reagents=[],
                notes=None,
            )
        expected_exception = (
            "1 validation error for SpecimenProcedure\n"
            "  Assertion failed, immunolabeling cannot be empty if procedure_type is Immunolabeling."
            " [type=assertion_error, input_value={'specimen_id': '1000', '...nts': [], 'notes': None},"
            " input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/assertion_error"
        )
        self.assertEqual(expected_exception, repr(e.exception))

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Hybridization Chain Reaction",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenter_full_name="guy person",
                protocol_id="10",
                reagents=[],
                notes=None,
            )
        expected_exception = (
            "1 validation error for SpecimenProcedure\n"
            "  Assertion failed, hcr_series cannot be empty if procedure_type is HCR."
            " [type=assertion_error, input_value={'specimen_id': '1000', '...nts': [],"
            " 'notes': None}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/assertion_error"
        )

        self.assertEqual(expected_exception, repr(e.exception))

        self.assertIsNotNone(
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Other - see notes",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenter_full_name="guy person",
                protocol_id="10",
                reagents=[],
                notes="some extra information",
            )
        )

    def test_coordinate_volume_validator(self):
        """Test validator for list lengths on NanojectInjection"""

        # Should be okay
        inj1 = NanojectInjection(
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
                protocol_id="abc",
                injection_coordinate_ml=1,
                injection_coordinate_ap=1,
                injection_angle=1,
                injection_coordinate_depth=[0.1],
                injection_volume=[1, 2],
            )


if __name__ == "__main__":
    unittest.main()
