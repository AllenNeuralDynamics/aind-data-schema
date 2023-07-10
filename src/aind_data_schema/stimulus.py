""" schema for session stimulus """

from __future__ import annotations

from datetime import time
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindModel
from aind_data_schema.device import FrequencyUnit
from aind_data_schema.procedures import TimeUnit


class PulseShape(Enum):
    """Types of Opto stim pulse shapes"""

    SQUARE = "Square"
    RAMP = "Ramp"
    SINE = "Sinusoidal"


class OptoStim(AindModel):
    """Description of opto stimulation parameters"""

    stimulus_name: str = Field(..., title="Stimulus name")
    pulse_shape: PulseShape = Field(..., title="Pulse shape")
    pulse_frequency: int = Field(..., title="Pulse frequency (Hz)")
    pulse_frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Pulse frequency unit")
    number_pulse_trains: int = Field(..., title="Number of pulse trains")
    pulse_width: int = Field(..., title="Pulse width (ms)")
    pulse_width_unit: TimeUnit = Field(TimeUnit.MS, title="Pulse width unit")
    pulse_train_duration: Decimal = Field(..., title="Pulse train duration (s)")
    pulse_train_duration_unit: TimeUnit = Field(TimeUnit.S, title="Pulse train duration unit")
    fixed_pulse_train_interval: bool = Field(..., title="Fixed pulse train interval")
    pulse_train_interval: Optional[Decimal] = Field(
        None, title="Pulse train interval (s)", description="Time between pulse trains"
    )
    pulse_train_interval_unit: TimeUnit = Field(TimeUnit.S, title="Pulse train interval unit")
    baseline_duration: Decimal = Field(
        ..., title="Baseline duration (s)", description="Duration of baseline recording prior to first pulse train"
    )
    baseline_duration_unit: TimeUnit = Field(TimeUnit.S, title="Baseline duration unit")
    other_parameters: Optional[Dict[str, Any]]
    notes: Optional[str] = Field(None, title="Notes")


class VisualStim(AindModel):
    """Description of visual stimulus parameters. Provides a high level description of stimulus."""

    stimulus_name: str = Field(..., title="Stimulus name")
    stimulus_parameters: Optional[Dict[str, Any]] = Field(
        None,
        title="Stimulus parameters",
        description="Define and list the parameter values used (e.g. all TF or orientation values)",
    )
    stimulus_template_name: Optional[List[str]] = Field(
        None, title="Stimulus template name", description="Name of image set or movie displayed"
    )
    stimulus_software: str = Field(
        ...,
        title="Stimulus software",
        description="The software used to control the stimulus (e.g. Bonsai)",
    )
    stimulus_software_version: str = Field(..., title="Stimulus software version")
    stimulus_script: str = Field(
        ...,
        title="Stimulus script",
        description="The specific code for this stimulus instance",
    )
    stimulus_script_version: str = Field(..., title="Stimulus srcipt version")
    notes: Optional[str] = Field(None, title="Notes")


class StimulusPresentation(AindModel):
    """Description of stimulus used during session"""

    stimulus: Union[OptoStim, VisualStim] = Field(..., title="Stimulus")
    stimulus_start_time: time = Field(
        ...,
        title="Stimulus start time",
        description="When a specific stimulus begins. This might be the same as the session start time.",
    )
    stimulus_end_time: time = Field(
        ...,
        title="Stimulus end time",
        description="When a specific stimulus ends. This might be the same as the session end time.",
    )
