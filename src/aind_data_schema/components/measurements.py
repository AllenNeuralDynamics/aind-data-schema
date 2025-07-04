"""Calibration data models"""

from typing import Annotated, List, Literal, Optional
from enum import Enum

from aind_data_schema_models.units import UNITS, PowerUnit, TimeUnit, VolumeUnit, VoltageUnit
from pydantic import model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel, Discriminated, Field, GenericModel
from aind_data_schema.components.configs import DeviceConfig
from aind_data_schema.components.reagent import Reagent
from aind_data_schema.utils.validators import TimeValidation


class FitType(Enum):
    """Type of fit for calibration data"""

    LINEAR_INTERPOLATION = "linear_interpolation"
    LINEAR = "linear"
    OTHER = "other"


class CalibrationFit(DataModel):
    """Fit equation for calibration data"""

    fit_type: FitType = Field(
        ...,
        title="Fit type",
    )
    fit_parameters: Optional[GenericModel] = Field(
        default=None,
        title="Fit parameters",
        description="Parameters of the fit equation, e.g. slope and intercept for linear fit",
    )

    @model_validator(mode="before")
    def validate_fit_type(cls, values):
        """Ensure that parameters are provided for linear and other fits"""
        fit_type = values.get("fit_type")
        fit_parameters = values.get("fit_parameters")

        if fit_type in {FitType.LINEAR, FitType.OTHER} and not fit_parameters:
            raise ValueError(f"Fit parameters must be provided for {fit_type.value} fit type")

        if fit_type == FitType.LINEAR_INTERPOLATION and fit_parameters is not None:
            raise ValueError("Fit parameters should not be provided for linear interpolation fit type")

        return values


class Calibration(DeviceConfig):
    """Generic calibration class"""

    calibration_date: Annotated[AwareDatetimeWithDefault, TimeValidation.BEFORE] = Field(
        ..., title="Date and time of calibration"
    )
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
    fit: Optional[CalibrationFit] = Field(
        default=None,
        title="Fit",
        description="Fit equation for the calibration data used during data acquisition",
    )
    notes: Optional[str] = Field(
        default=None,
        title="Notes",
    )


class VolumeCalibration(Calibration):
    """Calibration of a liquid delivery device based on solenoid/valve opening times"""

    input: List[float] = Field(..., title="Input times", description="Length of time solenoid/valve is open")
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
    """Calibration of a device that outputs power based on input strength"""

    input: List[float] = Field(..., title="Input", description="Power, voltage, or percentage input strength")
    input_unit: PowerUnit | VoltageUnit = Field(..., title="Input unit")
    output: List[float] = Field(..., title="Output", description="Power output (provide the average if repeated)")
    output_unit: PowerUnit = Field(..., title="Output unit")

    description: Literal["Power measured for various power or percentage input strengths"] = (
        "Power measured for various power or percentage input strengths"
    )


CALIBRATIONS = Discriminated[Calibration | VolumeCalibration | PowerCalibration]


class Maintenance(DeviceConfig):
    """Generic maintenance class"""

    maintenance_date: Annotated[AwareDatetimeWithDefault, TimeValidation.BEFORE] = Field(
        ..., title="Date and time of maintenance"
    )
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID")

    reagents: Optional[List[Reagent]] = Field(default=None, title="Reagents")
    notes: Optional[str] = Field(default=None, title="Notes")
