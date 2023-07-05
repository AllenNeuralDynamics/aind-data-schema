""" Schemas for Behavior Sessions """

from __future__ import annotations

from typing import List, Literal, Set, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel, Constant
from aind_data_schema.device import CameraAssembly, DAQDevice, Device, Disc, HarpDevice, Monitor, Treadmill, Tube


class BehaviorRig(AindCoreModel):
    """Description of an behavior rig"""

    schema_version: Constant("0.1.1", title="Schema version")
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies")
    visual_monitors: Optional[List[Monitor]] = Field(None, title="Visual monitors")
    mouse_platform: Optional[Union[Tube, Treadmill, Disc]] = Field(None, title="Mouse platform")
    daqs: Optional[List[Union[HarpDevice, DAQDevice]]] = Field(None, title="Data acquisition devices")
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices")
    notes: Optional[str] = Field(None, title="Notes")
