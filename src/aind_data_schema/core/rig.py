"""Core Rig model"""

from datetime import date
from typing import List, Literal, Optional, Set, Union

from aind_data_schema_models.modalities import Modality
from pydantic import Field, ValidationInfo, field_serializer, field_validator, model_validator
from typing_extensions import Annotated

from aind_data_schema.base import AindCoreModel
from aind_data_schema.components.coordinates import Axis, Origin
from aind_data_schema.components.devices import (
    LIGHT_SOURCES,
    Calibration,
    CameraAssembly,
    CameraTarget,
    DAQDevice,
    Detector,
    Device,
    DigitalMicromirrorDevice,
    Enclosure,
    EphysAssembly,
    FiberAssembly,
    Filter,
    HarpDevice,
    LaserAssembly,
    Lens,
    Monitor,
    MousePlatform,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OpenEphysAcquisitionBoard,
    Patch,
    PockelsCell,
    PolygonalScanner,
    RewardDelivery,
    Speaker,
)

MOUSE_PLATFORMS = Annotated[Union[tuple(MousePlatform.__subclasses__())], Field(discriminator="device_type")]
STIMULUS_DEVICES = Annotated[Union[Monitor, Olfactometer, RewardDelivery, Speaker], Field(discriminator="device_type")]
RIG_DAQ_DEVICES = Annotated[
    Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice], Field(discriminator="device_type")
]
RIG_ID_PATTERN = r"^[a-zA-Z0-9]+_[a-zA-Z0-9-]+_\d{8}$"


