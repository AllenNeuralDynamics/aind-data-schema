""" schema for session stimulus """

from __future__ import annotations

from datetime import time
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field
from pydantic.typing import Annotated, Literal

from aind_data_schema.base import AindModel
from aind_data_schema.utils.units import FrequencyUnit, PowerUnit, TimeUnit, VolumeUnit


class PulseShape(Enum):
    """Types of Opto stim pulse shapes"""

    SQUARE = "Square"
    RAMP = "Ramp"
    SINE = "Sinusoidal"


class OptoStimulation(AindModel):
    """Description of opto stimulation parameters"""

    stimulus_type: Literal["OptoStimulation"] = Field(
        default="OptoStimulation", title="OptoStimulation", const=True, readOnly=True
    )
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
        ...,
        title="Baseline duration (s)",
        description="Duration of baseline recording prior to first pulse train",
    )
    baseline_duration_unit: TimeUnit = Field(TimeUnit.S, title="Baseline duration unit")
    other_parameters: Optional[Dict[str, Any]]
    notes: Optional[str] = Field(None, title="Notes")


class VisualStimulation(AindModel):
    """Description of visual stimulus parameters. Provides a high level description of stimulus."""

    stimulus_type: Literal["VisualStimulation"] = Field(
        default="VisualStimulation", title="VisualStimulation", const=True, readOnly=True
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    stimulus_parameters: Optional[Dict[str, Any]] = Field(
        None,
        title="Stimulus parameters",
        description="Define and list the parameter values used (e.g. all TF or orientation values)",
    )
    stimulus_template_name: Optional[List[str]] = Field(
        None,
        title="Stimulus template name",
        description="Name of image set or movie displayed",
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
    stimulus_script_version: str = Field(..., title="Stimulus script version")
    notes: Optional[str] = Field(None, title="Notes")


class BehaviorStimulation(AindModel):
    """Description of behavior parameters. Provides a high level description of stimulus."""

    stimulus_type: Literal["BehaviorStimulation"] = Field(
        default="BehaviorStimulation", title="BehaviorStimulation", const=True, readOnly=True
    )
    behavior_name: str = Field(..., title="Behavior name")
    session_number: int = Field(..., title="Session number")
    behavior_software: str = Field(
        ...,
        title="Behavior software",
        description="The software used to control the behavior (e.g. Bonsai)",
    )
    behavior_software_version: str = Field(..., title="Behavior software version")
    behavior_script: str = Field(
        ...,
        title="Behavior script",
        description="URL for the commit of the code used to run the behavior",
    )
    behavior_script_version: str = Field(..., title="Behavior script version")
    input_parameters: Dict[str, Any] = Field(
        ..., title="Input parameters", description="Parameters used in behavior session"
    )
    output_parameters: Dict[str, Any] = Field(
        ...,
        title="Performance parameters",
        description="Performance metrics from session",
    )
    reward_consumed_during_training: Decimal = Field(..., title="Reward consumed during training (uL)")
    reward_consumed_total: Decimal = Field(..., title="Total reward consumed (uL)")
    reward_consumed_unit: VolumeUnit = Field(VolumeUnit.UL, title="Reward consumed unit")
    trials_total: int = Field(..., title="Total trials")
    trials_finished: int = Field(..., title="Finished trials")
    trials_rewarded: int = Field(..., title="Rewarded trials")
    notes: Optional[str] = Field(None, title="Notes")


class PhotoStimulationGroup(AindModel):
    """Description of a photostimulation group"""

    group_index: int = Field(..., title="Group index")
    number_of_neurons: int = Field(..., title="Number of neurons")
    stimulation_laser_power: Decimal = Field(..., title="Stimulation laser power (mW)")
    stimulation_laser_power_unit: PowerUnit = Field(PowerUnit.MW, title="Stimulation laser power unit")
    number_trials: int = Field(..., title="Number of trials")
    number_spirals: int = Field(..., title="Number of spirals")
    spiral_duration: Decimal = Field(..., title="Spiral duration (s)")
    spiral_duration_unit: TimeUnit = Field(TimeUnit.S, title="Spiral duration unit")
    inter_spiral_interval: Decimal = Field(..., title="Inter trial interval (s)")
    inter_spiral_interval_unit: TimeUnit = Field(TimeUnit.S, title="Inter trial interval unit")
    other_parameters: Optional[Dict[str, Any]]
    notes: Optional[str] = Field(None, title="Notes")


class PhotoStimulation(AindModel):
    """Description of a photostimulation session"""

    stimulus_type: Literal["PhotoStimulation"] = Field(
        default="PhotoStimulation", title="PhotoStimulation", const=True, readOnly=True
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    number_groups: int = Field(..., title="Number of groups")
    groups: List[PhotoStimulationGroup] = Field(..., title="Groups")
    inter_trial_interval: Decimal = Field(..., title="Inter trial interval (s)")
    inter_trial_interval_unit: TimeUnit = Field(TimeUnit.S, title="Inter trial interval unit")
    other_parameters: Optional[Dict[str, Any]]
    notes: Optional[str] = Field(None, title="Notes")


class StimulusEpoch(AindModel):
    """Description of stimulus used during session"""

    stimulus: Annotated[
        Union[OptoStimulation, VisualStimulation, BehaviorStimulation, PhotoStimulation],
        Field(..., title="Stimulus", discriminator="stimulus_type"),
    ]
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
