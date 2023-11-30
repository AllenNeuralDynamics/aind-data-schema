from datetime import date
from typing import List, Literal, Optional, Set

from pydantic import Field, model_validator

from aind_data_schema.base import AindCoreModel
from aind_data_schema.models.devices import (
    DAQ_DEVICES,
    LIGHT_SOURCES,
    MOUSE_PLATFORMS,
    STIMULUS_DEVICES,
    Calibration,
    CameraAssembly,
    Detector,
    Device,
    DigitalMicromirrorDevice,
    Enclosure,
    EphysAssembly,
    FiberAssembly,
    Filter,
    LaserAssembly,
    Lens,
    Objective,
    Patch,
    PockelsCell,
    PolygonalScanner,
    StickMicroscopeAssembly,
)
# from aind_data_schema.models.modalities import BEHAVIOR_VIDEOS, ECEPHYS, FIB, MODALITIES, POPHYS, SLAP, TRAINED_BEHAVIOR
from aind_data_schema.models.modalities import Modality


class Rig(AindCoreModel):
    """Description of a rig"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/rig.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": True})
    schema_version: Literal["0.2.0"] = Field("0.2.0")

    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    modification_date: date = Field(..., title="Date of modification")
    modalities: Set[Modality.ONE_OF] = Field(..., title="Modalities")
    mouse_platform: MOUSE_PLATFORMS
    stimulus_devices: List[STIMULUS_DEVICES] = Field([], title="Stimulus devices")
    cameras: List[CameraAssembly] = Field([], title="Camera assemblies")
    daqs: List[DAQ_DEVICES] = Field([], title="Data acquisition devices", discriminator="device_type")
    enclosure: Optional[Enclosure] = Field(None, title="Enclosure")
    ephys_assemblies: List[EphysAssembly] = Field([], title="Ephys probes")
    fiber_assemblies: List[FiberAssembly] = Field([], title="Inserted fiber optics")
    stick_microscopes: List[StickMicroscopeAssembly] = Field([], title="Stick microscopes")
    laser_assemblies: List[LaserAssembly] = Field([], title="Laser modules")
    patch_cords: List[Patch] = Field([], title="Patch cords")
    light_sources: List[LIGHT_SOURCES] = Field([], title="Light sources")
    detectors: List[Detector] = Field([], title="Detectors")
    objectives: List[Objective] = Field([], title="Objectives")
    filters: List[Filter] = Field([], title="Filters")
    lenses: List[Lens] = Field([], title="Lenses")
    digital_micromirror_devices: List[DigitalMicromirrorDevice] = Field([], title="DMDs")
    polygonal_scanners: List[PolygonalScanner] = Field([], title="Polygonal scanners")
    pockels_cells: List[PockelsCell] = Field([], title="Pockels cells")
    additional_devices: List[Device] = Field([], title="Additional devices")
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices")
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    notes: Optional[str] = Field(None, title="Notes")

    # @root_validator
    # def validate_device_names(cls, values):  # noqa: C901
    #     """validate that all DAQ channels are connected to devices that
    #     actually exist
    #     """
    #
    #     device_names = []
    #
    #     cameras = values.get("cameras")
    #     ephys_assemblies = values.get("ephys_assemblies")
    #     laser_assemblies = values.get("laser_assemblies")
    #     mouse_platform = values.get("mouse_platform")
    #     stimulus_devices = values.get("stimulus_devices")
    #     stick_microscopes = values.get("stick_microscopes")
    #     light_sources = values.get("light_sources")
    #     patch_coords = values.get("patch_cords")
    #     detectors = values.get("detectors")
    #     digital_micromirror_devices = values.get("digital_micromirror_devices")
    #     polygonal_scanners = values.get("polygonal_scanners")
    #     pockels_cells = values.get("pockels_cells")
    #     additional_devices = values.get("additional_devices")
    #     daqs = values.get("daqs")
    #
    #     if daqs is None:
    #         return values
    #
    #     for device_type in [
    #         daqs,
    #         stimulus_devices,
    #         light_sources,
    #         patch_coords,
    #         detectors,
    #         digital_micromirror_devices,
    #         polygonal_scanners,
    #         pockels_cells,
    #         additional_devices,
    #     ]:
    #         if device_type is not None:
    #             device_names += [device.name for device in device_type]
    #
    #     for camera_device in [cameras, stick_microscopes]:
    #         if camera_device is not None:
    #             device_names += [camera.camera.name for camera in camera_device]
    #
    #     if ephys_assemblies is not None:
    #         device_names += [probe.name for ephys_assembly in ephys_assemblies for probe in ephys_assembly.probes]
    #
    #     if laser_assemblies is not None:
    #         device_names += [laser.name for laser_assembly in laser_assemblies for laser in laser_assembly.lasers]
    #
    #     if mouse_platform is not None:
    #         device_names += [mouse_platform.name]
    #
    #     for daq in daqs:
    #         if daq.channels is not None:
    #             for channel in daq.channels:
    #                 if channel.device_name not in device_names:
    #                     raise ValueError(
    #                         f"Device name validation error: '{channel.device_name}' "
    #                         + f"is connected to '{channel.channel_name}' on '{daq.name}', but "
    #                         + "this device is not part of the rig."
    #                     )
    #
    #     return values


    @model_validator(mode="after")
    def validate_ephys_modality(self):
        error_message = ""
        if Modality.ECEPHYS in self.modalities:
            for key, value in {
                "ephys_assemblies": len(self.ephys_assemblies) > 0,
                "stick_microscopes": len(self.stick_microscopes) > 0,
            }.items():
                if value is False:
                    error_message += f"{key} field must be utilized for Ecephys modality\n"
        if error_message:
            raise AssertionError(error_message)
        return self

    @model_validator(mode="after")
    def validate_fib_modality(self):
        error_message = ""
        if Modality.FIB in self.modalities:
            for key, value in {
                "light_sources": len(self.light_sources) > 0,
                "detectors": len(self.detectors) > 0,
                "patch_cords": len(self.patch_cords) > 0,
            }.items():
                if value is False:
                    error_message += f"{key} field must be utilized for FIB modality\n"
        if error_message:
            raise AssertionError(error_message)
        return self

    @model_validator(mode="after")
    def validate_pophys_modality(self):
        error_message = ""
        if Modality.POPHYS in self.modalities:
            for key, value in {
                "light_sources": len(self.light_sources) > 0,
                "detectors": len(self.detectors) > 0,
                "objectives": len(self.objectives) > 0,
            }.items():
                if value is False:
                    error_message += f"{key} field must be utilized for POPHYS modality\n"
        if error_message:
            raise AssertionError(error_message)
        return self

    @model_validator(mode="after")
    def validate_slap_modality(self):
        error_message = ""
        if Modality.SLAP in self.modalities:
            for key, value in {
                "light_sources": len(self.light_sources) > 0,
                "detectors": len(self.detectors) > 0,
                "objectives": len(self.objectives) > 0,
            }.items():
                if value is False:
                    error_message += f"{key} field must be utilized for SLAP modality\n"
        if error_message:
            raise AssertionError(error_message)
        return self

    @model_validator(mode="after")
    def validate_behavior_videos_modality(self):
        error_message = ""
        if Modality.BEHAVIOR_VIDEOS in self.modalities:
            if len(self.cameras) == 0:
                error_message += "cameras field must be utilized for Behavior Videos modality\n"
        if error_message:
            raise AssertionError(error_message)
        return self

    @model_validator(mode="after")
    def validate_trained_behavior_modality(self):
        error_message = ""
        if Modality.TRAINED_BEHAVIOR in self.modalities:
            if len(self.stimulus_devices) == 0:
                error_message += "stimulus_devices field must be utilized for Trained Behavior modality\n"
        if error_message:
            raise AssertionError(error_message)
        return self
