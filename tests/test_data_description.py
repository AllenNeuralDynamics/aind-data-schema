""" test DataDescription """

import datetime
import json
import os
import unittest
from pathlib import Path
from typing import List

from aind_data_schema.data_description import (
    DataDescription,
    DataLevel,
    DerivedDataDescription,
    ExperimentType,
    Funding,
    Institution,
    Modality,
    RawDataDescription,
)

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
        data_descriptions.sort(key=lambda x: x[0])
        cls.data_descriptions = data_descriptions

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

        data_description_0_3_0 = self.data_descriptions[0]
        # data_description_0.3.0 is missing experiment type. It needs to be set
        # explicitly
        with self.assertRaises(Exception):
            DerivedDataDescription.from_data_description(
                process_name=process_name, data_description=data_description_0_3_0[1]
            )

        # data_description_0_6_2_wrong_field has a malformed funding_source input.
        # That field will need to be explicitly set.
        data_description_0_6_2_wrong_field = self.data_descriptions[-1]
        with self.assertRaises(Exception):
            DerivedDataDescription.from_data_description(
                process_name=process_name, data_description=data_description_0_6_2_wrong_field[1]
            )

        # Explicitly setting the fields should correct the validation errors
        derived_dd_0_3_0 = DerivedDataDescription.from_data_description(
            process_name=process_name,
            data_description=data_description_0_3_0[1],
            experiment_type=ExperimentType.ECEPHYS,
        )
        derived_dd_0_6_2_wrong_field = DerivedDataDescription.from_data_description(
            process_name=process_name,
            data_description=data_description_0_6_2_wrong_field[1],
            funding_source=[Funding(funder=Institution.AIND)],
        )

        self.assertEqual(ExperimentType.ECEPHYS, derived_dd_0_3_0.experiment_type)
        self.assertEqual([Funding(funder=Institution.AIND)], derived_dd_0_6_2_wrong_field.funding_source)

        # All the other json files should translate correctly:
        for data_description in self.data_descriptions[1:-1]:
            derived_dd = DerivedDataDescription.from_data_description(
                process_name=process_name, data_description=data_description[1]
            )
            self.assertEqual(ExperimentType.ECEPHYS, derived_dd.experiment_type)
            self.assertEqual(DataLevel.DERIVED_DATA, derived_dd.data_level)

        # Extra check on funding source parsing
        funding_dd1 = DerivedDataDescription.construct(
            funding_source=[
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
            ],
            institution=Institution.AIND,
            modality=Modality.ECEPHYS,
            experiment_type=ExperimentType.ECEPHYS,
            subject_id="12345",
            name="some_og_data",
        )
        derived_finding_dd1 = DerivedDataDescription.from_data_description(
            data_description=funding_dd1, process_name=process_name
        )
        self.assertEqual(Institution.AIND, derived_finding_dd1.funding_source[0].funder)

        # Extra check to verify None is returned with malformed input and nulls
        blank_dd = DataDescription.construct(funding_source=["Malformed input"])
        with self.assertRaises(Exception):
            DerivedDataDescription.from_data_description(
                process_name=process_name, data_description=blank_dd, institution=Institution.AIND
            )


if __name__ == "__main__":
    unittest.main()
