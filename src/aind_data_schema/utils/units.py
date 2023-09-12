"""Script for defining UnitWithValue classes"""
from decimal import Decimal
from enum import Enum, EnumMeta

from pydantic.generics import GenericModel, Generic, TypeVar


class UnitEnumMeta(EnumMeta):
    """Adds enum names to schema."""

    def __modify_schema__(cls, field_schema):
        """Adds enumNames to institution"""
        field_schema.update(
            enumNames=[e.value for e in cls],
        )


class Unit(Enum, metaclass=UnitEnumMeta):
    pass


class SizeUnit(Unit):
    """Enumeration of Length Measurements"""
    M = "meter"
    CM = "centimeter"
    MM = "millimeter"
    UM = "micrometer"
    NM = "nanometer"
    IN = "inch"
    PX = "pixel"


class MassUnit(Unit):
    """Enumeration of Mass Measurements"""
    KG = "kilogram"
    G = "gram"
    MG = "milligram"
    UG = "microgram"
    NG = "nanogram"


class FrequencyUnit(Unit):
    """Enumeration of Frequency Measurements"""
    KHZ = "kilohertz"
    HZ = "hertz"
    mHZ = "millihertz"


class VolumeUnit(Unit):
    """Enumeration of Volume Measurements"""
    L = "liter"
    ML = "milliliter"
    UL = "microliter"
    NL = "nanoliter"


class AngleUnit(Unit):
    """Enumeration of Angle Measurements"""
    RAD = "radians"
    DEG = "degrees"


class TimeUnit(Unit):
    """Enumeration of Time Measurements"""
    HR = "hour"
    M = "minute"
    S = "second"
    MS = "millisecond"
    US = "microsecond"
    NS = "nanosecond"


class PowerUnit(Unit):
    """Power units"""
    UW = "microwatt"
    MW = "milliwatt"


class CurrentUnit(Unit):
    """Current units"""
    UA = "microamps"


class ConcentrationUnit(Unit):
    """Concentraion units"""
    M = "molar"
    UM = "micromolar"
    NM = "nanomolar"


U = TypeVar("U", *Unit.__subclasses__())
V = TypeVar("V", Decimal, float, int)


class Measurement(GenericModel, Generic[V, U]):
    value: V
    unit: U
