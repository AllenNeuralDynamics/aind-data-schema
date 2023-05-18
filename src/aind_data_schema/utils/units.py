from typing import Generic, TypeVar, Optional, List, Type
from enum import Enum

from pydantic import BaseModel, validator, ValidationError, Field
from pydantic.generics import GenericModel


class Units:
    class Length:
        pass

    class Mass:
        pass

    class Frequency:
        pass

    class Volume:
        pass


ScalarType = TypeVar('ScalarType')
UnitType = TypeVar('UnitType', bound=str)

class ScalarValue(GenericModel, Generic[ScalarType, UnitType]):
    value: ScalarType
    unit: UnitType


class SizeUnit(Enum):
    MM = "mm"
    KM = "km"
    
SizeValue = ScalarValue[float, SizeUnit]