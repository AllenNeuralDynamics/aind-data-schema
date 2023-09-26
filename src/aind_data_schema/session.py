""" Schemas for Physiology and/or Behavior Sessions """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.device import Calibration, Maintenance, RelativePosition, SpoutSide
from aind_data_schema.stimulus import StimulusEpoch
from aind_data_schema.imaging.tile import Channel
from aind_data_schema.utils.units import FrequencyUnit, PowerUnit, SizeUnit, TimeUnit


class OphysSession(AindModel):
    """Description of ophys session"""


class EphysSession(AindModel):
    """Description of ephys session"""

    stick_microscopes: Optional[List[DomeModule]] = Field(
        ...,
        title="Stick microscopes",
        description="Must match stick microscope assemblies in rig file",
    )
    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
        unique_items=True,
    )
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        description="Path to file that details the CCF-to-lab coordinate transform",
        title="CCF coordinate transform",
    )
    notes: Optional[str] = Field(None, title="Notes")


class Behavior(AindModel):
    """Description of a behavior"""

    behavior_type: str = Field(..., title="Behavior type", description="Name of the behavior session")
    stimulus_epochs: List[StimulusEpoch] = Field(None, title="Stimulus")
    session_number: int = Field(..., title="Session number")
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


class Session(AindCoreModel):
    """Description of a physiology and/or behavior session"""

    schema_version: str = Field(
        "0.0.1",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: Optional[datetime] = Field(None, title="Session end time")
    session_type: str = Field(..., title="Session type")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
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
    #TODO: stimulus epoch is in Behavior...
    stimulus_epochs: Optional[List[StimulusEpoch]] = Field(None, title="Stimulus")

    notes: Optional[str] = Field(None, title="Notes")



    light_sources: List[Union[Laser, LightEmittingDiode]] = Field(..., title="Light source", unique_items=True)
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title="Cameras", unique_items=True)
    
    notes: Optional[str] = None