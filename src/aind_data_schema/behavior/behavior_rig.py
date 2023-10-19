""" Schemas for Behavior Rig. This is being deprecated after 2023-11-01. """

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field
from pydantic.typing import Annotated

from aind_data_schema.base import AindCoreModel
from aind_data_schema.device import (
    Calibration,
    CameraAssembly,
    DAQDevice,
    Device,
    Disc,
    HarpDevice,
    Monitor,
    RewardDelivery,
    Speaker,
    Treadmill,
    Tube,
)


class BehaviorRig(AindCoreModel):
    """Description of an behavior rig. This is being deprecated after 2023-11-01."""

    schema_version: str = Field("0.1.16", description="schema version", title="Version", const=True)

    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    mouse_platform: Annotated[
        Union[Tube, Treadmill, Disc], Field(..., title="Mouse platform", discriminator="device_type")
    ]
    stimulus_devices: Optional[
        Annotated[
            List[Union[Monitor, RewardDelivery, Speaker]],
            Field(None, title="Stimulus devices", unique_items=True, discriminator="device_type"),
        ]
    ]
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    daqs: Optional[
        Annotated[
            List[Union[HarpDevice, DAQDevice]],
            Field(None, title="Data acquisition devices", discriminator="device_type"),
        ]
    ]
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
