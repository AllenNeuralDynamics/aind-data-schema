"""Calibration data models"""

from typing import List, Optional, Annotated, Union

from aind_data_schema.base import Field, GenericModel, GenericModelType, AwareDatetimeWithDefault
from aind_data_schema.components.reagent import Reagent

from aind_data_schema_models.units import TimeUnit, VolumeUnit
from aind_data_schema.components.configs import DeviceConfig


class Calibration(DeviceConfig):
    """Generic calibration class"""

    calibration_date: AwareDatetimeWithDefault = Field(..., title="Date and time of calibration")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: GenericModelType = Field(GenericModel(), description="Calibration input", title="inputs")
    output: GenericModelType = Field(GenericModel(), description="Calibration output", title="outputs")
    notes: Optional[str] = Field(default=None, title="Notes")


class LiquidCalibration(Calibration):
    """Calibration of a liquid delivery device"""

    input: List[float] = Field(..., title="Input times", description="Length of time solenoid is open")
    input_unit: TimeUnit = Field(..., title="Input unit")
    output: List[float] = Field(..., title="Output", description="Liquid output")
    output_unit: VolumeUnit = Field(..., title="Output unit")


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
