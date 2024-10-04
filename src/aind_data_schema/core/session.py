""" Schemas for Physiology and/or Behavior Sessions """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import (
    AngleUnit,
    FrequencyUnit,
    MassUnit,
    PowerUnit,
    SizeUnit,
    SoundIntensityUnit,
    TimeUnit,
    VolumeUnit,
)
from pydantic import Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated

from aind_data_schema.base import AindCoreModel, AindGeneric, AindGenericType, AindModel, AwareDatetimeWithDefault
from aind_data_schema.components.coordinates import (
    Affine3dTransform,
    CcfCoords,
    Coordinates3d,
    Rotation3dTransform,
    Scale3dTransform,
    Translation3dTransform,
)
from aind_data_schema.components.devices import Calibration, Maintenance, RelativePosition, Scanner, Software, SpoutSide
from aind_data_schema.components.stimulus import (
    AuditoryStimulation,
    OlfactoryStimulation,
    OptoStimulation,
    PhotoStimulation,
    VisualStimulation,
)
from aind_data_schema.components.tile import Channel
from aind_data_schema.core.procedures import Anaesthetic, CoordinateReferenceLocation


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
    output_power_unit: PowerUnit = Field(default=PowerUnit.UW, title="Output power unit")
    fiber_name: str = Field(..., title="Fiber name (must match procedure)")


