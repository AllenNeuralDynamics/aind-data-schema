""" Schemas for Neurophysiology and Behavior Rigs"""

from __future__ import annotations

from datetime import date
from typing import List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel
from aind_data_schema.data_description import Modality
from aind_data_schema.device import (
    Calibration,
    CameraAssembly,
    DAQDevice,
    Detector,
    Device,
    Disc,
    EphysAssembly,
    Filter,
    HarpDevice,
    Laser,
    LaserAssembly,
    Lens,
    LightEmittingDiode,
    Monitor,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OpenEphysAcquisitionBoard,
    Patch,
    RewardDelivery,
    Speaker,
    StickMicroscopeAssembly,
    Treadmill,
    Tube,
    Wheel,
)


class Rig(AindCoreModel):
    """Description of a rig"""

    schema_version: str = Field("0.1.0", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    date_of_modification: date = Field(..., title="Date of modification")
    modalities: List[Modality] = Field(..., title="Modalities", unique_items=True)
    mouse_platform: Union[Disc, Treadmill, Tube, Wheel] = Field(..., title="Mouse platform")
    stimulus_devices: Optional[List[Union[Monitor, Olfactometer, RewardDelivery, Speaker]]] = Field(
        ..., title="Stimulus devices", unique_items=True,
        )
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    daqs: Optional[List[Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice]]] = Field(
        None, title="Data acquisition devices"
    )
    ephys_assemblies: Optional[List[EphysAssembly]] = Field(None, title="Ephys probes", unique_items=True)
    stick_microscopes: Optional[List[StickMicroscopeAssembly]] = Field(None, title="Stick microscopes")
    laser_assemblies: Optional[List[LaserAssembly]] = Field(None, title="Laser modules", unique_items=True)
    patch_cords: Optional[List[Patch]] = Field(..., title="Patch cords", unique_items=True)
    light_sources: Optional[List[Union[Laser, LightEmittingDiode]]] = Field(
        ..., title="Light sources", unique_items=True
        )
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    objectives: Optional[List[Objective]] = Field(None, title="Objectives", unique_items=True)
    filters: Optional[List[Filter]] = Field(None, title="Filters", unique_items=True)
    lenses: Optional[List[Lens]] = Field(None, title="Lenses", unique_items=True)
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices", unique_items=True)
    ccf_coordinate_transform: Optional[str] = Field(
        None, title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    notes: Optional[str] = Field(None, title="Notes")
