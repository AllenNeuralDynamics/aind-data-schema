"""Core Rig model"""

from datetime import date
from typing import List, Literal, Optional, Set

from pydantic import Field, ValidationInfo, field_validator

from aind_data_schema.base import AindCoreModel
from aind_data_schema.models.devices import (
    LIGHT_SOURCES,
    MOUSE_PLATFORMS,
    RIG_DAQ_DEVICES,
    STIMULUS_DEVICES,
    Calibration,
    CameraAssembly,
    DAQDevice,
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
from aind_data_schema.models.modalities import Modality


class Rig(AindCoreModel):
    """Description of a rig"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/rig.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": True})
    schema_version: Literal["0.2.0"] = Field("0.2.0")

    rig_id: str = Field(..., description="room_stim apparatus_version", title="Rig ID")
    modification_date: date = Field(..., title="Date of modification")
    mouse_platform: MOUSE_PLATFORMS
    stimulus_devices: List[STIMULUS_DEVICES] = Field([], title="Stimulus devices")
    cameras: List[CameraAssembly] = Field([], title="Camera assemblies")
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
    daqs: List[RIG_DAQ_DEVICES] = Field([], title="Data acquisition devices", discriminator="device_type")
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices")
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    modalities: Set[Modality.ONE_OF] = Field(..., title="Modalities")
    notes: Optional[str] = Field(None, title="Notes")

    @field_validator("daqs", mode="after")
    def validate_device_names(cls, value: List[DAQDevice], info: ValidationInfo) -> List[DAQDevice]:
        """validate that all DAQ channels are connected to devices that
        actually exist
        """
        daqs = value
        standard_devices = (
            daqs
            + info.data["stimulus_devices"]
            + info.data["light_sources"]
            + info.data["patch_cords"]
            + info.data["detectors"]
            + info.data["digital_micromirror_devices"]
            + info.data["polygonal_scanners"]
            + info.data["pockels_cells"]
            + info.data["additional_devices"]
        )
        camera_devices = info.data["cameras"] + info.data["stick_microscopes"]
        standard_device_names = [device.name for device in standard_devices]
        camera_names = [camera.camera.name for camera in camera_devices]
        ephys_assembly_names = [
            probe.name for ephys_assembly in info.data["ephys_assemblies"] for probe in ephys_assembly.probes
        ]
        laser_assembly_names = [
            laser.name for laser_assembly in info.data["laser_assemblies"] for laser in laser_assembly.lasers
        ]
        mouse_platform_names = [] if info.data.get("mouse_platform") is None else [info.data["mouse_platform"].name]
        all_device_names = (
            standard_device_names + camera_names + ephys_assembly_names + laser_assembly_names + mouse_platform_names
        )

        for daq in daqs:
            for channel in daq.channels:
                if channel.device_name not in all_device_names:
                    raise ValueError(
                        f"Device name validation error: '{channel.device_name}' "
                        + f"is connected to '{channel.channel_name}' on '{daq.name}', but "
                        + "this device is not part of the rig."
                    )
        return daqs

    @staticmethod
    def _validate_ephys_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate ecephys modality has ephys_assemblies and stick_microscopes"""
        errors = []
        if Modality.ECEPHYS in value:
            for k, v in {
                "ephys_assemblies": len(info.data["ephys_assemblies"]) > 0,
                "stick_microscopes": len(info.data["stick_microscopes"]) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for Ecephys modality")
        return errors

    @staticmethod
    def _validate_fib_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Valudate FIB modality has light_sources, detectors, and patch_cords"""
        errors = []
        if Modality.FIB in value:
            for k, v in {
                "light_sources": len(info.data["light_sources"]) > 0,
                "detectors": len(info.data["detectors"]) > 0,
                "patch_cords": len(info.data["patch_cords"]) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for FIB modality")
        return errors

    @staticmethod
    def _validate_pophys_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate POPHYS modality has light_sources, detectors, and objectives"""
        errors = []
        if Modality.POPHYS in value:
            for k, v in {
                "light_sources": len(info.data["light_sources"]) > 0,
                "detectors": len(info.data["detectors"]) > 0,
                "objectives": len(info.data["objectives"]) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for POPHYS modality")
        return errors

    @staticmethod
    def _validate_slap_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate SLAP modality has light_sources, detectors, and objectives"""
        errors = []
        if Modality.SLAP in value:
            for k, v in {
                "light_sources": len(info.data["light_sources"]) > 0,
                "detectors": len(info.data["detectors"]) > 0,
                "objectives": len(info.data["objectives"]) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for SLAP modality")
        return errors

    @staticmethod
    def _validate_behavior_videos_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate BEHAVIOR_VIDEOS modality has cameras"""
        errors = []
        if Modality.BEHAVIOR_VIDEOS in value:
            if len(info.data["cameras"]) == 0:
                errors.append("cameras field must be utilized for Behavior Videos modality")
        return errors

    @staticmethod
    def _validate_trained_behavior_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate TRAINED_BEHAVIOR has stimulus devices"""
        errors = []
        if Modality.TRAINED_BEHAVIOR in value:
            if len(info.data["stimulus_devices"]) == 0:
                errors.append("stimulus_devices field must be utilized for Trained Behavior modality")
        return errors

    @field_validator("modalities", mode="after")
    def validate_modalities(cls, value: Set[Modality.ONE_OF], info: ValidationInfo) -> Set[Modality.ONE_OF]:
        """Validate each modality in modalities field has associated data"""
        ephys_errors = cls._validate_ephys_modality(value, info)
        fib_errors = cls._validate_fib_modality(value, info)
        pophys_errors = cls._validate_pophys_modality(value, info)
        slap_errors = cls._validate_slap_modality(value, info)
        behavior_vids_errors = cls._validate_behavior_videos_modality(value, info)
        trained_behavior_errors = cls._validate_trained_behavior_modality(value, info)

        errors = (
            ephys_errors + fib_errors + pophys_errors + slap_errors + behavior_vids_errors + trained_behavior_errors
        )
        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)

        return value
