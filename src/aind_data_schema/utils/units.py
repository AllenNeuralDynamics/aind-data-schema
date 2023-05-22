"""Script for defining UnitWithValue classes"""

from enum import Enum
from typing import Generic, TypeVar

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
        MG = "milligram"

    class Frequency(Enum):
        """Enumeration of Frequency Measurements"""

        mHZ = "millihertz"
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

    class TimeMeasure(Enum):
        """Enumeration of Time Measurements"""

        S = "seconds"
        M = "minutes"
        HR = "hours"

    SizeType = TypeVar("SizeType", bound=Size)
    MassType = TypeVar("MassType", bound=Mass)
    FrequencyType = TypeVar("FrequencyType", bound=Frequency)
    VolumeType = TypeVar("VolumeType", bound=Volume)
    AngleType = TypeVar("AngleType", bound=Angle)
    TimeType = TypeVar("TimeType", bound=TimeMeasure)


ScalarType = TypeVar("ScalarType", float, int)


class GenericValues:
    """Constructs UnitWithValue class for each relevant measurement type"""

    class SizeValue(GenericModel, Generic[ScalarType, Units.SizeType]):
        """Generic for Size Measurements"""

        value: ScalarType
        unit: Units.SizeType = Units.Size.M

    class MassValue(GenericModel, Generic[ScalarType, Units.MassType]):
        """Generic for Mass Measurements"""

        value: ScalarType
        unit: Units.MassType = Units.Mass.G

    class VolumeValue(GenericModel, Generic[ScalarType, Units.VolumeType]):
        """Generic for Volume Measurements"""

        value: ScalarType
        unit: Units.VolumeType = Units.Volume.L

    class FrequencyValue(GenericModel, Generic[ScalarType, Units.FrequencyType]):
        """Generic for Frequency Measurements"""

        value: ScalarType
        unit: Units.FrequencyType = Units.Frequency.HZ

    class AngleValue(GenericModel, Generic[ScalarType, Units.AngleType]):
        """Generic for Angle Measurements"""

        value: ScalarType
        unit: Units.AngleType = Units.Angle.RAD

    class TimeValue(GenericModel, Generic[ScalarType, Units.TimeType]):
        """Generic for Time Measurements"""

        value: ScalarType
        unit: Units.AngleType = Units.TimeMeasure.S


SizeVal = GenericValues.SizeValue[ScalarType, Units.SizeType]
MassVal = GenericValues.MassValue[ScalarType, Units.MassType]
VolumeVal = GenericValues.VolumeValue[ScalarType, Units.VolumeType]
FrequencyVal = GenericValues.FrequencyValue[ScalarType, Units.FrequencyType]
AngleVal = GenericValues.AngleValue[ScalarType, Units.AngleType]
TimeVal = GenericValues.AngleValue[ScalarType, Units.TimeType]


# GenericType = TypeVar("GenericType", bound=)
# generictype = GenericValues.SizeValue[ScalarType, GenericType]

# val = generictype(value=,unit='potato')
