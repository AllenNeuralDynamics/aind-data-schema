""" Schemas for Physiology and/or Behavior Sessions """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated

from aind_data_schema.base import AindCoreModel, AindGeneric, AindGenericType, AindModel, AwareDatetimeWithDefault
from aind_data_schema.imaging.tile import Channel
from aind_data_schema.models.coordinates import CcfCoords, Coordinates3d
from aind_data_schema.models.devices import Calibration, Maintenance, RelativePosition, Software, SpoutSide
from aind_data_schema.models.modalities import Modality
from aind_data_schema.models.stimulus import (
    AuditoryStimulation,
    OlfactoryStimulation,
    OptoStimulation,
    PhotoStimulation,
    VisualStimulation,
)
from aind_data_schema.models.units import (
    AngleUnit,
    FrequencyUnit,
    MassUnit,
    PowerUnit,
    SizeUnit,
    SoundIntensityUnit,
    TimeUnit,
    VolumeUnit,
)


class StimulusModality(str, Enum):
    """Types of stimulus modalities"""

    AUDITORY = "Auditory"
    OLFACTORY = "Olfactory"
    OPTOGENETICS = "Optogenetics"
    NONE = "None"
    VIRTUAL_REALITY = "Virtual reality"
    VISUAL = "Visual"
    WHEEL_FRICTION = "Wheel friction"


# Ophys components
class FiberConnectionConfig(AindModel):
    """Description for a fiber photometry configuration"""

    patch_cord_name: str = Field(..., title="Patch cord name (must match rig)")
    patch_cord_output_power: Decimal = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(PowerUnit.UW, title="Output power unit")
    fiber_name: str = Field(..., title="Fiber name (must match procedure)")


