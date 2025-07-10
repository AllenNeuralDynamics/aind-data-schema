""" test Procedures """

import unittest
from datetime import date
from unittest.mock import patch

from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.mouse_anatomy import InjectionTargets
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import ConcentrationUnit, CurrentUnit, SizeUnit, TimeUnit, VolumeUnit
from pydantic import ValidationError
from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType

from aind_data_schema.components.configs import CatheterConfig
from aind_data_schema.components.coordinates import CoordinateSystemLibrary, Origin, Translation
from aind_data_schema.components.devices import Catheter
from aind_data_schema.components.injection_procedures import (
    InjectionDynamics,
    InjectionProfile,
    NonViralMaterial,
    TarsVirusIdentifiers,
    ViralMaterial,
)
from aind_data_schema.components.specimen_procedures import (
    HCRSeries,
    PlanarSectioning,
    Section,
    SectionOrientation,
    SpecimenProcedure,
)
from aind_data_schema.components.subject_procedures import BrainInjection, Injection, Surgery
from aind_data_schema.components.surgery_procedures import CatheterImplant, Craniotomy, CraniotomyType
from aind_data_schema.core.procedures import Procedures
from aind_data_schema.utils.exceptions import OneOfError
from aind_data_schema_models.mouse_anatomy import MouseBloodVessels


