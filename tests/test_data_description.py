""" test DataDescription """

import datetime
import unittest

from aind_data_schema.data_description import (DataDescription,
                                               DerivedDataDescription, Funding,
                                               RawDataDescription)


class DataDescriptionTest(unittest.TestCase):
    """test DataDescription"""

    BAD_NAME = "fizzbuzz"
    BASIC_NAME = "ecephys_1234_3033-12-21_04-22-11"
    DERIVED_NAME = (
        "ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11"
    )

    def test_from_name(self):
        """test the from_name methods"""

        f = Funding(funder="test")

        da = DataDescription.from_name(
            name=self.BASIC_NAME,
            institution="AIND",
            data_level="raw data",
            funding_source=[f],
            modality="exaSPIM",
            subject_id="12345",
        )
        assert da.name == self.BASIC_NAME

        with self.assertRaises(ValueError):
            DataDescription.from_name(
                name=self.BAD_NAME,
                institution="AIND",
                data_level="raw data",
                funding_source=[f],
            )

        rd = RawDataDescription.from_name(
            name=self.BASIC_NAME, institution="AIND", funding_source=[f]
        )
        assert rd.name == self.BASIC_NAME
        assert rd.data_level.value == "raw data"

        with self.assertRaises(ValueError):
            RawDataDescription.from_name(
                name=self.BAD_NAME,
                institution="AIND",
                data_level="raw data",
                funding_source=[f],
            )

        dd = DerivedDataDescription.from_name(
            name=self.DERIVED_NAME,
            institution="AIND",
            funding_source=[f],
            modality="SmartSPIM",
            subject_id="12345",
        )
        assert dd.name == self.DERIVED_NAME
        assert dd.data_level.value == "derived data"

        with self.assertRaises(ValueError):
            DerivedDataDescription.from_name(
                name=self.BAD_NAME,
                institution="AIND",
                data_level="raw data",
                funding_source=[f],
            )

    def test_from_data_description(self):
        """test the from_data_description method"""
        dt = datetime.datetime.now()
        d1 = RawDataDescription(
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            data_level="raw data",
            funding_source=[],
            modality="ecephys",
            subject_id="12345",
        )

        dt = datetime.datetime.now()
        d2 = DerivedDataDescription.from_data_description(
            input_data=d1,
            process_name="fishing",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[],
        )

        assert d2.modality == d1.modality
        assert d2.subject_id == d1.subject_id

        d3 = DerivedDataDescription.from_data_description(
            input_data=d2,
            process_name="bailing",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="HUST",
            funding_source=[],
        )

        assert d3.modality == d2.modality
        assert d3.subject_id == d2.subject_id

    def test_constructors(self):
        """test building from component parts"""
        f = Funding(funder="test")

        dt = datetime.datetime.now()
        da = RawDataDescription(
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            data_level="raw data",
            funding_source=[f],
            modality="ecephys",
            subject_id="12345",
        )

        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
            modality=da.modality,
            subject_id=da.subject_id,
        )

        r2 = DerivedDataDescription(
            input_data_name=r1.name,
            process_name="some-model",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
            modality="ecephys",
            subject_id="12345",
        )

        r3 = DerivedDataDescription(
            input_data_name=r2.name,
            process_name="a-paper",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
            modality="ecephys",
            subject_id="12345",
        )
        assert r3 is not None

        dd = DataDescription(
            label="test_data",
            modality="ecephys",
            subject_id="1234",
            data_level="raw data",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
        )

        assert dd is not None


if __name__ == "__main__":
    unittest.main()
