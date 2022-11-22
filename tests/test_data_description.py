""" test DataDescription """

import datetime
import unittest

from aind_data_schema.data_description import (
    DataDescription,
    DerivedDataDescription,
    RawDataDescription,
    Funding,
)


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
            name=self.DERIVED_NAME, institution="AIND", funding_source=[f]
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

    def test_constructors(self):
        """test building from component parts"""
        f = Funding(funder="test")

        dt = datetime.datetime.now()
        da = DataDescription(
            label="ecephys_1234",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            data_level="raw data",
            funding_source=[f],
        )

        r1 = DerivedDataDescription(
            input_data=da,
            process_name="spikesort-ks25",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
        )

        r2 = DerivedDataDescription(
            input_data=r1,
            process_name="some-model",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
        )

        r3 = DerivedDataDescription(
            input_data=r2,
            process_name="a-paper",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
        )
        assert r3 is not None

        ad = RawDataDescription(
            modality="ecephys",
            subject_id="1234",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution="AIND",
            funding_source=[f],
        )

        assert ad is not None


if __name__ == "__main__":
    unittest.main()
