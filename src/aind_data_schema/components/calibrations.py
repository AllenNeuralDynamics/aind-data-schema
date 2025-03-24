"""Calibration data models"""

from typing import List, Optional

from aind_data_schema.base import DataModel, Field, GenericModel, GenericModelType, AwareDatetimeWithDefault

from aind_data_schema_models.units import TimeUnit, VolumeUnit


class Calibration(DataModel):
    """Generic calibration class"""

    calibration_date: AwareDatetimeWithDefault = Field(..., title="Date and time of calibration")
    device_name: str = Field(..., title="Device name", description="Must match a device name in instrument")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: GenericModelType = Field(GenericModel(), description="Calibration input", title="inputs")
    output: GenericModelType = Field(GenericModel(), description="Calibration output", title="outputs")
    notes: Optional[str] = Field(default=None, title="Notes")


class WaterCalibration(Calibration):
    """Calibration of a water delivery device"""

    input: List[float] = Field(..., title="Input times", description="Length of time solenoid is open")
    input_unit: TimeUnit = Field(..., title="Input unit")
    output: List[float] = Field(..., title="Output", description="Water output")
    output_unit: VolumeUnit = Field(..., title="Output unit")
