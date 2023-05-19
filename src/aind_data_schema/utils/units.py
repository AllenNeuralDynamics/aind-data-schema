from typing import Generic, TypeVar, Optional, List, Type, Union
from enum import Enum

from pydantic import BaseModel, validator, ValidationError, Field
from pydantic.generics import GenericModel

ScalarType = TypeVar("ScalarType", bound=Union[int, float])
UnitType = TypeVar("UnitType")


class ValueWithUnit(GenericModel, Generic[ScalarType, UnitType]):
    value: ScalarType 
    unit: UnitType


class Units:

    class Size(Enum):
        MM = "mm"
        CM = "cm"
        M = "m"
        KM = "km"
    
    

    class Mass(Enum):
        KG = "kg"
        G = "g"
        pass

    class Frequency(Enum):
        pass

    class Volume(Enum):
        L = "L"
        ML = "mL"
        pass


    SizeType = TypeVar("SizeType", bound=Size)
    MassType = TypeVar("MassType", bound=Mass)
    FrequencyType = TypeVar("FrequencyType", bound=Frequency)
    VolumeType = TypeVar("VolumeType", bound=Volume)


    # SizeValue = ValueWithUnit[ScalarType,SizeType]
    MassValue = ValueWithUnit[ScalarType,MassType]
    FrequencyValue = ValueWithUnit[ScalarType,FrequencyType]
    VolumeValue = ValueWithUnit[ScalarType,VolumeType]


# ScalarType = TypeVar('ScalarType')
# UnitType = TypeVar('UnitType', bound=str)

# class ScalarValue(GenericModel, Generic[ScalarType, UnitType]):
#     value: ScalarType
#     unit: UnitType


# class SizeUnit(Enum):
#     MM = "mm"
#     KM = "km"
    
# SizeValue = ScalarValue[float, SizeUnit]

class SizeValue(GenericModel, Generic[ScalarType,UnitType]):
        value: ScalarType
        unit: UnitType = Units.Size.CM