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
    MS = "millisecond"
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

def create_3D_coordinate_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, x=(scalar_type, ...), y=(scalar_type, ...), z=(scalar_type, ...), unit=(unit_type, unit_default))
    return m

def create_3D_orientation_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, pitch=(scalar_type, ...), yaw=(scalar_type, ...), roll=(scalar_type, ...), unit=(unit_type, unit_default))
    return m


def create_3D_module_orientation_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, arc_angle=(scalar_type, ...), module_angle=(scalar_type, ...), rotation_angle=(scalar_type, ...), unit=(unit_type, unit_default))
    return m

def create_2D_module_orientation_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, arc_angle=(scalar_type, ...), module_angle=(scalar_type, ...), unit=(unit_type, unit_default))
    return m

def create_2D_coordinate_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, x=(scalar_type, ...), y=(scalar_type, ...), unit=(unit_type, unit_default))
    return m

def create_2D_size_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, width=(scalar_type, ...), height=(scalar_type, ...), unit=(unit_type, unit_default))
    return m

def create_filter_size_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, diameter=(scalar_type, ...), width=(scalar_type, ...), height=(scalar_type, ...),  unit=(unit_type, unit_default))
    return m


SizeValue = create_unit_with_value("SizeValue", Decimal, Size, Size.MM)

SizeValueCM = create_unit_with_value("SizeValueCM", Decimal, Size, Size.CM)
SizeValuePX = create_unit_with_value("SizeValuePX", int, Size, Size.PX)

FilterSizeValue = create_filter_size_with_value("FilterSizeValue", Decimal, Size, Size.MM)

WaveLengthNM = create_unit_with_value("WaveLengthNM", int, Size, Size.NM)
MassValue = create_unit_with_value("MassValue", Decimal, Mass, Mass.MG)
VolumeValue = create_unit_with_value("VolumeValue", Decimal, Volume, Volume.NL)
FrequencyValue = create_unit_with_value("FrequencyValue", Decimal, Frequency, Frequency.HZ)
AngleValue = create_unit_with_value("AngleValue", Decimal, Angle, Angle.DEG)
TimeValue = create_unit_with_value("TimeValue", Decimal, TimeMeasure, TimeMeasure.S)
PowerValue = create_unit_with_value("PowerValue", Decimal, Power, Power.MW)

CoordValue3D = create_3D_coordinate_with_value("CoordValue3D", Decimal, Size, Size.MM)
CoordValue2D = create_2D_coordinate_with_value("CoordValue2D", Decimal, Size, Size.MM)

SizeValue2DPX = create_2D_size_with_value("SizeValue2DPX", int, Size, Size.PX)

OrientationValue3D = create_3D_orientation_with_value("OrientationValue3D", Decimal, Angle, Angle.DEG)
ModuleOrientationValue2D = create_2D_module_orientation_with_value("ModuleOrientationValue2D", Decimal, Angle, Angle.DEG)
ModuleOrientationValue3D = create_3D_module_orientation_with_value("ModuleOrientationValue3D", Decimal, Angle, Angle.DEG)