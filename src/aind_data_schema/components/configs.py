""" Configurations for devices, software, and other components during acquisition """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import (
    AngleUnit,
    FrequencyUnit,
    PowerUnit,
    SizeUnit,
    SoundIntensityUnit,
    TimeUnit,
)

from aind_data_schema.components.devices import ImmersionMedium
from aind_data_schema.components.tile import AcquisitionTile
from aind_data_schema.components.coordinates import ImageAxis, AnatomicalDirection, AxisName, CcfCoords
from aind_data_schema_models.brain_atlas import CCFStructure
from pydantic import Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from aind_data_schema.base import (
    GenericModelType,
    DataModel,
)
from aind_data_schema.components.coordinates import (
    Coordinates3d,
    Rotation3dTransform,
    Scale3dTransform,
    Translation3dTransform,
)
from aind_data_schema.components.devices import RelativePosition, SpoutSide
from aind_data_schema.components.tile import Channel
from aind_data_schema.core.procedures import CoordinateReferenceLocation


class StimulusModality(str, Enum):
    """Types of stimulus modalities"""

    AUDITORY = "Auditory"
    FREE_MOVING = "Free moving"
    OLFACTORY = "Olfactory"
    OPTOGENETICS = "Optogenetics"
    NONE = "None"
    VIRTUAL_REALITY = "Virtual reality"
    VISUAL = "Visual"
    WHEEL_FRICTION = "Wheel friction"


class DeviceConfig(DataModel):
    """Parent class for all configurations"""

    device_name: str = Field(..., title="Device name", description="Must match a device defined in the instrument.json")


# Ophys components
class PatchCordConfig(DeviceConfig):
    """Description of a patch cord and its output power to another device"""

    output_power: Decimal = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(default=PowerUnit.UW, title="Output power unit")


