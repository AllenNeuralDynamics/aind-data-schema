"""Tests for the geometry module"""

import unittest

from aind_data_schema_models.units import SizeUnit

from aind_data_schema.components.geometry import Circle, Rectangle


class TestRectangle(unittest.TestCase):
    """Tests for the Rectangle class"""

    def test_create_rectangle(self):
        """Test creating a rectangle with specific dimensions and units"""
        rect = Rectangle(width=10.0, height=5.0, size_unit=SizeUnit.MM)
        self.assertEqual(rect.width, 10.0)
        self.assertEqual(rect.height, 5.0)
        self.assertEqual(rect.size_unit, SizeUnit.MM)

    def test_different_units(self):
        """Test creating a rectangle with different units"""
        rect = Rectangle(width=1.0, height=2.0, size_unit=SizeUnit.UM)
        self.assertEqual(rect.size_unit, SizeUnit.UM)


class TestCircle(unittest.TestCase):
    """Tests for the Circle class"""

    def test_create_circle(self):
        """Test creating a circle with specific radius and units"""
        circle = Circle(radius=3.0, radius_unit=SizeUnit.MM)
        self.assertEqual(circle.radius, 3.0)
        self.assertEqual(circle.radius_unit, SizeUnit.MM)

    def test_different_units(self):
        """Test creating a circle with different units"""
        circle = Circle(radius=500.0, radius_unit=SizeUnit.UM)
        self.assertEqual(circle.radius_unit, SizeUnit.UM)


if __name__ == "__main__":
    unittest.main()