class TriggerType(str, Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class DetectorConfig(AindModel):
    """Description of detector settings"""

    name: str = Field(..., title="Name")
    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(default=TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")


class LightEmittingDiodeConfig(AindModel):
    """Description of LED settings"""

    device_type: Literal["Light emitting diode"] = "Light emitting diode"
    name: str = Field(..., title="Name")
    excitation_power: Optional[Decimal] = Field(default=None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(default=PowerUnit.MW, title="Excitation power unit")


class FieldOfView(AindModel):
    """Description of an imaging field of view"""

    index: int = Field(..., title="Index")
    imaging_depth: int = Field(..., title="Imaging depth (um)")
    imaging_depth_unit: SizeUnit = Field(default=SizeUnit.UM, title="Imaging depth unit")
    targeted_structure: str = Field(..., title="Targeted structure")
    fov_coordinate_ml: Decimal = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: Decimal = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(default=SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(
        ...,
        title="FOV reference",
        description="Reference for ML/AP coordinates",
    )
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(default=SizeUnit.PX, title="FOV size unit")
    magnification: str = Field(..., title="Magnification")
    fov_scale_factor: Decimal = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field(default="um/pixel", title="FOV scale factor unit")
    frame_rate: Optional[Decimal] = Field(default=None, title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(default=FrequencyUnit.HZ, title="Frame rate unit")
    coupled_fov_index: Optional[int] = Field(
        default=None, title="Coupled FOV", description="Coupled planes for multiscope"
    )
    power: Optional[Decimal] = Field(
        default=None, title="Power", description="For coupled planes, this power is shared by both planes"
    )
    power_unit: PowerUnit = Field(default=PowerUnit.PERCENT, title="Power unit")
    power_ratio: Optional[Decimal] = Field(default=None, title="Power ratio for coupled planes")
    scanfield_z: Optional[int] = Field(
        default=None,
        title="Z stage position of the fastz actuator for a given targeted depth",
    )
    scanfield_z_unit: SizeUnit = Field(default=SizeUnit.UM, title="Z stage position unit")
    scanimage_roi_index: Optional[int] = Field(default=None, title="ScanImage ROI index")
    notes: Optional[str] = Field(default=None, title="Notes")


class StackChannel(Channel):
    """Description of a Channel used in a Stack"""

    start_depth: int = Field(..., title="Starting depth (um)")
    end_depth: int = Field(..., title="Ending depth (um)")
    depth_unit: SizeUnit = Field(default=SizeUnit.UM, title="Depth unit")


class Stack(AindModel):
    """Description of a two photon stack"""

    channels: List[StackChannel] = Field(..., title="Channels")
    number_of_planes: int = Field(..., title="Number of planes")
    step_size: float = Field(..., title="Step size (um)")
    step_size_unit: SizeUnit = Field(default=SizeUnit.UM, title="Step size unit")
    number_of_plane_repeats_per_volume: int = Field(..., title="Number of repeats per volume")
    number_of_volume_repeats: int = Field(..., title="Number of volume repeats")
    fov_coordinate_ml: float = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: float = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(default=SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(
        ...,
        title="FOV reference",
        description="Reference for ML/AP coordinates",
    )
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(default=SizeUnit.PX, title="FOV size unit")
    magnification: Optional[str] = Field(default=None, title="Magnification")
    fov_scale_factor: float = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field(default="um/pixel", title="FOV scale factor unit")
    frame_rate: Decimal = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(default=FrequencyUnit.HZ, title="Frame rate unit")
    targeted_structure: Optional[str] = Field(default=None, title="Targeted structure")


class SlapSessionType(str, Enum):
    """Type of slap session"""

    PARENT = "Parent"
    BRANCH = "Branch"


class SlapFieldOfView(FieldOfView):
    """Description of a Slap2 scan"""

    session_type: SlapSessionType = Field(..., title="Session type")
    dmd_dilation_x: int = Field(..., title="DMD Dilation X (pixels)")
    dmd_dilation_y: int = Field(..., title="DMD Dilation Y (pixels)")
    dilation_unit: SizeUnit = Field(default=SizeUnit.PX, title="Dilation unit")
    target_neuron: Optional[str] = Field(default=None, title="Target neuron")
    target_branch: Optional[str] = Field(default=None, title="Target branch")
    path_to_array_of_frame_rates: str = Field(..., title="Array of frame rates")


# Ephys Components
class DomeModule(AindModel):
    """Movable module that is mounted on the ephys dome insertion system"""

    assembly_name: str = Field(..., title="Assembly name")
    arc_angle: Decimal = Field(..., title="Arc Angle (deg)")
    module_angle: Decimal = Field(..., title="Module Angle (deg)")
    angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
    rotation_angle: Optional[Decimal] = Field(default=None, title="Rotation Angle (deg)")
    coordinate_transform: Optional[str] = Field(
        default=None,
        title="Transform from local manipulator axes to rig",
        description="Path to coordinate transform",
    )
    calibration_date: Optional[datetime] = Field(
        default=None, title="Date on which coordinate transform was last calibrated"
    )
    notes: Optional[str] = Field(default=None, title="Notes")


class ManipulatorModule(DomeModule):
    """A dome module connected to a 3-axis manipulator"""

    primary_targeted_structure: str = Field(..., title="Targeted structure")
    other_targeted_structure: Optional[List[str]] = Field(default=None, title="Other targeted structure")
    targeted_ccf_coordinates: List[CcfCoords] = Field(
        default=[],
        title="Targeted CCF coordinates",
    )
    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )
    anatomical_coordinates: Optional[Coordinates3d] = Field(default=None, title="Anatomical coordinates")
    anatomical_reference: Optional[Literal[CoordinateReferenceLocation.BREGMA, CoordinateReferenceLocation.LAMBDA]] = (
        Field(default=None, title="Anatomical coordinate reference")
    )
    surface_z: Optional[Decimal] = Field(default=None, title="Surface z")
    surface_z_unit: SizeUnit = Field(default=SizeUnit.UM, title="Surface z unit")
    dye: Optional[str] = Field(default=None, title="Dye")
    implant_hole_number: Optional[int] = Field(default=None, title="Implant hole number")


class FiberModule(ManipulatorModule):
    """Inserted fiber photometry probe recorded in a stream"""

    fiber_connections: List[FiberConnectionConfig] = Field(default=[], title="Fiber photometry devices")


class LaserConfig(AindModel):
    """Description of laser settings in a session"""

    device_type: Literal["Laser"] = "Laser"
    name: str = Field(..., title="Name", description="Must match rig json")
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[Decimal] = Field(default=None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(default=PowerUnit.MW, title="Excitation power unit")


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
    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)

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
    volume: Optional[Decimal] = Field(default=None, title="Volume (dB)")
    volume_unit: SoundIntensityUnit = Field(default=SoundIntensityUnit.DB, title="Volume unit")


# MRI components
class MriScanSequence(str, Enum):
    """MRI scan sequence"""

    RARE = "RARE"
    OTHER = "Other"


class ScanType(str, Enum):
    """Type of scan"""

    SETUP = "Set Up"
    SCAN_3D = "3D Scan"


class SubjectPosition(str, Enum):
    """Subject position"""

    PRONE = "Prone"
    SUPINE = "Supine"


class MRIScan(AindModel):
    """Description of a 3D scan"""

    scan_index: int = Field(..., title="Scan index")
    scan_type: ScanType = Field(..., title="Scan type")
    primary_scan: bool = Field(
        ..., title="Primary scan", description="Indicates the primary scan used for downstream analysis"
    )
    mri_scanner: Optional[Scanner] = Field(default=None, title="MRI scanner")
    scan_sequence_type: MriScanSequence = Field(..., title="Scan sequence")
    rare_factor: Optional[int] = Field(default=None, title="RARE factor")
    echo_time: Decimal = Field(..., title="Echo time (ms)")
    effective_echo_time: Optional[Decimal] = Field(default=None, title="Effective echo time (ms)")
    echo_time_unit: TimeUnit = Field(default=TimeUnit.MS, title="Echo time unit")
    repetition_time: Decimal = Field(..., title="Repetition time (ms)")
    repetition_time_unit: TimeUnit = Field(default=TimeUnit.MS, title="Repetition time unit")
    # fields required to get correct orientation
    vc_orientation: Optional[Rotation3dTransform] = Field(default=None, title="Scan orientation")
    vc_position: Optional[Translation3dTransform] = Field(default=None, title="Scan position")
    subject_position: SubjectPosition = Field(..., title="Subject position")
    # other fields
    voxel_sizes: Optional[Scale3dTransform] = Field(default=None, title="Voxel sizes", description="Resolution")
    processing_steps: List[
        Literal[
            ProcessName.FIDUCIAL_SEGMENTATION,
            ProcessName.IMAGE_ATLAS_ALIGNMENT,
            ProcessName.SKULL_STRIPPING,
        ]
    ] = Field([])
    additional_scan_parameters: AindGenericType = Field(..., title="Parameters")
    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("scan_sequence_type") == MriScanSequence.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if scan_sequence_type is Other."
                " Describe the scan_sequence_type in the notes field."
            )
        return value

    @model_validator(mode="after")
    def validate_primary_scan(self):
        """Validate that primary scan has vc_orientation and vc_position fields"""

        if self.primary_scan:
            if not self.vc_orientation or not self.vc_position or not self.voxel_sizes:
                raise ValueError("Primary scan must have vc_orientation, vc_position, and voxel_sizes fields")

        return self


class Stream(AindModel):
    """Data streams with a start and stop time"""

    stream_start_time: AwareDatetimeWithDefault = Field(..., title="Stream start time")
    stream_end_time: AwareDatetimeWithDefault = Field(..., title="Stream stop time")
    daq_names: List[str] = Field(default=[], title="DAQ devices")
    camera_names: List[str] = Field(default=[], title="Cameras")
    light_sources: List[LIGHT_SOURCE_CONFIGS] = Field(default=[], title="Light Sources")
    ephys_modules: List[ManipulatorModule] = Field(default=[], title="Ephys modules")
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
    slap_fovs: List[SlapFieldOfView] = Field(default=[], title="Slap2 fields of view")
    stack_parameters: Optional[Stack] = Field(default=None, title="Stack parameters")
    mri_scans: List[MRIScan] = Field(default=[], title="MRI scans")
    stream_modalities: List[Modality.ONE_OF] = Field(..., title="Modalities")
    software: Optional[List[Software]] = Field(default=[], title="Data stream software information")
    notes: Optional[str] = Field(default=None, title="Notes")

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

    @staticmethod
    def _validate_mri_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate MRI modality has scans"""
        if Modality.MRI in value:
            scans = info.data["mri_scans"]
            if not scans:
                return "mri_scans field must be utilized for MRI modality"
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
        mri_errors = cls._validate_mri_modality(value, info)

        if ephys_errors is not None:
            errors.append(ephys_errors)
        if fib_errors is not None:
            errors.append(fib_errors)
        if pophys_errors is not None:
            errors.append(pophys_errors)
        if behavior_vids_errors is not None:
            errors.append(behavior_vids_errors)
        if mri_errors is not None:
            errors.append(mri_errors)
        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)
        return value


class StimulusEpoch(AindModel):
    """Description of stimulus used during session"""

    stimulus_start_time: AwareDatetimeWithDefault = Field(
        ...,
        title="Stimulus start time",
        description="When a specific stimulus begins. This might be the same as the session start time.",
    )
    stimulus_end_time: AwareDatetimeWithDefault = Field(
        ...,
        title="Stimulus end time",
        description="When a specific stimulus ends. This might be the same as the session end time.",
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    session_number: Optional[int] = Field(default=None, title="Session number")
    software: Optional[List[Software]] = Field(
        default=[],
        title="Software",
        description="The software used to control the behavior/stimulus (e.g. Bonsai)",
    )
    script: Optional[Software] = Field(
        default=None,
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
    ] = Field(default=None, title="Stimulus parameters")
    stimulus_device_names: List[str] = Field(default=[], title="Stimulus devices")
    speaker_config: Optional[SpeakerConfig] = Field(default=None, title="Speaker Config")
    light_source_config: Optional[List[LIGHT_SOURCE_CONFIGS]] = Field(
        default=[], title="Light source config", description="Light sources for stimulation"
    )
    output_parameters: AindGenericType = Field(default=AindGeneric(), title="Performance metrics")
    reward_consumed_during_epoch: Optional[Decimal] = Field(default=None, title="Reward consumed during training (uL)")
    reward_consumed_unit: VolumeUnit = Field(default=VolumeUnit.UL, title="Reward consumed unit")
    trials_total: Optional[int] = Field(default=None, title="Total trials")
    trials_finished: Optional[int] = Field(default=None, title="Finished trials")
    trials_rewarded: Optional[int] = Field(default=None, title="Rewarded trials")
    notes: Optional[str] = Field(default=None, title="Notes")


class Session(AindCoreModel):
    """Description of a physiology and/or behavior session"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/session.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.1"] = Field("1.0.1")
    protocol_id: List[str] = Field(default=[], title="Protocol ID", description="DOI for protocols.io")
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    session_start_time: AwareDatetimeWithDefault = Field(..., title="Session start time")
    session_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Session end time")
    session_type: str = Field(..., title="Session type")
    iacuc_protocol: Optional[str] = Field(default=None, title="IACUC protocol")
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
        default=None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
    )
    animal_weight_post: Optional[Decimal] = Field(
        default=None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
    )
    weight_unit: MassUnit = Field(default=MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(default=None, title="Anaesthesia")
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
    headframe_registration: Optional[Affine3dTransform] = Field(
        default=None, title="Headframe registration", description="MRI transform matrix for headframe"
    )
    reward_delivery: Optional[RewardDeliveryConfig] = Field(default=None, title="Reward delivery")
    reward_consumed_total: Optional[Decimal] = Field(default=None, title="Total reward consumed (mL)")
    reward_consumed_unit: VolumeUnit = Field(default=VolumeUnit.ML, title="Reward consumed unit")
    notes: Optional[str] = Field(default=None, title="Notes")
