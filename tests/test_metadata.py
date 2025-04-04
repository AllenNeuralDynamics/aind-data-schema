"""Tests metadata module"""

import json
import unittest
from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import ValidationError

from aind_data_schema.components.devices import (
    EphysAssembly,
    EphysProbe,
    Manipulator,
    Laser,
)
from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.identifiers import Person, Code, ExternalPlatforms
from aind_data_schema.core.acquisition import Acquisition, SubjectDetails
from aind_data_schema.core.data_description import DataDescription, Funding
from aind_data_schema.core.metadata import Metadata, MetadataStatus, create_metadata_json
from aind_data_schema.core.procedures import (
    BrainInjection,
    Procedures,
    Surgery,
)
from aind_data_schema.core.processing import Processing, DataProcess, ProcessName, ProcessStage
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.subject import Subject
from aind_data_schema.components.subjects import BreedingInfo, Housing, Sex, Species, MouseSubject

from pathlib import Path
from tests.resources.spim_instrument import inst
from tests.resources.ephys_instrument import inst as ephys_inst

from aind_data_schema_models.species import Strain


EXAMPLES_DIR = Path(__file__).parents[1] / "examples"
EPHYS_INST_JSON = EXAMPLES_DIR / "ephys_instrument.json"
EPHYS_SESSION_JSON = EXAMPLES_DIR / "ephys_acquisition.json"

ephys_assembly = EphysAssembly(
    probes=[EphysProbe(probe_model="Neuropixels 1.0", name="Probe A")],
    manipulator=Manipulator(
        name="Probe manipulator",
        manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
        serial_number="4321",
    ),
    name="Ephys_assemblyA",
)

laser = Laser(
    manufacturer=Organization.HAMAMATSU,
    serial_number="1234",
    name="Laser A",
    wavelength=488,
)

