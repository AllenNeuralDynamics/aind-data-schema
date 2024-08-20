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
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.platforms import Platform
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

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
    BASIC_NAME = "ecephys_1234_3033-12-21_04-22-11"
    DERIVED_NAME = "ecephys_1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11"
    ANALYSIS_NAME = "project_analysis_3033-12-21_04-22-11"

    def test_constructors(self):
        """test building from component parts"""
        f = Funding(funder=Organization.NINDS, grant_number="grant001")

        dt = datetime.datetime.now()
        da = RawDataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level="raw",
            funding_source=[f],
            modality=[Modality.ECEPHYS],
            platform=Platform.ECEPHYS,
            subject_id="12345",
            investigators=[PIDName(name="Jane Smith")],
        )

        r1 = DerivedDataDescription(
            input_data_name=da.name,
            process_name="spikesort-ks25",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modality=da.modality,
            platform=da.platform,
            subject_id=da.subject_id,
            investigators=[PIDName(name="Jane Smith")],
        )

        r2 = DerivedDataDescription(
            input_data_name=r1.name,
            process_name="some-model",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modality=r1.modality,
            platform=r1.platform,
            subject_id="12345",
            investigators=[PIDName(name="Jane Smith")],
        )

        r3 = DerivedDataDescription(
            input_data_name=r2.name,
            process_name="a-paper",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            modality=r2.modality,
            platform=r2.platform,
            subject_id="12345",
            investigators=[PIDName(name="Jane Smith")],
        )
        assert r3 is not None

        dd = DataDescription(
            label="test_data",
            modality=[Modality.SPIM],
            platform=Platform.EXASPIM,
            subject_id="1234",
            data_level="raw",
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            investigators=[PIDName(name="Jane Smith")],
        )

        assert dd is not None

        # test construction fails
        with self.assertRaises(ValidationError):
            DataDescription(
                label="test_data",
                modality=[Modality.SPIM],
                platform="fake platform",
                subject_id="1234",
                data_level="raw",
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[PIDName(name="Jane Smith")],
            )

        ad = AnalysisDescription(
            analysis_name="analysis",
            project_name="project",
            creation_time=dt,
            subject_id="1234",
            modality=[Modality.SPIM],
            platform=Platform.EXASPIM,
            institution=Organization.AIND,
            funding_source=[f],
            investigators=[PIDName(name="Jane Smith")],
        )
        self.assertEqual(ad.name, build_data_name("project_analysis", dt))

        with self.assertRaises(ValueError):
            AnalysisDescription(
                analysis_name="ana lysis",
                project_name="pro_ject",
                subject_id="1234",
                modality=[Modality.SPIM],
                platform="exaspim",
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[PIDName(name="Jane Smith")],
            )

        with self.assertRaises(ValueError):
            DataDescription()

        with self.assertRaises(ValueError):
            DataDescription(creation_time=dt)

        with self.assertRaises(ValueError):
            DerivedDataDescription()

        with self.assertRaises(ValueError):
            DerivedDataDescription(creation_time=dt)

        with self.assertRaises(ValueError):
            AnalysisDescription()

        with self.assertRaises(ValueError):
            AnalysisDescription(creation_time=dt)

        with self.assertRaises(ValueError):
            RawDataDescription(platform="exaspim")

        with self.assertRaises(ValueError):
            AnalysisDescription(
                analysis_name="",
                project_name="project",
                subject_id="1234",
                modality=[Modality.SPIM],
                platform="exaspim",
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[PIDName(name="Jane Smith")],
            )

        with self.assertRaises(ValueError):
            AnalysisDescription(
                analysis_name="analysis",
                project_name="",
                subject_id="1234",
                modality=[Modality.SPIM],
                platform="exaspim",
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[PIDName(name="Jane Smith")],
            )

    def test_pattern_errors(self):
        """Tests that errors are raised if malformed strings are input"""
        with self.assertRaises(ValidationError) as e:
            DataDescription(
                label="test_data",
                modality=[Modality.SPIM],
                platform=Platform.EXASPIM,
                subject_id="1234",
                data_level="raw",
                project_name="a_32r&!#R$&#",
                creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[PIDName(name="Jane Smith")],
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
                modality=[Modality.SPIM],
                platform=Platform.EXASPIM,
                subject_id="1234",
                data_level="raw",
                creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[PIDName(name="Jane Smith")],
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
            modality=[Modality.SPIM],
            platform=Platform.EXASPIM,
            subject_id="12345",
            investigators=[PIDName(name="Jane Smith")],
        )

        da2 = RawDataDescription.model_validate_json(da1.model_dump_json())
        self.assertEqual(da1.creation_time, da2.creation_time)
        self.assertEqual(da1.name, da2.name)

    def test_parse_name(self):
        """tests for parsing names"""

        toks = DataDescription.parse_name(self.BASIC_NAME)
        assert toks["label"] == "ecephys_1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            DataDescription.parse_name(self.BAD_NAME)

        toks = RawDataDescription.parse_name(self.BASIC_NAME)
        assert toks["platform"] == Platform.ECEPHYS
        assert toks["subject_id"] == "1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            RawDataDescription.parse_name(self.BAD_NAME)

        toks = DerivedDataDescription.parse_name(self.DERIVED_NAME)
        assert toks["input_data_name"] == "ecephys_1234_3033-12-21_04-22-11"
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
        platform_abbreviations = [p().abbreviation for p in Platform.ALL]
        self.assertEqual(len(set(platform_abbreviations)), len(platform_abbreviations))

    def test_from_data_description(self):
        """Tests DerivedDataDescription.from_data_description method"""

        d1 = DataDescription(
            label="test_data",
            modality=[Modality.SPIM],
            platform=Platform.EXASPIM,
            subject_id="1234",
            data_level="raw",
            creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            investigators=[PIDName(name="Jane Smith")],
        )

        process_name = "spikesorter"

        dd1 = DerivedDataDescription.from_data_description(d1, process_name=process_name)
        dd2 = DerivedDataDescription.from_data_description(d1, process_name=process_name, subject_id="12345")
        self.assertTrue("test_data_2020-10-10_10-10-10_spikesorter_" in dd1.name)
        self.assertEqual("1234", dd1.subject_id)
        self.assertEqual("12345", dd2.subject_id)

    def test_derived_data_description_build_name(self):
        """Tests build name method in derived data description class"""

        dd = DerivedDataDescription(
            input_data_name="input",
            creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
            institution=Organization.AIND,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            modality=[Modality.ECEPHYS],
            platform=Platform.ECEPHYS,
            subject_id="12345",
            investigators=[PIDName(name="Jane Smith")],
        )
        self.assertEqual("input_2020-10-10_10-10-10", dd.name)


if __name__ == "__main__":
    unittest.main()
