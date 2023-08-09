"""Script for defining UnitWithValue classes"""

from decimal import Decimal
from enum import Enum

from pydantic import create_model


class SizeUnit(Enum):
    """Enumeration of Length Measurements"""

    M = "meter"
    CM = "centimeter"
    MM = "millimeter"

    UM = "micrometer"
    NM = "nanometer"
    IN = "inch"
    PX = "pixel"


class MassUnit(Enum):
    """Enumeration of Mass Measurements"""

    KG = "kilogram"
    G = "gram"
    MG = "milligram"
    UG = "microgram"
    NG = "nanogram"


class FrequencyUnit(Enum):
    """Enumeration of Frequency Measurements"""

    KHZ = "kilohertz"
    HZ = "hertz"
    mHZ = "millihertz"


class VolumeUnit(Enum):
    """Enumeration of Volume Measurements"""

    L = "liter"
    ML = "milliliter"
    UL = "microliter"
    NL = "nanoliter"


class AngleUnit(Enum):
    """Enumeration of Angle Measurements"""

    RAD = "radians"
    DEG = "degrees"


class TimeUnit(Enum):
    """Enumeration of Time Measurements"""

    HR = "hour"
    M = "minute"
    S = "second"
    MS = "millisecond"
    US = "microsecond"
    NS = "nanosecond"


class PowerUnit(Enum):
    """Power units"""

    UW = "microwatt"
    MW = "milliwatt"


class CurrentUnit(Enum):
    """Current units"""

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

def create_3D_size_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, length=(scalar_type, ...), width=(scalar_type, ...), height=(scalar_type, ...), unit=(unit_type, unit_default))
    return m

def create_filter_size_with_value(model_name, scalar_type, unit_type, unit_default):

    m = create_model(model_name, diameter=(scalar_type, ...), width=(scalar_type, ...), height=(scalar_type, ...),  unit=(unit_type, unit_default))
    return m


SizeValueMM = create_unit_with_value("SizeValueMM", Decimal, SizeUnit, SizeUnit.MM)
SizeValueCM = create_unit_with_value("SizeValueCM", Decimal, SizeUnit, SizeUnit.CM)
SizeValuePX = create_unit_with_value("SizeValuePX", int, SizeUnit, SizeUnit.PX)
SizeValueIN = create_unit_with_value("SizeValueIN", Decimal, SizeUnit, SizeUnit.IN)
SizeValueNM = create_unit_with_value("SizeValueNM", Decimal, SizeUnit, SizeUnit.NM)

FilterSizeValue = create_filter_size_with_value("FilterSizeValue", Decimal, SizeUnit, SizeUnit.MM)

WaveLengthNM = create_unit_with_value("WaveLengthNM", int, SizeUnit, SizeUnit.NM)
MassValue = create_unit_with_value("MassValue", Decimal, MassUnit, MassUnit.MG)
VolumeValue = create_unit_with_value("VolumeValue", Decimal, VolumeUnit, VolumeUnit.NL)
FrequencyValueHZ = create_unit_with_value("FrequencyValue", Decimal, FrequencyUnit, FrequencyUnit.HZ)
AngleValue = create_unit_with_value("AngleValue", Decimal, AngleUnit, AngleUnit.DEG)
TimeValue = create_unit_with_value("TimeValue", Decimal, TimeUnit, TimeUnit.S)
PowerValue = create_unit_with_value("PowerValue", Decimal, PowerUnit, PowerUnit.MW)

CoordValue3D = create_3D_coordinate_with_value("CoordValue3D", Decimal, SizeUnit, SizeUnit.MM)
CoordValue2D = create_2D_coordinate_with_value("CoordValue2D", Decimal, SizeUnit, SizeUnit.MM)

SizeValue2DPX = create_2D_size_with_value("SizeValue2DPX", int, SizeUnit, SizeUnit.PX)
SizeValue3DMM = create_3D_size_with_value("SizeValue3DMM", Decimal, SizeUnit, SizeUnit.MM)

OrientationValue3D = create_3D_orientation_with_value("OrientationValue3D", Decimal, AngleUnit, AngleUnit.DEG)
ModuleOrientationValue2D = create_2D_module_orientation_with_value("ModuleOrientationValue2D", Decimal, AngleUnit, AngleUnit.DEG)
ModuleOrientationValue3D = create_3D_module_orientation_with_value("ModuleOrientationValue3D", Decimal, AngleUnit, AngleUnit.DEG)