t = datetime.fromisoformat("2024-09-13T14:00:00")


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class."""
        cls.spim_instrument = inst

        subject = Subject(
            subject_id="123456",
            subject_details=MouseSubject(
                species=Species.MUS_MUSCULUS,
                strain=Strain.C57BL_6J,
                sex=Sex.MALE,
                date_of_birth=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc).date(),
                source=Organization.AI,
                breeding_info=BreedingInfo(
                    breeding_group="Emx1-IRES-Cre(ND)",
                    maternal_id="546543",
                    maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
                    paternal_id="232323",
                    paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
                ),
                genotype="Emx1-IRES-Cre/wt;Camk2a-tTA/wt;Ai93(TITL-GCaMP6f)/wt",
                housing=Housing(home_cage_enrichment=["Running wheel"], cage_id="123"),
            ),
        )
        dd = DataDescription(
            modalities=[Modality.ECEPHYS],
            subject_id="123456",
            data_level="raw",
            creation_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )
        procedures = Procedures(
            subject_id="12345",
        )
        processing = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    experimenters=[Person(name="Dr. Dan")],
                    process_type=ProcessName.ANALYSIS,
                    stage=ProcessStage.ANALYSIS,
                    output_path="/path/to/outputs",
                    start_date_time=t,
                    end_date_time=t,
                    code=Code(
                        url="https://url/for/pipeline",
                        version="0.1.1",
                    ),
                ),
            ]
        )

        cls.sample_name = "655019_2023-04-03T181709"
        cls.sample_location = "s3://bucket/655019_2023-04-03T181709"
        cls.subject = subject
        cls.dd = dd
        cls.procedures = procedures
        cls.processing = processing

        cls.subject_json = json.loads(subject.model_dump_json())
        cls.dd_json = json.loads(dd.model_dump_json())
        cls.procedures_json = json.loads(procedures.model_dump_json())
        cls.processing_json = json.loads(processing.model_dump_json())

    def test_valid_subject_info(self):
        """Tests that the record is marked as VALID if a valid subject model
        is present."""
        subject = self.subject
        d1 = Metadata(name="655019_2023-04-03T181709", location="bucket", subject=subject)
        self.assertEqual("655019_2023-04-03T181709", d1.name)
        self.assertEqual("bucket", d1.location)
        self.assertEqual(MetadataStatus.VALID, d1.metadata_status)
        self.assertEqual(subject, d1.subject)

    def test_missing_subject_info(self):
        """Marks the metadata status as MISSING if a Subject model is not
        present"""

        d1 = Metadata(
            name="655019_2023-04-03T181709",
            location="bucket",
        )
        self.assertEqual(MetadataStatus.MISSING, d1.metadata_status)
        self.assertEqual("655019_2023-04-03T181709", d1.name)
        self.assertEqual("bucket", d1.location)

        # Assert at least a name and location are required
        with self.assertRaises(ValidationError) as e:
            Metadata()

        self.assertIn("Field required", str(e.exception))
        self.assertIn("name", str(e.exception))
        self.assertIn("location", str(e.exception))

    def test_invalid_core_models(self):
        """Test that invalid models don't raise an error, but marks the
        metadata_status as INVALID"""

        # Invalid subject model
        d1 = Metadata(name="655019_2023-04-03T181709", location="bucket", subject=Subject.model_construct())
        self.assertEqual(MetadataStatus.INVALID, d1.metadata_status)

        # Valid subject model, but invalid procedures model
        s2 = Subject(
            subject_id="123345",
            subject_details=MouseSubject(
                species=Species.MUS_MUSCULUS,
                strain=Strain.C57BL_6J,
                sex=Sex.MALE,
                date_of_birth="2020-10-10",
                source=Organization.AI,
                breeding_info=BreedingInfo(
                    breeding_group="Emx1-IRES-Cre(ND)",
                    maternal_id="546543",
                    maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
                    paternal_id="232323",
                    paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
                ),
                genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)/wt",
            ),
        )
        d2 = Metadata(
            name="655019_2023-04-03T181709",
            location="bucket",
            subject=s2,
            procedures=Procedures.model_construct(injection_materials=["some materials"]),
        )
        self.assertEqual(MetadataStatus.INVALID, d2.metadata_status)

        # Tests constructed via dictionary
        d3 = Metadata(
            name="655019_2023-04-03T181709",
            location="bucket",
            subject=json.loads(Subject.model_construct().model_dump_json()),
        )
        self.assertEqual(MetadataStatus.INVALID, d3.metadata_status)

    def test_default_file_extension(self):
        """Tests that the default file extension used is as expected."""
        self.assertEqual(".nd.json", Metadata._FILE_EXTENSION.default)

    def test_injection_material_validator_spim(self):
        """Tests that the injection validator works for SPIM"""
        nano_inj = BrainInjection.model_construct()

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=datetime(2020, 12, 12, 12, 12, 12),
                    modalities=[Modality.SPIM],
                    subject_id="655019",
                    data_level="raw",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                acquisition=Acquisition.model_construct(subject_details=SubjectDetails.model_construct()),
                instrument=inst,
                processing=Processing.model_construct(),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_injection_material_validator_ephys(self):
        """Test that the injection validator works for ephys"""
        nano_inj = BrainInjection.model_construct()

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        modalities = [Modality.ECEPHYS]
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=datetime(2020, 12, 12, 12, 12, 12),
                    modalities=modalities,
                    subject_id="655019",
                    data_level="raw",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                instrument=ephys_inst,
                processing=Processing.model_construct(),
                acquisition=Acquisition.model_construct(
                    instrument_id="323_EPHYS1_20231003", subject_details=SubjectDetails.model_construct()
                ),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_validate_instrument_acquisition_compatibility(self):
        """Tests that instrument/acquisition compatibility validator works as expected"""

        modalities = [Modality.ECEPHYS]
        inst = Instrument.model_construct(
            instrument_id="123_EPHYS1_20220101",
            modalities=modalities,
            components=[ephys_assembly],
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
        )
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=datetime(2020, 12, 12, 12, 12, 12),
                    modalities=modalities,
                    subject_id="655019",
                    data_level="raw",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(),
                instrument=inst,
                processing=Processing.model_construct(),
                acquisition=Acquisition.model_construct(
                    instrument_id="123_EPHYS2_20230101",
                    subject_details=SubjectDetails.model_construct(mouse_platform_name="platform1"),
                ),
            )
        self.assertIn(
            "Instrument ID in acquisition 123_EPHYS2_20230101 does not match the instrument's 123_EPHYS1_20220101.",
            str(context.exception),
        )

    def test_validate_old_schema_version(self):
        """Tests that old schema versions are ignored during validation"""
        m = Metadata.model_construct(
            name="name",
            location="location",
            id="1",
        )

        m_dict = m.model_dump()

        m_dict["schema_version"] = "0.0.0"

        m2 = Metadata(**m_dict)

        self.assertIsNotNone(m2)

    def test_create_from_core_jsons(self):
        """Tests metadata json can be created with valid inputs"""
        core_jsons = {
            "subject": self.subject_json,
            "data_description": self.dd_json,
            "procedures": self.procedures_json,
            "instrument": None,
            "processing": self.processing_json,
            "acquisition": None,
            "quality_control": None,
        }
        expected_md = Metadata(
            name=self.sample_name,
            location=self.sample_location,
            data_description=self.dd,
            subject=self.subject,
            procedures=self.procedures,
            processing=self.processing,
        )
        expected_result = json.loads(expected_md.model_dump_json(by_alias=True))
        result = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons=core_jsons,
        )
        # check that metadata was created with expected values
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual(self.subject_json, result["subject"])
        self.assertEqual(self.procedures_json, result["procedures"])
        self.assertEqual(self.processing_json, result["processing"])
        self.assertIsNone(result["acquisition"])
        self.assertEqual(MetadataStatus.VALID.value, result["metadata_status"])
        # also check the other fields
        self.assertDictEqual(expected_result, result)

    def test_create_from_core_jsons_invalid(self):
        """Tests metadata json creation with invalid inputs"""
        core_jsons = {
            "subject": self.subject_json,
            "data_description": None,
            "procedures": self.procedures_json,
            "instrument": Instrument.model_construct().model_dump(),
            "processing": Procedures.model_construct(injection_materials=["some materials"]).model_dump(),
            "acquisition": None,
            "quality_control": None,
        }
        # invalid core_jsons
        metadata = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons=core_jsons,
        )
        self.assertEqual(MetadataStatus.INVALID.value, metadata["metadata_status"])

    def test_create_from_core_jsons_optional_overwrite(self):
        """Tests metadata json creation with created and external links"""
        external_links = {
            ExternalPlatforms.CODEOCEAN.value: ["123", "abc"],
        }
        result = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons={
                "subject": self.subject_json,
            },
            optional_external_links=external_links,
        )
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual(external_links, result["external_links"])


if __name__ == "__main__":
    unittest.main()
