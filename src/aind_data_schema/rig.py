""" Schemas for Neurophysiology and Behavior Rigs"""

from __future__ import annotations

from datetime import date
from typing import List, Optional, Union

from pydantic import Field, root_validator
from pydantic.typing import Annotated

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

    schema_version: str = Field("0.1.1", description="schema version", title="Version", const=True)
    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    modification_date: date = Field(..., title="Date of modification")
    modalities: List[Modality] = Field(..., title="Modalities", unique_items=True)
    mouse_platform: Annotated[
        Union[Disc, Treadmill, Tube, Wheel], Field(..., title="Mouse platform", discriminator="device_type")
    ]
    stimulus_devices: Optional[
        Annotated[
            List[Union[Monitor, Olfactometer, RewardDelivery, Speaker]],
            Field(None, title="Stimulus devices", unique_items=True, discriminator="device_type"),
        ]
    ]
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    daqs: Optional[
        Annotated[
            List[Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice]],
            Field(None, title="Data acquisition devices", discriminator="device_type"),
        ]
    ]
    ephys_assemblies: Optional[List[EphysAssembly]] = Field(None, title="Ephys probes", unique_items=True)
    stick_microscopes: Optional[List[StickMicroscopeAssembly]] = Field(None, title="Stick microscopes")
    laser_assemblies: Optional[List[LaserAssembly]] = Field(None, title="Laser modules", unique_items=True)
    patch_cords: Optional[List[Patch]] = Field(None, title="Patch cords", unique_items=True)
    light_sources: Optional[
        Annotated[
            List[Union[Laser, LightEmittingDiode]],
            Field(None, title="Light sources", unique_items=True, discriminator="device_type"),
        ]
    ]
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    objectives: Optional[List[Objective]] = Field(None, title="Objectives", unique_items=True)
    filters: Optional[List[Filter]] = Field(None, title="Filters", unique_items=True)
    lenses: Optional[List[Lens]] = Field(None, title="Lenses", unique_items=True)
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices", unique_items=True)
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    notes: Optional[str] = Field(None, title="Notes")

    

    @root_validator
    def validate_modality(cls, v):
        modalities = v.get("modalities")

        if Modality.ECEPHYS.value in modalities:
            ephys_assemblies = v.get("ephys_assemblies")
            stick_microscopes = v.get("stick_microscopes")
            if not ephys_assemblies:
                raise ValueError("ephys_assemblies field must be utilized for Ecephys modality")
            if not stick_microscopes:
                raise ValueError("stick_microscopes field must be utilized for Ecephys modality")
            
        if Modality.FIB.value in modalities:
            light_source = v.get("light_source")
            detector = v.get("detectors")
            patch_cords = v.get("patch_cords")
            if not light_source:
                raise ValueError("light_source field must be utilized for FIB modality")
            if not detector:
                raise ValueError("detectors field must be utilized for FIB modality")
            if not patch_cords:
                raise ValueError("patch_cords field must be utilized for FIB modality")
        
        if Modality.POPHYS.value in modalities:
            light_source = v.get("light_source")
            detector = v.get("detectors")
            objectives = v.get("objectives")
            if not light_source:
                raise ValueError("light_source field must be utilized for Pophys modality")
            if not detector:
                raise ValueError("detectors field must be utilized for Pophys modality")
            if not objectives:
                raise ValueError("objectives field must be utilized for Pophys modality")
            
        if Modality.SLAP.value in modalities:
            light_source = v.get("light_source")
            detector = v.get("detectors")
            objectives = v.get("objectives")
            if not light_source:
                raise ValueError("light_source field must be utilized for SLAP modality")
            if not detector:
                raise ValueError("detectors field must be utilized for SLAP modality")
            if not objectives:
                raise ValueError("objectives field must be utilized for SLAP modality")
            
        if Modality.BEHAVIOR_VIDEOS.value in modalities:
            cameras = v.get("cameras")
            if not cameras:
                raise ValueError("cameras field must be utilized for Behavior Videos modality")
            
        if Modality.TRAINED_BEHAVIOR.value in modalities:
            stimulus_devices = v.get("stimulus_devices")
            if not stimulus_devices:
                raise ValueError("stimulus_devices field must be utilized for Trained Behavior modality")

        

