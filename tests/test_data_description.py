""" test DataDescription """

import datetime
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from aind_data_schema_models.data_name_patterns import DataLevel
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import ValidationError

from aind_data_schema.core.data_description import DataDescription, Funding, build_data_name
from aind_data_schema.components.identifiers import Person

DATA_DESCRIPTION_FILES_PATH = Path(__file__).parent / "resources" / "ephys_data_description"


class DataDescriptionTest(unittest.TestCase):
    """test DataDescription"""

    BAD_NAME = "fizzbuzz"
    BASIC_NAME = "1234_3033-12-21_04-22-11"
    DERIVED_NAME = "1234_3033-12-21_04-22-11_spikesorted-ks25_2022-10-12_23-23-11"

    def test_funding_construction(self):
        """Test Funding construction"""
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        self.assertIsNotNone(f)

    def test_raw_data_description_construction(self):
        """Test DataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )
        self.assertIsNotNone(da)

    def test_build_name(self):
        """Test build_data_name function"""
        dt = datetime.datetime(2022, 10, 12, 23, 23, 11)
        name = build_data_name("project", dt)
        self.assertEqual(name, "project_2022-10-12_23-23-11")

    @patch("aind_data_schema.core.data_description.build_data_name")
    def test_build_name_validation_error(self, mock_build_data_name: MagicMock):
        """Test build_data_name function to trigger validation error"""
        mock_build_data_name.return_value = "invalid"

        dt = datetime.datetime(2022, 10, 12, 23, 23, 11)
        with self.assertRaises(ValueError):
            DataDescription(
                modalities=[Modality.SPIM],
                subject_id="1234",
                data_level=DataLevel.RAW,
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[Person(name="Jane Smith")],
                project_name="Test",
            )

    def test_derived_data_description_construction(self):
        """Test DataDescription.data_level == DERIVED construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )
        r1 = DataDescription.from_raw(da, "spikesort-ks25", creation_time=dt)
        self.assertIsNotNone(r1)

    def test_nested_derived_data_description_construction(self):
        """Test nested derived DataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )
        r1 = DataDescription.from_raw(da, "spikesort-ks25", creation_time=dt)
        r2 = DataDescription.from_raw(r1, "some-model", creation_time=dt)
        r3 = DataDescription.from_raw(r2, "a-paper", creation_time=dt)
        self.assertIsNotNone(r3)

    def test_data_description_construction(self):
        """Test DataDescription construction"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        dd = DataDescription(
            modalities=[Modality.SPIM],
            subject_id="1234",
            data_level=DataLevel.RAW,
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
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
                data_level=DataLevel.RAW,
                creation_time=dt,
                institution=Organization.AIND,
                funding_source=[f],
                investigators=[Person(name="Jane Smith")],
                project_name="Test",
            )

    def test_parse_name_invalid(self):
        """Test DataDescription construction failure with invalid data level"""

        with self.assertRaises(ValueError) as context:
            DataDescription.parse_name("name", "invalid_data_level")
        self.assertIn("DataLevel", str(context.exception))

    def test_derived_valid(self):
        """Test that you can construct a valid derived DataDescription"""

        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        dr = DataDescription(
            modalities=[Modality.SPIM],
            subject_id="1234",
            data_level=DataLevel.RAW,
            creation_time=dt,
            institution=Organization.AIND,
            funding_source=[f],
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )

        # also over-write with specimen ID
        dd = DataDescription.from_raw(dr, "process", subject_id="1234-56")
        self.assertIsNotNone(dd)

    def test_raw_no_subject_id(self):
        """Test that creating a raw data description without subject_id raises an error"""
        dt = datetime.datetime.now()

        with self.assertRaises(ValueError) as context:
            DataDescription(
                creation_time=dt,
                institution=Organization.AIND,
                data_level=DataLevel.RAW,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                modalities=[Modality.ECEPHYS],
                investigators=[Person(name="Jane Smith")],
                project_name="Test",
            )

        self.assertIn("subject_id", str(context.exception))

    def test_derived_bad_creation_time(self):
        """Test that a validation error is raised if the creation time is not a datetime object"""
        dt = datetime.datetime.now()

        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )

        with self.assertRaises(ValueError) as context:
            DataDescription.from_raw(da, "spikesort-ks25", creation_time="invalid creation time")

        self.assertIn("creation_time", str(context.exception))

    def test_data_description_missing_fields(self):
        """Test DataDescription missing fields"""
        with self.assertRaises(ValidationError):
            DataDescription()

    def test_pattern_errors(self):
        """Tests that errors are raised if malformed strings are input"""
        with self.assertRaises(ValidationError) as e:
            DataDescription(
                modalities=[Modality.SPIM],
                subject_id="1234",
                data_level=DataLevel.RAW,
                project_name="a_32r&!#R$&#",
                creation_time=datetime.datetime(2020, 10, 10, 10, 10, 10),
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[Person(name="Jane Smith")],
            )
        self.assertIn("String should match pattern", str(e.exception))

    def test_model_constructors(self):
        """test static methods for constructing models"""

        assert Organization.from_abbreviation("AIND") == Organization.AIND
        assert Organization.from_name("Allen Institute for Neural Dynamics") == Organization.AIND
        assert Modality.from_abbreviation("ecephys") == Modality.ECEPHYS
        assert Organization().name_map["Allen Institute for Neural Dynamics"] == Organization.AIND

    def test_round_trip(self):
        """make sure we can round trip from json"""

        dt = datetime.datetime.now()

        da1 = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
            modalities=[Modality.SPIM],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )

        da2 = DataDescription.model_validate_json(da1.model_dump_json())
        self.assertEqual(da1.creation_time, da2.creation_time)
        self.assertEqual(da1.name, da2.name)

    def test_parse_name(self):
        """tests for parsing names"""

        toks = DataDescription.parse_name(self.BASIC_NAME, DataLevel.RAW)
        assert toks["label"] == "1234"
        assert toks["creation_time"] == datetime.datetime(3033, 12, 21, 4, 22, 11)

        with self.assertRaises(ValueError):
            DataDescription.parse_name(self.BAD_NAME, DataLevel.RAW)

        toks = DataDescription.parse_name(self.DERIVED_NAME, DataLevel.DERIVED)
        assert toks["input"] == "1234_3033-12-21_04-22-11"
        assert toks["process_name"] == "spikesorted-ks25"
        assert toks["creation_time"] == datetime.datetime(2022, 10, 12, 23, 23, 11)

        with self.assertRaises(ValueError):
            DataDescription.parse_name(self.BAD_NAME, DataLevel.DERIVED)

    def test_unique_abbreviations(self):
        """Tests that abbreviations are unique"""
        modality_abbreviations = [m().abbreviation for m in Modality.ALL]
        self.assertEqual(len(set(modality_abbreviations)), len(modality_abbreviations))

    def test_source_data_field(self):
        """Tests the source_data field behavior"""

        # source_data should not be set for raw data
        with self.assertRaises(ValueError) as context:
            DataDescription(
                modalities=[Modality.SPIM],
                subject_id="1234",
                data_level=DataLevel.RAW,
                creation_time=datetime.datetime.now(),
                institution=Organization.AIND,
                funding_source=[Funding(funder=Organization.NINDS, grant_number="grant001")],
                investigators=[Person(name="Jane Smith")],
                project_name="Test",
                source_data=["some_source_data"],
            )
        self.assertIn("source_data must not be set when data_level is 'raw'", str(context.exception))

        # source_data should be set correctly for derived data
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")
        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )
        r1 = DataDescription.from_raw(da, "spikesort-ks25", creation_time=dt)
        self.assertIsNotNone(r1.source_data)
        self.assertEqual(len(r1.source_data), 1)
        self.assertEqual(r1.source_data[0], da.name)

    def test_from_raw_with_explicit_source_data(self):
        """Test from_raw with explicitly provided source_data parameter"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")

        # Create a raw DataDescription
        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )

        # Test scenario 3: RAW data → DERIVED with explicit source_data
        explicit_source = ["external_dataset_1", "external_dataset_2"]
        r1 = DataDescription.from_raw(da, "spikesort-ks25", source_data=explicit_source, creation_time=dt)

        # Should use the explicit source_data instead of the original name
        self.assertIsNotNone(r1.source_data)
        self.assertEqual(len(r1.source_data), 2)
        self.assertEqual(r1.source_data, explicit_source)
        self.assertNotIn(da.name, r1.source_data)

        # Test scenario 4: DERIVED data → DERIVED with additional source_data
        additional_source = ["another_external_dataset"]
        r2 = DataDescription.from_raw(r1, "clustering", source_data=additional_source, creation_time=dt)

        # Should combine existing source_data with new source_data
        self.assertIsNotNone(r2.source_data)
        self.assertEqual(len(r2.source_data), 3)  # 2 from r1 + 1 additional
        self.assertEqual(r2.source_data[:2], explicit_source)  # First two should be from r1
        self.assertEqual(r2.source_data[2:], additional_source)  # Last one should be additional

    def test_from_raw_chained_source_data_behavior(self):
        """Test source_data behavior in chained derived data without explicit source_data"""
        dt = datetime.datetime.now()
        f = Funding(funder=Organization.NINDS, grant_number="grant001")

        # Create a raw DataDescription
        da = DataDescription(
            creation_time=dt,
            institution=Organization.AIND,
            data_level=DataLevel.RAW,
            funding_source=[f],
            modalities=[Modality.ECEPHYS],
            subject_id="12345",
            investigators=[Person(name="Jane Smith")],
            project_name="Test",
        )

        # First derivation: RAW → DERIVED (should set source_data to original name)
        r1 = DataDescription.from_raw(da, "spikesort-ks25", creation_time=dt)
        self.assertEqual(r1.source_data, [da.name])

        # Second derivation: DERIVED → DERIVED (should append to existing source_data)
        r2 = DataDescription.from_raw(r1, "clustering", creation_time=dt)
        self.assertEqual(len(r2.source_data), 2)
        self.assertEqual(r2.source_data[0], da.name)  # Original source
        self.assertEqual(r2.source_data[1], r1.name)  # Previous derived data

        # Third derivation: should continue the chain
        r3 = DataDescription.from_raw(r2, "analysis", creation_time=dt)
        self.assertEqual(len(r3.source_data), 3)
        self.assertEqual(r3.source_data[0], da.name)  # Original source
        self.assertEqual(r3.source_data[1], r1.name)  # First derived
        self.assertEqual(r3.source_data[2], r2.name)  # Second derived


if __name__ == "__main__":
    unittest.main()
