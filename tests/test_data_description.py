""" test DataDescription """

import datetime
import json
import unittest

from aind_data_schema.data_description import (DataDescription, DerivedDataDescription, Funding, Institution, Modality,
                                               RawDataDescription)
from aind_data_schema.device import InstrumentType


class DataDescriptionTest(unittest.TestCase):
    """test DataDescription"""

    BAD_NAME = "fizzbuzz"
    BASIC_NAME = "ecephys_1234_3033-12-21_04-22-11"
    DERIVED_NAME = "ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11"

    def test_constructors(self):
        """test building from component parts"""
        f = Funding(funder="test")

        dt = datetime.datetime.now()
        da = RawDataDescription(
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            data_level="raw data",
            funding_source=[f],
            modality=Modality.ECEPHYS,
            instrument_type="ecephys",
            subject_id="12345",
        )

        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            modality=da.modality,
            instrument_type=da.instrument_type,
            subject_id=da.subject_id,
        )

        r2 = DerivedDataDescription(
            input_data_name=r1.name,
            process_name="some-model",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            modality=r1.modality,
            instrument_type=r1.instrument_type,
            subject_id="12345",
        )

        r3 = DerivedDataDescription(
            input_data_name=r2.name,
            process_name="a-paper",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
            modality=r2.modality,
            instrument_type=r2.instrument_type,
            subject_id="12345",
        )
        assert r3 is not None

        dd = DataDescription(
            label="test_data",
            modality=Modality.SPIM,
            instrument_type="exaSPIM",
            subject_id="1234",
            data_level="raw data",
            creation_date=dt.date(),
            creation_time=dt.time(),
            institution=Institution.AIND,
            funding_source=[f],
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
            modality=Modality.SPIM,
            instrument_type="exaSPIM",
            subject_id="12345",
        )

        da2 = RawDataDescription.parse_obj(json.loads(da1.json()))

        assert da1.creation_time == da2.creation_time
        assert da1.creation_date == da2.creation_date
        assert da1.name == da2.name


if __name__ == "__main__":
    unittest.main()
