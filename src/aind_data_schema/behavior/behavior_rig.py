""" Schemas for Behavior Sessions """

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel
from aind_data_schema.device import (
    CameraAssembly, 
    DAQDevice, 
    Device, 
    Disc, 
    HarpDevice, 
    Monitor, 
    Speaker,
    Treadmill, 
    Tube,
    WaterDelivery
)


class BehaviorRig(AindCoreModel):
    """Description of an behavior rig"""

    schema_version: str = Field("0.1.6", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    mouse_platform: Union[Tube, Treadmill, Disc] = Field(..., title="Mouse platform")
    water_delivery: WaterDelivery = Field(..., title="Water delivery")
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    speakers: Optional[List[Speaker]] = Field(None, title="Speakers", unique_items=True)
    visual_monitors: Optional[List[Monitor]] = Field(None, title="Visual monitors", unique_items=True)
    daqs: Optional[List[Union[HarpDevice, DAQDevice]]] = Field(None, title="Data acquisition devices")
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
