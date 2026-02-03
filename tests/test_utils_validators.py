""" Tests for compatibility check utilities """

import unittest
from datetime import date, datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Annotated
from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel
from aind_data_schema.components.coordinates import Rotation, Scale, Translation
from aind_data_schema.components.wrappers import AssetPath
from aind_data_schema.utils.validators import (
    TimeValidation,
    _convert_to_comparable,
    _recurse_helper,
    _system_check_helper,
    _time_validation_recurse_helper,
    _validate_time_constraint,
    recursive_check_paths,
    recursive_coord_system_check,
    recursive_get_all_names,
    recursive_time_validation_check,
    subject_specimen_id_compatibility,
    validate_creation_time_after_midnight,
)


class TestCompatibilityCheck(unittest.TestCase):
    """Tests compatibility checks"""

    def test_subj_spec_valid(self):
        """Test subject_id specimen_id valid"""
        subject_id = "123456"
        specimen_id = "123456-valid"
        self.assertTrue(subject_specimen_id_compatibility(subject_id, specimen_id))

    def test_subj_spec_invalid(self):
        """Test invalid subject_id specimen_id"""
        subject_id = "123456"
        specimen_id = "invalid"
        self.assertFalse(subject_specimen_id_compatibility(subject_id, specimen_id))


class TranslationWrapper(DataModel):
    """Wrapper for Translation class with a coordinate_system_name field"""

    coordinate_system_name: str
    translation: Translation


class TestRecurseHelper(unittest.TestCase):
    """Tests for _recurse_helper function"""

    def setUp(self):
        """Set up test data"""
        self.coordinate_system_name = "BREGMA_ARI"

    def test_recurse_helper_with_list(self):
        """Test _recurse_helper with a list of coordinates"""
        data = [
            TranslationWrapper(
                coordinate_system_name=self.coordinate_system_name,
                translation=Translation(
                    translation=[0.5, 1],
                ),
            ),
            TranslationWrapper(
                coordinate_system_name=self.coordinate_system_name,
                translation=Translation(
                    translation=[0.5, 1],
                ),
            ),
        ]
        _recurse_helper(data, coordinate_system_name=self.coordinate_system_name, axis_count=2)

    def test_recurse_helper_with_object(self):
        """Test _recurse_helper with a single coordinate object"""
        data = TranslationWrapper(
            coordinate_system_name=self.coordinate_system_name,
            translation=Translation(
                translation=[0.5, 1],
            ),
        )
        _recurse_helper(data, coordinate_system_name=self.coordinate_system_name, axis_count=2)


class TestRecursiveSystemCheckHelper(unittest.TestCase):
    """Test for _system_check_helper function"""

    def setUp(self):
        """Set up test data"""
        self.coordinate_system_name = "BREGMA_ARI"
        self.translation_wrapper = TranslationWrapper(
            coordinate_system_name=self.coordinate_system_name, translation=Translation(translation=[0.5, 1])
        )

    def test_system_check_helper_valid(self):
        """Test _system_check_helper with valid data"""
        _system_check_helper(self.translation_wrapper, self.coordinate_system_name, axis_count=2)
        # No exception raised means test passed

    def test_system_check_helper_missing_system_name(self):
        """Test _system_check_helper with missing coordinate_system_name"""
        with self.assertRaises(ValueError):
            _system_check_helper(self.translation_wrapper, None, axis_count=2)

    def test_system_check_helper_missing_axis_count(self):
        """Test _system_check_helper with missing axis_count"""
        with self.assertRaises(ValueError):
            _system_check_helper(self.translation_wrapper, self.coordinate_system_name, axis_count=None)

    def test_system_check_helper_wrong_system_name(self):
        """Test _system_check_helper with wrong coordinate_system_name"""
        with self.assertRaises(ValueError) as context:
            _system_check_helper(self.translation_wrapper, "WRONG_SYSTEM", axis_count=2)
        self.assertIn("WRONG_SYSTEM", str(context.exception))
        self.assertIn(self.coordinate_system_name, str(context.exception))

    def test_system_check_helper_wrong_axis_count(self):
        """Test _system_check_helper with wrong axis_count"""
        with self.assertRaises(ValueError) as context:
            _system_check_helper(self.translation_wrapper, self.coordinate_system_name, axis_count=3)
        self.assertIn("3", str(context.exception))
        self.assertIn("2", str(context.exception))

    def test_system_check_helper_multiple_axis_types(self):
        """Test _system_check_helper with multiple axis types"""

        class MultiAxisWrapper(DataModel):
            """Wrapper with multiple axis types"""

            coordinate_system_name: str
            translation: Translation
            rotation: Rotation
            scale: Scale

        obj = MultiAxisWrapper(
            coordinate_system_name=self.coordinate_system_name,
            translation=Translation(translation=[0.5, 1]),
            rotation=Rotation(angles=[90, 180]),
            scale=Scale(scale=[1.0, 2.0]),
        )

        _system_check_helper(obj, self.coordinate_system_name, axis_count=2)
        # No exception means test passed


