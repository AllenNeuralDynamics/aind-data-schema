""" test DataDescription """

import datetime
import json
import unittest
from pathlib import Path

from aind_data_schema.data_description import (
    DataDescription,
    DerivedDataDescription,
    ExperimentType,
    Funding,
    Institution,
    Modality,
    RawDataDescription,
)


class DataDescriptionTest(unittest.TestCase):
    """test DataDescription"""

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

    def test_from_data_description_file(self):
        """Tests DerivedDataDescription.from_data_description_file method"""
        data_description_files_path = Path(__file__).parent / "resources" / "ephys_data_description"
        data_description_args = [p for p in data_description_files_path.iterdir()]

        for data_description_arg in data_description_args:
            if "0.3.0" in data_description_arg.name:
                experiment_type = ExperimentType.ECEPHYS
            else:
                experiment_type = None
            derived_data_description_from_file = DerivedDataDescription.from_data_description_file(
                data_description_file=data_description_arg,
                process_name="test_process",
                experiment_type=experiment_type,
            )
            self.assertTrue(isinstance(derived_data_description_from_file, DerivedDataDescription))

    def test_from_data_description(self):
        """Tests DerivedDataDescription.from_data_description method"""
        """Tests DerivedDataDescription.from_data_description_file method"""
        data_description_files_path = Path(__file__).parent / "resources" / "ephys_data_description"
        data_description_objects = []
        for data_description_file in data_description_files_path.iterdir():
            with open(data_description_file, "r") as f:
                data_description_dict = json.load(f)
            if "experiment_type" not in data_description_dict:
                data_description_dict["experiment_type"] = ExperimentType.ECEPHYS
            data_description = DataDescription.construct(**data_description_dict)
            data_description_objects.append(data_description)

        for data_description in data_description_objects:
            if data_description.schema_version == "0.3.0":
                experiment_type = ExperimentType.ECEPHYS
            else:
                experiment_type = None
            derived_data_description_from_obj = DerivedDataDescription.from_data_description(
                data_description=data_description,
                process_name="test_process",
                experiment_type=experiment_type,
            )
            self.assertTrue(isinstance(derived_data_description_from_obj, DerivedDataDescription))

    def test_from_scratch(self):
        """Tests DerivedDataDescription.from_scratch method"""
        derived_data_description_from_scratch = DerivedDataDescription.from_scratch(
            process_name="test_process",
            modality=[Modality.ECEPHYS],
            experiment_type=ExperimentType.ECEPHYS,
            subject_id="00000",
            input_data_name="test_input_data_name",
        )
        self.assertTrue(isinstance(derived_data_description_from_scratch, DerivedDataDescription))


if __name__ == "__main__":
    unittest.main()
