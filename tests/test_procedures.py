""" test Procedures """

import unittest
from datetime import date

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import TimeUnit, ConcentrationUnit, VolumeUnit
from pydantic import ValidationError

from aind_data_schema.components.devices import FiberProbe
from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.procedures import (
    FiberImplant,
    BrainInjection,
    NonViralMaterial,
    OphysProbe,
    Procedures,
    Sectioning,
    SpecimenProcedure,
    Surgery,
    TarsVirusIdentifiers,
    ViralMaterial,
    InjectionDynamics,
    InjectionProfile,
    Injection,
    Craniotomy,
    CraniotomyType,
    HCRSeries,
)
from aind_data_schema_models.brain_atlas import CCFStructure
from aind_data_schema.components.coordinates import (
    Coordinate,
    Origin,
    Rotation,
    CoordinateSystemLibrary,
)
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.mouse_anatomy import InjectionTargets
from aind_data_schema_models.units import SizeUnit, CurrentUnit


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

    def test_injection_material_check(self):
        """Check for validation error when injection_materials is empty"""

        with self.assertRaises(ValidationError) as e:
            Procedures(
                subject_id="12345",
                subject_procedures=[
                    Surgery(
                        start_date=self.start_date,
                        experimenters=[Person(name="Mam Moth")],
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

    def test_injection_material_none(self):
        """Check for validation error when injection_materials is None"""
        with self.assertRaises(ValidationError) as e:
            Procedures(
                subject_id="12345",
                subject_procedures=[
                    Surgery(
                        start_date=self.start_date,
                        experimenters=[Person(name="Mam Moth")],
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
                                target=InjectionTargets.RETRO_ORBITAL,
                                relative_position=[AnatomicalRelative.LEFT],
                            ),
                        ],
                    )
                ],
            )

        self.assertIn("injection_materials", repr(e.exception))

    def test_injection_materials_list(self):
        """Valid injection_materials list"""

        p = Procedures(
            subject_id="12345",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            subject_procedures=[
                Surgery(
                    start_date=self.start_date,
                    experimenters=[Person(name="Mam Moth")],
                    ethics_review_id="234",
                    protocol_id="123",
                    coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
                    measured_coordinates={
                        Origin.BREGMA: Coordinate(
                            system_name="BREGMA_ARI",
                            position=[0, 0, 0],
                        ),
                        Origin.LAMBDA: Coordinate(
                            system_name="BREGMA_ARI",
                            position=[-4.1, 0, 0],
                        ),
                    },
                    procedures=[
                        Injection(
                            protocol_id="134",
                            injection_materials=[
                                ViralMaterial(
                                    material_type="Virus",
                                    name="AAV2-Flex-ChrimsonR",
                                    tars_identifiers=TarsVirusIdentifiers(
                                        virus_tars_id="AiV222",
                                        plasmid_tars_alias=["AiP222"],
                                        prep_lot_number="VT222",
                                    ),
                                    titer=2300000000,
                                )
                            ],
                            target=InjectionTargets.RETRO_ORBITAL,
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
                                    material_type="Reagent",
                                    name="drug_xyz",
                                    source=Organization.AI,
                                    lot_number="12345",
                                    concentration=1,
                                    concentration_unit=ConcentrationUnit.UM,
                                )
                            ],
                            target=InjectionTargets.INTRAPERITONEAL,
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
                            injection_materials=[
                                ViralMaterial(
                                    material_type="Virus",
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
                                Coordinate(
                                    system_name="BREGMA_ARID",
                                    position=[0.5, 1, 0, 1],
                                ),
                            ],
                            target=CCFStructure.VISP6A,
                        ),
                        FiberImplant(
                            protocol_id="dx.doi.org/120.123/fkjd",
                            probes=[
                                OphysProbe(
                                    ophys_probe=FiberProbe(
                                        name="Probe A",
                                        manufacturer=Organization.DORIC,
                                        model="8",
                                        core_diameter=2,
                                        numerical_aperture=1,
                                        ferrule_material="Ceramic",
                                        total_length=10,
                                    ),
                                    targeted_structure=CCFStructure.MOP,
                                    coordinate=Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 2, 0, 2],
                                        angles=Rotation(
                                            angles=[10, 0, 0],
                                        ),
                                    ),
                                )
                            ],
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
                experimenters=[Person(name="Mam Moth")],
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
                experimenters=[Person(name="Mam Moth")],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn("Antibody required if procedure_type is Immunolabeling", repr(e.exception))

        with self.assertRaises(ValidationError) as e:
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Hybridization Chain Reaction",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=[Person(name="Mam Moth")],
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
                experimenters=[Person(name="Mam Moth")],
                protocol_id=["10"],
                notes=None,
            )
        self.assertIn("Sectioning required if procedure_type is Sectioning", repr(e.exception))

        self.assertIsNotNone(
            SpecimenProcedure(
                specimen_id="1000",
                procedure_type="Other",
                start_date=date.fromisoformat("2020-10-10"),
                end_date=date.fromisoformat("2020-10-11"),
                experimenters=[Person(name="Mam Moth")],
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
                experimenters=[Person(name="Mam Moth")],
                protocol_id=["10"],
                notes="some extra information",
                procedure_details=[
                    HCRSeries.model_construct(),
                    Sectioning.model_construct(),
                ],
            )
        self.assertIn("SpecimenProcedure.procedure_details should only contain one type of model", repr(e.exception))

    def test_coordinate_volume_validator(self):
        """Test validator for list lengths on BrainInjection"""

        # Should be okay
        inj1 = BrainInjection(
            protocol_id="abc",
            coordinates=[
                Coordinate(
                    system_name="BREGMA_ARID",
                    position=[0.5, 1, 0, 0],
                ),
                Coordinate(
                    system_name="BREGMA_ARID",
                    position=[0.5, 1, 0, 1],
                ),
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
                    material_type="Virus",
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
                coordinates=[
                    Coordinate(
                        system_name="BREGMA_ARID",
                        position=[0.5, 1, 0, 0],
                    ),
                    Coordinate(
                        system_name="BREGMA_ARID",
                        position=[0.5, 1, 0, 1],
                    ),
                ],
                injection_materials=[
                    ViralMaterial(
                        material_type="Virus",
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

        section = Sectioning(
            number_of_slices=3,
            output_specimen_ids=["123456_001", "123456_002", "123456_003"],
            section_orientation="Coronal",
            section_thickness=0.2,
            section_distance_from_reference=0.3,
            reference=Origin.BREGMA,
            section_strategy="Whole Brain",
            targeted_structure=CCFStructure.MOP,
        )
        self.assertEqual(section.number_of_slices, len(section.output_specimen_ids))

        # Number of output ids does not match number of slices
        with self.assertRaises(ValidationError):
            Sectioning(
                number_of_slices=2,
                output_specimen_ids=["123456_001", "123456_002", "123456_003"],
                section_orientation="Coronal",
                section_thickness=0.2,
                section_distance_from_reference=0.3,
                reference=Origin.BREGMA,
                section_strategy="Whole Brain",
                targeted_structure=CCFStructure.MOP,
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
                        experimenters=[Person(name="Mam Moth")],
                        protocol_id=["10"],
                        notes="some notes",
                    ),
                    SpecimenProcedure(
                        specimen_id="2000",
                        procedure_type="Other",
                        start_date=date.fromisoformat("2020-10-10"),
                        end_date=date.fromisoformat("2020-10-11"),
                        experimenters=[Person(name="Mam Moth")],
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
                        experimenters=[Person(name="Mam Moth")],
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
            position=Coordinate(system_name="BREGMA_ARID", position=[0.5, 1, 0, 0]),
            size=2.0,
            size_unit=SizeUnit.MM,
        )
        self.assertIsNotNone(craniotomy)

        # Missing position for required craniotomy types should raise an error
        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.CIRCLE,
                size=2.0,
                size_unit=SizeUnit.MM,
            )
        self.assertIn("Craniotomy.position must be provided for craniotomy type Circle", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.SQUARE,
                size=2.0,
                size_unit=SizeUnit.MM,
            )
        self.assertIn("Craniotomy.position must be provided for craniotomy type Square", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.WHC,
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

    def test_craniotomy_size_validation(self):
        """Test validation for craniotomy size"""

        # Should be okay
        craniotomy = Craniotomy(
            protocol_id="123",
            craniotomy_type=CraniotomyType.CIRCLE,
            position=Coordinate(system_name="BREGMA_ARID", position=[0.5, 1, 0, 0]),
            size=2.0,
            size_unit=SizeUnit.MM,
        )
        self.assertIsNotNone(craniotomy)

        # Missing size for required craniotomy types should raise an error
        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.CIRCLE,
                position=Coordinate(system_name="BREGMA_ARID", position=[0.5, 1, 0, 0]),
            )
        self.assertIn("Craniotomy.size must be provided for craniotomy type Circle", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Craniotomy(
                protocol_id="123",
                craniotomy_type=CraniotomyType.SQUARE,
                position=Coordinate(system_name="BREGMA_ARID", position=[0.5, 1, 0, 0]),
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


if __name__ == "__main__":
    unittest.main()