class TestRecursiveCoordSystemCheck(unittest.TestCase):
    """Tests for recursive_coord_system_check function"""

    def setUp(self):
        """Set up test data"""
        self.coordinate_system_name = "BREGMA_ARI"

    def test_recursive_coord_system_check_with_valid_data(self):
        """Test recursive_coord_system_check with valid data"""
        data = TranslationWrapper(
            coordinate_system_name=self.coordinate_system_name,
            translation=Translation(
                translation=[0.5, 1],
            ),
        )
        recursive_coord_system_check(data, self.coordinate_system_name, axis_count=2)

    def test_recursive_coord_system_check_with_invalid_system_name(self):
        """Test recursive_coord_system_check with invalid system name"""
        data = TranslationWrapper(
            coordinate_system_name="Invalid system name",
            translation=Translation(
                translation=[0.5, 1],
            ),
        )
        with self.assertRaises(ValueError) as context:
            recursive_coord_system_check(data, self.coordinate_system_name, axis_count=2)

        self.assertIn("System name mismatch", str(context.exception))

    def test_recursive_coord_system_check_with_empty_data(self):
        """Test recursive_coord_system_check with empty data"""
        data = None
        recursive_coord_system_check(data, self.coordinate_system_name, axis_count=0)

    def test_recursive_coord_system_check_with_list_of_coordinates(self):
        """Test recursive_coord_system_check with a list of coordinates"""
        data = [
            TranslationWrapper(
                coordinate_system_name=self.coordinate_system_name,
                translation=Translation(
                    translation=[0.5, 1],
                ),
            ),
            TranslationWrapper(
                coordinate_system_name=self.coordinate_system_name,
                translation=Translation(
                    translation=[0.5, 1],
                ),
            ),
        ]
        recursive_coord_system_check(data, self.coordinate_system_name, axis_count=2)

    def test_recursive_coord_system_check_with_axis_count_mismatch(self):
        """Test recursive_coord_system_check with axis count mismatch"""
        data = TranslationWrapper(
            coordinate_system_name=self.coordinate_system_name,
            translation=Translation(
                translation=[0.5, 1, 2],
            ),
        )
        with self.assertRaises(ValueError) as context:
            recursive_coord_system_check(data, self.coordinate_system_name, axis_count=2)

        self.assertIn("Axis count mismatch", str(context.exception))

    def test_recursive_coord_system_check_with_missing_coordinate_system(self):
        """Test recursive_coord_system_check with missing coordinate system for object WITH transforms"""

        # Object with transforms should still require coordinate system
        data = TranslationWrapper(
            coordinate_system_name=self.coordinate_system_name, translation=Translation(translation=[0.5, 1])
        )

        with self.assertRaises(ValueError) as context:
            recursive_coord_system_check(data, None, axis_count=0)

        self.assertIn("CoordinateSystem is required", str(context.exception))

    def test_recursive_coord_system_check_object_without_transforms(self):
        """Test recursive_coord_system_check with object without transforms (should not require coordinate system)"""

        class ObjectWithoutTransforms(DataModel):
            """Object without any transform components"""

            coordinate_system_name: str
            some_field: str

        data = ObjectWithoutTransforms(coordinate_system_name=self.coordinate_system_name, some_field="test_value")

        # Should not raise any exception even with None coordinate_system_name and axis_count
        recursive_coord_system_check(data, None, axis_count=0)

    def test_system_check_helper_object_without_transforms(self):
        """Test _system_check_helper with object without transforms (should not require coordinate system)"""

        class ObjectWithoutTransforms(DataModel):
            """Object without any transform components"""

            coordinate_system_name: str
            some_field: str

        data = ObjectWithoutTransforms(coordinate_system_name=self.coordinate_system_name, some_field="test_value")

        # Should not raise any exception even with None coordinate_system_name and axis_count
        _system_check_helper(data, None, axis_count=0)

    def test_mixed_objects_with_and_without_transforms(self):
        """Test with a mix of objects with and without transforms"""

        class ObjectWithoutTransforms(DataModel):
            """Object without any transform components"""

            coordinate_system_name: str
            some_field: str

        class ContainerModel(DataModel):
            """Container with mixed objects"""

            with_transform: TranslationWrapper
            without_transform: ObjectWithoutTransforms

        container = ContainerModel(
            with_transform=TranslationWrapper(
                coordinate_system_name=self.coordinate_system_name, translation=Translation(translation=[0.5, 1])
            ),
            without_transform=ObjectWithoutTransforms(
                coordinate_system_name="any_name", some_field="test"  # This can be anything since no transforms
            ),
        )

        # Should pass validation - only the object with transforms is checked
        recursive_coord_system_check(container, self.coordinate_system_name, axis_count=2)


