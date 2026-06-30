"""Classes to define geometry"""

from aind_data_schema_models.units import SizeUnit
from pydantic import Field

from aind_data_schema.base import DataModel


class Rectangle(DataModel):
    """Rectangle geometry"""

    width: float = Field(..., title="Width")
    height: float = Field(..., title="Height")
    size_unit: SizeUnit = Field(..., title="Size unit")


class Circle(DataModel):
    """Circle geometry"""

    radius: float = Field(..., title="Radius")
    radius_unit: SizeUnit = Field(..., title="Radius unit")
