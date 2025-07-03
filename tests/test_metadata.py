"""Tests metadata module"""

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.species import Strain
from pydantic import ValidationError

from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.devices import EphysAssembly, EphysProbe, Laser, Manipulator
from aind_data_schema.components.identifiers import Code, Database, Person
from aind_data_schema.components.subjects import BreedingInfo, Housing, MouseSubject, Sex, Species
from aind_data_schema.components.surgery_procedures import BrainInjection
from aind_data_schema.core.acquisition import Acquisition, AcquisitionSubjectDetails, DataStream
from aind_data_schema.core.data_description import DataDescription, Funding
from aind_data_schema_models.data_name_patterns import DataLevel
from aind_data_schema.components.connections import Connection
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.metadata import Metadata, create_metadata_json
from aind_data_schema.core.procedures import Procedures, Surgery
from aind_data_schema.core.processing import DataProcess, Processing, ProcessName, ProcessStage
from aind_data_schema.core.subject import Subject
from examples.aibs_smartspim_instrument import inst as spim_inst
from examples.ephys_instrument import inst as ephys_inst
from aind_data_schema.components.subject_procedures import TrainingProtocol
from aind_data_schema.core.acquisition import StimulusEpoch

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
        cls.spim_instrument = spim_inst

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
                acquisition=Acquisition.model_construct(subject_details=AcquisitionSubjectDetails.model_construct()),
                instrument=self.spim_instrument,
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
                    instrument_id="323_EPHYS1_20231003", subject_details=AcquisitionSubjectDetails.model_construct()
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
                    subject_details=AcquisitionSubjectDetails.model_construct(mouse_platform_name="platform1"),
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
        self.assertIsNotNone(metadata)

    def test_create_from_core_jsons_optional_overwrite(self):
        """Tests metadata json creation with created and external links"""
        other_identifiers = {
            Database.CODEOCEAN.value: ["123", "abc"],
        }
        result = create_metadata_json(
            name=self.sample_name,
            location=self.sample_location,
            core_jsons={
                "subject": self.subject_json,
            },
            other_identifiers=other_identifiers,
        )
        self.assertEqual(self.sample_name, result["name"])
        self.assertEqual(self.sample_location, result["location"])
        self.assertEqual(other_identifiers, result["other_identifiers"])

    def test_validate_expected_files_by_modality(self):
        """Tests that warnings are issued when metadata is missing required files"""
        # Test case where required files are missing for 'subject'
        with self.assertWarns(UserWarning) as w:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                subject=self.subject,
                # Missing required files: data_description, procedures, instrument, acquisition
            )

        warning_messages = [str(warning.message) for warning in w.warnings]
        self.assertIn("Metadata missing required file: data_description", warning_messages)
        self.assertIn("Metadata missing required file: procedures", warning_messages)
        self.assertIn("Metadata missing required file: instrument", warning_messages)
        self.assertIn("Metadata missing required file: acquisition", warning_messages)

        # Test case where no required files exist
        with self.assertWarns(UserWarning) as w:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                # No required files provided
            )

        warning_messages = [str(warning.message) for warning in w.warnings]
        self.assertIn(
            "Metadata must contain at least one of the following files: ['subject', 'processing', 'model']",
            warning_messages,
        )

    def test_validate_acquisition_connections(self):
        """Tests that acquisition connections are validated correctly."""
        # Case where all connection devices are present in instrument components
        instrument = Instrument.model_construct(
            instrument_id="Test",
            components=[
                EphysProbe.model_construct(name="Probe A"),
                Laser.model_construct(name="Laser A"),
            ],
            modalities=[],
        )
        acquisition = Acquisition.model_construct(
            instrument_id="Test",
            data_streams=[
                DataStream.model_construct(active_devices=["Probe A", "Laser A"], modalities=[], configurations=[]),
            ],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )
        metadata = Metadata(
            name="Test Metadata",
            location="Test Location",
            instrument=instrument,
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata)

        # Case where connection devices are missing
        acquisition = Acquisition.model_construct(
            instrument_id="Test",
            data_streams=[
                DataStream.model_construct(
                    active_devices=["Probe A", "Laser A"],
                    modalities=[],
                    configurations=[],
                    connections=[Connection(device_names=["Probe A", "Missing Device"], connection_data={})],
                ),
            ],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )
        with self.assertRaises(ValueError) as context:
            Metadata(
                name="Test Metadata",
                location="Test Location",
                instrument=instrument,
                acquisition=acquisition,
            )
        self.assertIn(
            "Connection 'object_type='Connection' device_names=['Probe A', 'Missing Device'] connection_data={}'",
            str(context.exception),
        )

    def test_validate_acquisition_active_devices(self):
        """Tests that acquisition active devices are validated correctly."""
        # Case where all active devices are present in instrument components
        instrument = Instrument.model_construct(
            instrument_id="Test",
            components=[
                EphysProbe.model_construct(name="Probe A"),
                Laser.model_construct(name="Laser A"),
            ],
            modalities=[],
        )
        acquisition = Acquisition.model_construct(
            instrument_id="Test",
            data_streams=[
                DataStream.model_construct(active_devices=["Probe A", "Laser A"], modalities=[], configurations=[]),
            ],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )
        metadata = Metadata(
            name="Test Metadata",
            location="Test Location",
            instrument=instrument,
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata)

        # Case where active devices are missing from both instrument and procedures
        acquisition = Acquisition.model_construct(
            instrument_id="Test",
            data_streams=[
                DataStream.model_construct(
                    active_devices=["Probe A", "Missing Device"], modalities=[], configurations=[]
                ),
            ],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )
        with self.assertRaises(ValueError) as context:
            Metadata(
                name="Test Metadata",
                location="Test Location",
                instrument=instrument,
                acquisition=acquisition,
            )
        self.assertIn(
            "Active devices '{'Missing Device'}' were not found in either the Instrument.components or "
            "in an individual procedure's implanted_device field.",
            str(context.exception),
        )

    def test_validate_training_protocol_references(self):
        """Tests that training protocol references are validated correctly."""

        # Case where training protocol references match
        training_protocol = TrainingProtocol.model_construct(training_name="Protocol A")
        procedures = Procedures.model_construct(subject_procedures=[training_protocol])
        stimulus_epoch = StimulusEpoch.model_construct(training_protocol_name="Protocol A")
        acquisition = Acquisition.model_construct(
            instrument_id="Test",
            stimulus_epochs=[stimulus_epoch],
            data_streams=[],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )

        metadata = Metadata(
            name="Test Metadata",
            location="Test Location",
            procedures=procedures,
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata)

        # Case where training protocol reference doesn't match
        stimulus_epoch_invalid = StimulusEpoch.model_construct(training_protocol_name="Missing Protocol")
        acquisition_invalid = Acquisition.model_construct(
            instrument_id="Test",
            stimulus_epochs=[stimulus_epoch_invalid],
            data_streams=[],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )

        with self.assertWarns(UserWarning) as w:
            metadata = Metadata(
                name="Test Metadata",
                location="Test Location",
                procedures=procedures,
                acquisition=acquisition_invalid,
            )

        warning_messages = [str(warning.message) for warning in w.warnings]
        self.assertIn(
            (
                "Training protocol 'Missing Protocol' in StimulusEpoch not found in Procedures."
                " Available protocols: ['Protocol A']"
            ),
            warning_messages,
        )
        self.assertIsNotNone(metadata)

        # Case where no training protocols exist in procedures
        procedures_empty = Procedures.model_construct(subject_procedures=[])
        with self.assertWarns(UserWarning) as w:
            metadata = Metadata(
                name="Test Metadata",
                location="Test Location",
                procedures=procedures_empty,
                acquisition=acquisition_invalid,
            )

        warning_messages = [str(warning.message) for warning in w.warnings]
        self.assertIn(
            (
                "Training protocol 'Missing Protocol' in StimulusEpoch not found in Procedures. "
                "Available protocols: []"
            ),
            warning_messages,
        )
        self.assertIsNotNone(metadata)

        # Case where stimulus epoch has no training protocol name (should pass)
        stimulus_epoch_none = StimulusEpoch.model_construct(training_protocol_name=None)
        acquisition_none = Acquisition.model_construct(
            instrument_id="Test",
            data_streams=[],
            stimulus_epochs=[stimulus_epoch_none],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )

        metadata_none = Metadata(
            name="Test Metadata",
            location="Test Location",
            procedures=procedures,
            acquisition=acquisition_none,
        )
        self.assertIsNotNone(metadata_none)

        # Case where acquisition is None (should pass)
        metadata_no_acquisition = Metadata(
            name="Test Metadata",
            location="Test Location",
            procedures=procedures,
        )
        self.assertIsNotNone(metadata_no_acquisition)

        # Case where procedures is None (should pass)
        metadata_no_procedures = Metadata(
            name="Test Metadata",
            location="Test Location",
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata_no_procedures)

    def test_validate_data_description_name_time_consistency(self):
        """Tests that data_description.name creation_time is on or after midnight
        on the same day as acquisition.acquisition_end_time"""

        # Create a specific datetime for testing
        test_datetime = datetime(2023, 4, 3, 18, 17, 9, tzinfo=timezone.utc)

        # Create a data description with a name that should match the acquisition end time
        data_description = DataDescription(
            creation_time=test_datetime,
            modalities=[Modality.ECEPHYS],
            subject_id="655019",
            data_level=DataLevel.RAW,
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS)],
            investigators=[Person(name="Test Person")],
            project_name="Test Project",
        )

        # Create acquisition with matching end time using model_construct
        acquisition = Acquisition.model_construct(
            instrument_id="Test",
            acquisition_start_time=datetime(2023, 4, 3, 18, 0, 0, tzinfo=timezone.utc),
            acquisition_end_time=test_datetime,
            data_streams=[],
            subject_details=AcquisitionSubjectDetails.model_construct(),
        )

        # This should pass - creation time is exactly at acquisition end time
        metadata_matching = Metadata(
            name="Test Metadata",
            location="Test Location",
            data_description=data_description,
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata_matching)

        # Test with creation time later on the same day - should pass
        later_same_day = datetime(2023, 4, 3, 23, 59, 59, tzinfo=timezone.utc)
        data_description_later = DataDescription(
            creation_time=later_same_day,
            modalities=[Modality.ECEPHYS],
            subject_id="655019",
            data_level=DataLevel.RAW,
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS)],
            investigators=[Person(name="Test Person")],
            project_name="Test Project",
        )
        
        metadata_later_same_day = Metadata(
            name="Test Metadata",
            location="Test Location",
            data_description=data_description_later,
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata_later_same_day)

        # Test with creation time on the next day - should pass
        next_day = datetime(2023, 4, 4, 0, 0, 1, tzinfo=timezone.utc)
        data_description_next_day = DataDescription(
            creation_time=next_day,
            modalities=[Modality.ECEPHYS],
            subject_id="655019",
            data_level=DataLevel.RAW,
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS)],
            investigators=[Person(name="Test Person")],
            project_name="Test Project",
        )
        
        metadata_next_day = Metadata(
            name="Test Metadata",
            location="Test Location",
            data_description=data_description_next_day,
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata_next_day)

        # Test with creation time before midnight of acquisition day - should fail
        before_midnight = datetime(2023, 4, 2, 23, 59, 59, tzinfo=timezone.utc)
        data_description_before = DataDescription(
            creation_time=before_midnight,
            modalities=[Modality.ECEPHYS],
            subject_id="655019",
            data_level=DataLevel.RAW,
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS)],
            investigators=[Person(name="Test Person")],
            project_name="Test Project",
        )

        # This should fail - creation time is before the acquisition day
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="Test Metadata",
                location="Test Location",
                data_description=data_description_before,
                acquisition=acquisition,
            )
        self.assertIn("Creation time from data_description.name", str(context.exception))
        self.assertIn("must be on or after midnight of the acquisition day", str(context.exception))

        # Test case where data_description is None (should pass)
        metadata_no_data_desc = Metadata(
            name="Test Metadata",
            location="Test Location",
            acquisition=acquisition,
        )
        self.assertIsNotNone(metadata_no_data_desc)

        # Test case where acquisition is None (should pass)
        metadata_no_acquisition = Metadata(
            name="Test Metadata",
            location="Test Location",
            data_description=data_description,
        )
        self.assertIsNotNone(metadata_no_acquisition)


if __name__ == "__main__":
    unittest.main()
