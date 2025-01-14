""" tests for base """

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, call, mock_open, patch

from pydantic import ValidationError, create_model, SkipValidation, Field
from typing import Literal

from aind_data_schema.base import (
    GenericModel,
    AwareDatetimeWithDefault,
    is_dict_corrupt,
    DataModel,
    DataCoreModel,
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

    def test_units(self):
        """Test that models with value/value_unit pairs throw errors properly"""

        class TestModel(DataModel):
            """temporary test model"""

            value: Optional[str] = Field(default=None)
            value_unit: Optional[str] = Field(default=None)

        self.assertRaises(ValidationError, lambda: TestModel(value="value"))

        test0 = TestModel(value="value", value_unit="unit")
        self.assertIsNotNone(test0)

        # it's fine if units are set and the value isn't
        test1 = TestModel(value_unit="unit")
        self.assertIsNotNone(test1)

        # Multi-unit condition
        class MultiModel(DataModel):
            """temporary test model with multiple variables"""

            value_multi_one_with_depth: Optional[str] = Field(default=None)
            value_multi_two_with_depth: Optional[str] = Field(default=None)
            value_multi_unit: Optional[str] = Field(default=None)

        self.assertRaises(ValidationError, lambda: MultiModel(value_multi_one_with_depth="value"))

        test2 = MultiModel(value_multi_one_with_depth="value1", value_multi_unit="unit")
        self.assertIsNotNone(test2)

        test3 = MultiModel(value_multi_unit="unit")
        self.assertIsNotNone(test3)

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

    def test_generic_model_constructor(self):
        """Tests default constructor for GenericModel"""
        model = GenericModel()
        self.assertEqual("{}", model.model_dump_json())

        params = {"foo": "bar"}
        model = GenericModel(**params)
        self.assertEqual('{"foo":"bar"}', model.model_dump_json())

    def test_generic_model_validate_fieldnames(self):
        """Tests that fieldnames are validated in GenericModel"""
        expected_error = "1 validation error for GenericModel\n" "  Value error, Field names cannot contain '.' or '$' "
        invalid_params = [
            {"$foo": "bar"},
            {"foo": {"foo.name": "bar"}},
        ]
        for params in invalid_params:
            with self.assertRaises(ValidationError) as e:
                GenericModel(**params)
            self.assertIn(expected_error, repr(e.exception))
            with self.assertRaises(ValidationError) as e:
                GenericModel.model_validate(params)
            self.assertIn(expected_error, repr(e.exception))

    def test_ccf_validator(self):
        """Tests that CCFStructure validator works"""

        class StructureModel(DataModel):
            """Test model with a targeted_structure"""

            targeted_structure: CCFStructure.ONE_OF

        self.assertRaises(ValueError, StructureModel, targeted_structure="invalid")

    def test_schema_bump(self):
        """Test that schema version are bumped successfully
        and that validation errors prevent bumping"""

        class Modelv1(DataCoreModel):
            """test class"""

            describedBy: str = "modelv1"
            schema_version: SkipValidation[Literal["1.0.0"]] = "1.0.0"

        class Modelv2(DataCoreModel):
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
        s.subject_id = "s" * (MAX_FILE_SIZE + 1000)
        s.write_standard_file(output_directory=Path("dir"), suffix=".foo.bar")

        mock_open.assert_has_calls([call(Path("dir/subject.foo.bar"), "w")])
        mock_logging_warning.assert_called_once_with(
            f"File size exceeds {MAX_FILE_SIZE / 1024} KB: dir/subject.foo.bar"
        )


if __name__ == "__main__":
    unittest.main()
