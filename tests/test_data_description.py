""" test DataDescription """

import datetime
import json
import os
import re
import unittest
from pathlib import Path
from typing import List

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.data_description import (
    AnalysisDescription,
    DataDescription,
    DataRegex,
    DerivedDataDescription,
    Funding,
    RawDataDescription,
    build_data_name,
)

DATA_DESCRIPTION_FILES_PATH = Path(__file__).parent / "resources" / "ephys_data_description"
PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


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
            data_descriptions.append((file_path, DataDescription.model_construct(**contents)))
        cls.data_descriptions = dict(data_descriptions)

    BAD_NAME = "fizzbuzz"
    BASIC_NAME = "1234_3033-12-21T042211"
    DERIVED_NAME = "1234_3033-12-21T042211_spikesorted-ks25_2022-10-12T232311"
    ANALYSIS_NAME = "project_analysis_3033-12-21T042211"

    def test_funding_construction(self):
        """Test Funding construction"""
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        self.assertIsNotNone(f)

    def test_raw_data_description_construction(self):
        """Test RawDataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = RawDataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level="raw",
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )
        self.assertIsNotNone(da)

    def test_derived_data_description_construction(self):
        """Test DerivedDataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = RawDataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level="raw",
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )
        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modalities=da.modalities,
            subject_id=da.subject_id,
            investigators=[Person(name="Jane Smith")],
        )
        self.assertIsNotNone(r1)

    def test_nested_derived_data_description_construction(self):
        """Test nested DerivedDataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = RawDataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level="raw",
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )
        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modalities=da.modalities,
            subject_id=da.subject_id,
            investigators=[Person(name="Jane Smith")],
        )
        r2 = DerivedDataDescription(
            input_data_name=r1.name,
            process_name="some-model",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modalities=r1.modalities,
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )
        r3 = DerivedDataDescription(
            input_data_name=r2.name,
            process_name="a-paper",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modalities=r2.modalities,
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )
        self.assertIsNotNone(r3)

    def test_data_description_construction(self):
        """Test DataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        dd = DataDescription(
            modalities=[Modality.SPIM],
            subject_id="1234",
            data_level="raw",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            investigators=[Person(name="Jane Smith")],
        )
        self.assertIsNotNone(dd)

    def test_data_description_construction_failure(self):
        """Test DataDescription construction failure"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        with self.assertRaises(ValidationError):
            DataDescription(
                modalities=[Modality.SPIM],
                subject_id="",
                data_level="raw",
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[Person(name="Jane Smith")],
            )

    def test_analysis_description_construction(self):
        """Test AnalysisDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        ad = AnalysisDescription(
            analysis_name="analysis",
            project_name="project",
            creation_time=dt,
            subject_id="1234",
            modalities=[Modality.SPIM],
            institution=Organization.AIND,
            funding_source=[f],
            investigators=[Person(name="Jane Smith")],
        )
        self.assertEqual(ad.name, build_data_name("project_analysis", dt))

    def test_analysis_description_invalid_name(self):
        """Test AnalysisDescription invalid name"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        with self.assertRaises(ValueError):
            AnalysisDescription(
                analysis_name="ana lysis",
                project_name="pro_ject",
                subject_id="1234",
                modalities=[Modality.SPIM],
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[Person(name="Jane Smith")],
            )

    def test_data_description_missing_fields(self):
        """Test DataDescription missing fields"""
        dt = datetime.datetime.now()
        with self.assertRaises(ValueError):
            DataDescription()
        with self.assertRaises(ValueError):
            DataDescription(creation_time=dt)

    def test_derived_data_description_missing_fields(self):
        """Test DerivedDataDescription missing fields"""
        dt = datetime.datetime.now()
        with self.assertRaises(ValueError):
            DerivedDataDescription()
        with self.assertRaises(ValueError):
            DerivedDataDescription(creation_time=dt)

    def test_analysis_description_missing_fields(self):
        """Test AnalysisDescription missing fields"""
        dt = datetime.datetime.now()
        with self.assertRaises(ValueError):
            AnalysisDescription()
        with self.assertRaises(ValueError):
            AnalysisDescription(creation_time=dt)

    def test_raw_data_description_invalid_platform(self):
        """Test RawDataDescription invalid platform"""
        with self.assertRaises(ValueError):
            RawDataDescription(platform="exaspim")

    def test_analysis_description_empty_fields(self):
        """Test AnalysisDescription empty fields"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        with self.assertRaises(ValueError):
            AnalysisDescription(
                analysis_name="",
                project_name="project",
                subject_id="1234",
                modalities=[Modality.SPIM],
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[Person(name="Jane Smith")],
            )
        with self.assertRaises(ValueError):
            AnalysisDescription(
                analysis_name="analysis",
                project_name="",
                subject_id="1234",
                modalities=[Modality.SPIM],
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[Person(name="Jane Smith")],
            )

    def test_pattern_errors(self):
        """Tests that errors are raised if malformed strings are input"""
        with self.assertRaises(ValidationError) as e:
            DataDescription(
                modalities=[Modality.SPIM],
                subject_id="1234",
                data_level="raw",
                project_name="a_32r&!#R$&#",
                creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[Person(name="Jane Smith")],
            )
        expected_exception = (
            "1 validation error for DataDescription\n"
            "project_name\n"
            f"  String should match pattern '{DataRegex.NO_SPECIAL_CHARS_EXCEPT_SPACE.value}'"
            " [type=string_pattern_mismatch, input_value='a_32r&!#R$&#', input_type=str]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/string_pattern_mismatch"
        )
        self.assertEqual(expected_exception, repr(e.exception))

    def test_model_constructors(self):
        """test static methods for constructing models"""

        assert Organization.from_abbreviation("AIND") == Organization.AIND
        assert Organization.from_name("Allen Institute for Neural Dynamics") == Organization.AIND
        assert Modality.from_abbreviation("ecephys") == Modality.ECEPHYS
        assert Organization().name_map["Allen Institute for Neural Dynamics"] == Organization.AIND

    def test_name_label_error(self):
        """Tests an error is raised if label and name are None"""

        with self.assertRaises(ValidationError) as e:
            DataDescription(
                modalities=[Modality.SPIM],
                subject_id="1234",
                data_level="raw",
                creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[Person(name="Jane Smith")],
            )
        self.assertTrue("Value error, Either label or name must be set" in repr(e.exception))

    def test_round_trip(self):
        """make sure we can round trip from json"""

        dt = datetime.datetime.now()

        da1 = RawDataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level="raw",
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            modalities=[Modality.SPIM],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )

        da2 = RawDataDescription.model_validate_json(da1.model_dump_json())
        self.assertEqual(da1.creation_time, da2.creation_time)
        self.assertEqual(da1.name, da2.name)

    def test_parse_name(self):
        """tests for parsing names"""

        toks = DataDescription.parse_name(self.BASIC_NAME)
        assert toks["label"] == "1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            DataDescription.parse_name(self.BAD_NAME)

        toks = RawDataDescription.parse_name(self.BASIC_NAME)
        assert toks["subject_id"] == "1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            RawDataDescription.parse_name(self.BAD_NAME)

        toks = DerivedDataDescription.parse_name(self.DERIVED_NAME)
        assert toks["input_data_name"] == "1234_3033-12-21T042211"
        assert toks["process_name"] == "spikesorted-ks25"
        assert toks["creation_time"] == datetime.datetime(2022, 10, 12, 23, 23, 11)

        with self.assertRaises(ValueError):
            DerivedDataDescription.parse_name(self.BAD_NAME)

        toks = AnalysisDescription.parse_name(self.ANALYSIS_NAME)
        assert toks["project_abbreviation"] == "project"
        assert toks["analysis_name"] == "analysis"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            AnalysisDescription.parse_name(self.BAD_NAME)

    def test_unique_abbreviations(self):
        """Tests that abbreviations are unique"""
        modality_abbreviations = [m().abbreviation for m in Modality.ALL]
        self.assertEqual(len(set(modality_abbreviations)), len(modality_abbreviations))


