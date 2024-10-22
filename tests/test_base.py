""" tests for Subject """

import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from pydantic import create_model, ValidationError, Field
from typing import Optional

from aind_data_schema.base import AwareDatetimeWithDefault, AindModel
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

        class TestModel(AindModel):
            value: Optional[str] = Field(default=None)
            value_unit: Optional[str] = Field(default=None)

        self.assertRaises(ValidationError, lambda: TestModel(
            value="value"
        ))

        test0 = TestModel(
            value="value",
            value_unit="unit"
        )
        self.assertIsNotNone(test0)

        # it's fine if units are set and the value isn't
        test1 = TestModel(
            value_unit="unit"
        )
        self.assertIsNotNone(test1)

        # Multi-unit condition
        class MultiModel(AindModel):
            value_one_with_depth: Optional[str] = Field(default=None)
            value_two_with_depth: Optional[str] = Field(default=None)
            value_unit: Optional[str] = Field(default=None)

        self.assertRaises(ValidationError, lambda: MultiModel(
            value_one_with_depth="value"
        ))

        test2 = MultiModel(
            value_one_with_depth="value1",
            value_unit="unit"
        )
        self.assertIsNotNone(test2)

        test3 = MultiModel(
            value_unit="unit"
        )
        self.assertIsNotNone(test3)


if __name__ == "__main__":
    unittest.main()
