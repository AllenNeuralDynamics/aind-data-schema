""" Tests for compatibility check utilities """

import unittest
from unittest.mock import MagicMock, patch
from aind_data_schema.utils.validators import (
    subject_specimen_id_compatibility,
    _recurse_helper,
    recursive_coord_system_check,
    recursive_get_all_names,
    recursive_check_paths,
    recursive_device_name_check,
    SystemNameException,
    AxisCountException,
    CoordinateSystemException,
)
from enum import Enum
from pydantic import BaseModel
from aind_data_schema.components.coordinates import Translation
from aind_data_schema.components.wrappers import AssetPath
from pathlib import Path


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


class TestRecurseHelper(unittest.TestCase):
    """Tests for _recurse_helper function"""

    def setUp(self):
        """Set up test data"""
        self.system_name = "BREGMA_ARI"

    def test_recurse_helper_with_list(self):
        """Test _recurse_helper with a list of coordinates"""
        data = [
            Translation(
                translation=[0.5, 1],
                system_name=self.system_name,
            ),
            Translation(
                translation=[0.5, 1],
                system_name=self.system_name,
            ),
        ]
        _recurse_helper(data, system_name=self.system_name, axis_count=2)

    def test_recurse_helper_with_object(self):
        """Test _recurse_helper with a single coordinate object"""
        data = Translation(
            translation=[0.5, 1],
            system_name=self.system_name,
        )
        _recurse_helper(data, system_name=self.system_name, axis_count=2)


class TestRecursiveCoordSystemCheck(unittest.TestCase):
    """Tests for recursive_coord_system_check function"""

    def setUp(self):
        """Set up test data"""
        self.system_name = "BREGMA_ARI"

    def test_recursive_coord_system_check_with_valid_data(self):
        """Test recursive_coord_system_check with valid data"""
        data = Translation(
            translation=[0.5, 1],
            system_name=self.system_name,
        )
        recursive_coord_system_check(data, self.system_name, axis_count=2)

    def test_recursive_coord_system_check_with_invalid_system_name(self):
        """Test recursive_coord_system_check with invalid system name"""
        data = Translation(
            translation=[0.5, 1],
            system_name="Invalid System",
        )
        with self.assertRaises(SystemNameException) as context:
            recursive_coord_system_check(data, self.system_name, axis_count=2)

        self.assertIn("System name mismatch", str(context.exception))

    def test_recursive_coord_system_check_with_empty_data(self):
        """Test recursive_coord_system_check with empty data"""
        data = None
        recursive_coord_system_check(data, self.system_name, axis_count=0)

    def test_recursive_coord_system_check_with_list_of_coordinates(self):
        """Test recursive_coord_system_check with a list of coordinates"""
        data = [
            Translation(
                translation=[0.5, 1],
                system_name=self.system_name,
            ),
            Translation(
                translation=[0.5, 1],
                system_name=self.system_name,
            ),
        ]
        recursive_coord_system_check(data, self.system_name, axis_count=2)

    def test_recursive_coord_system_check_with_axis_count_mismatch(self):
        """Test recursive_coord_system_check with axis count mismatch"""
        data = Translation(
            translation=[0.5, 1, 2],
            system_name=self.system_name,
        )
        with self.assertRaises(AxisCountException) as context:
            recursive_coord_system_check(data, self.system_name, axis_count=2)

        self.assertIn("Axis count mismatch", str(context.exception))

    def test_recursive_coord_system_check_with_missing_coordinate_system(self):
        """Test recursive_coord_system_check with missing coordinate system"""

        class MockData(BaseModel):
            """Test class"""

            system_name: str

        data = MockData(system_name=self.system_name)

        with self.assertRaises(CoordinateSystemException) as context:
            recursive_coord_system_check(data, None, axis_count=0)

        self.assertIn("CoordinateSystem is required", str(context.exception))

    def test_recursion(self):
        """Test actual recursion, where the system changes"""

        class SystemMock(BaseModel):
            """Test class"""

            name: str = "Client system"
            axes: list[bool] = [True, True]

        class CoordinateMock(BaseModel):
            """Test class"""

            system_name: str = "Client system"
            translation: list[float] = [0.5, 1]

        class ClientMockData(BaseModel):
            """Test class"""

            coordinate_system: SystemMock = SystemMock()
            coordinate: CoordinateMock = CoordinateMock()

        class ParentMockData(BaseModel):
            """Test class"""

            child: ClientMockData = ClientMockData()

        # No exception raised, because system_name and axis_count get replaced
        data = ParentMockData()
        recursive_coord_system_check(data, system_name="Parent system", axis_count=5)
        self.assertTrue(True)

        # Change the system name
        data = ParentMockData()
        data.child.coordinate.system_name = "Parent system"
        with self.assertRaises(SystemNameException) as context:
            recursive_coord_system_check(data, system_name="Parent system", axis_count=5)
        self.assertIn("System name mismatch", str(context.exception))

        # Change the axis count
        data = ParentMockData()
        data.child.coordinate.translation = []
        with self.assertRaises(AxisCountException) as context:
            recursive_coord_system_check(data, system_name="Parent system", axis_count=5)
        self.assertIn("Axis count mismatch", str(context.exception))

        # No parent system
        data = ParentMockData()
        recursive_coord_system_check(data, system_name=None, axis_count=None)


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


class TestRecursiveDeviceNameCheck(unittest.TestCase):
    """Tests for recursive_device_name_check function"""

    def setUp(self):
        """Set up test data"""
        self.implanted_devices = ["Device1", "Device2", "Device3"]

    def test_valid_implanted_device_name(self):
        """Test valid implanted device name"""
        obj = TestImplantedDevice(
            implanted_device_name="Device1",
        )
        recursive_device_name_check(obj, self.implanted_devices)

    def test_invalid_implanted_device_name(self):
        """Test invalid implanted device name"""
        obj = TestImplantedDevice(
            implanted_device_name="InvalidDevice",
        )
        with self.assertRaises(ValueError) as context:
            recursive_device_name_check(obj, self.implanted_devices)
        self.assertIn("implanted_device_name InvalidDevice not found in implanted_devices", str(context.exception))

    def test_valid_implanted_device_names(self):
        """Test valid implanted device names"""
        obj = TestImplantedDeviceNames(
            implanted_device_names=["Device1", "Device2"],
        )
        recursive_device_name_check(obj, self.implanted_devices)

    def test_invalid_implanted_device_names(self):
        """Test invalid implanted device names"""
        obj = TestImplantedDeviceNames(
            implanted_device_names=["Device1", "InvalidDevice"],
        )
        with self.assertRaises(ValueError) as context:
            recursive_device_name_check(obj, self.implanted_devices)
        self.assertIn(
            "implanted_device_names ['InvalidDevice'] not found in implanted_devices",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
