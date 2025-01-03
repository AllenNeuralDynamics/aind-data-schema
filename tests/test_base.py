""" tests for Subject """

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from pydantic import ValidationError, create_model, SkipValidation
from typing import Literal

from aind_data_schema.base import (
    AindGeneric,
    AwareDatetimeWithDefault,
    is_dict_corrupt,
    AindModel,
    AindCoreModel,
    MAX_FILE_SIZE,
)
from aind_data_schema.core.subject import Subject
from aind_data_schema_models.brain_atlas import CCFStructure


class BaseTests(unittest.TestCase):
    """tests for the base module"""

    def test_described_by(self):
        """test that described by works"""

        s = Subject.model_construct()

        self.assertEqual(
            "https://raw.githubusercontent.com/AllenNeuralDynamics/"
            "aind-data-schema/main/src/aind_data_schema/core/subject.py",
            s.describedBy,
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_write_standard_file(self, mock_open: MagicMock):
        """Tests writer with suffix and output directory defined"""

        s = Subject.model_construct()
        with patch("os.path.getsize", return_value=1):
            s.write_standard_file(output_directory=Path("dir"), suffix=".foo.bar")
        mock_open.assert_has_calls([call(Path("dir/subject.foo.bar"), "w")])
        self.assertEqual(1, 1)

    def test_aware_datetime_with_default(self):
        """Tests AwareDatetimeWithDefault adds tzinfo as default"""

        test_model = create_model("TempModel", dt=(AwareDatetimeWithDefault, ...))
        datetime_without_tz = datetime(2020, 10, 10, 1, 2, 3)
        expected_dt = datetime(2020, 10, 10, 1, 2, 3).astimezone()
        model_instance = test_model(dt=datetime_without_tz)

        # Verify that a timezone was attached if not supplied.
        self.assertEqual(expected_dt, model_instance.dt)

    def test_aware_datetime_with_setting(self):
        """Tests AwareDatetimeWithDefault honors timezone input by user"""

        test_model = create_model("TempModel", dt=(AwareDatetimeWithDefault, ...))
        datetime_with_tz = datetime(2020, 10, 10, 1, 2, 3, tzinfo=timezone.utc)
        model_instance = test_model(dt=datetime_with_tz)

        expected_json = '{"dt":"2020-10-10T01:02:03Z"}'
        self.assertEqual(expected_json, model_instance.model_dump_json())

    def test_is_dict_corrupt(self):
        """Tests is_dict_corrupt method"""
        good_contents = [
            {"a": 1, "b": {"c": 2, "d": 3}},
            {"a": 1, "b": {"c": 2, "d": 3}, "e": ["f", "g"]},
            {"a": 1, "b": {"c": 2, "d": 3}, "e": ["f.valid", "g"]},
            {"a": 1, "b": {"c": {"d": 2}, "e": 3}},
            {"a": 1, "b": [{"c": 2}, {"d": 3}], "e": 4},
        ]
        bad_contents = [
            {"a.1": 1, "b": {"c": 2, "d": 3}},
            {"a": 1, "b": {"c": 2, "$d": 3}},
            {"a": 1, "b": {"c": {"d": 2}, "$e": 3}},
            {"a": 1, "b": {"c": 2, "d": 3, "e.csv": 4}},
            {"a": 1, "b": [{"c": 2}, {"d.csv": 3}], "e": 4},
        ]
        invalid_types = [
            json.dumps({"a": 1, "b": {"c": 2, "d": 3}}),
            [{"a": 1}, {"b": {"c": 2, "d": 3}}],
            1,
            None,
        ]
        for contents in good_contents:
            with self.subTest(contents=contents):
                self.assertFalse(is_dict_corrupt(contents))
        for contents in bad_contents:
            with self.subTest(contents=contents):
                self.assertTrue(is_dict_corrupt(contents))
        for contents in invalid_types:
            with self.subTest(contents=contents):
                self.assertTrue(is_dict_corrupt(contents))

    def test_aind_generic_constructor(self):
        """Tests default constructor for AindGeneric"""
        model = AindGeneric()
        self.assertEqual("{}", model.model_dump_json())

        params = {"foo": "bar"}
        model = AindGeneric(**params)
        self.assertEqual('{"foo":"bar"}', model.model_dump_json())

    def test_aind_generic_validate_fieldnames(self):
        """Tests that fieldnames are validated in AindGeneric"""
        expected_error = "1 validation error for AindGeneric\n" "  Value error, Field names cannot contain '.' or '$' "
        invalid_params = [
            {"$foo": "bar"},
            {"foo": {"foo.name": "bar"}},
        ]
        for params in invalid_params:
            with self.assertRaises(ValidationError) as e:
                AindGeneric(**params)
            self.assertIn(expected_error, repr(e.exception))
            with self.assertRaises(ValidationError) as e:
                AindGeneric.model_validate(params)
            self.assertIn(expected_error, repr(e.exception))

    def test_ccf_validator(self):
        """Tests that CCFStructure validator works"""

        class StructureModel(AindModel):
            """Test model with a targeted_structure"""

            targeted_structure: CCFStructure.ONE_OF

        self.assertRaises(ValueError, StructureModel, targeted_structure="invalid")

    def test_schema_bump(self):
        """Test that schema version are bumped successfully
        and that validation errors prevent bumping"""

        class Modelv1(AindCoreModel):
            """test class"""

            describedBy: str = "modelv1"
            schema_version: SkipValidation[Literal["1.0.0"]] = "1.0.0"

        class Modelv2(AindCoreModel):
            """test class"""

            describedBy: str = "modelv2"
            schema_version: SkipValidation[Literal["1.0.1"]] = "1.0.1"
            extra_field: str = "extra_field"

        v1_init = Modelv1()
        self.assertEqual("1.0.0", v1_init.schema_version)

        v2_from_v1 = Modelv2(**v1_init.model_dump())
        self.assertEqual("1.0.1", v2_from_v1.schema_version)

        # Check that adding additional fields still fails validation
        # this is to ensure you can't get a bumped schema_version without passing validation
        self.assertRaises(ValidationError, lambda: Modelv1(**v2_from_v1.model_dump()))

    @patch("builtins.open", new_callable=mock_open)
    @patch("logging.warning")
    def test_write_standard_file_size_warning(self, mock_logging_warning: MagicMock, mock_open: MagicMock):
        """Tests that a warning is logged if the file size exceeds MAX_FILE_SIZE"""

        s = Subject.model_construct()
        s.subject_id = "s"*(MAX_FILE_SIZE + 1000)
        s.write_standard_file(output_directory=Path("dir"), suffix=".foo.bar")

        mock_open.assert_has_calls([call(Path("dir/subject.foo.bar"), "w")])
        mock_logging_warning.assert_called_once_with(
            f"File size exceeds {MAX_FILE_SIZE / 1024} KB: dir/subject.foo.bar"
        )


if __name__ == "__main__":
    unittest.main()