class MockEnum(Enum):
    """Mock Enum for testing"""

    VALUE1 = "value1"
    VALUE2 = "value2"


class NestedModel(BaseModel):
    """Nested model for testing"""

    name: str
    value: int


class ComplexModel(BaseModel):
    """Complex model for testing"""

    name: str
    nested: NestedModel
    nested_list: list[NestedModel]
    enum_field: MockEnum


class ComplexParentModel(BaseModel):
    """Multi-level model for testing"""

    name: str
    child: ComplexModel


class TestRecursiveGetAllNames(unittest.TestCase):
    """Tests for recursive_get_all_names function"""

    def test_single_level(self):
        """Test single level model"""
        model = NestedModel(name="test_name", value=42)
        result = recursive_get_all_names(model)
        self.assertEqual(result, ["test_name"])

    def test_nested_model(self):
        """Test nested model"""
        nested_model = NestedModel(name="nested_name", value=42)
        model = ComplexModel(
            name="complex_name",
            nested=nested_model,
            nested_list=[],
            enum_field=MockEnum.VALUE1,
        )
        result = recursive_get_all_names(model)
        self.assertEqual(result, ["complex_name", "nested_name"])

    def test_nested_list(self):
        """Test model with nested list"""
        nested_model0 = NestedModel(name="nested_name0", value=41)
        nested_model1 = NestedModel(name="nested_name1", value=42)
        nested_model2 = NestedModel(name="nested_name2", value=43)
        model = ComplexModel(
            name="complex_name",
            nested=nested_model0,
            nested_list=[nested_model1, nested_model2],
            enum_field=MockEnum.VALUE1,
        )
        result = recursive_get_all_names(model)
        self.assertEqual(result, ["complex_name", "nested_name0", "nested_name1", "nested_name2"])

    def test_empty_model(self):
        """Test empty model"""
        model = None
        result = recursive_get_all_names(model)
        self.assertEqual(result, [])

    def test_enum_field(self):
        """Test model with enum field"""
        nested_model = NestedModel(name="nested_name", value=42)
        model = ComplexModel(
            name="complex_name",
            nested=nested_model,
            nested_list=[],
            enum_field=MockEnum.VALUE1,
        )
        result = recursive_get_all_names(model)
        self.assertEqual(result, ["complex_name", "nested_name"])

    def test_multi_level(self):
        """Test multi-level nesting"""
        nested_model = NestedModel(name="nested_name", value=42)
        model = ComplexModel(
            name="complex_name",
            nested=nested_model,
            nested_list=[],
            enum_field=MockEnum.VALUE1,
        )
        parent_model = ComplexParentModel(name="parent_name", child=model)
        result = recursive_get_all_names(parent_model)
        self.assertEqual(result, ["parent_name", "complex_name", "nested_name"])