class TriggerType(str, Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class DetectorConfig(AindModel):
    """Description of detector settings"""

    name: str = Field(..., title="Name")
    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")


class LightEmittingDiodeConfig(AindModel):
    """Description of LED settings"""

    device_type: Literal["LightEmittingDiode"] = "LightEmittingDiode"
    name: str = Field(..., title="Name")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class FieldOfView(AindModel):
    """Description of an imaging field of view"""

    index: int = Field(..., title="Index")
    imaging_depth: int = Field(..., title="Imaging depth (um)")
    imaging_depth_unit: SizeUnit = Field(SizeUnit.UM, title="Imaging depth unit")
    targeted_structure: str = Field(..., title="Targeted structure")
    fov_coordinate_ml: Decimal = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: Decimal = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(
        ...,
        title="FOV reference",
        description="Reference for ML/AP coordinates",
    )
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")
    magnification: str = Field(..., title="Magnification")
    fov_scale_factor: Decimal = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field("um/pixel", title="FOV scale factor unit")
    frame_rate: Optional[Decimal] = Field(None, title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    coupled_fov_index: Optional[int] = Field(None, title="Coupled FOV", description="Coupled planes for multiscope")
    power: Optional[Decimal] = Field(None, title="Power")
    power_unit: PowerUnit = Field(PowerUnit.PERCENT, title="Power unit")
    scanfield_z: Optional[int] = Field(
        None,
        title="Z stage position of the fastz actuator for a given targeted depth",
    )
    scanfield_z_unit: SizeUnit = Field(SizeUnit.UM, title="Z stage position unit")
    scanimage_roi_index: Optional[int] = Field(None, title="ScanImage ROI index")
    notes: Optional[str] = Field(None, title="Notes")


class StackChannel(Channel):
    """Description of a Channel used in a Stack"""

    start_depth: int = Field(..., title="Starting depth (um)")
    end_depth: int = Field(..., title="Ending depth (um)")
    depth_unit: SizeUnit = Field(SizeUnit.UM, title="Depth unit")


class Stack(AindModel):
    """Description of a two photon stack"""

    channels: List[StackChannel] = Field(..., title="Channels")
    number_of_planes: int = Field(..., title="Number of planes")
    step_size: float = Field(..., title="Step size (um)")
    step_size_unit: SizeUnit = Field(SizeUnit.UM, title="Step size unit")
    number_of_plane_repeats_per_volume: int = Field(..., title="Number of repeats per volume")
    number_of_volume_repeats: int = Field(..., title="Number of volume repeats")
    fov_coordinate_ml: float = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: float = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(
        ...,
        title="FOV reference",
        description="Reference for ML/AP coordinates",
    )
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")
    magnification: Optional[str] = Field(None, title="Magnification")
    fov_scale_factor: float = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field("um/pixel", title="FOV scale factor unit")
    frame_rate: Decimal = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    targeted_structure: Optional[str] = Field(None, title="Targeted structure")


class SlapSessionType(str, Enum):
    """Type of slap session"""

    PARENT = "Parent"
    BRANCH = "Branch"


class SlapFieldOfView(FieldOfView):
    """Description of a Slap2 scan"""

    session_type: SlapSessionType = Field(..., title="Session type")
    dmd_dilation_x: int = Field(..., title="DMD Dilation X (pixels)")
    dmd_dilation_y: int = Field(..., title="DMD Dilation Y (pixels)")
    dilation_unit: SizeUnit = Field(SizeUnit.PX, title="Dilation unit")
    target_neuron: Optional[str] = Field(None, title="Target neuron")
    target_branch: Optional[str] = Field(None, title="Target branch")
    path_to_array_of_frame_rates: str = Field(..., title="Array of frame rates")


# Ephys Components
class DomeModule(AindModel):
    """Movable module that is mounted on the ephys dome insertion system"""

    assembly_name: str = Field(..., title="Assembly name")
    arc_angle: Decimal = Field(..., title="Arc Angle (deg)")
    module_angle: Decimal = Field(..., title="Module Angle (deg)")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")
    rotation_angle: Optional[Decimal] = Field(None, title="Rotation Angle (deg)")
    coordinate_transform: Optional[str] = Field(
        None,
        title="Transform from local manipulator axes to rig",
        description="Path to coordinate transform",
    )
    calibration_date: Optional[datetime] = Field(None, title="Date on which coordinate transform was last calibrated")
    notes: Optional[str] = Field(None, title="Notes")


class ManipulatorModule(DomeModule):
    """A dome module connected to a 3-axis manipulator"""

    primary_targeted_structure: str = Field(..., title="Targeted structure")
    targeted_ccf_coordinates: List[CcfCoords] = Field(
        default=[],
        title="Targeted CCF coordinates",
    )
    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )
    implant_hole_number: Optional[int] = Field(None, title="Implant hole number")


class EphysProbeConfig(AindModel):
    """Probes in a EphysProbeModule"""

    name: str = Field(..., title="Ephys probe name (must match rig JSON)")
    other_targeted_structures: List[str] = []


class EphysModule(ManipulatorModule):
    """Probe recorded in a Stream"""

    ephys_probes: List[EphysProbeConfig] = Field(..., title="Ephys probes used in this module")


class FiberModule(ManipulatorModule):
    """Inserted fiber photometry probe recorded in a stream"""

    fiber_connections: List[FiberConnectionConfig] = Field(default=[], title="Fiber photometry devices")


class LaserConfig(AindModel):
    """Description of laser settings in a session"""

    device_type: Literal["Laser"] = "Laser"
    name: str = Field(..., title="Name", description="Must match rig json")
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


LIGHT_SOURCE_CONFIGS = Annotated[
    Union[LightEmittingDiodeConfig, LaserConfig],
    Field(discriminator="device_type"),
]


# Behavior components
class RewardSolution(str, Enum):
    """Reward solution name"""

    WATER = "Water"
    OTHER = "Other"


class RewardSpoutConfig(AindModel):
    """Reward spout session information"""

    side: SpoutSide = Field(..., title="Spout side", description="Must match rig")
    starting_position: RelativePosition = Field(..., title="Starting position")
    variable_position: bool = Field(
        ...,
        title="Variable position",
        description="True if spout position changes during session as tracked in data",
    )


class RewardDeliveryConfig(AindModel):
    """Description of reward delivery configuration"""

    reward_solution: RewardSolution = Field(..., title="Reward solution", description="If Other use notes")
    reward_spouts: List[RewardSpoutConfig] = Field(..., title="Reward spouts")
    notes: Optional[str] = Field(None, title="Notes", validate_default=True)

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("reward_solution") == RewardSolution.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if reward_solution is Other. Describe the reward_solution in the notes field."
            )
        return value


