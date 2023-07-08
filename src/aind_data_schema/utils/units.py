"""Script for defining UnitWithValue classes"""

from decimal import Decimal
from enum import Enum

from pydantic import create_model


class Size(Enum):
    """Enumeration of Length Measurements"""

    M = "meter"
    CM = "centimeter"
    MM = "millimeter"
    UM = "micrometer"
    NG = "nanometer"
    IN = "inch"
    PX = "pixel"


class Mass(Enum):
    """Enumeration of Mass Measurements"""

    KG = "kilogram"
    G = "gram"
    MG = "milligram"
    UG = "microgram"
    NG = "nanogram"


class Frequency(Enum):
    """Enumeration of Frequency Measurements"""

    KHZ = "kilohertz"
    HZ = "hertz"
    mHZ = "millihertz"


class Volume(Enum):
    """Enumeration of Volume Measurements"""

    L = "liter"
    ML = "milliliter"
    UL = "microliter"
    NL = "nanoliter"


class Angle(Enum):
    """Enumeration of Angle Measurements"""

    RAD = "radians"
    DEG = "degrees"


class TimeMeasure(Enum):
    """Enumeration of Time Measurements"""

    HR = "hour"
    M = "minute"
    S = "second"
    MS = "milisecond"
    US = "microsecond"
    NS = "nanosecond"


def create_unit_with_value(model_name, scalar_type, unit_type, unit_default):
    """this uses create_model instead of generics, which lets us set default values"""

    m = create_model(model_name, value=(scalar_type, ...), unit=(unit_type, unit_default))
    return m


SizeValue = create_unit_with_value("SizeValue", Decimal, Size, Size.MM)
MassValue = create_unit_with_value("MassValue", Decimal, Mass, Mass.MG)
VolumeValue = create_unit_with_value("VolumeValue", Decimal, Volume, Volume.NL)
FrequencyValue = create_unit_with_value("FrequencyValue", Decimal, Frequency, Frequency.HZ)
AngleValue = create_unit_with_value("AngleValue", Decimal, Angle, Angle.DEG)
TimeValue = create_unit_with_value("TimeValue", Decimal, TimeMeasure, TimeMeasure.S)
