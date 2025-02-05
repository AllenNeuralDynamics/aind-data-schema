"""Tests metadata module"""

import json
import re
import unittest
from datetime import datetime, time, timezone
from unittest.mock import MagicMock, patch
import uuid

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.platforms import Platform
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components.devices import MousePlatform
from aind_data_schema.core.acquisition import Acquisition
from aind_data_schema.core.data_description import DataDescription, Funding
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.metadata import ExternalPlatforms, Metadata, MetadataStatus, create_metadata_json
from aind_data_schema.core.procedures import (
    IontophoresisInjection,
    NanojectInjection,
    Procedures,
    Surgery,
    ViralMaterial,
)
from aind_data_schema.core.processing import PipelineProcess, Processing
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session
from aind_data_schema.core.subject import BreedingInfo, Housing, Sex, Species, Subject

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class."""
        subject = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="12345",
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
            background_strain="C57BL/6J",
        )
        dd = DataDescription(
            label="test_data",
            modality=[Modality.ECEPHYS],
            platform=Platform.ECEPHYS,
            subject_id="123456",
            data_level="raw",
            creation_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            investigators=[PIDName(name="Jane Smith")],
        )
        procedures = Procedures(
            subject_id="12345",
        )
        processing = Processing(
            processing_pipeline=PipelineProcess(processor_full_name="Processor", data_processes=[]),
        )

        cls.sample_name = "ecephys_655019_2023-04-03_18-17-09"
        cls.sample_location = "s3://bucket/ecephys_655019_2023-04-03_18-17-09"
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
        s1 = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="123345",
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
        )
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=s1)
        self.assertEqual("ecephys_655019_2023-04-03_18-17-09", d1.name)
        self.assertEqual("bucket", d1.location)
        self.assertEqual(MetadataStatus.VALID, d1.metadata_status)
        self.assertEqual(s1, d1.subject)

    def test_missing_subject_info(self):
        """Marks the metadata status as MISSING if a Subject model is not
        present"""

        d1 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
        )
        self.assertEqual(MetadataStatus.MISSING, d1.metadata_status)
        self.assertEqual("ecephys_655019_2023-04-03_18-17-09", d1.name)
        self.assertEqual("bucket", d1.location)

        # Assert at least a name and location are required
        with self.assertRaises(ValidationError) as e:
            Metadata()
        expected_exception_message = (
            "2 validation errors for Metadata\n"
            "name\n"
            "  Field required [type=missing, input_value={}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "location\n"
            "  Field required [type=missing, input_value={}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing"
        )
        self.assertEqual(expected_exception_message, str(e.exception))

    def test_invalid_core_models(self):
        """Test that invalid models don't raise an error, but marks the
        metadata_status as INVALID"""

        # Invalid subject model
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=Subject.model_construct())
        self.assertEqual(MetadataStatus.INVALID, d1.metadata_status)

        # Valid subject model, but invalid procedures model
        s2 = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="123345",
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
        )
        d2 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            subject=s2,
            procedures=Procedures.model_construct(injection_materials=["some materials"]),
        )
        self.assertEqual(MetadataStatus.INVALID, d2.metadata_status)

        # Tests constructed via dictionary
        d3 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            subject=json.loads(Subject.model_construct().model_dump_json()),
        )
        self.assertEqual(MetadataStatus.INVALID, d3.metadata_status)

    def test_default_file_extension(self):
        """Tests that the default file extension used is as expected."""
        self.assertEqual(".nd.json", Metadata._FILE_EXTENSION.default)

    def test_validate_smartspim_metadata(self):
        """Tests that smartspim validator works as expected"""
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct()
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])

        # Tests missing metadata
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.SMARTSPIM,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.SPIM],
                ),
                procedures=Procedures.model_construct(subject_procedures=[surgery1]),
                acquisition=Acquisition.model_construct(),
            )
        self.assertIn(
            "SPIM metadata missing required file: subject",
            str(context.exception),
        )

        # Tests excluded metadata getting included
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.SMARTSPIM,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.SPIM],
                ),
                subject=Subject.model_construct(),
                session=Session.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery1]),
                acquisition=Acquisition.model_construct(),
            )
        self.assertIn(
            "SPIM metadata includes excluded file: session",
            str(context.exception),
        )

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.SMARTSPIM,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.SPIM],
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                acquisition=Acquisition.model_construct(),
                instrument=Instrument.model_construct(),
                processing=Processing.model_construct(),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_multi_modal_metadata(self):
        """Test that metadata with multiple modalities correctly prioritizes REQUIRED > OPTIONAL > EXCLUDED"""
        # Tests excluded metadata getting included
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct(injection_materials=[viral_material])
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])

        mouse_platform = MousePlatform.model_construct(name="platform1")
        rig = Rig.model_construct(rig_id="123_EPHYS1_20220101", mouse_platform=mouse_platform)
        session = Session.model_construct(rig_id="123_EPHYS1_20220101", mouse_platform_name="platform1")

        m = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            data_description=DataDescription.model_construct(
                label="some label",
                platform=Platform.SMARTSPIM,
                creation_time=time(12, 12, 12),
                modality=[Modality.BEHAVIOR, Modality.SPIM],  # technically this is impossible, but we need to test it
            ),
            subject=Subject.model_construct(),
            session=session,  # SPIM excludes session, but BEHAVIOR requires it
            procedures=Procedures.model_construct(subject_procedures=[surgery1]),
            acquisition=Acquisition.model_construct(),
            rig=rig,
            processing=Processing.model_construct(),
            instrument=Instrument.model_construct(),
        )
        self.assertIsNotNone(m)

    def test_validate_ecephys_metadata(self):
        """Tests that ecephys validator works as expected"""
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct()
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])

        # Tests missing metadata
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.ECEPHYS,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.ECEPHYS],
                ),
                procedures=Procedures.model_construct(subject_procedures=[surgery1]),
                rig=Rig.model_construct(),
            )
        self.assertIn(
            "ECEPHYS metadata missing required file: subject",
            str(context.exception),
        )

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.ECEPHYS,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.ECEPHYS],
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                rig=Rig.model_construct(),
                processing=Processing.model_construct(),
                session=Session.model_construct(),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_validate_underscore_modality(self):
        """Tests that ecephys validator works as expected"""
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct(injection_materials=[viral_material])
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])
        mouse_platform = MousePlatform.model_construct(name="platform1")
        rig = Rig.model_construct(rig_id="123_EPHYS2_20230101", mouse_platform=mouse_platform)
        session = Session.model_construct(rig_id="123_EPHYS2_20230101", mouse_platform_name="platform1")

        # Tests missing metadata
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        m = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            data_description=DataDescription.model_construct(
                label="some label",
                platform=Platform.ECEPHYS,
                creation_time=time(12, 12, 12),
                modality=[Modality.BEHAVIOR_VIDEOS],
            ),
            subject=Subject.model_construct(),
            procedures=Procedures.model_construct(subject_procedures=[surgery1]),
            rig=rig,
            session=session,
        )
        self.assertIsNotNone(m)

    def test_validate_rig_session_compatibility(self):
        """Tests that rig/session compatibility validator works as expected"""
        mouse_platform = MousePlatform.model_construct(name="platform1")
        rig = Rig.model_construct(rig_id="123_EPHYS1_20220101", mouse_platform=mouse_platform)
        session = Session.model_construct(rig_id="123_EPHYS2_20230101", mouse_platform_name="platform2")
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.ECEPHYS,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.ECEPHYS],
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(),
                rig=rig,
                processing=Processing.model_construct(),
                session=session,
            )
        self.assertIn(
            "Rig ID in session 123_EPHYS2_20230101 does not match the rig's 123_EPHYS1_20220101.",
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
        m_dict.pop("id")

        m2 = Metadata(**m_dict)

        self.assertIsNotNone(m2)

    def test_create_from_core_jsons(self):
        """Tests metadata json can be created with valid inputs"""
        core_jsons = {
            "subject": self.subject_json,
            "data_description": None,
            "procedures": self.procedures_json,
            "session": None,
            "rig": None,
            "processing": self.processing_json,
            "acquisition": None,
            "instrument": None,
            "quality_control": None,
        }
        expected_md = Metadata(
            name=self.sample_name,
            location=self.sample_location,
            subject=self.subject,
            procedures=self.procedures,
            processing=self.processing,
        )
        expected_result = json.loads(expected_md.model_dump_json(by_alias=True))
        # there are some userwarnings when creating Subject from json
        result = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons=core_jsons,
        )
        # check that metadata was created with expected values
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual(MetadataStatus.VALID.value, result["metadata_status"])
        self.assertEqual(self.subject_json, result["subject"])
        self.assertEqual(self.procedures_json, result["procedures"])
        self.assertEqual(self.processing_json, result["processing"])
        self.assertIsNone(result["acquisition"])
        # also check the other fields
        # small hack to mock the _id, created, and last_modified fields
        expected_result["_id"] = result["_id"]
        expected_result["created"] = result["created"]
        expected_result["last_modified"] = result["last_modified"]
        self.assertDictEqual(expected_result, result)

    def test_create_from_core_jsons_optional_overwrite(self):
        """Tests metadata json creation with created and external links"""
        created = datetime(2024, 10, 31, 12, 0, 0, tzinfo=timezone.utc)
        external_links = {
            ExternalPlatforms.CODEOCEAN.value: ["123", "abc"],
        }
        result = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons={
                "subject": self.subject_json,
            },
            optional_created=created,
            optional_external_links=external_links,
        )
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual("2024-10-31T12:00:00Z", result["created"])
        self.assertEqual(external_links, result["external_links"])

    @patch("logging.warning")
    def test_create_from_core_jsons_invalid(self, mock_warning: MagicMock):
        """Tests that metadata json is marked invalid if there are errors"""
        # data_description triggers cross-validation of other fields to fail
        core_jsons = {
            "subject": self.subject_json,
            "data_description": self.dd_json,
            "procedures": self.procedures_json,
            "session": None,
            "rig": None,
            "processing": self.processing_json,
            "acquisition": None,
            "instrument": None,
            "quality_control": None,
        }
        result = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons=core_jsons,
        )
        # check that metadata was still created
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual(self.subject_json, result["subject"])
        self.assertEqual(self.dd_json, result["data_description"])
        self.assertEqual(self.procedures_json, result["procedures"])
        self.assertEqual(self.processing_json, result["processing"])
        self.assertIsNone(result["acquisition"])
        # check that metadata was marked as invalid
        self.assertEqual(MetadataStatus.INVALID.value, result["metadata_status"])
        mock_warning.assert_called_once()
        self.assertIn("Issue with metadata construction!", mock_warning.call_args_list[0].args[0])

    def test_last_modified(self):
        """Test that the last_modified field enforces timezones"""
        m = Metadata.model_construct(
            name="name",
            location="location",
            id=uuid.uuid4(),
        )
        m_dict = m.model_dump(by_alias=True)

        # Test that naive datetime is coerced to timezone-aware datetime
        date = "2022-11-22T08:43:00"
        date_with_timezone = datetime.fromisoformat(date).astimezone()
        m_dict["last_modified"] = "2022-11-22T08:43:00"
        m2 = Metadata(**m_dict)
        self.assertIsNotNone(m2)
        self.assertEqual(m2.last_modified, date_with_timezone)

        # Also check that last_modified is now in UTC
        self.assertEqual(m2.last_modified.tzinfo, timezone.utc)

        # Test that timezone-aware datetime is not coerced
        date_minus = "2022-11-22T08:43:00-07:00"
        m_dict["last_modified"] = date_minus
        m3 = Metadata(**m_dict)
        self.assertIsNotNone(m3)
        self.assertEqual(m3.last_modified, datetime.fromisoformat(date_minus))

        # Test that UTC datetime is not coerced
        date_utc = "2022-11-22T08:43:00+00:00"
        m_dict["last_modified"] = date_utc
        m4 = Metadata(**m_dict)
        self.assertIsNotNone(m4)
        self.assertEqual(m4.last_modified, datetime.fromisoformat(date_utc))

        def roundtrip_lm(model):
            """Helper function to roundtrip last_modified field"""
            model_json = model.model_dump_json(by_alias=True)
            model_dict = json.loads(model_json)
            return model_dict["last_modified"]

        # Test that the output looks right
        self.assertEqual(m.last_modified.isoformat().replace("+00:00", "Z"), roundtrip_lm(m))
        self.assertEqual("2022-11-22T15:43:00Z", roundtrip_lm(m3))
        self.assertEqual("2022-11-22T08:43:00Z", roundtrip_lm(m4))


if __name__ == "__main__":
    unittest.main()
