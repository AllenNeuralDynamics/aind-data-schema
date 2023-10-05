""" test DataDescription """

import datetime
import json
import os
import unittest
from pathlib import Path
from typing import List

from aind_data_schema.data_description import (
    DataDescription,
    DerivedDataDescription,
    Funding,
    Institution,
    Modality,
    Platform,
    RawDataDescription,
)
from aind_data_schema.schema_upgrade.data_description_upgrade import DataDescriptionUpgrade

DATA_DESCRIPTION_FILES_PATH = Path(__file__).parent / "resources" / "ephys_data_description"


class DataDescriptionTest(unittest.TestCase):
    """test DataDescription"""

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

    BAD_NAME = "fizzbuzz"
    BASIC_NAME = "ecephys_1234_3033-12-21_04-22-11"
    DERIVED_NAME = "ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11"

    def test_constructors(self):
        """test building from component parts"""
        f = Funding(funder=Institution.NINDS, grant_number="grant001")

        dt = datetime.datetime.now()
        da = RawDataDescription(
            creation_time=dt,
            institution=Institution.AIND,
            data_level="raw",
            funding_source=[f],
            modality=[Modality.ECEPHYS],
            platform=Platform.ECEPHYS,
            subject_id="12345",
            investigators=["Jane Smith"],
        )

        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_time=dt,
            institution=Institution.AIND,
            funding_source=[f],
            modality=da.modality,
            platform=da.platform,
            subject_id=da.subject_id,
            investigators=["Jane Smith"],
        )

        r2 = DerivedDataDescription(
            input_data_name=r1.name,
            process_name="some-model",
            creation_time=dt,
            institution=Institution.AIND,
            funding_source=[f],
            modality=r1.modality,
            platform=r1.platform,
            subject_id="12345",
            investigators=["Jane Smith"],
        )

        r3 = DerivedDataDescription(
            input_data_name=r2.name,
            process_name="a-paper",
            creation_time=dt,
            institution=Institution.AIND,
            funding_source=[f],
            modality=r2.modality,
            platform=r2.platform,
            subject_id="12345",
            investigators=["Jane Smith"],
        )
        assert r3 is not None

        dd = DataDescription(
            label="test_data",
            modality=[Modality.SPIM],
            platform="exaspim",
            subject_id="1234",
            data_level="raw",
            creation_time=dt,
            institution=Institution.AIND,
            funding_source=[f],
            investigators=["Jane Smith"],
        )

        assert dd is not None

        # test construction fails
        with self.assertRaises(AttributeError):
            _ = DataDescription(
                label="test_data",
                modality=[Modality.SPIM],
                platform="fake platform",
                subject_id="1234",
                data_level="raw",
                creation_time=dt,
                institution=Institution.AIND,
                funding_source=[f],
                investigators=["Jane Smith"],
            )

    def test_round_trip(self):
        """make sure we can round trip from json"""

        dt = datetime.datetime.now()

        da1 = RawDataDescription(
            creation_time=dt,
            institution=Institution.AIND,
            data_level="raw",
            funding_source=[],
            modality=[Modality.SPIM],
            platform=Platform.EXASPIM,
            subject_id="12345",
            investigators=["Jane Smith"],
        )

        da2 = RawDataDescription.parse_obj(json.loads(da1.json()))

        assert da1.creation_time == da2.creation_time
        assert da1.name == da2.name

    def test_parse_name(self):
        """tests for parsing names"""

        toks = DataDescription.parse_name(self.BASIC_NAME)
        assert toks["label"] == "ecephys_1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            toks = DataDescription.parse_name(self.BAD_NAME)

        toks = RawDataDescription.parse_name(self.BASIC_NAME)
        assert toks["platform"] == Platform.ECEPHYS
        assert toks["subject_id"] == "1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            toks = RawDataDescription.parse_name(self.BAD_NAME)

        toks = DerivedDataDescription.parse_name(self.DERIVED_NAME)
        assert toks["input_data_name"] == "ecephys_1234_3033-12-21_04-22-11"
        assert toks["process_name"] == "spikesorted-ks25"
        assert toks["creation_time"] == datetime.datetime(2022, 10, 12, 23, 23, 11)

        with self.assertRaises(ValueError):
            toks = DerivedDataDescription.parse_name(self.BAD_NAME)

    def test_abbreviation_enums(self):
        """Tests that BaseName enums can be constructed from abbreviations"""
        # Tests that Modality constructed as expected
        self.assertEqual(Modality.ECEPHYS, Modality("ECEPHYS"))
        self.assertEqual(Modality.ECEPHYS, Modality("ecephys"))
        self.assertEqual(Modality.POPHYS, Modality("POPHYS"))
        self.assertEqual(Modality.POPHYS, Modality("ophys"))
        self.assertEqual(Modality.BEHAVIOR_VIDEOS, Modality("BEHAVIOR_VIDEOS"))
        self.assertEqual(Modality.BEHAVIOR_VIDEOS, Modality("behavior-videos"))

        # Tests that Platform constructed as expected
        self.assertEqual(Platform.ECEPHYS, Platform("ECEPHYS"))
        self.assertEqual(Platform.ECEPHYS, Platform("ecephys"))
        self.assertEqual(Platform.MESOSPM, Platform("MESOSPM"))
        self.assertEqual(Platform.MESOSPM, Platform("mesoSPIM"))
        self.assertEqual(Platform.MULTIPLANE_OPHYS, Platform("MULTIPLANE_OPHYS"))
        self.assertEqual(Platform.MULTIPLANE_OPHYS, Platform("multiplane-ophys"))

    def test_unique_abbreviations(self):
        """Tests that abbreviations are unique"""
        modality_abbreviations = [m.value.abbreviation for m in Modality]
        self.assertEqual(len(set(modality_abbreviations)), len(modality_abbreviations))
        platform_abbreviations = [p.value.abbreviation for p in Platform]
        self.assertEqual(len(set(platform_abbreviations)), len(platform_abbreviations))

    def test_from_data_description(self):
        """Tests DerivedDataDescription.from_data_description method"""

        process_name = "spike_sorter"

        data_description_0_3_0 = self.data_descriptions["data_description_0.3.0.json"]
        upgrader_0_3_0 = DataDescriptionUpgrade(old_data_description_model=data_description_0_3_0)
        new_dd_0_3_0 = upgrader_0_3_0.upgrade_data_description(platform=Platform.ECEPHYS)
        derived_dd_0_3_0 = DerivedDataDescription.from_data_description(new_dd_0_3_0, process_name=process_name)
        self.assertEqual(Platform.ECEPHYS, derived_dd_0_3_0.platform)

        data_description_0_4_0 = self.data_descriptions["data_description_0.4.0.json"]
        upgrader_0_4_0 = DataDescriptionUpgrade(old_data_description_model=data_description_0_4_0)
        new_dd_0_4_0 = upgrader_0_4_0.upgrade_data_description()
        derived_dd_0_4_0 = DerivedDataDescription.from_data_description(new_dd_0_4_0, process_name=process_name)
        self.assertEqual(Platform.ECEPHYS, derived_dd_0_4_0.platform)

        data_description_0_6_0 = self.data_descriptions["data_description_0.6.0.json"]
        upgrader_0_6_0 = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_0)
        new_dd_0_6_0 = upgrader_0_6_0.upgrade_data_description()
        derived_dd_0_6_0 = DerivedDataDescription.from_data_description(new_dd_0_6_0, process_name=process_name)
        self.assertEqual(Platform.ECEPHYS, derived_dd_0_6_0.platform)

        data_description_0_6_2 = self.data_descriptions["data_description_0.6.2.json"]
        upgrader_0_6_2 = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_2)
        new_dd_0_6_2 = upgrader_0_6_2.upgrade_data_description()
        derived_dd_0_6_2 = DerivedDataDescription.from_data_description(new_dd_0_6_2, process_name=process_name)
        self.assertEqual(Platform.ECEPHYS, derived_dd_0_6_2.platform)

        data_description_0_6_2_wrong_field = self.data_descriptions["data_description_0.6.2_wrong_field.json"]
        upgrader_0_6_2_wrong_field = DataDescriptionUpgrade(
            old_data_description_model=data_description_0_6_2_wrong_field
        )
        new_dd_0_6_2_wrong_field = upgrader_0_6_2_wrong_field.upgrade_data_description(
            funding_source=[Funding(funder=Institution.AIND)]
        )
        derived_dd_0_6_2_wrong_field = DerivedDataDescription.from_data_description(
            new_dd_0_6_2_wrong_field, process_name=process_name
        )
        self.assertEqual(Platform.ECEPHYS, derived_dd_0_6_2_wrong_field.platform)

        # Test Override
        derived_dd_0_6_2_wrong_field2 = DerivedDataDescription.from_data_description(
            new_dd_0_6_2_wrong_field,
            process_name=process_name,
            platform=Platform.SMARTSPIM,
        )
        self.assertEqual(Platform.SMARTSPIM, derived_dd_0_6_2_wrong_field2.platform)


if __name__ == "__main__":
    unittest.main()
