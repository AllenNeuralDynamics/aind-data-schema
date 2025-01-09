""" tests for base """

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, call, mock_open, patch

from pydantic import Field, ValidationError, create_model

from aind_data_schema.base import GenericModel, MetadataModel, AwareDatetimeWithDefault, is_dict_corrupt
from aind_data_schema.core.subject import Subject


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

        class TestModel(MetadataModel):
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
        class MultiModel(MetadataModel):
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


if __name__ == "__main__":
    unittest.main()