class TestRecursiveCheckPaths(unittest.TestCase):
    """Tests for recursive_check_paths function"""

    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_path_exists(self, mock_warning: MagicMock, mock_exists: MagicMock):
        """Test when the path exists"""
        mock_exists.return_value = True
        test_path = AssetPath("test_file.txt")
        recursive_check_paths(test_path, Path("/base/directory"))
        mock_warning.assert_not_called()
        recursive_check_paths(test_path, None)
        mock_warning.assert_not_called()

    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_path_does_not_exist(self, mock_warning: MagicMock, mock_exists: MagicMock):
        """Test when the path does not exist"""
        mock_exists.return_value = False
        test_path = AssetPath("test_file.txt")
        recursive_check_paths(test_path, Path("/base/directory"))
        mock_warning.assert_called_once_with(
            "AssetPath /base/directory/test_file.txt does not exist,"
            " ensure file paths are relative to the metadata directory"
        )

    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_nested_paths_in_list(self, mock_warning: MagicMock, mock_exists: MagicMock):
        """Test nested paths in a list"""
        mock_exists.side_effect = [True, False]
        test_paths = [AssetPath("existing_file.txt"), AssetPath("missing_file.txt")]
        recursive_check_paths(test_paths, Path("/base/directory"))
        mock_warning.assert_called_once_with(
            "AssetPath /base/directory/missing_file.txt does not exist,"
            " ensure file paths are relative to the metadata directory"
        )

    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_nested_paths_in_dict(self, mock_warning: MagicMock, mock_exists: MagicMock):
        """Test nested paths in a dictionary"""
        mock_exists.side_effect = [False, True]
        test_paths = {"file1": AssetPath("missing_file.txt"), "file2": AssetPath("existing_file.txt")}
        recursive_check_paths(test_paths, Path("/base/directory"))
        mock_warning.assert_called_once_with(
            "AssetPath /base/directory/missing_file.txt does not exist,"
            " ensure file paths are relative to the metadata directory"
        )

    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_nested_paths_in_object(self, mock_warning: MagicMock, mock_exists: MagicMock):
        """Test nested paths in a custom object"""

        class MockObject:
            """Test object"""

            def __init__(self, path1, path2):
                """Test object init"""
                self.path1 = path1
                self.path2 = path2

        mock_exists.side_effect = [False, True]
        obj = MockObject(AssetPath("missing_file.txt"), AssetPath("existing_file.txt"))
        recursive_check_paths(obj, Path("/base/directory"))
        mock_warning.assert_called_once_with(
            "AssetPath /base/directory/missing_file.txt does not exist,"
            " ensure file paths are relative to the metadata directory"
        )

    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_no_paths(self, mock_warning: MagicMock, mock_exists: MagicMock):
        """Test when no paths are present"""
        data = {"key": "value", "list": [1, 2, 3]}
        recursive_check_paths(data, Path("/base/directory"))
        mock_warning.assert_not_called()

    @patch("pathlib.Path.is_absolute")
    @patch("pathlib.Path.exists")
    @patch("logging.warning")
    def test_absolute_path_warning(self, mock_warning: MagicMock, mock_is_absolute: MagicMock, mock_exists: MagicMock):
        """Test when the path is absolute"""
        mock_is_absolute.return_value = True
        mock_exists.return_value = True
        test_path = AssetPath("/absolute/path/to/file.txt")
        recursive_check_paths(test_path, None)
        mock_warning.assert_called_with(
            "AssetPath /absolute/path/to/file.txt is absolute, ensure file paths are relative to the metadata directory"
        )

    @patch("pathlib.Path.is_absolute", return_value=False)
    @patch("pathlib.Path.exists", returns_value=True)
    @patch("logging.warning")
    def test_relative_path_no_warning(
        self, mock_warning: MagicMock, mock_is_absolute: MagicMock, mock_exists: MagicMock
    ):
        """Test when the path is relative"""
        test_path = AssetPath("relative/path/to/file.txt")
        recursive_check_paths(test_path, None)
        mock_warning.assert_not_called()

    def test_return_enum(self):
        """Test return enum"""
        data = MockEnum.VALUE1
        recursive_check_paths(data, None)
        self.assertTrue(True)
        # No exception raised, because enum is valid


