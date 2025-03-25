"""Calibration data models"""

from typing import List, Optional, Annotated, Union, Literal

from aind_data_schema.base import Field, AwareDatetimeWithDefault
from aind_data_schema.components.reagent import Reagent

from aind_data_schema_models.units import (
    SizeUnit,
    MassUnit,
    FrequencyUnit,
    SpeedUnit,
    VolumeUnit,
    AngleUnit,
    TimeUnit,
    PowerUnit,
    CurrentUnit,
    ConcentrationUnit,
    TemperatureUnit,
    SoundIntensityUnit,
    VoltageUnit,
    MemoryUnit,
    UnitlessUnit,
)
from aind_data_schema.components.configs import DeviceConfig


UNITS = Union[
    SizeUnit,
    MassUnit,
    FrequencyUnit,
    SpeedUnit,
    VolumeUnit,
    AngleUnit,
    TimeUnit,
    PowerUnit,
    CurrentUnit,
    ConcentrationUnit,
    TemperatureUnit,
    SoundIntensityUnit,
    VoltageUnit,
    MemoryUnit,
    UnitlessUnit,
]


class Calibration(DeviceConfig):
    """Generic calibration class"""

    calibration_date: AwareDatetimeWithDefault = Field(..., title="Date and time of calibration")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: List[float | str] = Field(..., description="Calibration input", title="inputs")
    input_unit: UNITS = Field(..., title="Input unit")
    output: List[float | str] = Field(..., description="Calibration output", title="outputs")
    output_unit: UNITS = Field(..., title="Output unit")
    notes: Optional[str] = Field(
        default=None,
        title="Notes",
        description="Fit equation, etc",
    )


class LiquidCalibration(Calibration):
    """Calibration of a liquid delivery device"""

    input: List[float] = Field(..., title="Input times", description="Length of time solenoid is open")
    input_unit: TimeUnit = Field(..., title="Input unit")
    output: List[float] = Field(..., title="Output", description="Liquid output")
    output_unit: VolumeUnit = Field(..., title="Output unit")

    description: Literal["Liquid volume measured for various solenoid opening times"] = (
        "Liquid volume measured for various solenoid opening times"
    )


CALIBRATIONS = Annotated[
    Union[
        Calibration,
        LiquidCalibration,
    ],
    Field(discriminator="object_type"),
]


class Maintenance(DeviceConfig):
    """Generic maintenance class"""

    maintenance_date: AwareDatetimeWithDefault = Field(..., title="Date and time of maintenance")
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID")

    reagents: Optional[List[Reagent]] = Field(default=None, title="Reagents")
    notes: Optional[str] = Field(default=None, title="Notes")
