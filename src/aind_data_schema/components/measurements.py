"""Calibration data models"""

from typing import List, Literal, Optional

from aind_data_schema_models.units import UNITS, PowerUnit, TimeUnit, VolumeUnit

from aind_data_schema.base import AwareDatetimeWithDefault, Discriminated, Field
from aind_data_schema.components.configs import DeviceConfig
from aind_data_schema.components.reagent import Reagent


class Calibration(DeviceConfig):
    """Generic calibration class"""

    calibration_date: AwareDatetimeWithDefault = Field(..., title="Date and time of calibration")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: List[float | str] = Field(..., description="Calibration input", title="Inputs")
    input_unit: UNITS = Field(..., title="Input unit")
    repeats: Optional[int] = Field(
        default=None,
        title="Number of repeats",
        description="If each input was repeated multiple times, provide the number of repeats",
    )
    output: List[float | str] = Field(
        ..., description="Calibration output (provide the average if repeated)", title="Outputs"
    )
    output_unit: UNITS = Field(..., title="Output unit")
    notes: Optional[str] = Field(
        default=None,
        title="Notes",
        description="Fit equation, etc",
    )


class VolumeCalibration(Calibration):
    """Calibration of a liquid delivery device"""

    input: List[float] = Field(..., title="Input times", description="Length of time solenoid is open")
    input_unit: TimeUnit = Field(..., title="Input unit")
    repeats: Optional[int] = Field(
        default=None,
        title="Number of repeats",
        description="If each input was repeated multiple times, provide the number of repeats",
    )
    output: List[float] = Field(..., title="Output", description="Volume output (provide the average if repeated)")
    output_unit: VolumeUnit = Field(..., title="Output unit")

    description: Literal["Volume measured for various solenoid opening times"] = (
        "Volume measured for various solenoid opening times"
    )


class PowerCalibration(Calibration):
    """Calibration of a laser device"""

    input: List[float] = Field(..., title="Input", description="Power or percentage input strength")
    input_unit: PowerUnit = Field(..., title="Input unit")
    output: List[float] = Field(..., title="Output", description="Power output (provide the average if repeated)")
    output_unit: PowerUnit = Field(..., title="Output unit")

    description: Literal["Power measured for various power or percentage input strengths"] = (
        "Power measured for various power or percentage input strengths"
    )


CALIBRATIONS = Discriminated[Calibration | VolumeCalibration | PowerCalibration]


class Maintenance(DeviceConfig):
    """Generic maintenance class"""

    maintenance_date: AwareDatetimeWithDefault = Field(..., title="Date and time of maintenance")
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID")

    reagents: Optional[List[Reagent]] = Field(default=None, title="Reagents")
    notes: Optional[str] = Field(default=None, title="Notes")
