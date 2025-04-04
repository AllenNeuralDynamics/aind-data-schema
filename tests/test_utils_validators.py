""" Tests for compatibility check utilities """

import unittest
from aind_data_schema.utils.validators import (
    subject_specimen_id_compatibility,
    _recurse_helper,
    recursive_coord_system_check,
    recursive_get_all_names,
    SystemNameException,
    AxisCountException,
    CoordinateSystemException,
)
from enum import Enum
from pydantic import BaseModel
from aind_data_schema.components.coordinates import AtlasCoordinate


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
            AtlasCoordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
            AtlasCoordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
        ]
        _recurse_helper(data, system_name=self.system_name, axis_count=2)

    def test_recurse_helper_with_object(self):
        """Test _recurse_helper with a single coordinate object"""
        data = AtlasCoordinate(
            system_name=self.system_name,
            position=[0.5, 1],
        )
        _recurse_helper(data, system_name=self.system_name, axis_count=2)


class TestRecursiveCoordSystemCheck(unittest.TestCase):
    """Tests for recursive_coord_system_check function"""

    def setUp(self):
        """Set up test data"""
        self.system_name = "BREGMA_ARI"

    def test_recursive_coord_system_check_with_valid_data(self):
        """Test recursive_coord_system_check with valid data"""
        data = AtlasCoordinate(
            system_name=self.system_name,
            position=[0.5, 1],
        )
        recursive_coord_system_check(data, self.system_name, axis_count=2)

    def test_recursive_coord_system_check_with_invalid_system_name(self):
        """Test recursive_coord_system_check with invalid system name"""
        data = AtlasCoordinate(
            system_name="Invalid System",
            position=[0.5, 1],
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
            AtlasCoordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
            AtlasCoordinate(
                system_name=self.system_name,
                position=[0.5, 1],
            ),
        ]
        recursive_coord_system_check(data, self.system_name, axis_count=2)

    def test_recursive_coord_system_check_with_axis_count_mismatch(self):
        """Test recursive_coord_system_check with axis count mismatch"""
        data = AtlasCoordinate(
            system_name=self.system_name,
            position=[0.5, 1, 2],
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
            position: list[float] = [0.5, 1]

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
        data.child.coordinate.position = []
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


if __name__ == "__main__":
    unittest.main()
