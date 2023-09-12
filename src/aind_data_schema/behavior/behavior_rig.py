""" Schemas for Behavior Sessions """

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel
from aind_data_schema.device import (
    Calibration,
    CameraAssembly,
    DAQDevice,
    Device,
    Disc,
    HarpDevice,
    Monitor,
    Speaker,
    Treadmill,
    Tube,
    RewardDelivery
)


class BehaviorRig(AindCoreModel):
    """Description of an behavior rig"""

    schema_version: str = Field("0.1.11", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    mouse_platform: Union[Tube, Treadmill, Disc] = Field(..., title="Mouse platform")
    stimulus_devices: List[Union[RewardDelivery, Monitor, Speaker]] = Field(
        ...,
        title="Stimulus devices",
        unique_items=True,
        )
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    daqs: Optional[List[Union[HarpDevice, DAQDevice]]] = Field(None, title="Data acquisition devices")
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
