"""Calibration data models"""

from typing import Annotated, List, Literal, Optional, Union

from aind_data_schema_models.units import UNITS, PowerUnit, TimeUnit, VolumeUnit

from aind_data_schema.base import AwareDatetimeWithDefault, Field
from aind_data_schema.components.acquisition_configs import DeviceConfig
from aind_data_schema.components.reagent import Reagent


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


class LaserCalibration(Calibration):
    """Calibration of a laser device"""

    input: List[float] = Field(..., title="Input times", description="Power output percentage")
    input_unit: PowerUnit = Field(..., title="Input unit")
    output: List[float] = Field(..., title="Output", description="Laser strength")
    output_unit: PowerUnit = Field(..., title="Output unit")

    description: Literal["Laser power measured for various percentage output strengths"] = (
        "Laser power measured for various percentage output strengths"
    )


CALIBRATIONS = Annotated[
    Union[
        Calibration,
        LiquidCalibration,
        LaserCalibration,
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
