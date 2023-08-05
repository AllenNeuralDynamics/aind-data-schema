""" Schemas for Behavior Sessions """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.procedures import VolumeUnit, WeightUnit
from aind_data_schema.stimulus import StimulusEpoch
from aind_data_schema.utils.units import create_unit_with_value, Volume
from aind_data_schema.device import RelativePosition, SpoutSide

class RewardSolution(Enum):
    """Reward solution name"""

    WATER = "Water"
    OTHER = "Other"


class RewardSpout(AindModel):
    """Reward spout session information"""

    side: SpoutSide = Field(..., title="Spout side", description="Must match rig")
    starting_position: RelativePosition = Field(..., title="Starting position")
    variable_position: bool = Field(..., title="Variable position", description="True if spout position changes during session as tracked in data")
    reward_valve_calibration: Calibration = Field(..., title="Reward valve calibration")


class RewardDelivery(AindModel):
    """Reward delivery information"""

    reward_solution: RewardSolution = Field(..., title="Reward solution", description="If Other use notes")
    reward_spouts: List[RewardSpout] = Field(..., title="Reward spouts", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")


class BehaviorSession(AindCoreModel):
    """Description of a behavior session"""

    schema_version: str = Field(
        "0.0.3",
        description="Schema version",
        title="Schema Version",
        const=True,
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    rig_id: str = Field(..., title="Rig ID")
    spot_calibrations: List[Calibration] = Field(..., title="Spot calibrations")
    subject_id: int = Field(..., title="Subject ID")
    animal_weight_prior: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
        units="g",
    )
    animal_weight_post: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
        units="g",
    )
    weight_unit: WeightUnit = Field(WeightUnit.G, title="Weight unit")
    behavior_type: str = Field(..., title="Behavior type", description="Name of the behavior session")
    stimulus_epochs: List[StimulusEpoch] = Field(None, title="Stimulus")
    session_number: int = Field(..., title="Session number")
    output_parameters: Dict[str, Any] = Field(
        ..., title="Performance parameters", description="Performance metrics from session"
    )
    reward_consumed_during_training: create_unit_with_value("reward_consumed_during_training", Decimal, Volume, VolumeUnit.UL) = Field(..., title="Reward consumer during training")
    reward_consumed_total: create_unit_with_value("reward_consumed_total", Decimal, Volume, VolumeUnit.UL) = Field(..., title="Total reward consumed")
    trials_total: int = Field(..., title="Total trials")
    trials_finished: int = Field(..., title="Finished trials")
    trials_rewarded: int = Field(..., title="Rewarded trials")
    notes: Optional[str] = Field(None, title="Notes")