class TriggerType(str, Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class DetectorConfig(DeviceConfig):
    """Description of detector settings"""

    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(default=TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")


class LightEmittingDiodeConfig(DeviceConfig):
    """Description of LED settings"""

    excitation_power: Optional[Decimal] = Field(default=None, title="Excitation power (mW)")
    excitation_power_unit: Optional[PowerUnit] = Field(default=None, title="Excitation power unit")


class FieldOfView(DataModel):
    """Description of an imaging field of view"""

    index: int = Field(..., title="Index")
    imaging_depth: int = Field(..., title="Imaging depth (um)")
    imaging_depth_unit: SizeUnit = Field(default=SizeUnit.UM, title="Imaging depth unit")
    targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")
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
    frame_rate_unit: Optional[FrequencyUnit] = Field(default=None, title="Frame rate unit")
    coupled_fov_index: Optional[int] = Field(
        default=None, title="Coupled FOV", description="Coupled planes for multiscope"
    )
    power: Optional[Decimal] = Field(
        default=None, title="Power", description="For coupled planes, this power is shared by both planes"
    )
    power_unit: Optional[PowerUnit] = Field(default=None, title="Power unit")
    power_ratio: Optional[Decimal] = Field(default=None, title="Power ratio for coupled planes")
    scanfield_z: Optional[int] = Field(
        default=None,
        title="Z stage position of the fastz actuator for a given targeted depth",
    )
    scanfield_z_unit: Optional[SizeUnit] = Field(default=None, title="Z stage position unit")
    scanimage_roi_index: Optional[int] = Field(default=None, title="ScanImage ROI index")
    notes: Optional[str] = Field(default=None, title="Notes")


class StackChannel(Channel):
    """Description of a Channel used in a Stack"""

    start_depth: int = Field(..., title="Starting depth (um)")
    end_depth: int = Field(..., title="Ending depth (um)")
    depth_unit: SizeUnit = Field(default=SizeUnit.UM, title="Depth unit")


class Stack(DataModel):
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
    targeted_structure: Optional[CCFStructure.ONE_OF] = Field(default=None, title="Targeted structure")


class SlapAcquisitionType(str, Enum):
    """Type of slap acquisition"""

    PARENT = "Parent"
    BRANCH = "Branch"


class SlapFieldOfView(FieldOfView):
    """Description of a Slap2 scan"""

    experiment_type: SlapAcquisitionType = Field(..., title="Acquisition type")
    dmd_dilation_x: int = Field(..., title="DMD Dilation X (pixels)")
    dmd_dilation_y: int = Field(..., title="DMD Dilation Y (pixels)")
    dilation_unit: SizeUnit = Field(default=SizeUnit.PX, title="Dilation unit")
    target_neuron: Optional[str] = Field(default=None, title="Target neuron")
    target_branch: Optional[str] = Field(default=None, title="Target branch")
    path_to_array_of_frame_rates: str = Field(..., title="Array of frame rates")


class MousePlatformConfig(DeviceConfig):
    """Configuration for mouse platforms"""

    objects_in_arena: Optional[List[str]] = Field(default=None, title="Objects in area")
    active_control: bool = Field(
        default=False,
        title="Active control",
        description="True when movement of the mouse platform is in any way controlled by the experimenter",
    )


# Ephys Components
class DomeModule(DeviceConfig):
    """Movable module that is mounted on the ephys dome insertion system"""

    arc_angle: Decimal = Field(..., title="Arc Angle (deg)")
    module_angle: Decimal = Field(..., title="Module Angle (deg)")
    angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
    rotation_angle: Optional[Decimal] = Field(default=None, title="Rotation Angle (deg)")
    coordinate_transform: Optional[str] = Field(
        default=None,
        title="Transform from local manipulator axes to instrument",
        description="Path to coordinate transform",
    )
    calibration_date: Optional[datetime] = Field(
        default=None, title="Date on which coordinate transform was last calibrated"
    )
    notes: Optional[str] = Field(default=None, title="Notes")


class ManipulatorModule(DomeModule):
    """A dome module connected to a 3-axis manipulator"""

    primary_targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")
    other_targeted_structure: Optional[List[CCFStructure.ONE_OF]] = Field(
        default=None, title="Other targeted structure"
    )
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
    surface_z_unit: Optional[SizeUnit] = Field(default=None, title="Surface z unit")
    dye: Optional[str] = Field(default=None, title="Dye")
    implant_hole_number: Optional[int] = Field(default=None, title="Implant hole number")


class FiberAssemblyConfig(ManipulatorModule):
    """Inserted fiber photometry probe recorded in a stream"""

    fiber_connections: List[PatchCordConfig] = Field(default=[], title="Fiber photometry devices")


class LaserConfig(DeviceConfig):
    """Description of laser settings in an acquisition"""

    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[Decimal] = Field(default=None, title="Excitation power (mW)")
    excitation_power_unit: Optional[PowerUnit] = Field(default=None, title="Excitation power unit")


# Behavior components
class RewardSolution(str, Enum):
    """Reward solution name"""

    WATER = "Water"
    OTHER = "Other"


class RewardSpoutConfig(DataModel):
    """Reward spout acquisition information"""

    side: SpoutSide = Field(..., title="Spout side", description="Must match instrument")
    starting_position: RelativePosition = Field(..., title="Starting position")
    variable_position: bool = Field(
        ...,
        title="Variable position",
        description="True if spout position changes during acquisition as tracked in data",
    )


class RewardDeliveryConfig(DataModel):
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


class SpeakerConfig(DeviceConfig):
    """Description of auditory speaker configuration"""

    volume: Optional[Decimal] = Field(default=None, title="Volume (dB)")
    volume_unit: Optional[SoundIntensityUnit] = Field(default=None, title="Volume unit")


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


class MRIScan(DeviceConfig):
    """Description of a 3D scan"""

    scan_index: int = Field(..., title="Scan index")
    scan_type: ScanType = Field(..., title="Scan type")
    primary_scan: bool = Field(
        ..., title="Primary scan", description="Indicates the primary scan used for downstream analysis"
    )
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
    additional_scan_parameters: GenericModelType = Field(..., title="Parameters")
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


class Immersion(DataModel):
    """Description of immersion medium"""

    medium: ImmersionMedium = Field(..., title="Immersion medium")
    refractive_index: Decimal = Field(..., title="Index of refraction")


class ProcessingSteps(DataModel):
    """Description of downstream processing steps"""

    channel_name: str = Field(..., title="Channel name")
    process_name: List[
        Literal[
            ProcessName.IMAGE_ATLAS_ALIGNMENT,
            ProcessName.IMAGE_BACKGROUND_SUBTRACTION,
            ProcessName.IMAGE_CELL_SEGMENTATION,
            ProcessName.IMAGE_DESTRIPING,
            ProcessName.IMAGE_FLAT_FIELD_CORRECTION,
            ProcessName.IMAGE_IMPORTING,
            ProcessName.IMAGE_THRESHOLDING,
            ProcessName.IMAGE_TILE_ALIGNMENT,
            ProcessName.IMAGE_TILE_FUSING,
            ProcessName.IMAGE_TILE_PROJECTION,
            ProcessName.FILE_FORMAT_CONVERSION,
        ]
    ] = Field(...)


class InVitroImagingConfig(DataModel):
    """Configuration of an imaging instrument"""

    tiles: List[AcquisitionTile] = Field(..., title="Acquisition tiles")
    axes: List[ImageAxis] = Field(..., title="Acquisition axes")
    chamber_immersion: Immersion = Field(..., title="Acquisition chamber immersion data")
    sample_immersion: Optional[Immersion] = Field(default=None, title="Acquisition sample immersion data")
    processing_steps: List[ProcessingSteps] = Field(
        default=[],
        title="Processing steps",
        description="List of downstream processing steps planned for each channel",
    )

    @field_validator("axes", mode="before")
    def from_direction_code(cls, v: Union[str, List[ImageAxis]]) -> List[ImageAxis]:
        """Map direction codes to Axis model"""
        if type(v) is str:
            direction_lookup = {
                "L": AnatomicalDirection.LR,
                "R": AnatomicalDirection.RL,
                "A": AnatomicalDirection.AP,
                "P": AnatomicalDirection.PA,
                "I": AnatomicalDirection.IS,
                "S": AnatomicalDirection.SI,
            }

            name_lookup = [AxisName.X, AxisName.Y, AxisName.Z]

            axes = []
            for i, c in enumerate(v):
                axis = ImageAxis(name=name_lookup[i], direction=direction_lookup[c], dimension=i)
                axes.append(axis)
            return axes
        else:
            return v
