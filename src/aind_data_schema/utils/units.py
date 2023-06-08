"""Script for defining UnitWithValue classes"""

from enum import Enum

from pydantic import create_model


class Size(Enum):
    """Enumeration of Length Measurements"""

    M = "meter"
    CM = "centimeter"
    MM = "millimeter"

    UM = "micrometer"
    NM = "nanometer"
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


class Power(Enum):
    UW = "microwatt"
    MW = "milliwatt"
    UA = "microamps"


def create_unit_with_value(model_name, scalar_type, unit_type, unit_default):
    """this uses create_model instead of generics, which lets us set default values"""

    m = create_model(model_name, value=(scalar_type, ...), unit=(unit_type, unit_default))
    return m


SizeValue = create_unit_with_value("SizeValue", float, Size, Size.MM)

SizeValueCM = create_unit_with_value("SizeValueCM", float, Size, Size.CM)
SizeValuePX = create_unit_with_value("SizeValuePX", int, Size, Size.PX)

WaveLengthNM = create_unit_with_value("WaveLengthNM", int, Size, Size.NM)
MassValue = create_unit_with_value("MassValue", float, Mass, Mass.MG)
VolumeValue = create_unit_with_value("VolumeValue", float, Volume, Volume.NL)
FrequencyValue = create_unit_with_value("FrequencyValue", float, Frequency, Frequency.HZ)
AngleValue = create_unit_with_value("AngleValue", float, Angle, Angle.DEG)
TimeValue = create_unit_with_value("TimeValue", float, TimeMeasure, TimeMeasure.S)
PowerValue = create_unit_with_value("PowerValue", float, Power, Power.MW)
