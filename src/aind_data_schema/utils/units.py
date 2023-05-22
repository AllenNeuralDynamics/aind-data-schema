"""Script for defining UnitWithValue classes"""

from typing import Generic, TypeVar, Optional, List, Type, Union
from enum import Enum

from pydantic import BaseModel, validator, ValidationError, Field
from pydantic.generics import GenericModel


class Units:
    """Class containing enumerations of relevant measurement types"""

    class Size(Enum):
        """Enumeration of Length Measurements"""

        MM = "millimetre"
        CM = "centimetre"
        M = "metre"
        KM = "kilometre"
    

    class Mass(Enum):
        """Enumeration of Mass Measurements"""

        KG = "kilogram"
        G = "gram"
        

    class Frequency(Enum):
        """Enumeration of Frequency Measurements"""

        mHZ = "millihertz" # UGH this is bad
        HZ = "hertz"
        KHZ = "kilohertz"
        MHZ = "megahertz"
        GHZ = "gigahertz"
        THZ = "terahertz"


    class Volume(Enum):
        """Enumeration of Volume Measurements"""

        L = "litre"
        ML = "millilitre"


    class Angle(Enum):
        """Enumeration of Angle Measurements"""

        RAD = "radians"
        DEG = "degrees"


ScalarType = TypeVar("ScalarType", float, int)


class GenericValues:
    """Constructs UnitWithValue class for each relevant measurement type"""

    SizeType = TypeVar("SizeType", bound=Units.Size)
    MassType = TypeVar("MassType", bound=Units.Mass)
    FrequencyType = TypeVar("FrequencyType", bound=Units.Frequency)
    VolumeType = TypeVar("VolumeType", bound=Units.Volume)
    AngleType = TypeVar("AngleType", bound=Units.Angle)


    class SizeValue(GenericModel, Generic[ScalarType, SizeType]):
        """Generic for Size Measurements"""

        value: ScalarType
        unit: Units.SizeType = Units.Size.M


    class MassValue(GenericModel, Generic[ScalarType, MassType]):
        """Generic for Mass Measurements"""

        value: ScalarType
        unit: Units.MassType = Units.Mass.G


    class VolumeValue(GenericModel, Generic[ScalarType, VolumeType]):
        """Generic for Volume Measurements"""
        
        value: ScalarType
        unit: Units.VolumeType = Units.Volume.L


    class FrequencyValue(GenericModel, Generic[ScalarType, FrequencyType]):
        """Generic for Frequency Measurements"""
        
        value: ScalarType
        unit: Units.FrequencyType = Units.Frequency.HZ


    class AngleValue(GenericModel, Generic[ScalarType, AngleType]):
        """Generic for Angle Measurements"""
        
        value: ScalarType
        unit: Units.AngleType = Units.Angle.RAD


SizeVal = GenericValues.SizeValue[ScalarType, Units.SizeType]
MassVal = GenericValues.MassValue[ScalarType, Units.MassType]
VolumeVal = GenericValues.VolumeValue[ScalarType, Units.VolumeType]
FrequencyVal = GenericValues.FrequencyValue[ScalarType, Units.FrequencyType]
AngleVal = GenericValues.AngleValue[ScalarType, Units.AngleType]