""" Configurations for devices, software, and other components during acquisition """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, List, Literal, Optional, Union

from aind_data_schema_models.brain_atlas import CCFStructure
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.devices import ImmersionMedium
from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import (
    AngleUnit,
    FrequencyUnit,
    PowerUnit,
    PressureUnit,
    SizeUnit,
    SoundIntensityUnit,
    TimeUnit,
)
from pydantic import Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel, GenericModelType
from aind_data_schema.components.coordinates import Coordinate, CoordinateSystem, Scale, Transform, CoordinateTransform
from aind_data_schema.components.identifiers import Code
from aind_data_schema.components.wrappers import AssetPath


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


class Valence(str, Enum):
    """Valence of a stimulus"""

    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    UNKNOWN = "Unknown"


class SlapAcquisitionType(str, Enum):
    """Type of slap acquisition"""

    PARENT = "Parent"
    BRANCH = "Branch"


class DeviceConfig(DataModel):
    """Parent class for all configurations"""

    device_name: str = Field(..., title="Device name", description="Must match a device defined in the instrument.json")


class TriggerType(str, Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class DetectorConfig(DeviceConfig):
    """Configuration of detector settings"""

    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(default=TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")

    compression: Optional[Code] = Field(
        default=None,
        title="Compression",
        description="Compression algorithm used during acquisition",
    )


class LaserConfig(DeviceConfig):
    """Configuration of laser settings in an acquisition"""

    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    power: Optional[Decimal] = Field(default=None, title="Excitation power (mW)")
    power_unit: Optional[PowerUnit] = Field(default=None, title="Excitation power unit")


class LightEmittingDiodeConfig(DeviceConfig):
    """Configuration of LED settings"""

    power: Optional[Decimal] = Field(default=None, title="Excitation power (mW)")
    power_unit: Optional[PowerUnit] = Field(default=None, title="Excitation power unit")


class MicroscopeConfig(DeviceConfig):
    """Configuration of a generic microscope"""

    magnification: Optional[str] = Field(default=None, title="Magnification", description="e.g. 10x")


class SlapMicroscopeConfig(MicroscopeConfig):
    """Configuration of a Slap microscope"""

    slap_acquisition_type: SlapAcquisitionType = Field(..., title="Slap experiment type")
    target_type: SlapAcquisitionType = Field(..., title="Target type")
    target_neuron: Optional[str] = Field(default=None, title="Target neuron")
    target_branch: Optional[str] = Field(default=None, title="Target branch")
    path_to_array_of_frame_rates: AssetPath = Field(
        ..., title="Array of frame rates", description="Relative path from metadata json to file"
    )

    dilation: Optional[int] = Field(default=None, title="Dilation")
    dilation_unit: Optional[SizeUnit] = Field(default=None, title="Dilation unit")


class Channel(DataModel):
    """Configuration of a channel"""

    channel_name: str = Field(..., title="Channel")
    intended_measurement: Optional[str] = Field(
        default=None, title="Intended measurement", description="What signal is this channel measuring"
    )
    detector: DetectorConfig = Field(..., title="Detector configuration")
    additional_device_names: Optional[List[DeviceConfig]] = Field(
        default=None, title="Additional device names", description="Mirrors, dichroics, etc"
    )

    # excitation
    light_sources: List[
        Annotated[
            Union[
                LaserConfig,
                LightEmittingDiodeConfig,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(default=[], title="Light source configurations")
    excitation_filters: Optional[List[DeviceConfig]] = Field(default=None, title="Excitation filters")
    # emission
    emission_filters: Optional[List[DeviceConfig]] = Field(default=None, title="Emission filter names")
    emission_wavelength: Optional[int] = Field(default=None, title="Emission wavelength")
    emission_wavelength_unit: Optional[SizeUnit] = Field(default=None, title="Emission wavelength unit")


class SlapChannel(Channel):
    """Configuration of a channel for Slap"""

    description: Optional[str] = Field(default=None, title="Description")


class PatchCordConfig(DeviceConfig):
    """Configuration of a patch cord and its output power to another device"""

    channels: List[Channel] = Field(..., title="Channels")


class SinglePlaneConfig(DataModel):
    """Configuration of a single plane ophys config"""

    imaging_depth: int = Field(..., title="Imaging depth (um)")
    imaging_depth_unit: SizeUnit = Field(default=SizeUnit.UM, title="Imaging depth unit")


class MultiPlaneConfig(SinglePlaneConfig):
    """Configuration of a single multi-plane FOV"""

    index: int = Field(..., title="Index")
    coupled_plane_index: Optional[int] = Field(
        default=None, title="Coupled plane index", description="Coupled planes for multiscope"
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


class StackConfig(DataModel):
    """Configuration of a two photon stack"""

    start_depth: int = Field(..., title="Starting depth (um)")
    end_depth: int = Field(..., title="Ending depth (um)")
    depth_unit: SizeUnit = Field(default=SizeUnit.UM, title="Depth unit")
    number_of_planes: int = Field(..., title="Number of planes")
    step_size: float = Field(..., title="Step size (um)")
    step_size_unit: SizeUnit = Field(default=SizeUnit.UM, title="Step size unit")
    number_of_plane_repeats_per_volume: int = Field(..., title="Number of repeats per volume")
    number_of_volume_repeats: int = Field(..., title="Number of volume repeats")


class FieldOfView(DataModel):
    """Configuration of an imaging field of view"""

    channel_name: str = Field(..., title="Channel name")
    targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")
    center_coordinate: Optional[Coordinate] = Field(
        default=None,
        title="FOV coordinate",
        description="Center point of the FOV in the instrument coordinate system",
    )
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(default=SizeUnit.PX, title="FOV size unit")
    fov_scale_factor: Decimal = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field(default="um/pixel", title="FOV scale factor unit")
    frame_rate: Decimal = Field(default=..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(default=FrequencyUnit.HZ, title="Frame rate unit")
    planes: List[
        Annotated[
            Union[SinglePlaneConfig, MultiPlaneConfig, StackConfig],
            Field(discriminator="object_type"),
        ]
    ] = Field(..., title="Two photon imaging configurations")
    notes: Optional[str] = Field(default=None, title="Notes")


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
    calibration_date: Optional[datetime] = Field(
        default=None, title="Date on which coordinate transform was last calibrated"
    )
    coordinate_transform: Optional[AssetPath] = Field(
        default=None, title="Path to coordinate transform file", description="Relative path from metadata json to file"
    )  # [TODO] Remove
    notes: Optional[str] = Field(default=None, title="Notes")


class ManipulatorConfig(DomeModule):
    """A dome module connected to a 3-axis manipulator"""

    # Target
    primary_targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")
    other_targeted_structure: Optional[List[CCFStructure.ONE_OF]] = Field(
        default=None, title="Other targeted structure"
    )
    atlas_coordinates: Optional[List[Coordinate]] = Field(
        default=None,
        title="Targeted coordinates in the Acquisition Atlas",
    )

    # Coordinates
    manipulator_coordinates: List[Coordinate] = Field(
        ...,
        title="Targeted coordinates in the Instrument CoordinateSystem",
    )
    manipulator_axis_positions: Optional[List[Coordinate]] = Field(
        default=None,
        title="Manipulator local axis positions, in the device CoordinateSystem",
    )

    dye: Optional[str] = Field(default=None, title="Dye")
    implant_hole_number: Optional[int] = Field(default=None, title="Implant hole number")

    @model_validator(mode="after")
    def validate_len_coordinates(self):
        """Validate number of coordinates targeted"""

        lengths = []
        if self.atlas_coordinates:
            lengths.append(len(self.atlas_coordinates))
        if self.manipulator_coordinates:
            lengths.append(len(self.manipulator_coordinates))
        if self.manipulator_axis_positions:
            lengths.append(len(self.manipulator_axis_positions))

        if len(set(lengths)) > 1:
            raise ValueError(
                "Length of atlas_coordinates, manipulator_coordinates, and manipulator_axis_positions must be the same"
            )

        return self


class FiberAssemblyConfig(ManipulatorConfig):
    """Inserted fiber photometry probe recorded in a stream"""

    patch_cord_connections: List[PatchCordConfig] = Field(default=[], title="Fiber photometry devices")


class Liquid(str, Enum):
    """Solution names"""

    WATER = "Water"
    SUCROSE = "Sucrose"
    QUININE = "Quinine"
    CITRIC_ACID = "Citric acid"
    OTHER = "Other"


class LickSpoutConfig(DataModel):
    """Lick spout acquisition information"""

    solution: Liquid = Field(..., title="Solution")
    solution_valence: Valence = Field(..., title="Valence")

    relative_position: List[AnatomicalRelative] = Field(..., title="Initial relative position")
    position: Optional[Transform] = Field(default=None, title="Initial position")

    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)

    @model_validator(mode="after")
    def validate_other(cls, values):
        """Validator for other/notes"""

        if values.solution == Liquid.OTHER and not values.notes:
            raise ValueError(
                "Notes cannot be empty if LickSpoutConfig.solution is Other."
                "Describe the solution in the notes field."
            )
        return values


class AirPuffConfig(DataModel):
    """Air puff device configuration"""

    valence: Valence = Field(default=Valence.NEGATIVE, title="Valence")
    relative_position: List[AnatomicalRelative] = Field(..., title="Initial relative position")
    position: Optional[Transform] = Field(default=None, title="Initial position")

    pressure: Optional[float] = Field(default=None, title="Pressure")
    pressure_unit: Optional[PressureUnit] = Field(default=None, title="Pressure unit")

    duration: Optional[float] = Field(default=None, title="Duration")


class SpeakerConfig(DeviceConfig):
    """Configuration of auditory speaker configuration"""

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
    """Configuration of a 3D scan"""

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
    vc_transform: Optional[Transform] = Field(default=None, title="Scan transform")
    subject_position: SubjectPosition = Field(..., title="Subject position")
    # other fields
    voxel_sizes: Optional[Scale] = Field(default=None, title="Voxel sizes", description="Resolution")
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
        """Validate that primary scan has vc_transform and voxel_sizes fields"""

        if self.primary_scan:
            if not self.vc_transform or not self.voxel_sizes:
                raise ValueError("Primary scan must have vc_transform and voxel_sizes fields")

        return self


class Immersion(DataModel):
    """Configuration of immersion medium"""

    medium: ImmersionMedium = Field(..., title="Immersion medium")
    refractive_index: Decimal = Field(..., title="Index of refraction")


class SampleChamberConfig(DataModel):
    """Configuration of a sample chamber"""

    chamber_immersion: Immersion = Field(..., title="Acquisition chamber immersion data")
    sample_immersion: Optional[Immersion] = Field(default=None, title="Acquisition sample immersion data")


class Image(DataModel):
    """Configuration of an image"""

    channel_name: str = Field(..., title="Channel name")
    coordinate_transform: CoordinateTransform = Field(..., title="Image coordinate transformations")
    file_name: Optional[str] = Field(default=None, title="File name")
    imaging_angle: int = Field(
        default=0,
        title="Imaging angle",
        description="Angle of the detector relative to the image plane relative to perpendicular",
    )
    imaging_angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Imaging angle unit")
    image_start_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Image acquisition start time")
    image_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Image acquisition end time")


class ImagingConfig(DataModel):
    """Configuration of an imaging instrument"""

    channels: List[Channel] = Field(..., title="Channels")
    images: List[Annotated[Union[FieldOfView, Image], Field(discriminator="object_type")]] = Field(..., title="Images")
    coordinate_system: Optional[CoordinateSystem] = Field(default=None, title="Coordinate system")

    @model_validator(mode="after")
    def check_image_channels(self):
        """Check that the required channels are present for the images"""

        channel_names = [channel.channel_name for channel in self.channels]

        for image in self.images:
            if image.channel_name not in channel_names:
                raise ValueError(f"Channel {image.channel_name} must be defined in the ImagingConfig.channels list")
        return self

    @model_validator(mode="after")
    def require_cs_images(self):
        """Check that a coordinate system is present if any images are Image"""

        if any(isinstance(image, Image) for image in self.images) and not self.coordinate_system:
            raise ValueError("Coordinate system is required if any images are Image")
        return self
