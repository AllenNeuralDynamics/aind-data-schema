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
    ExperimentType,
    Funding,
    Institution,
    Modality,
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
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            data_level="raw data",
            funding_source=[f],
            modality=[Modality.ECEPHYS],
            experiment_type="ecephys",
            subject_id="12345",
            investigators=["Jane Smith"],
        )

        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            modality=da.modality,
            experiment_type=da.experiment_type,
            subject_id=da.subject_id,
            investigators=["Jane Smith"],
        )

        r2 = DerivedDataDescription(
            input_data_name=r1.name,
            process_name="some-model",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            modality=r1.modality,
            experiment_type=r1.experiment_type,
            subject_id="12345",
            investigators=["Jane Smith"],
        )

        r3 = DerivedDataDescription(
            input_data_name=r2.name,
            process_name="a-paper",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            modality=r2.modality,
            experiment_type=r2.experiment_type,
            subject_id="12345",
            investigators=["Jane Smith"],
        )
        assert r3 is not None

        dd = DataDescription(
            label="test_data",
            modality=[Modality.SPIM],
            experiment_type="exaSPIM",
            subject_id="1234",
            data_level="raw data",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            investigators=["Jane Smith"],
        )

        assert dd is not None

    def test_round_trip(self):
        """make sure we can round trip from json"""

        dt = datetime.datetime.now()

        da1 = RawDataDescription(
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            data_level="raw data",
            funding_source=[],
            modality=[Modality.SPIM],
            experiment_type="exaSPIM",
            subject_id="12345",
            investigators=["Jane Smith"],
        )

        da2 = RawDataDescription.parse_obj(json.loads(da1.json()))

        assert da1.creation_time == da2.creation_time
        assert da1.creation_date == da2.creation_date
        assert da1.name == da2.name

    def test_parse_name(self):
        """tests for parsing names"""

        toks = DataDescription.parse_name(self.BASIC_NAME)
        assert toks["label"] == "ecephys_1234"
        assert toks["creation_date"] == datetime.date(3033, 12, 21)
        assert toks["creation_time"] == datetime.time(4, 22, 11)

        with self.assertRaises(ValueError):
            toks = DataDescription.parse_name(self.BAD_NAME)

        toks = RawDataDescription.parse_name(self.BASIC_NAME)
        assert toks["experiment_type"] == "ecephys"
        assert toks["subject_id"] == "1234"
        assert toks["creation_date"] == datetime.date(3033, 12, 21)
        assert toks["creation_time"] == datetime.time(4, 22, 11)

        with self.assertRaises(ValueError):
            toks = RawDataDescription.parse_name(self.BAD_NAME)

        toks = DerivedDataDescription.parse_name(self.DERIVED_NAME)
        assert toks["input_data_name"] == "ecephys_1234_3033-12-21_04-22-11"
        assert toks["process_name"] == "spikesorted-ks25"
        assert toks["creation_date"] == datetime.date(2022, 10, 12)
        assert toks["creation_time"] == datetime.time(23, 23, 11)

        with self.assertRaises(ValueError):
            toks = DerivedDataDescription.parse_name(self.BAD_NAME)

    def test_modality_enums(self):
        """Tests that BaseName enums can be constructed from attr names"""
        self.assertEqual(Modality.ECEPHYS, Modality("ECEPHYS"))
        self.assertEqual(Modality.ECEPHYS, Modality("ecephys"))

    def test_from_data_description(self):
        """Tests DerivedDataDescription.from_data_description method"""

        process_name = "spike_sorter"

        data_description_0_3_0 = self.data_descriptions["data_description_0.3.0.json"]
        upgrader_0_3_0 = DataDescriptionUpgrade(old_data_description_model=data_description_0_3_0)
        new_dd_0_3_0 = upgrader_0_3_0.upgrade_data_description(experiment_type=ExperimentType.ECEPHYS)
        derived_dd_0_3_0 = DerivedDataDescription.from_data_description(new_dd_0_3_0, process_name=process_name)
        self.assertEqual(ExperimentType.ECEPHYS, derived_dd_0_3_0.experiment_type)

        data_description_0_4_0 = self.data_descriptions["data_description_0.4.0.json"]
        upgrader_0_4_0 = DataDescriptionUpgrade(old_data_description_model=data_description_0_4_0)
        new_dd_0_4_0 = upgrader_0_4_0.upgrade_data_description()
        derived_dd_0_4_0 = DerivedDataDescription.from_data_description(new_dd_0_4_0, process_name=process_name)
        self.assertEqual(ExperimentType.ECEPHYS, derived_dd_0_4_0.experiment_type)

        data_description_0_6_0 = self.data_descriptions["data_description_0.6.0.json"]
        upgrader_0_6_0 = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_0)
        new_dd_0_6_0 = upgrader_0_6_0.upgrade_data_description()
        derived_dd_0_6_0 = DerivedDataDescription.from_data_description(new_dd_0_6_0, process_name=process_name)
        self.assertEqual(ExperimentType.ECEPHYS, derived_dd_0_6_0.experiment_type)

        data_description_0_6_2 = self.data_descriptions["data_description_0.6.2.json"]
        upgrader_0_6_2 = DataDescriptionUpgrade(old_data_description_model=data_description_0_6_2)
        new_dd_0_6_2 = upgrader_0_6_2.upgrade_data_description()
        derived_dd_0_6_2 = DerivedDataDescription.from_data_description(new_dd_0_6_2, process_name=process_name)
        self.assertEqual(ExperimentType.ECEPHYS, derived_dd_0_6_2.experiment_type)

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
        self.assertEqual(ExperimentType.ECEPHYS, derived_dd_0_6_2_wrong_field.experiment_type)

        # Test Override
        derived_dd_0_6_2_wrong_field2 = DerivedDataDescription.from_data_description(
            new_dd_0_6_2_wrong_field, process_name=process_name, experiment_type=ExperimentType.OTHER
        )
        self.assertEqual(ExperimentType.OTHER, derived_dd_0_6_2_wrong_field2.experiment_type)


if __name__ == "__main__":
    unittest.main()