class SpeakerConfig(AindModel):
    """Description of auditory speaker configuration"""

    name: str = Field(..., title="Name", description="Must match rig json")
    volume: Optional[Decimal] = Field(None, title="Volume (dB)")
    volume_unit: SoundIntensityUnit = Field(SoundIntensityUnit.DB, title="Volume unit")


class Stream(AindModel):
    """Data streams with a start and stop time"""

    stream_start_time: AwareDatetimeWithDefault = Field(..., title="Stream start time")
    stream_end_time: AwareDatetimeWithDefault = Field(..., title="Stream stop time")
    daq_names: List[str] = Field(default=[], title="DAQ devices")
    camera_names: List[str] = Field(default=[], title="Cameras")
    light_sources: List[LIGHT_SOURCE_CONFIGS] = Field(default=[], title="Light Sources")
    ephys_modules: List[EphysModule] = Field(default=[], title="Ephys modules")
    stick_microscopes: List[DomeModule] = Field(
        default=[],
        title="Stick microscopes",
        description="Must match stick microscope assemblies in rig file",
    )
    manipulator_modules: List[ManipulatorModule] = Field(default=[], title="Manipulator modules")
    detectors: List[DetectorConfig] = Field(default=[], title="Detectors")
    fiber_connections: List[FiberConnectionConfig] = Field(default=[], title="Implanted fiber photometry devices")
    fiber_modules: List[FiberModule] = Field(default=[], title="Inserted fiber modules")
    ophys_fovs: List[FieldOfView] = Field(default=[], title="Fields of view")
    slap_fovs: Optional[SlapFieldOfView] = Field(None, title="Slap2 field of view")
    stack_parameters: Optional[Stack] = Field(None, title="Stack parameters")
    stream_modalities: List[Modality.ONE_OF] = Field(..., title="Modalities")
    notes: Optional[str] = Field(None, title="Notes")

    @staticmethod
    def _validate_ephys_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate ecephys modality has ephys_assemblies and stick_microscopes"""
        if Modality.ECEPHYS in value:
            ephys_modules = info.data["ephys_modules"]
            for k, v in {
                "ephys_modules": ephys_modules,
            }.items():
                if not v:
                    return f"{k} field must be utilized for Ecephys modality"
        return None

    @staticmethod
    def _validate_fib_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate FIB modality has light_sources, detectors, and fiber_connections"""
        if Modality.FIB in value:
            light_source = info.data["light_sources"]
            detector = info.data["detectors"]
            fiber_connections = info.data["fiber_connections"]
            for k, v in {
                "light_sources": light_source,
                "detectors": detector,
                "fiber_connections": fiber_connections,
            }.items():
                if not v:
                    return f"{k} field must be utilized for FIB modality"
        return None

    @staticmethod
    def _validate_pophys_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate POPHYS modality has ophys_fovs and stack_parameters"""
        if Modality.POPHYS in value:
            ophys_fovs = info.data["ophys_fovs"]
            stack_parameters = info.data["stack_parameters"]
            if not ophys_fovs and not stack_parameters:
                return "ophys_fovs field OR stack_parameters field must be utilized for Pophys modality"
        else:
            return None

    @staticmethod
    def _validate_behavior_videos_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate BEHAVIOR_VIDEOS modality has cameras"""
        if Modality.BEHAVIOR_VIDEOS in value and len(info.data["camera_names"]) == 0:
            return "camera_names field must be utilized for Behavior Videos modality"
        else:
            return None

    @field_validator("stream_modalities", mode="after")
    def validate_stream_modalities(cls, value: List[Modality.ONE_OF], info: ValidationInfo) -> List[Modality.ONE_OF]:
        """Validate each modality in stream_modalities field has associated data"""
        errors = []
        ephys_errors = cls._validate_ephys_modality(value, info)
        fib_errors = cls._validate_fib_modality(value, info)
        pophys_errors = cls._validate_pophys_modality(value, info)
        behavior_vids_errors = cls._validate_behavior_videos_modality(value, info)

        if ephys_errors is not None:
            errors.append(ephys_errors)
        if fib_errors is not None:
            errors.append(fib_errors)
        if pophys_errors is not None:
            errors.append(pophys_errors)
        if behavior_vids_errors is not None:
            errors.append(behavior_vids_errors)
        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)
        return value


