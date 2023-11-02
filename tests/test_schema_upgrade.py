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
        # Should complain about platform being None
        with self.assertRaises(Exception) as e:
            upgrader.upgrade_data_description()

        expected_error_message = (
            "ValidationError("
            "model='DataDescription', "
            "errors=[{"
            "'loc': ('platform',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly
        new_data_description = upgrader.upgrade_data_description(platform=Platform.ECEPHYS)
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
            upgrader.upgrade_data_description()

        expected_error_message = (
            "ValidationError("
            "model='DataDescription', "
            "errors=[{"
            "'loc': ('platform',), "
            "'msg': 'none is not an allowed value', "
            "'type': 'type_error.none.not_allowed'"
            "}])"
        )
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting platform explicitly and DataLevel
        new_data_description = upgrader.upgrade_data_description(platform=Platform.ECEPHYS, data_level=DataLevel.RAW)
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
        new_data_description2 = upgrader.upgrade_data_description(platform=Platform.ECEPHYS, data_level="raw level")
        self.assertEqual(DataLevel.RAW, new_data_description2.data_level)

        # Should fail if inputting unknown string
        with self.assertRaises(Exception) as e1:
            upgrader.upgrade_data_description(platform=Platform.ECEPHYS, data_level="asfnewnjfq")

        expected_error_message1 = (
            "ValidationError(model='DataDescription', "
            "errors=[{'loc': ('data_level',), "
            "'msg': \"'asfnewnjfq' is not a valid DataLevel\", "
            "'type': 'value_error'}])"
        )

        self.assertEqual(expected_error_message1, repr(e1.exception))

        # Should also fail if inputting wrong type
        with self.assertRaises(Exception) as e2:
            upgrader.upgrade_data_description(platform=Platform.ECEPHYS, data_level=["raw"])
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
        new_data_description3 = upgrader3.upgrade_data_description(platform=Platform.ECEPHYS, data_level=DataLevel.RAW)
        self.assertEqual(DataLevel.RAW, new_data_description3.data_level)

    def test_upgrades_0_4_0(self):
        """Tests data_description_0.4.0.json is mapped correctly."""
        data_description_0_4_0 = self.data_descriptions["data_description_0.4.0.json"]
        upgrader = DataDescriptionUpgrade(old_data_description_model=data_description_0_4_0)

        # Should work by setting platform explicitly
        new_data_description = upgrader.upgrade_data_description()
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
        new_data_description = upgrader.upgrade_data_description()
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
        new_data_description = upgrader.upgrade_data_description()
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

        # Should complain about funder not being correct
        with self.assertRaises(Exception) as e:
            upgrader.upgrade_data_description()

        expected_error_message = "AttributeError('NOT A REAL FUNDER')"
        self.assertEqual(expected_error_message, repr(e.exception))

        # Should work by setting funding_source explicitly
        new_data_description = upgrader.upgrade_data_description(funding_source=[Funding(funder=Institution.AIND)])
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
        new_data_description = upgrader.upgrade_data_description()
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


if __name__ == "__main__":
    unittest.main()