class TestImplantedDevice(BaseModel):
    """Test class with implanted_device_name"""

    implanted_device_name: str


class TestImplantedDeviceNames(BaseModel):
    """Test class with implanted_device_names"""

    implanted_device_names: list[str]


class TestTimeValidation(unittest.TestCase):
    """Tests for time validation functions"""

    def setUp(self):
        """Set up test data"""
        self.start_time = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        self.end_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def test_validate_time_constraint_between_valid(self):
        """Test _validate_time_constraint with valid BETWEEN constraint"""
        valid_time = datetime(2023, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception
        _validate_time_constraint(valid_time, TimeValidation.BETWEEN, self.start_time, self.end_time, "test_field")

    def test_validate_time_constraint_between_invalid_before(self):
        """Test _validate_time_constraint with invalid BETWEEN constraint (before start)"""
        invalid_time = datetime(2023, 1, 1, 9, 0, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValueError) as context:
            _validate_time_constraint(
                invalid_time, TimeValidation.BETWEEN, self.start_time, self.end_time, "test_field"
            )
        self.assertIn("must be between", str(context.exception))
        self.assertIn("test_field", str(context.exception))

    def test_validate_time_constraint_between_invalid_after(self):
        """Test _validate_time_constraint with invalid BETWEEN constraint (after end)"""
        invalid_time = datetime(2023, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValueError) as context:
            _validate_time_constraint(
                invalid_time, TimeValidation.BETWEEN, self.start_time, self.end_time, "test_field"
            )
        self.assertIn("must be between", str(context.exception))
        self.assertIn("test_field", str(context.exception))

    def test_validate_time_constraint_after_valid(self):
        """Test _validate_time_constraint with valid AFTER constraint"""
        valid_time = datetime(2023, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception
        _validate_time_constraint(valid_time, TimeValidation.AFTER, self.start_time, self.end_time, "test_field")

    def test_validate_time_constraint_after_invalid(self):
        """Test _validate_time_constraint with invalid AFTER constraint"""
        invalid_time = datetime(2023, 1, 1, 9, 0, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValueError) as context:
            _validate_time_constraint(invalid_time, TimeValidation.AFTER, self.start_time, self.end_time, "test_field")
        self.assertIn("must be after", str(context.exception))
        self.assertIn("test_field", str(context.exception))

    def test_validate_time_constraint_before_valid(self):
        """Test _validate_time_constraint with valid BEFORE constraint"""
        valid_time = datetime(2023, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception
        _validate_time_constraint(valid_time, TimeValidation.BEFORE, self.start_time, self.end_time, "test_field")

    def test_validate_time_constraint_before_invalid(self):
        """Test _validate_time_constraint with invalid BEFORE constraint"""
        invalid_time = datetime(2023, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        with self.assertRaises(ValueError) as context:
            _validate_time_constraint(invalid_time, TimeValidation.BEFORE, self.start_time, self.end_time, "test_field")
        self.assertIn("must be before", str(context.exception))
        self.assertIn("test_field", str(context.exception))

    def test_time_validation_recurse_helper_with_list(self):
        """Test _time_validation_recurse_helper with a list"""

        class MockTimeModel(BaseModel):
            """Mock time model with a time field"""

            time_field: Annotated[datetime, TimeValidation.BETWEEN]

        data = [
            MockTimeModel(time_field=datetime(2023, 1, 1, 11, 0, 0, tzinfo=timezone.utc)),
            MockTimeModel(time_field=datetime(2023, 1, 1, 11, 30, 0, tzinfo=timezone.utc)),
        ]
        # Should not raise exception
        _time_validation_recurse_helper(data, self.start_time, self.end_time)

    def test_time_validation_recurse_helper_with_object(self):
        """Test _time_validation_recurse_helper with an object"""

        class MockTimeModel(BaseModel):
            """Mock time model with a time field"""

            time_field: Annotated[datetime, TimeValidation.BETWEEN]

        data = MockTimeModel(time_field=datetime(2023, 1, 1, 11, 0, 0, tzinfo=timezone.utc))
        # Should not raise exception
        _time_validation_recurse_helper(data, self.start_time, self.end_time)

    def test_recursive_time_validation_check_with_acquisition_times(self):
        """Test recursive_time_validation_check with acquisition times in data"""

        class MockAcquisition(BaseModel):
            """Mock acquisition model with time fields"""

            acquisition_start_time: AwareDatetimeWithDefault
            acquisition_end_time: AwareDatetimeWithDefault
            stream_start_time: Annotated[AwareDatetimeWithDefault, TimeValidation.BETWEEN]
            stream_end_time: Annotated[AwareDatetimeWithDefault, TimeValidation.BETWEEN]

        # Valid case
        data = MockAcquisition(
            acquisition_start_time=self.start_time,
            acquisition_end_time=self.end_time,
            stream_start_time=datetime(2023, 1, 1, 10, 30, 0, tzinfo=timezone.utc),
            stream_end_time=datetime(2023, 1, 1, 11, 30, 0, tzinfo=timezone.utc),
        )
        # Should not raise exception
        recursive_time_validation_check(data)

    def test_recursive_time_validation_check_with_invalid_times(self):
        """Test recursive_time_validation_check with invalid times"""

        class MockAcquisition(BaseModel):
            """Mock acquisition model with time fields"""

            stream_start_time: Annotated[AwareDatetimeWithDefault, TimeValidation.BETWEEN]
            stream_end_time: Annotated[AwareDatetimeWithDefault, TimeValidation.BETWEEN]

        # Invalid case - stream time before acquisition start
        data = MockAcquisition(
            stream_start_time=datetime(2023, 1, 1, 9, 0, 0, tzinfo=timezone.utc),  # Before acquisition start
            stream_end_time=datetime(2023, 1, 1, 11, 30, 0, tzinfo=timezone.utc),
        )

        with self.assertRaises(ValueError) as context:
            recursive_time_validation_check(data, self.start_time, self.end_time)
        self.assertIn("must be between", str(context.exception))

    def test_recursive_time_validation_check_with_none_data(self):
        """Test recursive_time_validation_check with None data"""
        # Should not raise exception
        recursive_time_validation_check(None)

    def test_recursive_time_validation_check_with_no_time_annotations(self):
        """Test recursive_time_validation_check with data that has no time annotations"""

        class MockData(BaseModel):
            """Mock data model with no time annotations"""

            regular_field: str

        data = MockData(regular_field="test")
        # Should not raise exception
        recursive_time_validation_check(data, self.start_time, self.end_time)


class TestValidateCreationTimeAfterMidnight(unittest.TestCase):
    """Tests for validate_creation_time_after_midnight function"""

    def setUp(self):
        """Set up test data"""
        self.reference_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def test_valid_creation_time_same_day(self):
        """Test valid creation time on same day"""
        creation_time = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception
        validate_creation_time_after_midnight(creation_time, self.reference_time)

    def test_valid_creation_time_next_day(self):
        """Test valid creation time on next day"""
        creation_time = datetime(2023, 1, 2, 5, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception
        validate_creation_time_after_midnight(creation_time, self.reference_time)

    def test_valid_creation_time_at_midnight(self):
        """Test valid creation time exactly at midnight"""
        creation_time = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception
        validate_creation_time_after_midnight(creation_time, self.reference_time)

    def test_invalid_creation_time_before_midnight(self):
        """Test invalid creation time before midnight of reference day"""
        creation_time = datetime(2022, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        with self.assertRaises(ValueError) as context:
            validate_creation_time_after_midnight(creation_time, self.reference_time)
        self.assertIn("must be on or after midnight", str(context.exception))

    def test_timezone_naive_creation_time(self):
        """Test timezone-naive creation time gets reference timezone"""
        creation_time = datetime(2023, 1, 1, 10, 0, 0)  # No timezone
        # Should not raise exception - timezone will be added from reference
        validate_creation_time_after_midnight(creation_time, self.reference_time)

    def test_timezone_naive_creation_time_invalid(self):
        """Test timezone-naive creation time that's invalid"""
        creation_time = datetime(2022, 12, 31, 10, 0, 0)  # No timezone, day before
        with self.assertRaises(ValueError) as context:
            validate_creation_time_after_midnight(creation_time, self.reference_time)
        self.assertIn("must be on or after midnight", str(context.exception))

    def test_none_creation_time(self):
        """Test None creation time"""
        # Should not raise exception
        validate_creation_time_after_midnight(None, self.reference_time)

    def test_none_reference_time(self):
        """Test None reference time"""
        creation_time = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        # Should not raise exception - function returns early when reference_time is None
        validate_creation_time_after_midnight(creation_time, None)

    def test_different_timezones(self):
        """Test with different timezones"""
        # Reference time in UTC
        reference_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        # Creation time in different timezone (EST = UTC-5)
        est = timezone(timedelta(hours=-5))
        creation_time = datetime(2023, 1, 1, 7, 0, 0, tzinfo=est)  # Same moment as 12:00 UTC
        # Should not raise exception
        validate_creation_time_after_midnight(creation_time, reference_time)

    def test_date_object_creation_time(self):
        """Test with date object instead of datetime"""
        from datetime import date

        creation_date = date(2023, 1, 1)
        # Should not raise exception - date gets converted to datetime at midnight
        validate_creation_time_after_midnight(creation_date, self.reference_time)

    def test_invalid_date_object_creation_time(self):
        """Test with invalid date object"""
        from datetime import date

        creation_date = date(2022, 12, 31)  # Day before reference
        with self.assertRaises(ValueError) as context:
            validate_creation_time_after_midnight(creation_date, self.reference_time)
        self.assertIn("must be on or after midnight", str(context.exception))


class TestConvertToComparable(unittest.TestCase):
    """Tests for _convert_to_comparable function"""

    def test_convert_date_to_datetime(self):
        """Test converting date to datetime with timezone from reference"""
        reference_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        test_date = date(2023, 1, 2)

        result = _convert_to_comparable(test_date, reference_time)

        expected = datetime(2023, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

    def test_return_datetime_unchanged(self):
        """Test that datetime objects are returned unchanged"""
        reference_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        test_datetime = datetime(2023, 1, 2, 10, 30, 0, tzinfo=timezone.utc)

        result = _convert_to_comparable(test_datetime, reference_time)

        self.assertEqual(result, test_datetime)


if __name__ == "__main__":
    unittest.main()
