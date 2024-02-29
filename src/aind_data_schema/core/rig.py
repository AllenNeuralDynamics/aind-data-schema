"""Core Rig model"""

from datetime import date
from typing import List, Literal, Optional, Set, Union

from pydantic import Field, model_validator
from typing_extensions import Annotated

from aind_data_schema.base import AindCoreModel
from aind_data_schema.models.coordinates import Axis, Origin
from aind_data_schema.models.devices import (
    LIGHT_SOURCES,
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
from aind_data_schema.models.modalities import Modality

MOUSE_PLATFORMS = Annotated[Union[tuple(MousePlatform.__subclasses__())], Field(discriminator="device_type")]
STIMULUS_DEVICES = Annotated[Union[Monitor, Olfactometer, RewardDelivery, Speaker], Field(discriminator="device_type")]
RIG_DAQ_DEVICES = Annotated[
    Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice], Field(discriminator="device_type")
]


class Rig(AindCoreModel):
    """Description of a rig"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/rig.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.2.16"] = Field("0.2.16")
    rig_id: str = Field(..., description="room_rig name_date modified", title="Rig ID")
    modification_date: date = Field(..., title="Date of modification")
    mouse_platform: MOUSE_PLATFORMS
    stimulus_devices: List[STIMULUS_DEVICES] = Field(default=[], title="Stimulus devices")
    cameras: List[CameraAssembly] = Field(default=[], title="Camera assemblies")
    enclosure: Optional[Enclosure] = Field(None, title="Enclosure")
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
    daqs: List[RIG_DAQ_DEVICES] = Field(default=[], title="Data acquisition devices", discriminator="device_type")
    calibrations: List[Calibration] = Field(..., title="Full calibration of devices")
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    origin: Optional[Origin] = Field(None, title="Origin point for rig position transforms")
    rig_axes: Optional[List[Axis]] = Field(default=[], title="Rig axes", min_length=3, max_length=3)
    modalities: Set[Modality.ONE_OF] = Field(..., title="Modalities")
    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="after")
    def validate_device_names(self):
        """validate that all DAQ channels are connected to devices that
        actually exist
        """
        non_reward_delivery_stimulus_devices = [
            d for d in self.stimulus_devices if not isinstance(d, RewardDelivery)
        ]
        standard_devices = (
            self.daqs
            + self.light_sources
            + self.patch_cords
            + self.detectors
            + self.digital_micromirror_devices
            + self.polygonal_scanners
            + self.pockels_cells
            + self.additional_devices
            + non_reward_delivery_stimulus_devices
        )
        camera_devices = self.cameras + self.stick_microscopes
        standard_device_names = [device.name for device in standard_devices]
        camera_names = [camera.camera.name for camera in camera_devices]
        ephys_assembly_names = [
            probe.name for ephys_assembly in self.ephys_assemblies for probe in ephys_assembly.probes
        ]
        laser_assembly_names = [
            laser.name for laser_assembly in self.laser_assemblies for laser in laser_assembly.lasers
        ]
        mouse_platform_names = [] if getattr(self, "mouse_platform", None) is None else [self.mouse_platform.name]
        reward_deliveries = [d for d in self.stimulus_devices if isinstance(d, RewardDelivery)]
        reward_delivery_device_names = []
        for rd in reward_deliveries:
            for rs in rd.reward_spouts:
                reward_delivery_device_names += [rs.name, rs.solenoid_valve.name]

        all_device_names = (
            standard_device_names
            + camera_names
            + ephys_assembly_names
            + laser_assembly_names
            + mouse_platform_names
            + reward_delivery_device_names
        )

        for daq in self.daqs:
            for channel in daq.channels:
                if channel.device_name not in all_device_names:
                    raise ValueError(
                        f"Device name validation error: '{channel.device_name}' "
                        + f"is connected to '{channel.channel_name}' on '{daq.name}', but "
                        + "this device is not part of the rig."
                    )
        return self

    def _validate_ephys_modality(self) -> List[str]:
        """Validate ecephys modality has ephys_assemblies and stick_microscopes"""
        errors = []
        if Modality.ECEPHYS in self.modalities:
            for k, v in {
                "ephys_assemblies": len(self.ephys_assemblies) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for Ecephys modality")
        return errors

    def _validate_fib_modality(self) -> List[str]:
        """Validate FIB modality has light_sources, detectors, and patch_cords"""
        errors = []
        if Modality.FIB in self.modalities:
            for k, v in {
                "light_sources": len(self.light_sources) > 0,
                "detectors": len(self.detectors) > 0,
                "patch_cords": len(self.patch_cords) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for FIB modality")
        return errors

    def _validate_pophys_modality(self) -> List[str]:
        """Validate POPHYS modality has light_sources, detectors, and objectives"""
        errors = []
        if Modality.POPHYS in self.modalities:
            for k, v in {
                "light_sources": len(self.light_sources) > 0,
                "detectors": len(self.detectors) > 0,
                "objectives": len(self.objectives) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for POPHYS modality")
        return errors

    def _validate_slap_modality(self) -> List[str]:
        """Validate SLAP modality has light_sources, detectors, and objectives"""
        errors = []
        if Modality.SLAP in self.modalities:
            for k, v in {
                "light_sources": len(self.light_sources) > 0,
                "detectors": len(self.detectors) > 0,
                "objectives": len(self.objectives) > 0,
            }.items():
                if v is False:
                    errors.append(f"{k} field must be utilized for SLAP modality")
        return errors

    def _validate_behavior_videos_modality(self) -> List[str]:
        """Validate BEHAVIOR_VIDEOS modality has cameras"""
        errors = []
        if Modality.BEHAVIOR_VIDEOS in self.modalities:
            if len(self.cameras) == 0:
                errors.append("cameras field must be utilized for Behavior Videos modality")
        return errors

    def _validate_behavior_modality(self) -> List[str]:
        """Validate that BEHAVIOR modality has stimulus_devices"""
        errors = []
        if Modality.BEHAVIOR in self.modalities:
            if len(self.stimulus_devices) == 0:
                errors.append("stimulus_devices field must be utilized for Behavior modality")

        return errors

    @model_validator(mode="after")
    def validate_modalities(self):
        """Validate each modality in modalities field has associated data"""
        ephys_errors = self._validate_ephys_modality()
        fib_errors = self._validate_fib_modality()
        pophys_errors = self._validate_pophys_modality()
        slap_errors = self._validate_slap_modality()
        behavior_vids_errors = self._validate_behavior_videos_modality()
        behavior_errors = self._validate_behavior_modality()

        errors = ephys_errors + fib_errors + pophys_errors + slap_errors + behavior_vids_errors + behavior_errors
        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)

        return self
