"""Tests methods in schema_upgrade package """

import datetime
import json
import os
import unittest
from pathlib import Path
from typing import List

from aind_data_schema.data_description import (
    DataDescription,
    DataLevel,
    Funding,
    Group,
    Institution,
    Modality,
    Platform,
    RelatedData,
)
from aind_data_schema.processing import DataProcess, PipelineProcess, Processing
from aind_data_schema.schema_upgrade.data_description_upgrade import (
    DataDescriptionUpgrade,
    FundingUpgrade,
    InstitutionUpgrade,
    ModalityUpgrade,
)
from aind_data_schema.schema_upgrade.processing_upgrade import DataProcessUpgrade, ProcessingUpgrade

DATA_DESCRIPTION_FILES_PATH = Path(__file__).parent / "resources" / "ephys_data_description"
PROCESSING_FILES_PATH = Path(__file__).parent / "resources" / "ephys_processing"


class TestDataDescriptionUpgrade(unittest.TestCase):
    """Tests methods in DataDescriptionUpgrade class"""

    @classmethod
    def setUpClass(cls):
        """Load json files before running tests."""
        data_description_files: List[str] = os.listdir(DATA_DESCRIPTION_FILES_PATH)
        data_descriptions = []
        for file_path in data_description_files:
            with open(DATA_DESCRIPTION_FILES_PATH / file_path) as f:
                contents = json.load(f)
            data_descriptions.append((file_path, DataDescription.construct(**contents)))
        cls.data_descriptions = dict(data_descriptions)

    def test_upgrades_0_3_0(self):
        """Tests data_description_0.3.0.json is mapped correctly."""
        data_description_0_3_0 = self.data_descriptions["data_description_0.3.0.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_3_0)
        # Should complain about platform being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError("
            "model='DataDescription', "
            "errors=[{"
            "'loc': ('platform',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'}"
            "])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly
        new_data_description = upgrader.upgrade(platform=Platform.ECEPHYS)
        self.assertEqual(datetime.datetime(2022, 6, 28, 10, 31, 30), new_data_description.creation_time)
        self.assertEqual("ecephys_623705_2022-06-28_10-31-30", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("623705", new_data_description.subject_id)
        self.assertEqual([], new_data_description.related_data)
        self.assertIsNone(new_data_description.data_summary)

    def test_upgrades_0_3_0_wrong_field(self):
        """Tests data_description_0.3.0_wrong_field.json is mapped correctly."""
        data_description_0_3_0 = self.data_descriptions["data_description_0.3.0_wrong_field.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_3_0)
        # Should complain about platform being None and missing data level
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError("
            "model='DataDescription', "
            "errors=[{"
            "'loc': ('platform',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly and DataLevel
        new_data_description = upgrader.upgrade(platform=Platform.ECEPHYS, data_level=DataLevel.RAW)
        self.assertEqual(datetime.datetime(2022, 7, 26, 10, 52, 15), new_data_description.creation_time)
        self.assertEqual("ecephys_624643_2022-07-26_10-52-15", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("624643", new_data_description.subject_id)
        self.assertEqual([], new_data_description.related_data)
        self.assertIsNone(new_data_description.data_summary)

        # Should also work by inputting legacy
        new_data_description2 = upgrader.upgrade(platform=Platform.ECEPHYS, data_level="raw level")
        self.assertEqual(DataLevel.RAW, new_data_description2.data_level)

        # Should fail if inputting unknown string
        with self.assertRaises(Exception) as e1:
            upgrader.upgrade(platform=Platform.ECEPHYS, data_level="asfnewnjfq")

        expected_error_message1 = (
            "ValidationError(model='DataDescription', "
            "errors=[{'loc': ('data_level',), "
            "'msg': \"'asfnewnjfq' is not a valid DataLevel\", "
            "'type': 'value_error'}])"
        )

        self.assertEqual(expected_error_message1, repr(e1.exception))

        # Should also fail if inputting wrong type
        with self.assertRaises(Exception) as e2:
            upgrader.upgrade(platform=Platform.ECEPHYS, data_level=["raw"])
        expected_error_message2 = (
            "ValidationError(model='DataDescription', "
            "errors=[{'loc': ('data_level',), "
            "'msg': '__init__() takes exactly 3 positional arguments "
            "(2 given)', 'type': 'type_error'}])"
        )

        self.assertEqual(expected_error_message2, repr(e2.exception))

        # Should work if data_level is missing in original json doc and
        # user sets it explicitly
        data_description_dict = data_description_0_3_0.dict()
        del data_description_dict["data_level"]
        data_description_0_3_0_no_data_level = DataDescription.construct(**data_description_dict)
        upgrader3 = DataDescriptionUpgrade(old_data_description_model=data_description_0_3_0_no_data_level)
        new_data_description3 = upgrader3.upgrade(platform=Platform.ECEPHYS, data_level=DataLevel.RAW)
        self.assertEqual(DataLevel.RAW, new_data_description3.data_level)

    def test_upgrades_0_4_0(self):
        """Tests data_description_0.4.0.json is mapped correctly."""
        data_description_0_4_0 = self.data_descriptions["data_description_0.4.0.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_4_0)

        # Should work by setting platform explicitly
        new_data_description = upgrader.upgrade()
        self.assertEqual(datetime.datetime(2023, 4, 13, 14, 35, 51), new_data_description.creation_time)
        self.assertEqual("ecephys_664438_2023-04-13_14-35-51", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("664438", new_data_description.subject_id)
        self.assertEqual([], new_data_description.related_data)
        self.assertIsNone(new_data_description.data_summary)

    def test_upgrades_0_6_0(self):
        """Tests data_description_0.6.0.json is mapped correctly."""
        data_description_0_6_0 = self.data_descriptions["data_description_0.6.0.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_0)

        # Should work by setting experiment type explicitly
        new_data_description = upgrader.upgrade()
        self.assertEqual(datetime.datetime(2023, 4, 10, 17, 9, 26), new_data_description.creation_time)
        self.assertEqual("ecephys_661278_2023-04-10_17-09-26", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("661278", new_data_description.subject_id)
        self.assertEqual([], new_data_description.related_data)
        self.assertIsNone(new_data_description.data_summary)

    def test_upgrades_0_6_2(self):
        """Tests data_description_0.6.2.json is mapped correctly."""
        data_description_0_6_2 = self.data_descriptions["data_description_0.6.2.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_2)

        # Should work by setting experiment type explicitly
        new_data_description = upgrader.upgrade()
        self.assertEqual(datetime.datetime(2023, 3, 23, 22, 31, 18), new_data_description.creation_time)
        self.assertEqual("661279_2023-03-23_15-31-18", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertEqual(Group.EPHYS, new_data_description.group)
        self.assertEqual(["John Doe", "Mary Smith"], new_data_description.investigators)
        self.assertEqual("mri-guided-electrophysiology", new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("661279", new_data_description.subject_id)
        self.assertEqual(
            [
                RelatedData(
                    related_data_path="\\\\allen\\aind\\scratch\\ephys\\persist\\data\\MRI\\processed\\661279",
                    relation="Contains MRI and processing used to choose insertion locations.",
                )
            ],
            new_data_description.related_data,
        )
        self.assertEqual(
            (
                "This dataset was collected to evaluate the accuracy and feasibility "
                "of the AIND MRI-guided insertion pipeline. "
                "One probe targets the retinotopic center of LGN, with drifting grating for "
                "receptive field mapping to evaluate targeting. "
                "Other targets can be evaluated in histology."
            ),
            new_data_description.data_summary,
        )

        # Testing a few edge cases
        new_dd_0_6_2 = upgrader.upgrade(modality=[Modality.ECEPHYS])
        self.assertEqual([Modality.ECEPHYS], new_dd_0_6_2.modality)
        # Blank Modality
        data_description_0_6_2.modality = None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError(model='DataDescription', "
            "errors=[{'loc': ('modality',), 'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

    def test_upgrades_0_6_2_wrong_field(self):
        """Tests data_description_0.6.2_wrong_field.json is mapped correctly."""
        data_description_0_6_2_wrong_field = self.data_descriptions["data_description_0.6.2_wrong_field.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_2_wrong_field)

        # Should complain about funder not being correct
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = "AttributeError('NOT A REAL FUNDER')"
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting funding_source explicitly
        new_data_description = upgrader.upgrade(funding_source=[Funding(funder=Institution.AIND)])
        self.assertEqual(datetime.datetime(2023, 3, 23, 22, 31, 18), new_data_description.creation_time)
        self.assertEqual("661279_2023-03-23_15-31-18", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertEqual(Group.EPHYS, new_data_description.group)
        self.assertEqual(["John Doe", "Mary Smith"], new_data_description.investigators)
        self.assertEqual("mri-guided-electrophysiology", new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("661279", new_data_description.subject_id)
        self.assertEqual(
            [
                RelatedData(
                    related_data_path="\\\\allen\\aind\\scratch\\ephys\\persist\\data\\MRI\\processed\\661279",
                    relation="Contains MRI and processing used to choose insertion locations.",
                )
            ],
            new_data_description.related_data,
        )
        self.assertEqual(
            (
                "This dataset was collected to evaluate the accuracy and feasibility "
                "of the AIND MRI-guided insertion pipeline. "
                "One probe targets the retinotopic center of LGN, with drifting grating for "
                "receptive field mapping to evaluate targeting. "
                "Other targets can be evaluated in histology."
            ),
            new_data_description.data_summary,
        )

    def test_upgrades_0_10_0(self):
        """Tests data_description_0.6.0.json is mapped correctly."""
        data_description_0_10_0 = self.data_descriptions["data_description_0.10.0.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_10_0)

        # Should work by setting experiment type explicitly
        new_data_description = upgrader.upgrade()
        self.assertEqual(datetime.datetime(2023, 10, 18, 16, 00, 6), new_data_description.creation_time)
        self.assertEqual("ecephys_691897_2023-10-18_16-00-06", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("691897", new_data_description.subject_id)
        self.assertEqual([], new_data_description.related_data)
        self.assertEqual(Platform.ECEPHYS, new_data_description.platform)
        self.assertIsNone(new_data_description.data_summary)

    # def test_edge_cases(self):
    #     """Tests a few edge cases"""
    #     data_description_0_6_2 = deepcopy(self.data_descriptions["data_description_0.6.2.json"])
    #     upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_2)
    #     new_dd_0_6_2 = upgrader.upgrade(modality=[Modality.ECEPHYS])
    #     self.assertEqual([Modality.ECEPHYS], new_dd_0_6_2.modality)


class TestModalityUpgrade(unittest.TestCase):
    """Tests ModalityUpgrade methods"""

    def test_modality_upgrade(self):
        """Tests edge case"""
        self.assertIsNone(ModalityUpgrade.upgrade_modality(None))
        self.assertEqual(Modality.ECEPHYS, ModalityUpgrade.upgrade_modality(Modality.ECEPHYS))

    def test_modality_lookup(self):
        """Tests old modality lookup case"""
        dd_dict = {
            "describedBy": "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema"
            "/main/src/aind_data_schema/data_description.py",
            "schema_version": "0.3.0",
            "license": "CC-BY-4.0",
            "creation_time": "16:01:12",
            "creation_date": "2022-11-01",
            "name": "SmartSPIM_623711_2022-10-27_16-48-54_stitched_2022-11-01_16-01-12",
            "institution": "AIND",
            "funding_source": None,
            "data_level": "derived data",
            "group": None,
            "project_name": None,
            "project_id": None,
            "restrictions": None,
            "modality": "SmartSPIM",
            "platform": Platform.SMARTSPIM,
            "subject_id": "623711",
            "input_data_name": "SmartSPIM_623711_2022-10-27_16-48-54",
        }
        dd = DataDescription.construct(**dd_dict)
        upgrader = DataDescriptionUpgrade(old_data_description_model=dd)
        upgrader.upgrade()


class TestFundingUpgrade(unittest.TestCase):
    """Tests FundingUpgrade methods"""

    def test_funding_upgrade(self):
        """Tests edge case"""
        self.assertIsNone(FundingUpgrade.upgrade_funding(None))
        self.assertEqual(
            Funding(funder=Institution.AIND),
            FundingUpgrade.upgrade_funding(
                {
                    "funder": {
                        "name": "Allen Institute for Neural Dynamics",
                        "abbreviation": "AIND",
                        "registry": {
                            "name": "Research Organization Registry",
                            "abbreviation": "ROR",
                        },
                        "registry_identifier": "04szwah67",
                    },
                    "grant_number": None,
                    "fundee": None,
                }
            ),
        )


class TestInstitutionUpgrade(unittest.TestCase):
    """Tests InstitutionUpgrade methods"""

    def test_institution_upgrade(self):
        """Tests edge case"""
        self.assertIsNone(InstitutionUpgrade.upgrade_institution(None))


class TestProcessingUpgrade(unittest.TestCase):
    """Tests methods in ProcessingUpgrade class"""

    @classmethod
    def setUpClass(cls):
        """Load json files before running tests."""
        processing_files: List[str] = os.listdir(PROCESSING_FILES_PATH)
        processings = []
        for file_path in processing_files:
            with open(PROCESSING_FILES_PATH / file_path) as f:
                contents = json.load(f)
            processings.append((file_path, Processing.construct(**contents)))
        cls.processings = dict(processings)

    def test_upgrades_0_0_1(self):
        """Tests processing_0.0.1.json is mapped correctly."""
        processing_0_0_1 = self.processings["processing_0.0.1.json"]
        upgrader = ProcessingUpgrade(old_processing_model=processing_0_0_1)
        # Should complain about processor_full_name being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError("
            "model='PipelineProcess', "
            "errors=[{"
            "'loc': ('processor_full_name',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly
        new_processing = upgrader.upgrade(processor_full_name="Unit Test")
        processing_pipeline = new_processing.processing_pipeline
        self.assertEqual(processing_pipeline.processor_full_name, "Unit Test")
        ephys_preprocessing_process = processing_pipeline.data_processes[0]
        self.assertEqual(ephys_preprocessing_process.name.value, "Ephys preprocessing")
        self.assertEqual(ephys_preprocessing_process.software_version, "0.1.5")
        self.assertEqual(
            ephys_preprocessing_process.code_url, "https://github.com/AllenNeuralDynamics/aind-data-transfer", "0.1.5"
        )
        self.assertEqual(ephys_preprocessing_process.software_version, "0.1.5")

    def test_upgrades_0_1_0(self):
        """Tests processing_0.1.0.json is mapped correctly."""
        processing_0_1_0 = self.processings["processing_0.1.0.json"]
        upgrader = ProcessingUpgrade(old_processing_model=processing_0_1_0)
        # Should complain about processor_full_name being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError("
            "model='PipelineProcess', "
            "errors=[{"
            "'loc': ('processor_full_name',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly
        new_processing = upgrader.upgrade(processor_full_name="Unit Test")
        processing_pipeline = new_processing.processing_pipeline
        self.assertEqual(processing_pipeline.processor_full_name, "Unit Test")
        ephys_preprocessing_process = processing_pipeline.data_processes[0]
        self.assertEqual(ephys_preprocessing_process.name.value, "Ephys preprocessing")
        self.assertEqual(ephys_preprocessing_process.software_version, "0.5.0")
        self.assertEqual(
            ephys_preprocessing_process.code_url, "https://github.com/AllenNeuralDynamics/aind-data-transfer"
        )

    def test_upgrades_0_2_1(self):
        """Tests processing_0.2.1.json is mapped correctly."""
        processing_0_2_1 = self.processings["processing_0.2.1.json"]
        upgrader = ProcessingUpgrade(old_processing_model=processing_0_2_1)
        # Should complain about processor_full_name being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError("
            "model='PipelineProcess', "
            "errors=[{"
            "'loc': ('processor_full_name',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly
        new_processing = upgrader.upgrade(processor_full_name="Unit Test")
        processing_pipeline = new_processing.processing_pipeline
        self.assertEqual(processing_pipeline.processor_full_name, "Unit Test")
        ephys_preprocessing_process = processing_pipeline.data_processes[0]
        self.assertEqual(ephys_preprocessing_process.name.value, "Ephys preprocessing")
        self.assertEqual(ephys_preprocessing_process.software_version, "0.16.2")
        self.assertEqual(
            ephys_preprocessing_process.code_url, "https://github.com/AllenNeuralDynamics/aind-data-transfer"
        )

    def test_upgrades_0_2_5(self):
        """Tests processing_0.1.0.json is mapped correctly."""
        processing_0_2_5 = self.processings["processing_0.2.5.json"]
        upgrader = ProcessingUpgrade(old_processing_model=processing_0_2_5)
        # Should complain about processor_full_name being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade()

        expected_error_message = (
            "ValidationError("
            "model='PipelineProcess', "
            "errors=[{"
            "'loc': ('processor_full_name',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly
        new_processing = upgrader.upgrade(processor_full_name="Unit Test")
        processing_pipeline = new_processing.processing_pipeline
        self.assertEqual(processing_pipeline.processor_full_name, "Unit Test")
        ephys_preprocessing_process = processing_pipeline.data_processes[0]
        self.assertEqual(ephys_preprocessing_process.name.value, "Ephys preprocessing")
        self.assertEqual(ephys_preprocessing_process.software_version, "0.29.3")
        self.assertEqual(
            ephys_preprocessing_process.code_url, "https://github.com/AllenNeuralDynamics/aind-data-transfer"
        )

    def test_upgrades_current(self):
        """Tests processing_0.1.0.json is mapped correctly."""
        datetime_now = datetime.datetime.now()

        data_process = DataProcess(
            name="Ephys preprocessing",
            software_version="0.1000.0",
            code_url="my-code-repo",
            start_date_time=datetime_now,
            end_date_time=datetime_now,
            input_location="my-input-location",
            output_location="my-output-location",
            parameters={"param1": "value1"},
        )
        processing_pipeline = PipelineProcess(
            data_processes=[data_process],
            pipeline_url="my-pipeline-url",
            pipeline_version="0.1.0",
            processor_full_name="Unit Test",
        )
        current_processing = Processing(
            processing_pipeline=processing_pipeline,
        )

        upgrader = ProcessingUpgrade(old_processing_model=current_processing)
        new_processing = upgrader.upgrade()
        processing_pipeline = new_processing.processing_pipeline
        self.assertEqual(processing_pipeline.processor_full_name, "Unit Test")
        self.assertEqual(processing_pipeline.pipeline_url, "my-pipeline-url")
        self.assertEqual(processing_pipeline.pipeline_version, "0.1.0")
        ephys_preprocessing_process = processing_pipeline.data_processes[0]
        self.assertEqual(ephys_preprocessing_process.name.value, "Ephys preprocessing")
        self.assertEqual(ephys_preprocessing_process.software_version, "0.1000.0")
        self.assertEqual(ephys_preprocessing_process.code_url, "my-code-repo")


class TestDataProcessUpgrade(unittest.TestCase):
    """Tests methods in DataProcessUpgrade class"""

    def test_upgrade_from_old_model(self):
        """Tests data process from old model is upgraded correctly."""
        datetime_now = datetime.datetime.now()
        old_data_process_dict = dict(
            name="Ephys preprocessing",
            version="0.1.5",
            code_url="my-code-repo",
            start_date_time=datetime_now,
            end_date_time=datetime_now,
            input_location="my-input-location",
            output_location="my-output-location",
            parameters={"param1": "value1"},
        )
        old_data_process = DataProcess.construct(**old_data_process_dict)

        upgrader = DataProcessUpgrade(old_data_process_model=old_data_process)
        new_data_process = upgrader.upgrade()

        # the upgrader updates version to software_version
        self.assertEqual(new_data_process.software_version, "0.1.5")
        self.assertEqual(new_data_process.code_url, "my-code-repo")
        self.assertEqual(new_data_process.start_date_time, datetime_now)
        self.assertEqual(new_data_process.end_date_time, datetime_now)
        self.assertEqual(new_data_process.input_location, "my-input-location")
        self.assertEqual(new_data_process.output_location, "my-output-location")
        self.assertEqual(new_data_process.parameters, {"param1": "value1"})

    def test_upgrade_from_other_with_no_notes(self):
        """Tests "Other" data process with not "notes" is upgraded correctly."""
        processing_path = PROCESSING_FILES_PATH / "processing_other_no_notes.json"
        with open(processing_path, "r") as f:
            processing_dict = json.load(f)
            data_process_no_notes = DataProcess.construct(**processing_dict["data_processes"][1])

        upgrader = DataProcessUpgrade(data_process_no_notes)
        new_data_process = upgrader.upgrade()

        # the upgrader updates version to software_version
        self.assertEqual(new_data_process.software_version, "0.29.3")
        self.assertEqual(new_data_process.code_url, "https://github.com/AllenNeuralDynamics/aind-data-transfer")
        # notes that are None for "Other" data processes are replaced with "missing notes"
        self.assertEqual(new_data_process.notes, "missing notes")

    def test_upgrade_from_current_model(self):
        """Tests data process from current model is upgraded correctly."""
        datetime_now = datetime.datetime.now()
        data_process_dict = dict(
            name="Ephys preprocessing",
            software_version="0.1.5",
            code_url="my-code-repo",
            start_date_time=datetime_now,
            end_date_time=datetime_now,
            input_location="my-input-location",
            output_location="my-output-location",
            parameters={"param1": "value1"},
        )
        data_process = DataProcess(**data_process_dict)

        upgrader = DataProcessUpgrade(old_data_process_model=data_process)
        new_data_process = upgrader.upgrade()

        # the upgrader updates version to software_version
        self.assertEqual(new_data_process.software_version, "0.1.5")
        self.assertEqual(new_data_process.code_url, "my-code-repo")
        self.assertEqual(new_data_process.start_date_time, datetime_now)
        self.assertEqual(new_data_process.end_date_time, datetime_now)
        self.assertEqual(new_data_process.input_location, "my-input-location")
        self.assertEqual(new_data_process.output_location, "my-output-location")
        self.assertEqual(new_data_process.parameters, {"param1": "value1"})


if __name__ == "__main__":
    unittest.main()
