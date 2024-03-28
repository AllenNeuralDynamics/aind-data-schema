"""Module for defining UnitWithValue classes"""

from decimal import Decimal
from enum import Enum

from pydantic import create_model


class SizeUnit(str, Enum):
    """Enumeration of Length Measurements"""

    M = "meter"
    CM = "centimeter"
    MM = "millimeter"
    UM = "micrometer"
    NM = "nanometer"
    IN = "inch"
    PX = "pixel"


class MassUnit(str, Enum):
    """Enumeration of Mass Measurements"""

    KG = "kilogram"
    G = "gram"
    MG = "milligram"
    UG = "microgram"
    NG = "nanogram"


class FrequencyUnit(str, Enum):
    """Enumeration of Frequency Measurements"""

    KHZ = "kilohertz"
    HZ = "hertz"
    mHZ = "millihertz"


class SpeedUnit(str, Enum):
    """Enumeration of Speed Measurements"""

    RPM = "rotations per minute"


class VolumeUnit(str, Enum):
    """Enumeration of Volume Measurements"""

    L = "liter"
    ML = "milliliter"
    UL = "microliter"
    NL = "nanoliter"


class AngleUnit(str, Enum):
    """Enumeration of Angle Measurements"""

    RAD = "radians"
    DEG = "degrees"


class TimeUnit(str, Enum):
    """Enumeration of Time Measurements"""

    HR = "hour"
    M = "minute"
    S = "second"
    MS = "millisecond"
    US = "microsecond"
    NS = "nanosecond"


class PowerUnit(str, Enum):
    """Unit for power, set or measured"""

    UW = "microwatt"
    MW = "milliwatt"
    PERCENT = "percent"


class CurrentUnit(str, Enum):
    """Current units"""

    UA = "microamps"


class ConcentrationUnit(str, Enum):
    """Concentraion units"""

    M = "molar"
    UM = "micromolar"
    NM = "nanomolar"
    MASS_PERCENT = "% m/m"
    VOLUME_PERCENT = "% v/v"


class TemperatureUnit(str, Enum):
    """Temperature units"""

    C = "Celsius"
    K = "Kelvin"


class SoundIntensityUnit(str, Enum):
    """Sound intensity units"""

    DB = "decibels"


class UnitlessUnit(str, Enum):
    """Unitless options"""

    PERCENT = "percent"
    FC = "fraction of cycle"


def create_unit_with_value(model_name, scalar_type, unit_type, unit_default):
    """this uses create_model instead of generics, which lets us set default values"""

    m = create_model(model_name, value=(scalar_type, ...), unit=(unit_type, unit_default))
    return m


SizeValue = create_unit_with_value("SizeValue", Decimal, SizeUnit, SizeUnit.MM)
MassValue = create_unit_with_value("MassValue", Decimal, MassUnit, MassUnit.MG)
VolumeValue = create_unit_with_value("VolumeValue", Decimal, VolumeUnit, VolumeUnit.NL)
FrequencyValue = create_unit_with_value("FrequencyValue", Decimal, FrequencyUnit, FrequencyUnit.HZ)
AngleValue = create_unit_with_value("AngleValue", Decimal, AngleUnit, AngleUnit.DEG)
TimeValue = create_unit_with_value("TimeValue", Decimal, TimeUnit, TimeUnit.S)
PowerValue = create_unit_with_value("PowerValue", Decimal, PowerUnit, PowerUnit.MW)