class StimulusEpoch(AindModel):
    """Description of stimulus used during session"""

    stimulus_start_time: datetime = Field(
        ...,
        title="Stimulus start time",
        description="When a specific stimulus begins. This might be the same as the session start time.",
    )
    stimulus_end_time: datetime = Field(
        ...,
        title="Stimulus end time",
        description="When a specific stimulus ends. This might be the same as the session end time.",
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    session_number: Optional[int] = Field(None, title="Session number")
    software: Optional[List[Software]] = Field(
        default=[],
        title="Software",
        description="The software used to control the behavior/stimulus (e.g. Bonsai)",
    )
    script: Optional[Software] = Field(
        None,
        title="Script",
        description="provide URL to the commit of the script and the parameters used",
    )
    stimulus_modalities: List[StimulusModality] = Field(..., title="Stimulus modalities")
    stimulus_parameters: Optional[
        List[
            Annotated[
                Union[AuditoryStimulation, OptoStimulation, OlfactoryStimulation, PhotoStimulation, VisualStimulation],
                Field(discriminator="stimulus_type"),
            ]
        ]
    ] = Field(None, title="Stimulus parameters")
    stimulus_device_names: List[str] = Field(default=[], title="Stimulus devices")
    speaker_config: Optional[SpeakerConfig] = Field(None, title="Speaker Config")
    light_source_config: Optional[LIGHT_SOURCE_CONFIGS] = Field(None, title="Light source config")
    output_parameters: AindGenericType = Field(AindGeneric(), title="Performance metrics")
    reward_consumed_during_epoch: Optional[Decimal] = Field(None, title="Reward consumed during training (uL)")
    reward_consumed_unit: VolumeUnit = Field(VolumeUnit.UL, title="Reward consumed unit")
    trials_total: Optional[int] = Field(None, title="Total trials")
    trials_finished: Optional[int] = Field(None, title="Finished trials")
    trials_rewarded: Optional[int] = Field(None, title="Rewarded trials")
    notes: Optional[str] = Field(None, title="Notes")


class Session(AindCoreModel):
    """Description of a physiology and/or behavior session"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/session.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.2.2"] = Field("0.2.2")
    protocol_id: List[str] = Field([], title="Protocol ID", description="DOI for protocols.io")
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    session_start_time: AwareDatetimeWithDefault = Field(..., title="Session start time")
    session_end_time: Optional[AwareDatetimeWithDefault] = Field(None, title="Session end time")
    session_type: str = Field(..., title="Session type")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    calibrations: List[Calibration] = Field(
        default=[],
        title="Calibrations",
        description="Calibrations of rig devices prior to session",
    )
    maintenance: List[Maintenance] = Field(
        default=[],
        title="Maintenance",
        description="Maintenance of rig devices prior to session",
    )
    subject_id: str = Field(..., title="Subject ID")
    animal_weight_prior: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
    )
    animal_weight_post: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
    )
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
    )
    stimulus_epochs: List[StimulusEpoch] = Field(default=[], title="Stimulus")
    mouse_platform_name: str = Field(..., title="Mouse platform")
    active_mouse_platform: bool = Field(
        ..., title="Active mouse platform", description="Is the mouse platform being actively controlled"
    )
    reward_delivery: Optional[RewardDeliveryConfig] = Field(None, title="Reward delivery")
    reward_consumed_total: Optional[Decimal] = Field(None, title="Total reward consumed (uL)")
    reward_consumed_unit: VolumeUnit = Field(VolumeUnit.UL, title="Reward consumed unit")
    notes: Optional[str] = Field(None, title="Notes")
