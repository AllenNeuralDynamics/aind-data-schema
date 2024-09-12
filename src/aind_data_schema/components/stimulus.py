""" schema for session stimulus """

from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional

from aind_data_schema_models.units import ConcentrationUnit, FrequencyUnit, PowerUnit, TimeUnit
from pydantic import Field

from aind_data_schema.base import AindGeneric, AindGenericType, AindModel


class PulseShape(str, Enum):
    """Types of Opto stim pulse shapes"""

    SQUARE = "Square"
    RAMP = "Ramp"
    SINE = "Sinusoidal"


class FilterType(str, Enum):
    """Types of bandpass filters for auditory stim"""

    BUTTERWORTH = "Butterworth"
    OTHER = "Other"


class OptoStimulation(AindModel):
    """Description of opto stimulation parameters"""

    stimulus_type: Literal["Opto Stimulation"] = "Opto Stimulation"
    stimulus_name: str = Field(..., title="Stimulus name")
    pulse_shape: PulseShape = Field(..., title="Pulse shape")
    pulse_frequency: List[Decimal] = Field(..., title="Pulse frequency (Hz)")
    pulse_frequency_unit: FrequencyUnit = Field(default=FrequencyUnit.HZ, title="Pulse frequency unit")
    number_pulse_trains: List[int] = Field(..., title="Number of pulse trains")
    pulse_width: List[int] = Field(..., title="Pulse width (ms)")
    pulse_width_unit: TimeUnit = Field(default=TimeUnit.MS, title="Pulse width unit")
    pulse_train_duration: List[Decimal] = Field(..., title="Pulse train duration (s)")
    pulse_train_duration_unit: TimeUnit = Field(default=TimeUnit.S, title="Pulse train duration unit")
    fixed_pulse_train_interval: bool = Field(..., title="Fixed pulse train interval")
    pulse_train_interval: Optional[Decimal] = Field(
        default=None, title="Pulse train interval (s)", description="Time between pulse trains"
    )
    pulse_train_interval_unit: TimeUnit = Field(default=TimeUnit.S, title="Pulse train interval unit")
    baseline_duration: Decimal = Field(
        ...,
        title="Baseline duration (s)",
        description="Duration of baseline recording prior to first pulse train",
    )
    baseline_duration_unit: TimeUnit = Field(default=TimeUnit.S, title="Baseline duration unit")
    other_parameters: AindGenericType = Field(AindGeneric(), title="Other parameters")
    notes: Optional[str] = Field(default=None, title="Notes")


class VisualStimulation(AindModel):
    """Description of visual stimulus parameters. Provides a high level description of stimulus."""

    stimulus_type: Literal["Visual Stimulation"] = "Visual Stimulation"
    stimulus_name: str = Field(..., title="Stimulus name")
    stimulus_parameters: AindGenericType = Field(
        AindGeneric(),
        title="Stimulus parameters",
        description="Define and list the parameter values used (e.g. all TF or orientation values)",
    )
    stimulus_template_name: List[str] = Field(
        default=[],
        title="Stimulus template name",
        description="Name of image set or movie displayed",
    )
    notes: Optional[str] = Field(default=None, title="Notes")


class PhotoStimulationGroup(AindModel):
    """Description of a photostimulation group"""

    group_index: int = Field(..., title="Group index")
    number_of_neurons: int = Field(..., title="Number of neurons")
    stimulation_laser_power: Decimal = Field(..., title="Stimulation laser power (mW)")
    stimulation_laser_power_unit: PowerUnit = Field(default=PowerUnit.MW, title="Stimulation laser power unit")
    number_trials: int = Field(..., title="Number of trials")
    number_spirals: int = Field(..., title="Number of spirals")
    spiral_duration: Decimal = Field(..., title="Spiral duration (s)")
    spiral_duration_unit: TimeUnit = Field(default=TimeUnit.S, title="Spiral duration unit")
    inter_spiral_interval: Decimal = Field(..., title="Inter trial interval (s)")
    inter_spiral_interval_unit: TimeUnit = Field(default=TimeUnit.S, title="Inter trial interval unit")
    other_parameters: AindGenericType = Field(AindGeneric(), title="Other parameters")
    notes: Optional[str] = Field(default=None, title="Notes")


class PhotoStimulation(AindModel):
    """Description of a photostimulation session"""

    stimulus_type: Literal["Photo Stimulation"] = "Photo Stimulation"
    stimulus_name: str = Field(..., title="Stimulus name")
    number_groups: int = Field(..., title="Number of groups")
    groups: List[PhotoStimulationGroup] = Field(..., title="Groups")
    inter_trial_interval: Decimal = Field(..., title="Inter trial interval (s)")
    inter_trial_interval_unit: TimeUnit = Field(default=TimeUnit.S, title="Inter trial interval unit")
    other_parameters: AindGenericType = Field(AindGeneric(), title="Other parameters")
    notes: Optional[str] = Field(default=None, title="Notes")


class OlfactometerChannelConfig(AindModel):
    """Description of olfactometer channel configurations"""

    channel_index: int = Field(..., title="Channel index")
    odorant: str = Field(..., title="Odorant")
    odorant_dilution: Decimal = Field(..., title="Odorant dilution")
    odorant_dilution_unit: ConcentrationUnit = Field(default=ConcentrationUnit.VOLUME_PERCENT, title="Dilution unit")
    notes: Optional[str] = Field(default=None, title="Notes")


class OlfactoryStimulation(AindModel):
    """Description of a olfactory stimulus"""

    stimulus_type: Literal["Olfactory Stimulation"] = "Olfactory Stimulation"
    stimulus_name: str = Field(..., title="Stimulus name")
    channels: List[OlfactometerChannelConfig]
    notes: Optional[str] = Field(default=None, title="Notes")


class AuditoryStimulation(AindModel):
    """Description of an auditory stimulus"""

    stimulus_type: Literal["Auditory Stimulation"] = "Auditory Stimulation"
    sitmulus_name: str = Field(..., title="Stimulus name")
    sample_frequency: Decimal = Field(..., title="Sample frequency")
    amplitude_modulation_frequency: Optional[int] = Field(default=None, title="Amplitude modulation frequency")
    frequency_unit: FrequencyUnit = Field(default=FrequencyUnit.HZ, title="Tone frequency unit")
    bandpass_low_frequency: Optional[Decimal] = Field(default=None, title="Bandpass low frequency")
    bandpass_high_frequency: Optional[Decimal] = Field(default=None, title="Bandpass high frequency")
    bandpass_filter_type: Optional[FilterType] = Field(default=None, title="Bandpass filter type")
    bandpass_order: Optional[int] = Field(default=None, title="Bandpass order")
    notes: Optional[str] = Field(default=None, title="Notes")
