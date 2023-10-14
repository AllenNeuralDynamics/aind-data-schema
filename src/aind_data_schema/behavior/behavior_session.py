""" Schemas for Behavior Sessions. This is being deprecated after 2023-11-01."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import Field, root_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.device import Calibration, Maintenance, RelativePosition, SpoutSide
from aind_data_schema.stimulus import StimulusEpoch
from aind_data_schema.utils.units import MassUnit


class RewardSolution(Enum):
    """Reward solution name"""

    WATER = "Water"
    OTHER = "Other"


class RewardSpout(AindModel):
    """Reward spout session information"""

    side: SpoutSide = Field(..., title="Spout side", description="Must match rig")
    starting_position: RelativePosition = Field(..., title="Starting position")
    variable_position: bool = Field(
        ..., title="Variable position", description="True if spout position changes during session as tracked in data"
    )
    reward_valve_calibration: Calibration = Field(..., title="Reward valve calibration")


class RewardDelivery(AindModel):
    """Reward delivery information"""

    reward_solution: RewardSolution = Field(..., title="Reward solution", description="If Other use notes")
    reward_spouts: List[RewardSpout] = Field(..., title="Reward spouts", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")

    @root_validator
    def validate_other(cls, v):
        """Validator for other/notes"""

        if v.get("reward_solution") == RewardSolution.OTHER and not v.get("notes"):
            raise ValueError(
                "Notes cannot be empty if reward_solution is Other. Describe the reward_solution in the notes field."
            )
        return v


class BehaviorSession(AindCoreModel):
    """Description of a behavior session. This is being deprecated after 2023-11-01."""

    schema_version: str = Field(
        "0.0.10",
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
    calibrations: Optional[List[Calibration]] = Field(
        None, title="Calibrations", description="Calibrations of rig devices prior to session"
    )
    maintenance: Optional[List[Maintenance]] = Field(
        None, title="Maintenance", description="Maintenance of rig devices prior to session"
    )
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
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    behavior_type: str = Field(..., title="Behavior type", description="Name of the behavior session")
    stimulus_epochs: List[StimulusEpoch] = Field(None, title="Stimulus")
    notes: Optional[str] = Field(None, title="Notes")
