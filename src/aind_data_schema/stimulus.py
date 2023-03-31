""" schema for session stimulus """

from __future__ import annotations

from datetime import date, time
from enum import Enum
from typing import Optional, Dict, Any

from pydantic import Field

from .base import AindCoreModel, AindModel
from .device import FrequencyUnit
from .procedures import TimeUnit


class PulseShape(Enum):
    """Types of Opto stim pulse shapes"""
    SQUARE = "Square"
    RAMP = "Ramp"
    SINE = "Sinusoidal"


class OptoStim(AindModel):
    """Description of optophysiology stimulation parameters"""

    pulse_shape: PulseShape = Field(..., title="Pulse shape")
    pulse_frequency: int = Field(..., title="Pulse frequency (Hz)")
    pulse_frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Pulse frequency unit")
    number_pulse_trains: int = Field(..., title="Number of pulse trains")
    pulse_width: int = Field(..., title="Pulse width (ms)")
    pulse_width_unit: TimeUnit = Field(TimeUnit.MS, title="Pulse width unit")
    pulse_train_duration: float = Field(..., title="Pulse train duration (s)")
    pulse_train_duration_unit: TimeUnit = Field(TimeUnit.S, title="Pulse train duration unit")
    pulse_train_interval: float = Field(
        ..., 
        title="Pulse train interval (s)",
        description="Time between pulse trains"
        )
    pulse_train_interval_unit: TimeUnit = Field(TimeUnit.S, title="Pulse train interval unit")
    baseline_duration: float = Field(
        ..., 
        title="Baseline duration (s)",
        description="Duration of baseline recording prior to first pulse train")
    baseline_duration_unit: TimeUnit = Field(TimeUnit.S, title="Baseline duration unit")
    other_parameters: Optional[Dict[str, Any]]
    notes: Optional[str] = Field(None, title="Notes")


class Stimulus(AindCoreModel):
    """Description of stimulus used in a recording session"""

    schema_version: str = Field(
        "0.0.1",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    stimulus: OptoStim = Field(..., title="Stimulus") #in future this can be union of other stim types
