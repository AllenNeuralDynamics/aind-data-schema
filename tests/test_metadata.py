"""Tests metadata module"""

import json
import re
import unittest
from datetime import datetime, time, timezone
from unittest.mock import MagicMock, call, patch
import uuid

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components.devices import (
    Device,
    EphysAssembly,
    EphysProbe,
    LickSensorType,
    Manipulator,
    MotorizedStage,
    MousePlatform,
    Objective,
    RewardDelivery,
    RewardSpout,
    SpoutSide,
    ScanningStage,
    Laser,
)
from aind_data_schema.components.identifiers import Person, Code
from aind_data_schema.core.acquisition import Acquisition, SubjectDetails
from aind_data_schema.core.data_description import DataDescription, Funding
from aind_data_schema.core.metadata import ExternalPlatforms, Metadata, MetadataStatus, create_metadata_json
from aind_data_schema.core.procedures import (
    IontophoresisInjection,
    NanojectInjection,
    Procedures,
    Surgery,
    ViralMaterial,
)
from aind_data_schema.core.processing import Processing, DataProcess, ProcessName, ProcessStage
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.subject import BreedingInfo, Housing, Sex, Species, Subject
from tests.resources.spim_instrument import inst
from tests.resources.ephys_instrument import inst as ephys_inst
from pathlib import Path

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)

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
            modalities=[Modality.ECEPHYS],
            subject_id="123456",
            data_level="raw",
            creation_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            investigators=[Person(name="Jane Smith")],
        )
        procedures = Procedures(
            subject_id="12345",
        )
        processing = Processing(
            data_processes=[
                DataProcess(
                    experimenters=[Person(name="Dr. Dan")],
                    name=ProcessName.ANALYSIS,
                    stage=ProcessStage.ANALYSIS,
                    input_location="/path/to/inputs",
                    output_location="/path/to/outputs",
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
        d1 = Metadata(name="655019_2023-04-03T181709", location="bucket", subject=s1)
        self.assertEqual("655019_2023-04-03T181709", d1.name)
        self.assertEqual("bucket", d1.location)
        self.assertEqual(MetadataStatus.VALID, d1.metadata_status)
        self.assertEqual(s1, d1.subject)

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
        d1 = Metadata(name="655019_2023-04-03T181709", location="bucket", subject=Subject.model_construct())
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

    def test_validate_smartspim_metadata(self):
        """Tests that smartspim validator works as expected"""
        nano_inj = NanojectInjection.model_construct()

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=time(12, 12, 12),
                    modalities=[Modality.SPIM],
                    subject_id="655019",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                acquisition=Acquisition.model_construct(),
                instrument=inst,
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

        objective = Objective(
            name="TLX Objective",
            numerical_aperture=0.2,
            magnification=3.6,
            immersion="multi",
            manufacturer=Organization.THORLABS,
            model="TL4X-SAP",
            notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
        )

        reward_delivery = RewardDelivery(
            reward_spouts=[
                RewardSpout(
                    name="Left spout",
                    side=SpoutSide.LEFT,
                    spout_diameter=1.2,
                    solenoid_valve=Device(name="Solenoid Left"),
                    lick_sensor=Device(
                        name="Janelia_Lick_Detector Left",
                        manufacturer=Organization.JANELIA,
                    ),
                    lick_sensor_type=LickSensorType("Capacitive"),
                ),
                RewardSpout(
                    name="Right spout",
                    side=SpoutSide.RIGHT,
                    spout_diameter=1.2,
                    solenoid_valve=Device(name="Solenoid Right"),
                    lick_sensor=Device(
                        name="Janelia_Lick_Detector Right",
                        manufacturer=Organization.JANELIA,
                    ),
                    lick_sensor_type=LickSensorType("Capacitive"),
                ),
            ],
            stage_type=MotorizedStage(
                name="NewScaleMotor for LickSpouts",
                serial_number="xxxx",  # grabbing from GUI/SettingFiles
                manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                travel=15.0,  # unit is mm
                firmware=(
                    "https://github.com/AllenNeuralDynamics/python-newscale,branch: axes-on-target,commit #7c17497"
                ),
            ),
        )
        scan_stage = ScanningStage(
            name="Sample stage Z",
            model="LS-50",
            manufacturer=Organization.ASI,
            stage_axis_direction="Detection axis",
            stage_axis_name="Z",
            travel=50,
        )

        inst = Instrument.model_construct(
            instrument_id="123_EPHYS1_20220101",
            modalities=[Modality.BEHAVIOR, Modality.SPIM],
            components=[objective, reward_delivery, mouse_platform, scan_stage, laser],
        )
        acquisition = Acquisition.model_construct(instrument_id="123_EPHYS1_20220101", mouse_platform_name="platform1")

        m = Metadata(
            name="655019_2023-04-03T181709",
            location="bucket",
            data_description=DataDescription.model_construct(
                subject_id="655019",
                creation_time=time(12, 12, 12),
                modalities=[Modality.BEHAVIOR, Modality.SPIM],  # technically this is impossible, but we need to test it
            ),
            subject=Subject.model_construct(),
            acquisition=acquisition,  # SPIM excludes acquisition, but BEHAVIOR requires it
            procedures=Procedures.model_construct(subject_procedures=[surgery1]),
            instrument=inst,
            processing=Processing.model_construct(),
        )
        self.assertIsNotNone(m)

    def test_validate_ecephys_metadata(self):
        """Tests that ecephys validator works as expected"""
        nano_inj = NanojectInjection.model_construct()

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        modalities = [Modality.ECEPHYS]
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=time(12, 12, 12),
                    modalities=modalities,
                    subject_id="655019",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                instrument=ephys_inst,
                processing=Processing.model_construct(),
                acquisition=Acquisition.model_construct(
                    instrument_id="323_EPHYS1_20231003",
                    subject_details=SubjectDetails.model_construct()
                ),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_validate_instrument_session_compatibility(self):
        """Tests that instrument/session compatibility validator works as expected"""

        modalities = [Modality.ECEPHYS]
        mouse_platform = MousePlatform.model_construct(name="platform1")
        inst = Instrument.model_construct(
            instrument_id="123_EPHYS1_20220101",
            modalities=modalities,
            components=[ephys_assembly, mouse_platform],
        )
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=time(12, 12, 12),
                    modalities=modalities,
                    subject_id="655019",
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
            "Instrument ID in session 123_EPHYS2_20230101 does not match the instrument's 123_EPHYS1_20220101.",
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
            "data_description": self.dd_json,
            "procedures": self.procedures_json,
            "session": None,
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
        # there are some userwarnings when creating Subject from json
        with self.assertWarns(UserWarning):
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
        # small hack to mock the _id, created, and last_modified fields
        expected_result["_id"] = result["_id"]
        expected_result["created"] = result["created"]
        expected_result["last_modified"] = result["last_modified"]
        self.assertDictEqual(expected_result, result)

    def test_create_from_core_jsons_invalid(self):
        """Tests metadata json creation with invalid inputs"""
        core_jsons = {
            "subject": self.subject_json,
            "data_description": None,
            "procedures": self.procedures_json,
            "session": None,
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
        created = datetime(2024, 10, 31, 12, 0, 0, tzinfo=timezone.utc)
        external_links = {
            ExternalPlatforms.CODEOCEAN.value: ["123", "abc"],
        }
        # there are some userwarnings when creating from json
        with self.assertWarns(UserWarning):
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
    @patch("aind_data_schema.core.metadata.is_dict_corrupt")
    def test_create_from_core_jsons_corrupt(self, mock_is_dict_corrupt: MagicMock, mock_warning: MagicMock):
        """Tests metadata json creation ignores corrupt core jsons"""
        # mock corrupt procedures and processing
        mock_is_dict_corrupt.side_effect = lambda x: (x == self.procedures_json or x == self.processing_json)
        core_jsons = {
            "subject": self.subject_json,
            "data_description": None,
            "procedures": self.procedures_json,
            "session": None,
            "instrument": None,
            "processing": self.processing_json,
            "acquisition": None,
            "quality_control": None,
        }
        # there are some userwarnings when creating Subject from json
        with self.assertWarns(UserWarning):
            result = create_metadata_json(
                name=self.sample_name,
                location=self.sample_location,
                core_jsons=core_jsons,
            )
        # check that metadata was still created
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual(self.subject_json, result["subject"])
        self.assertIsNone(result["acquisition"])
        self.assertEqual(MetadataStatus.VALID.value, result["metadata_status"])
        # check that corrupt core jsons were ignored
        self.assertIsNone(result["procedures"])
        self.assertIsNone(result["processing"])
        mock_warning.assert_has_calls(
            [
                call("Provided processing is corrupt! It will be ignored."),
                call("Provided procedures is corrupt! It will be ignored."),
            ],
            any_order=True,
        )

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