class Rig(AindCoreModel):
    """Description of a rig"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/rig.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.1"] = Field("1.0.1")
    rig_id: str = Field(
        ...,
        description="Unique rig identifier, name convention: <room>-<apparatus name>-<date modified YYYYMMDD>",
        title="Rig ID",
        pattern=RIG_ID_PATTERN,
    )
    modification_date: date = Field(..., title="Date of modification")
    mouse_platform: MOUSE_PLATFORMS
    stimulus_devices: List[STIMULUS_DEVICES] = Field(default=[], title="Stimulus devices")
    cameras: List[CameraAssembly] = Field(default=[], title="Camera assemblies")
    enclosure: Optional[Enclosure] = Field(default=None, title="Enclosure")
    ephys_assemblies: List[EphysAssembly] = Field(default=[], title="Ephys probes")
    fiber_assemblies: List[FiberAssembly] = Field(default=[], title="Inserted fiber optics")
    stick_microscopes: List[CameraAssembly] = Field(default=[], title="Stick microscopes")
    laser_assemblies: List[LaserAssembly] = Field(default=[], title="Laser modules")
    patch_cords: List[Patch] = Field(default=[], title="Patch cords")
    light_sources: List[LIGHT_SOURCES] = Field(default=[], title="Light sources")
    detectors: List[Detector] = Field(default=[], title="Detectors")
    objectives: List[Objective] = Field(default=[], title="Objectives")
    filters: List[Filter] = Field(default=[], title="Filters")
    lenses: List[Lens] = Field(default=[], title="Lenses")
    digital_micromirror_devices: List[DigitalMicromirrorDevice] = Field(default=[], title="DMDs")
    polygonal_scanners: List[PolygonalScanner] = Field(default=[], title="Polygonal scanners")
    pockels_cells: List[PockelsCell] = Field(default=[], title="Pockels cells")
    additional_devices: List[Device] = Field(default=[], title="Additional devices")
    daqs: List[RIG_DAQ_DEVICES] = Field(default=[], title="Data acquisition devices")
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices")
    ccf_coordinate_transform: Optional[str] = Field(
        default=None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    origin: Optional[Origin] = Field(default=None, title="Origin point for rig position transforms")
    rig_axes: Optional[List[Axis]] = Field(default=None, title="Rig axes", min_length=3, max_length=3)
    modalities: Set[Modality.ONE_OF] = Field(..., title="Modalities")
    notes: Optional[str] = Field(default=None, title="Notes")

    @field_serializer("modalities", when_used="json")
    def serialize_modalities(modalities: Set[Modality.ONE_OF]):
        """sort modalities by name when serializing to JSON"""
        return sorted(modalities, key=lambda x: x.name)

    @model_validator(mode="after")
    def validate_cameras_other(self):
        """check if any cameras contain an 'other' field"""

        if self.notes is None:
            for camera_assembly in self.cameras + self.stick_microscopes:
                if camera_assembly.camera_target == CameraTarget.OTHER:
                    raise ValueError(
                        f"Notes cannot be empty if a camera target contains an 'Other' field. "
                        f"Describe the camera target from ({camera_assembly.name}) in the notes field"
                    )

        return self

    @field_validator("daqs", mode="after")
    def validate_device_names(cls, value: List[DAQDevice], info: ValidationInfo) -> List[DAQDevice]:
        """validate that all DAQ channels are connected to devices that
        actually exist
        """
        daqs = value
        non_reward_delivery_stimulus_devices = [
            d for d in info.data.get("stimulus_devices", []) if not isinstance(d, RewardDelivery)
        ]
        standard_devices = (
            daqs
            + info.data.get("light_sources", [])
            + info.data.get("patch_cords", [])
            + info.data.get("detectors", [])
            + info.data.get("digital_micromirror_devices", [])
            + info.data.get("polygonal_scanners", [])
            + info.data.get("pockels_cells", [])
            + info.data.get("additional_devices", [])
            + non_reward_delivery_stimulus_devices
        )
        camera_devices = info.data.get("cameras", []) + info.data.get("stick_microscopes", [])
        standard_device_names = [device.name for device in standard_devices]
        camera_names = [camera.camera.name for camera in camera_devices]
        ephys_assembly_names = [
            probe.name for ephys_assembly in info.data.get("ephys_assemblies", []) for probe in ephys_assembly.probes
        ]
        laser_assembly_names = [
            laser.name for laser_assembly in info.data.get("laser_assemblies", []) for laser in laser_assembly.lasers
        ]
        mouse_platform_names = [] if info.data.get("mouse_platform") is None else [info.data["mouse_platform"].name]
        reward_deliveries = [d for d in info.data.get("stimulus_devices", []) if isinstance(d, RewardDelivery)]
        reward_delivery_device_names = []
        for rd in reward_deliveries:
            for rs in rd.reward_spouts:
                reward_delivery_device_names += [rs.name, rs.solenoid_valve.name, rs.lick_sensor.name]

        all_device_names = (
            standard_device_names
            + camera_names
            + ephys_assembly_names
            + laser_assembly_names
            + mouse_platform_names
            + reward_delivery_device_names
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
                "ephys_assemblies": len(info.data.get("ephys_assemblies", [])) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for Ecephys modality")
        return errors

    @staticmethod
    def _validate_fib_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate FIB modality has light_sources, detectors, and patch_cords"""
        errors = []
        if Modality.FIB in value:
            for k, v in {
                "light_sources": len(info.data.get("light_sources", [])) > 0,
                "detectors": len(info.data.get("detectors", [])) > 0,
                "patch_cords": len(info.data.get("patch_cords", [])) > 0,
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
                "light_sources": len(info.data.get("light_sources", [])) > 0,
                "detectors": len(info.data.get("detectors", [])) > 0,
                "objectives": len(info.data.get("objectives", [])) > 0,
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
                "light_sources": len(info.data.get("light_sources", [])) > 0,
                "detectors": len(info.data.get("detectors", [])) > 0,
                "objectives": len(info.data.get("objectives", [])) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for SLAP modality")
        return errors

    @staticmethod
    def _validate_behavior_videos_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate BEHAVIOR_VIDEOS modality has cameras"""
        errors = []
        if Modality.BEHAVIOR_VIDEOS in value:
            if len(info.data.get("cameras", [])) == 0:
                errors.append("cameras field must be utilized for Behavior Videos modality")
        return errors

    @staticmethod
    def _validate_behavior_modality(value: Set[Modality.ONE_OF], info: ValidationInfo) -> List[str]:
        """Validate that BEHAVIOR modality has stimulus_devices"""
        errors = []
        if Modality.BEHAVIOR in value:
            if len(info.data.get("stimulus_devices", [])) == 0:
                errors.append("stimulus_devices field must be utilized for Behavior modality")

        return errors

    @field_validator("modalities", mode="after")
    def validate_modalities(cls, value: Set[Modality.ONE_OF], info: ValidationInfo) -> Set[Modality.ONE_OF]:
        """Validate each modality in modalities field has associated data"""
        ephys_errors = cls._validate_ephys_modality(value, info)
        fib_errors = cls._validate_fib_modality(value, info)
        pophys_errors = cls._validate_pophys_modality(value, info)
        slap_errors = cls._validate_slap_modality(value, info)
        behavior_vids_errors = cls._validate_behavior_videos_modality(value, info)
        behavior_errors = cls._validate_behavior_modality(value, info)

        errors = ephys_errors + fib_errors + pophys_errors + slap_errors + behavior_vids_errors + behavior_errors
        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)

        return value
