""" Schemas for Behavior Sessions """

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Union

from pydantic import Field

from ..base import AindCoreModel, AindModel
from ..device import (
    CameraAssembly,
    DAQDevice,
    Device,
    Disc,
    HarpDevice,
    Monitor,
    Treadmill,
    Tube,
)

class BehaviorRig(AindCoreModel):
    """Description of an behavior rig"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/behavior/behavior_rig.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field("0.0.1", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    visual_monitors: Optional[List[Monitor]] = Field(None, title="Visual monitors", unique_items=True)
    mouse_platform: Optional[Union[Tube, Treadmill, Disc]] = Field(None, title="Mouse platform")
    daqs: Optional[List[Union[HarpDevice, DAQDevice]]] = Field(
        None, title="Data acquisition devices"
    )
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