class DerivedDataDescriptionTest(unittest.TestCase):
    """test DerivedDataDescription"""

    def test_from_data_description(self):
        """Tests DerivedDataDescription.from_data_description method"""

        d1 = DataDescription(
            modalities=[Modality.SPIM],
            subject_id="1234",
            data_level="raw",
            creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            investigators=[Person(name="Jane Smith")],
        )

        process_name = "spikesorter"

        dd1 = DerivedDataDescription.from_data_description(d1, process_name=process_name)
        # check that the original name is in the derived name
        print(dd1.name)
        self.assertTrue("1234_2020-10-10T101010_spikesorter_" in dd1.name)
        # check that the subject ID is retained
        self.assertEqual("1234", dd1.subject_id)
        # check that the data level is upgraded
        self.assertEqual("derived", dd1.data_level)

    def test_derived_data_description_build_name(self):
        """Tests build name method in derived data description class"""

        dd = DerivedDataDescription(
            input_data_name="12345_2020-10-10T101010",
            creation_time=datetime.datetime(2021, 10, 10, 10, 10, 10),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
        )
        self.assertEqual("12345_2020-10-10T101010_2021-10-10T101010", dd.name)

        dd2 = DerivedDataDescription(
            input_data_name="12345_2020-10-10T101010",
            creation_time=datetime.datetime(2021, 10, 10, 10, 10, 10),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            process_name="spikesorter",
        )
        self.assertIn("12345_2020-10-10T101010_spikesorter", dd2.name)


if __name__ == "__main__":
    unittest.main()
