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
    DigitalMicromirrorDevice,
    Disc,
    Enclosure,
    EphysAssembly,
    FiberAssembly,
    Filter,
    HarpDevice,
    Lamp,
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
    PockelsCell,
    PolygonalScanner,
    RewardDelivery,
    Speaker,
    StickMicroscopeAssembly,
    Treadmill,
    Tube,
    Wheel,
)

devices = [Calibration,
    CameraAssembly,
    DAQDevice,
    Detector,
    Device,
    DigitalMicromirrorDevice,
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
    PockelsCell,
    PolygonalScanner,
    RewardDelivery,
    Speaker,
    StickMicroscopeAssembly,
    Treadmill,
    Tube,
    Wheel,
]

class Rig(AindCoreModel):
    """Description of a rig"""

    schema_version: str = Field("0.1.7", description="schema version", title="Version", const=True)
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
    enclosure: Optional[Enclosure] = Field(None, title="Enclosure")
    ephys_assemblies: Optional[List[EphysAssembly]] = Field(None, title="Ephys probes", unique_items=True)
    fiber_assemblies: Optional[List[FiberAssembly]] = Field(None, title="Inserted fiber optics", unique_items=True)
    stick_microscopes: Optional[List[StickMicroscopeAssembly]] = Field(None, title="Stick microscopes")
    laser_assemblies: Optional[List[LaserAssembly]] = Field(None, title="Laser modules", unique_items=True)
    patch_cords: Optional[List[Patch]] = Field(None, title="Patch cords", unique_items=True)
    light_sources: Optional[
        Annotated[
            List[Union[Lamp, Laser, LightEmittingDiode]],
            Field(None, title="Light sources", unique_items=True, discriminator="device_type"),
        ]
    ]
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    objectives: Optional[List[Objective]] = Field(None, title="Objectives", unique_items=True)
    filters: Optional[List[Filter]] = Field(None, title="Filters", unique_items=True)
    lenses: Optional[List[Lens]] = Field(None, title="Lenses", unique_items=True)
    digital_micromirror_devices: Optional[List[DigitalMicromirrorDevice]] = Field(None, title="DMDs", unique_items=True)
    polygonal_scanners: Optional[List[PolygonalScanner]] = Field(None, title="Polygonal scanners", unique_items=True)
    pockels_cells: Optional[List[PockelsCell]] = Field(None, title="Pockels cells", unique_items=True)
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices", unique_items=True)
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    notes: Optional[str] = Field(None, title="Notes")

    @root_validator
    def validate_device_names(cls, values):  # noqa: C901
        """validate that all DAQ channels are connected to devices that
        actually exist
        """

        device_names = []

        # model_types = [type(model) for model in devices]

        # to_check = [field for field in values.keys() if any(isinstance(values.get(field), model) for model in model_types)]
        # print("values: ", values.keys())
        # print("checked: ", to_check)

        # to_check2 = []

        # for field in values.keys():
        #     cur_value = values.get(field)
        #     for model_type in devices:
        #         if type(cur_value) is list:
        #             for value in cur_value:
        #                     if isinstance(value, model_type):
        #                         to_check2 += [field]
        #         else:
        #             if isinstance(cur_value, model_type):
        #                 to_check2 += [field]

        cameras = values.get("cameras")
        ephys_assemblies = values.get("ephys_assemblies")
        laser_assemblies = values.get("laser_assemblies")
        mouse_platform = values.get("mouse_platform")
        stimulus_devices = values.get("stimulus_devices")
        stick_microscopes = values.get("stick_microscopes")
        light_sources = values.get("light_sources")
        patch_coords = values.get("patch_cords")
        detectors = values.get("detectors")
        objectives = values.get("objectives")
        filters = values.get("filters")
        lenses = values.get("lenses")  
        digital_micromirror_devices = values.get("digital_micromirror_devices")
        polygonal_scanners = values.get("polygonal_scanners")
        pockels_cells = values.get("pockels_cells")
        additional_devices = values.get("additional_devices")
        daqs = values.get("daqs")



        if daqs is None:
            return values

        # device_names = [None]

        # for field in to_check2:
        #     v = values.get(field)
        #     if v is not None:
        #         if isinstance(v, list):
        #             for item in v:
        #                 print("type: ", type(item))
        #                 print("item: ", item)
        #                 if isinstance(item, CameraAssembly):
        #                     device_names += item.camera.name
        #                 else:
        #                     device_names += [device.name for device in item]
        #         else:
        #             device_names += [v.name]

        #         print(device_names)

        for device_type in [daqs, stimulus_devices, light_sources, patch_coords,detectors, objectives, filters, lenses, digital_micromirror_devices, polygonal_scanners, pockels_cells, additional_devices]:
            if device_type is not None:
                device_names += [device.name for device in device_type]

        for camera_device in [cameras, stick_microscopes]:
            if camera_device is not None:
                device_names += [camera.camera.name for camera in camera_device]

        if ephys_assemblies is not None:
            device_names += [probe.name for ephys_assembly in ephys_assemblies for probe in ephys_assembly.probes]

        if laser_assemblies is not None:
            device_names += [laser.name for laser_assembly in laser_assemblies for laser in laser_assembly.lasers]

        if mouse_platform is not None:
            device_names += [mouse_platform.name]

    
        print(device_names)


        for daq in daqs:
            if daq.channels is not None:
                for channel in daq.channels:
                    if channel.device_name not in device_names:
                        raise ValueError(
                            f"Device name validation error: '{channel.device_name}' "
                            + f"is connected to '{channel.channel_name}' on '{daq.name}', but "
                            + "this device is not part of the rig."
                        )

        return values
    def validate_modality(cls, v):  # noqa: C901
        """Validator to ensure all expected fields are present, based on given modality"""

        modalities = v.get("modalities")

        modalities = [modality.value for modality in modalities]

        error_message = ""

        if Modality.ECEPHYS.value in modalities:
            ephys_assemblies = v.get("ephys_assemblies")
            stick_microscopes = v.get("stick_microscopes")

            for key, value in {"ephys_assemblies": ephys_assemblies, "stick_microscopes": stick_microscopes}.items():
                if value is None:
                    error_message += f"{key} field must be utilized for Ecephys modality\n"

        if Modality.FIB.value in modalities:
            light_source = v.get("light_sources")
            detector = v.get("detectors")
            patch_cords = v.get("patch_cords")
            for key, value in {
                "light_sources": light_source,
                "detectors": detector,
                "patch_cords": patch_cords,
            }.items():
                if value is None:
                    error_message += f"{key} field must be utilized for FIB modality\n"

        if Modality.POPHYS.value in modalities:
            light_source = v.get("light_sources")
            detector = v.get("detectors")
            objectives = v.get("objectives")
            for key, value in {"light_sources": light_source, "detectors": detector, "objectives": objectives}.items():
                if not value:
                    error_message += f"{key} field must be utilized for POPHYS modality\n"

        if Modality.SLAP.value in modalities:
            light_source = v.get("light_source")
            detector = v.get("detectors")
            objectives = v.get("objectives")
            for key, value in {"light_source": light_source, "detectors": detector, "objectives": objectives}.items():
                if not value:
                    error_message += f"{key} field must be utilized for SLAP modality\n"

        if Modality.BEHAVIOR_VIDEOS.value in modalities:
            cameras = v.get("cameras")
            if not cameras:
                error_message += "cameras field must be utilized for Behavior Videos modality\n"

        if Modality.TRAINED_BEHAVIOR.value in modalities:
            stimulus_devices = v.get("stimulus_devices")
            if not stimulus_devices:
                error_message += "stimulus_devices field must be utilized for Trained Behavior modality\n"

        if error_message:
            raise ValueError(error_message)

        return v
