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
    ExperimentType,
    Funding,
    Group,
    Institution,
    Modality,
    RelatedData,
)
from aind_data_schema.schema_upgrade.data_description_upgrade import (
    DataDescriptionUpgrade,
    FundingUpgrade,
    InstitutionUpgrade,
    ModalityUpgrade,
)

DATA_DESCRIPTION_FILES_PATH = Path(__file__).parent / "resources" / "ephys_data_description"


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
        # Should complain about experiment type being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade_data_description()

        expected_error_message = (
            "ValidationError("
            "model='DataDescription', "
            "errors=[{"
            "'loc': ('experiment_type',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting experiment type explicitly
        new_data_description = upgrader.upgrade_data_description(experiment_type=ExperimentType.ECEPHYS)
        self.assertEqual(datetime.time(10, 31, 30), new_data_description.creation_time)
        self.assertEqual(datetime.date(2022, 6, 28), new_data_description.creation_date)
        self.assertEqual("ecephys_623705_2022-06-28_10-31-30", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW_DATA, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.project_id)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.ECEPHYS], new_data_description.modality)
        self.assertEqual("623705", new_data_description.subject_id)
        self.assertEqual([], new_data_description.related_data)
        self.assertIsNone(new_data_description.data_summary)

    def test_upgrades_0_4_0(self):
        """Tests data_description_0.4.0.json is mapped correctly."""
        data_description_0_4_0 = self.data_descriptions["data_description_0.4.0.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_4_0)

        # Should work by setting experiment type explicitly
        new_data_description = upgrader.upgrade_data_description()
        self.assertEqual(datetime.time(14, 35, 51), new_data_description.creation_time)
        self.assertEqual(datetime.date(2023, 4, 13), new_data_description.creation_date)
        self.assertEqual("ecephys_664438_2023-04-13_14-35-51", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW_DATA, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.project_id)
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
        new_data_description = upgrader.upgrade_data_description()
        self.assertEqual(datetime.time(17, 9, 26), new_data_description.creation_time)
        self.assertEqual(datetime.date(2023, 4, 10), new_data_description.creation_date)
        self.assertEqual("ecephys_661278_2023-04-10_17-09-26", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW_DATA, new_data_description.data_level)
        self.assertIsNone(new_data_description.group)
        self.assertEqual([], new_data_description.investigators)
        self.assertIsNone(new_data_description.project_name)
        self.assertIsNone(new_data_description.project_id)
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
        new_data_description = upgrader.upgrade_data_description()
        self.assertEqual(datetime.time(22, 31, 18), new_data_description.creation_time)
        self.assertEqual(datetime.date(2023, 3, 23), new_data_description.creation_date)
        self.assertEqual("661279_2023-03-23_15-31-18", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW_DATA, new_data_description.data_level)
        self.assertEqual(Group.EPHYS, new_data_description.group)
        self.assertEqual(["John Doe", "Mary Smith"], new_data_description.investigators)
        self.assertEqual("MRI-Guided Elecrophysiology", new_data_description.project_name)
        self.assertIsNone(new_data_description.project_id)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.EPHYS], new_data_description.modality)
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
        new_dd_0_6_2 = upgrader.upgrade_data_description(modality=[Modality.ECEPHYS])
        self.assertEqual([Modality.ECEPHYS], new_dd_0_6_2.modality)
        # Blank Modality
        data_description_0_6_2.modality = None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade_data_description()

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

        # Should complain about experiment type being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade_data_description()

        expected_error_message = "AttributeError('ALLEN INSITUTE FOR NEURAL DYNAMICS')"
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting funding_source explicitly
        new_data_description = upgrader.upgrade_data_description(funding_source=[Funding(funder=Institution.AIND)])
        self.assertEqual(datetime.time(22, 31, 18), new_data_description.creation_time)
        self.assertEqual(datetime.date(2023, 3, 23), new_data_description.creation_date)
        self.assertEqual("661279_2023-03-23_15-31-18", new_data_description.name)
        self.assertEqual(Institution.AIND, new_data_description.institution)
        self.assertEqual([Funding(funder=Institution.AIND)], new_data_description.funding_source)
        self.assertEqual(DataLevel.RAW_DATA, new_data_description.data_level)
        self.assertEqual(Group.EPHYS, new_data_description.group)
        self.assertEqual(["John Doe", "Mary Smith"], new_data_description.investigators)
        self.assertEqual("MRI-Guided Elecrophysiology", new_data_description.project_name)
        self.assertIsNone(new_data_description.project_id)
        self.assertIsNone(new_data_description.restrictions)
        self.assertEqual([Modality.EPHYS], new_data_description.modality)
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

    # def test_edge_cases(self):
    #     """Tests a few edge cases"""
    #     data_description_0_6_2 = deepcopy(self.data_descriptions["data_description_0.6.2.json"])
    #     upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_2)
    #     new_dd_0_6_2 = upgrader.upgrade_data_description(modality=[Modality.ECEPHYS])
    #     self.assertEqual([Modality.ECEPHYS], new_dd_0_6_2.modality)


class TestModalityUpgrade(unittest.TestCase):
    """Tests ModalityUpgrade methods"""

    def test_modality_upgrade(self):
        """Tests edge case"""
        self.assertIsNone(ModalityUpgrade.upgrade_modality(None))
        self.assertEqual(Modality.ECEPHYS, ModalityUpgrade.upgrade_modality(Modality.ECEPHYS))


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
                        "registry": {"name": "Research Organization Registry", "abbreviation": "ROR"},
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


if __name__ == "__main__":
    unittest.main()