class ProceduresTests(unittest.TestCase):
    """test Procedures"""

    def setUp(self):
        """Set up test data"""
        self.start_date = date.fromisoformat("2020-10-10")

    def test_required_field_validation_check(self):
        """Tests that validation error is thrown if subject_id is not set."""
        with self.assertRaises(ValidationError):
            Procedures()

        p = Procedures(subject_id="12345")
        self.assertEqual("12345", p.subject_id)

    @patch("aind_data_schema_models.mouse_anatomy.get_emapa_id")
    def test_injection_material_check(self, mock_get_emapa_id):
        """Check for validation error when injection_materials is empty"""

        mock_get_emapa_id.return_value = "123456"

        with self.assertRaises(ValidationError) as e:
            Procedures(
                subject_id="12345",
                subject_procedures=[
                    Surgery(
                        start_date=self.start_date,
                        experimenters=["Mam Moth"],
                        procedures=[
                            Injection(
                                protocol_id="134",
                                injection_materials=[],  # An empty list is invalid
                                dynamics=[
                                    InjectionDynamics(
                                        volume=1,
                                        volume_unit=VolumeUnit.UL,
                                        duration=1,
                                        duration_unit=TimeUnit.S,
                                        profile=InjectionProfile.BOLUS,
                                    )
                                ],
                                targeted_structure=InjectionTargets.RETRO_ORBITAL,
                                relative_position=[AnatomicalRelative.LEFT],
                            ),
                        ],
                    )
                ],
            )

        self.assertIn("injection_materials", repr(e.exception))

    @patch("aind_data_schema_models.mouse_anatomy.get_emapa_id")
    def test_injection_material_none(self, mock_get_emapa_id):
        """Check for validation error when injection_materials is None"""
        mock_get_emapa_id.return_value = "123456"
        with self.assertRaises(ValidationError) as e:
            Procedures(
                subject_id="12345",
                subject_procedures=[
                    Surgery(
                        start_date=self.start_date,
                        experimenters=["Mam Moth"],
                        procedures=[
                            Injection(
                                protocol_id="134",
                                injection_materials=None,
                                dynamics=[
                                    InjectionDynamics(
                                        volume=1,
                                        volume_unit=VolumeUnit.UL,
                                        duration=1,
                                        duration_unit=TimeUnit.S,
                                        profile=InjectionProfile.BOLUS,
                                    )
                                ],
                                targeted_structure=InjectionTargets.RETRO_ORBITAL,
                                relative_position=[AnatomicalRelative.LEFT],
                            ),
                        ],
                    )
                ],
            )

        self.assertIn("injection_materials", repr(e.exception))

    @patch("aind_data_schema_models.mouse_anatomy.get_emapa_id")
    def test_injection_materials_list(self, mock_get_emapa_id):
        """Valid injection_materials list"""
        mock_get_emapa_id.return_value = "123456"

        p = Procedures(
            subject_id="12345",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            subject_procedures=[
                Surgery(
                    start_date=self.start_date,
                    experimenters=["Mam Moth"],
                    ethics_review_id="234",
                    protocol_id="123",
                    coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
                    measured_coordinates={
                        Origin.BREGMA: Translation(
                            translation=[0, 0, 0],
                        ),
                        Origin.LAMBDA: Translation(
                            translation=[-4.1, 0, 0],
                        ),
                    },
                    procedures=[
                        Injection(
                            protocol_id="134",
                            injection_materials=[
                                ViralMaterial(
                                    name="AAV2-Flex-ChrimsonR",
                                    tars_identifiers=TarsVirusIdentifiers(
                                        virus_tars_id="AiV222",
                                        plasmid_tars_alias=["AiP222"],
                                        prep_lot_number="VT222",
                                    ),
                                    titer=2300000000,
                                )
                            ],
                            targeted_structure=InjectionTargets.RETRO_ORBITAL,
                            relative_position=[AnatomicalRelative.LEFT],
                            dynamics=[
                                InjectionDynamics(
                                    volume=1,
                                    volume_unit=VolumeUnit.UL,
                                    duration=1,
                                    duration_unit=TimeUnit.S,
                                    profile=InjectionProfile.BOLUS,
                                )
                            ],
                        ),
                        Injection(
                            protocol_id="234",
                            injection_materials=[
                                NonViralMaterial(
                                    name="drug_xyz",
                                    source=Organization.AI,
                                    lot_number="12345",
                                    concentration=1,
                                    concentration_unit=ConcentrationUnit.UM,
                                )
                            ],
                            targeted_structure=InjectionTargets.INTRAPERITONEAL,
                            dynamics=[
                                InjectionDynamics(
                                    volume=1,
                                    volume_unit=VolumeUnit.UL,
                                    profile=InjectionProfile.BOLUS,
                                )
                            ],
                        ),
                        BrainInjection(
                            protocol_id="bca",
                            coordinate_system_name="BREGMA_ARI",
                            injection_materials=[
                                ViralMaterial(
                                    name="AAV2-Flex-ChrimsonR",
                                    tars_identifiers=TarsVirusIdentifiers(
                                        virus_tars_id="AiV222",
                                        plasmid_tars_alias=["AiP222"],
                                        prep_lot_number="VT222",
                                    ),
                                    titer=2300000000,
                                )
                            ],
                            dynamics=[
                                InjectionDynamics(
                                    volume=1,
                                    volume_unit=VolumeUnit.UL,
                                    duration=1,
                                    duration_unit=TimeUnit.S,
                                    profile=InjectionProfile.BOLUS,
                                )
                            ],
                            coordinates=[
                                [
                                    Translation(
                                        translation=[0.5, 1, 0, 1],
                                    ),
                                ],
                            ],
                            targeted_structure=CCFv3.VISP6A,
                        ),
                    ],
                )
            ],
        )

        self.assertEqual(1, len(p.subject_procedures))
        self.assertEqual(p, Procedures.model_validate_json(p.model_dump_json()))

    def test_validate_procedure_type(self):
        """Test that the procedure type validation error works"""

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Other",
                start_date=self.start_date,
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn("notes cannot be empty if procedure_type is Other", repr(e.exception))

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Immunolabeling",
                start_date=self.start_date,
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn(
            "FluorescentStain or ProbeReagent required if procedure_type is Immunolabeling", repr(e.exception)
        )

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Hybridization Chain Reaction",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn("HCRSeries required if procedure_type is HCR", repr(e.exception))

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Sectioning",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn("Sectioning required if procedure_type is Sectioning", repr(e.exception))

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type=SpecimenProcedureType.BARSEQ,
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn("GeneProbeSet required if procedure_type is BarSEQ", repr(e.exception))

        self.assertIsNotNone(
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Other",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes="some extra information",
            )
        )

    def test_validate_procedure_type_multiple(self):
        """Test that error thrown when multiple types are passed to procedure_details"""

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Other",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=["Mam Moth"],
                protocol_id=["10"],
                notes="some extra information",
                procedure_details=[
                    HCRSeries.model_construct(),
                    PlanarSectioning.model_construct(),
                ],
            )
        self.assertIn("SpecimenProcedure.procedure_details should only contain one type of model", repr(e.exception))

    def test_coordinate_volume_validator(self):
        """Test validator for list lengths on BrainInjection"""

        # Should be okay
        inj1 = BrainInjection(
            protocol_id="abc",
            coordinate_system_name="BREGMA_ARI",
            coordinates=[
                [
                    Translation(
                        translation=[0.5, 1, 0, 0],
                    ),
                ],
                [
                    Translation(
                        translation=[0.5, 1, 0, 1],
                    ),
                ],
            ],
            dynamics=[
                InjectionDynamics(
                    volume=1,
                    volume_unit=VolumeUnit.UL,
                    profile=InjectionProfile.PULSED,
                ),
                InjectionDynamics(
                    volume=2,
                    volume_unit=VolumeUnit.UL,
                    profile=InjectionProfile.PULSED,
                ),
            ],
            injection_materials=[
                ViralMaterial(
                    name="AAV2-Flex-ChrimsonR",
                    tars_identifiers=TarsVirusIdentifiers(
                        virus_tars_id="AiV222",
                        plasmid_tars_alias=["AiP222", "AiP223"],
                        prep_lot_number="VT222",
                    ),
                    titer=2300000000,
                )
            ],
        )
        self.assertEqual(len(inj1.coordinates), len(inj1.dynamics))

        # Different coordinates and dynamics list lengths should raise an error
        with self.assertRaises(ValidationError) as e:
            BrainInjection(
                protocol_id="abc",
                coordinate_system_name="BREGMA_ARI",
                coordinates=[
                    [
                        Translation(
                            translation=[0.5, 1, 0, 0],
                        ),
                    ],
                    [
                        Translation(
                            translation=[0.5, 1, 0, 1],
                        ),
                    ],
                ],
                injection_materials=[
                    ViralMaterial(
                        name="AAV2-Flex-ChrimsonR",
                        tars_identifiers=TarsVirusIdentifiers(
                            virus_tars_id="AiV222",
                            plasmid_tars_alias=["AiP222"],
                            prep_lot_number="VT222",
                        ),
                        titer=2300000000,
                    )
                ],
                dynamics=[
                    InjectionDynamics(
                        volume=1,
                        volume_unit=VolumeUnit.UL,
                        profile=InjectionProfile.PULSED,
                    ),
                ],
            )

        self.assertIn("Unmatched list sizes for injection volumes and coordinate depths", repr(e.exception))

    def test_sectioning(self):
        """Test sectioning"""

        # Updated initialization to use the new Section class
        sectioning_procedure = PlanarSectioning(
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            sections=[
                Section(
                    output_specimen_id="123456_001",
                    targeted_structure=CCFv3.MOP,
                    coordinate_system_name="BREGMA_ARI",
                    start_coordinate=Translation(
                        translation=[0.3, 0, 0],
                    ),
                    end_coordinate=Translation(
                        translation=[0.5, 0, 0],
                    ),
                ),
                Section(
                    output_specimen_id="123456_002",
                    coordinate_system_name="BREGMA_ARI",
                    start_coordinate=Translation(
                        translation=[0.5, 0, 0],
                    ),
                    end_coordinate=Translation(
                        translation=[0.7, 0, 0],
                    ),
                ),
                Section(
                    output_specimen_id="123456_003",
                    coordinate_system_name="BREGMA_ARI",
                    start_coordinate=Translation(
                        translation=[0.7, 0, 0],
                    ),
                    thickness=0.1,
                    thickness_unit=SizeUnit.MM,
                ),
            ],
            section_orientation=SectionOrientation.CORONAL,
        )
        self.assertIsNotNone(sectioning_procedure)

        # Raise error if neither end_coordinate nor thickness is provided
        with self.assertRaises(OneOfError):
            PlanarSectioning(
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
                sections=[
                    Section(
                        output_specimen_id="123456_001",
                        coordinate_system_name="BREGMA_ARI",
                        start_coordinate=Translation(
                            translation=[0.3, 0, 0],
                        ),
                    ),
                ],
                section_orientation=SectionOrientation.CORONAL,
            )

    def test_validate_identical_specimen_ids(self):
        """Test that all specimen_id fields are identical in specimen_procedures"""

        with self.assertRaises(ValidationError) as e:
            Procedures(
                subject_id="12345",
                specimen_procedures=[
                    SpecimenProcedure(
                        specimen_id="1000",
                        procedure_type="Other",
                        start_date=date.fromisoformat("2020-10-10"),
                        end_date=date.fromisoformat("2020-10-11"),
                        experimenters=["Mam Moth"],
                        protocol_id=["10"],
                        notes="some notes",
                    ),
                    SpecimenProcedure(
                        specimen_id="2000",
                        procedure_type="Other",
                        start_date=date.fromisoformat("2020-10-10"),
                        end_date=date.fromisoformat("2020-10-11"),
                        experimenters=["Mam Moth"],
                        protocol_id=["10"],
                        notes="some notes",
                    ),
                ],
            )
        expected_exception = "All specimen_id must be identical in the specimen_procedures."
        self.assertIn(expected_exception, str(e.exception))

    def test_validate_subject_specimen_ids(self):
        """Test that the subject_id and specimen_id match"""

        with self.assertRaises(ValidationError) as e:
            Procedures(
                subject_id="12345",
                specimen_procedures=[
                    SpecimenProcedure(
                        specimen_id="9999_1000",
                        procedure_type="Other",
                        start_date=date.fromisoformat("2020-10-10"),
                        end_date=date.fromisoformat("2020-10-11"),
                        experimenters=["Mam Moth"],
                        protocol_id=["10"],
                        notes="some notes",
                    )
                ],
            )
        expected_exception = "specimen_id must be an extension of the subject_id."
        self.assertIn(expected_exception, str(e.exception))

    def test_craniotomy_position_validation(self):
        """Test validation for craniotomy position"""

        # Should be okay
        craniotomy = Craniotomy(
            protocol_id="123",
            craniotomy_type=CraniotomyType.CIRCLE,
            coordinate_system_name="TestSystem",
            position=Translation(
                translation=[0.5, 1, 0, 0],
            ),
            size=2.0,
            size_unit=SizeUnit.MM,
        )
        self.assertIsNotNone(craniotomy)

        # Missing position for required craniotomy types should raise an error
        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.CIRCLE,
                coordinate_system_name="TestSystem",
                size=2.0,
                size_unit=SizeUnit.MM,
            )
        self.assertIn("Craniotomy.position must be provided for craniotomy type Circle", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.SQUARE,
                coordinate_system_name="TestSystem",
                size=2.0,
                size_unit=SizeUnit.MM,
            )
        self.assertIn("Craniotomy.position must be provided for craniotomy type Square", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.WHC,
                coordinate_system_name="TestSystem",
            )
        self.assertIn(
            "Craniotomy.position must be provided for craniotomy type Whole hemisphere craniotomy", str(e.exception)
        )

        # Should be okay for craniotomy types that do not require position
        craniotomy = Craniotomy(
            protocol_id="123",
            craniotomy_type=CraniotomyType.DHC,
        )
        self.assertIsNotNone(craniotomy)

    def test_craniotomy_system_name_if_position(self):
        """Test that coordinate_system_name is required if position is provided"""
        # Should be okay
        craniotomy = Craniotomy(
            protocol_id="123",
            craniotomy_type=CraniotomyType.CIRCLE,
            coordinate_system_name="TestSystem",
            position=Translation(
                translation=[0.5, 1, 0, 0],
            ),
            size=2.0,
            size_unit=SizeUnit.MM,
        )
        self.assertIsNotNone(craniotomy)

        # Missing coordinate_system_name for required craniotomy types should raise an error
        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.CIRCLE,
                position=Translation(
                    translation=[0.5, 1, 0, 0],
                ),
                size=2.0,
                size_unit=SizeUnit.MM,
            )
        self.assertIn(
            "Craniotomy.coordinate_system_name must be provided if Craniotomy.position is provided", str(e.exception)
        )

    def test_craniotomy_size_validation(self):
        """Test validation for craniotomy size"""

        # Should be okay
        craniotomy = Craniotomy(
            protocol_id="123",
            craniotomy_type=CraniotomyType.CIRCLE,
            coordinate_system_name="TestSystem",
            position=Translation(
                translation=[0.5, 1, 0, 0],
            ),
            size=2.0,
            size_unit=SizeUnit.MM,
        )
        self.assertIsNotNone(craniotomy)

        # Missing size for required craniotomy types should raise an error
        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.CIRCLE,
                coordinate_system_name="TestSystem",
                position=Translation(
                    translation=[0.5, 1, 0, 0],
                ),
            )
        self.assertIn("Craniotomy.size must be provided for craniotomy type Circle", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.SQUARE,
                coordinate_system_name="TestSystem",
                position=Translation(
                    translation=[0.5, 1, 0, 0],
                ),
            )
        self.assertIn("Craniotomy.size must be provided for craniotomy type Square", str(e.exception))

        # Should be okay for craniotomy types that do not require size
        craniotomy = Craniotomy(
            protocol_id="123",
            craniotomy_type=CraniotomyType.DHC,
        )
        self.assertIsNotNone(craniotomy)

    def test_check_volume_or_current(self):
        """Test validation for InjectionDynamics to ensure either volume or injection_current is provided"""

        # Should be valid with volume provided
        dynamics = InjectionDynamics(
            profile=InjectionProfile.BOLUS,
            volume=1.0,
            volume_unit=VolumeUnit.UL,
        )
        self.assertIsNotNone(dynamics)

        # Should be valid with injection_current provided
        dynamics = InjectionDynamics(
            profile=InjectionProfile.BOLUS,
            injection_current=0.5,
            injection_current_unit=CurrentUnit.UA,
        )
        self.assertIsNotNone(dynamics)

        # Should raise an error when neither volume nor injection_current is provided
        with self.assertRaises(ValueError) as e:
            InjectionDynamics(
                profile=InjectionProfile.BOLUS,
            )
        self.assertIn("Either volume or injection_current must be provided.", str(e.exception))

    def test_get_device_names(self):
        """Test get_device_names method returns correct device names"""

        # Test with no devices
        procedures = Procedures(subject_id="12345")
        self.assertEqual(procedures.get_device_names(), [])

    def test_get_device_names_with_surgery_procedures(self):
        """Test get_device_names method with nested surgery procedures"""

        device1 = Catheter(
            name="Catheter",
            catheter_port="Single",
            catheter_design="Magnetic",
            catheter_material="Naked",
        )

        config = CatheterConfig(
            device_name="Catheter",
            targeted_structure=MouseBloodVessels.CAROTID_ARTERY,
        )

        # Test with surgery containing procedures with implanted devices
        surgery_procedure = CatheterImplant(
            where_performed=Organization.AIND,
            implanted_device=device1,
            device_config=config,
        )

        procedures = Procedures(
            subject_id="12345",
            subject_procedures=[
                Surgery(
                    start_date=self.start_date,
                    experimenters=["Test Person"],
                    procedures=[surgery_procedure],
                )
            ],
        )
        device_names = procedures.get_device_names()
        self.assertIn("Catheter", device_names)
        self.assertEqual(len(device_names), 1)

    def test_procedures_addition_coordinate_system_validation(self):
        """Test that Procedures addition raises error for different coordinate systems"""

        # Create two procedures with different coordinate systems
        p1 = Procedures(
            subject_id="12345",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
        )

        p2 = Procedures(
            subject_id="12345",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,  # Different coordinate system
        )

        # Test that combining procedures with different coordinate systems raises ValueError
        with self.assertRaises(ValueError) as context:
            _ = p1 + p2

        self.assertIn("Cannot combine Procedures objects with different coordinate systems", str(context.exception))
        self.assertIn("BREGMA_ARI", str(context.exception))
        self.assertIn("BREGMA_ARID", str(context.exception))

        # Test that combining procedures with same coordinate systems works
        p3 = Procedures(
            subject_id="12345",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,  # Same coordinate system as p1
        )

        combined = p1 + p3
        self.assertEqual(combined.coordinate_system, CoordinateSystemLibrary.BREGMA_ARI)
        self.assertEqual(len(combined.subject_procedures), 0)  # Both started with empty procedures


if __name__ == "__main__":
    unittest.main()
