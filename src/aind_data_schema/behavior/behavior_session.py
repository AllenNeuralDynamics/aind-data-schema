""" Schemas for Behavior Sessions """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel
from aind_data_schema.procedures import VolumeUnit, WeightUnit
from aind_data_schema.stimulus import StimulusEpoch


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
    water_consumed_during_training: Decimal = Field(..., title="Water consumed during training (uL)")
    water_consumed_total: Decimal = Field(..., title="Total water consumed (uL)")
    water_consumed_unit: VolumeUnit = Field(VolumeUnit.UL, title="Water consumed unit")
    trials_total: int = Field(..., title="Total trials")
    trials_finished: int = Field(..., title="Finished trials")
    trials_rewarded: int = Field(..., title="Rewarded trials")
    notes: Optional[str] = Field(None, title="Notes")
