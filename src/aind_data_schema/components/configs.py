""" Configurations for devices, software, and other components during acquisition """

from decimal import Decimal
from enum import Enum
from typing import List, Optional

from aind_data_schema_models.brain_atlas import BrainStructureModel
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.devices import ImmersionMedium
from aind_data_schema_models.units import (
    AngleUnit,
    FrequencyUnit,
    PowerUnit,
    PressureUnit,
    SizeUnit,
    SoundIntensityUnit,
    TimeUnit,
    VolumeUnit,
)
from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from pydantic import Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel, DiscriminatedList, GenericModel
from aind_data_schema.components.coordinates import (
    TRANSFORM_TYPES,
    AtlasCoordinate,
    CoordinateSystem,
    Scale,
    Translation,
)
from aind_data_schema.components.identifiers import Code
from aind_data_schema.components.wrappers import AssetPath


class PowerFunction(str, Enum):
    """Power functions"""

    CONSTANT = "Constant"
    LINEAR = "Linear"
    EXPONENTIAL = "Exponential"
    OTHER = "Other"


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


class Liquid(str, Enum):
    """Solution names"""

    WATER = "Water"
    SUCROSE = "Sucrose"
    QUININE = "Quinine"
    CITRIC_ACID = "Citric acid"
    OTHER = "Other"


class TriggerType(str, Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


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


class DeviceConfig(DataModel):
    """Parent class for all configurations"""

    device_name: str = Field(..., title="Device name", description="Must match a device defined in the instrument.json")


# IMAGING CONFIGS


class DetectorConfig(DeviceConfig):
    """Configuration of detector settings"""

    exposure_time: float = Field(..., title="Exposure time")
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
    power: Optional[float] = Field(default=None, title="Excitation power")
    power_unit: Optional[PowerUnit] = Field(default=None, title="Excitation power unit")


class LightEmittingDiodeConfig(DeviceConfig):
    """Configuration of LED settings"""

    power: Optional[float] = Field(default=None, title="Excitation power")
    power_unit: Optional[PowerUnit] = Field(default=None, title="Excitation power unit")


LIGHT_CONFIGS = DiscriminatedList[LaserConfig | LightEmittingDiodeConfig]


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
    light_sources: LIGHT_CONFIGS = Field(default=[], title="Light source configurations")
    variable_power: Optional[bool] = Field(
        default=False,
        title="Variable power",
        description="Set to true when the power varies across Planes -- put the power in the Plane.power field",
    )
    excitation_filters: Optional[List[DeviceConfig]] = Field(default=None, title="Excitation filters")
    # emission
    emission_filters: Optional[List[DeviceConfig]] = Field(default=None, title="Emission filters")
    emission_wavelength: Optional[int] = Field(default=None, title="Emission wavelength")
    emission_wavelength_unit: Optional[SizeUnit] = Field(default=None, title="Emission wavelength unit")


class SlapChannel(Channel):
    """Configuration of a channel for Slap"""

    dilation: int = Field(..., title="Dilation")
    dilation_unit: SizeUnit = Field(..., title="Dilation unit")

    description: Optional[str] = Field(default=None, title="Description")


class PatchCordConfig(DeviceConfig):
    """Configuration of a patch cord and its output power to another device"""

    channels: List[Channel] = Field(..., title="Channels")


class Immersion(DataModel):
    """Configuration of immersion medium"""

    medium: ImmersionMedium = Field(..., title="Immersion medium")
    refractive_index: float = Field(..., title="Index of refraction")


class SampleChamberConfig(DeviceConfig):
    """Configuration of a sample chamber"""

    chamber_immersion: Immersion = Field(..., title="Acquisition chamber immersion data")
    sample_immersion: Optional[Immersion] = Field(default=None, title="Acquisition sample immersion data")


class Plane(DataModel):
    """Configuration of an imaging plane"""

    depth: float = Field(..., title="Depth")
    depth_unit: SizeUnit = Field(..., title="Depth unit")

    power: float = Field(..., title="Power")
    power_unit: PowerUnit = Field(..., title="Power unit")
    targeted_structure: BrainStructureModel = Field(..., title="Targeted structure")


class CoupledPlane(Plane):
    """Configuration of a pair of coupled imaging plane"""

    plane_index: int = Field(..., title="Plane index")
    coupled_plane_index: int = Field(..., title="Coupled plane index", description="Plane index of the coupled plane")
    power_ratio: float = Field(..., title="Power ratio")


class SlapPlane(Plane):
    """Configuration of an imagine plane on a Slap microscope"""

    dmd_dilation_x: int = Field(..., title="DMD Dilation X (pixels)")
    dmd_dilation_y: int = Field(..., title="DMD Dilation Y (pixels)")
    dilation_unit: SizeUnit = Field(default=SizeUnit.PX, title="Dilation unit")

    slap_acquisition_type: SlapAcquisitionType = Field(..., title="Slap experiment type")
    target_neuron: Optional[str] = Field(default=None, title="Target neuron")
    target_branch: Optional[str] = Field(default=None, title="Target branch")
    path_to_array_of_frame_rates: AssetPath = Field(
        ..., title="Array of frame rates", description="Relative path from metadata json to file"
    )


class Image(DataModel):
    """Description of an N-D image"""

    channel_name: str = Field(..., title="Channel name")
    dimensions_unit: SizeUnit = Field(default=SizeUnit.PX, title="Dimensions unit")
    image_to_acquisition_transform: TRANSFORM_TYPES = Field(
        ...,
        title="Image to acquisition transform",
        description="Position, rotation, and scale of the image. Note that depth should be in the planes.",
    )

    dimensions: Optional[Scale] = Field(default=None, title="Dimensions")


class ImageSPIM(Image):
    """Description of an N-D image acquired with SPIM"""

    file_name: AssetPath = Field(..., title="File name")
    imaging_angle: int = Field(
        default=0,
        title="Imaging angle",
        description="Angle of the detector relative to the image plane relative to perpendicular",
    )
    imaging_angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Imaging angle unit")

    image_start_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Image acquisition start time")
    image_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Image acquisition end time")


class PlanarImage(Image):
    """Description of an N-D image acquired in a specific imaging plane"""

    planes: DiscriminatedList[Plane | CoupledPlane | SlapPlane] = Field(..., title="Imaging planes")

    @model_validator(mode="after")
    def limit_plane_to_one(self):
        """Check that only one plane is defined"""

        if any(not isinstance(plane, CoupledPlane) for plane in self.planes) and len(self.planes) > 1:
            raise ValueError("For single-plane optical physiology only a single Plane should be in PlanarImage.planes")

        return self


class PlanarImageStack(PlanarImage):
    """Description of a stack of images acquired in a specific imaging plane"""

    power_function: PowerFunction = Field(..., title="Power function")
    depth_start: float = Field(..., title="Starting depth")
    depth_end: float = Field(..., title="Ending depth")
    depth_step: float = Field(..., title="Step size")
    depth_unit: SizeUnit = Field(..., title="Depth unit")


class SamplingStrategy(DataModel):
    """Description of an image sampling strategy"""

    frame_rate: float = Field(..., title="Frame rate")
    frame_rate_unit: FrequencyUnit = Field(default=FrequencyUnit.HZ, title="Frame rate unit")


class InterleavedStrategy(SamplingStrategy):
    """Description of an interleaved image sampling strategy"""

    image_index_sequence: List[int] = Field(..., title="Interleaving sequence")


class StackStrategy(SamplingStrategy):
    """Description of a stack image sampling strategy"""

    image_repeats: int = Field(..., title="Number of image repeats")
    stack_repeats: int = Field(..., title="Number of stack repeats")


class ImagingConfig(DeviceConfig):
    """Configuration of an imaging instrument"""

    channels: DiscriminatedList[Channel | SlapChannel] = Field()
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Coordinate system",
        description=(
            "Required for ImageSPIM objects and when the imaging coordinate system differs from the "
            "Acquisition.coordinate_system"
        ),
    )  # note: exact field name is used by a validator
    images: DiscriminatedList[PlanarImage | PlanarImageStack | ImageSPIM] = Field(..., title="Images")
    sampling_strategy: Optional[SamplingStrategy] = Field(
        default=None,
        title="Sampling strategy",
    )

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

        if any(isinstance(image, ImageSPIM) for image in self.images) and not self.coordinate_system:
            raise ValueError(
                "ImagingConfig.coordinate_system is required when ImagingConfig.images are ImageSPIM objects"
            )
        return self


# MOUSE PLATFORM CONFIGS


class MousePlatformConfig(DeviceConfig):
    """Configuration for mouse platforms"""

    objects_in_arena: Optional[List[str]] = Field(default=None, title="Objects in area")
    active_control: bool = Field(
        default=False,
        title="Active control",
        description="True when movement of the mouse platform is dynamically controlled by the experimenter",
    )


class LickSpoutConfig(DeviceConfig):
    """Lick spout acquisition information"""

    solution: Liquid = Field(..., title="Solution")
    solution_valence: Valence = Field(..., title="Valence")

    volume: float = Field(..., title="Volume")
    volume_unit: VolumeUnit = Field(..., title="Volume unit")

    relative_position: List[AnatomicalRelative] = Field(..., title="Initial relative position")

    # Transform
    coordinate_system: Optional[CoordinateSystem] = Field(default=None, title="Device coordinate system")
    transform: Optional[TRANSFORM_TYPES] = Field(
        default=None,
        title="Device to acquisition transform",
        description="Entry coordinate, depth, and rotation in the Acquisition.coordinate_system",
    )
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


class AirPuffConfig(DeviceConfig):
    """Air puff device configuration"""

    valence: Valence = Field(default=Valence.NEGATIVE, title="Valence")
    relative_position: List[AnatomicalRelative] = Field(..., title="Initial relative position")

    # Transform
    coordinate_system: Optional[CoordinateSystem] = Field(default=None, title="Device coordinate system")
    transform: Optional[TRANSFORM_TYPES] = Field(
        default=None,
        title="Device to acquisition transform",
    )

    pressure: Optional[float] = Field(default=None, title="Pressure")
    pressure_unit: Optional[PressureUnit] = Field(default=None, title="Pressure unit")

    duration: Optional[float] = Field(default=None, title="Duration")


class SpeakerConfig(DeviceConfig):
    """Configuration of auditory speaker configuration"""

    volume: Optional[float] = Field(default=None, title="Volume (dB)")
    volume_unit: Optional[SoundIntensityUnit] = Field(default=None, title="Volume unit")


# EPHYS CONFIGS


class ManipulatorConfig(DeviceConfig):
    """Configuration of a manipulator"""

    coordinate_system: CoordinateSystem = Field(..., title="Device coordinate system")
    local_axis_positions: Translation = Field(..., title="Local axis positions")


class ProbeConfig(DeviceConfig):
    """Configuration for a device inserted into a brain"""

    # Target
    primary_targeted_structure: BrainStructureModel = Field(..., title="Targeted structure")
    other_targeted_structure: Optional[List[BrainStructureModel]] = Field(
        default=None, title="Other targeted structure"
    )
    atlas_coordinate: Optional[AtlasCoordinate] = Field(
        default=None,
        title="Target coordinate in Acquisition.atlas",
    )

    # Transform
    coordinate_system: CoordinateSystem = Field(
        ...,
        title="Device coordinate system",
        description=(
            "Device coordinate system, defines un-rotated probe's orientation relative to the "
            "Acquisition.coordinate_system"
        ),
    )
    transform: TRANSFORM_TYPES = Field(
        ...,
        title="Device to acquisition transform",
        description="Entry coordinate, depth, and rotation in the Acquisition.coordinate_system",
    )

    dye: Optional[str] = Field(default=None, title="Dye")
    notes: Optional[str] = Field(default=None, title="Notes")


class MISModuleConfig(DataModel):
    """Modular insertion system module configuration"""

    arc_angle: float = Field(..., title="Arc Angle (deg)")
    module_angle: float = Field(..., title="Module Angle (deg)")
    rotation_angle: Optional[float] = Field(default=None, title="Rotation Angle (deg)")
    angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
    notes: Optional[str] = Field(default=None, title="Notes")


class EphysAssemblyConfig(DeviceConfig):
    """Group of configurations for an ephys assembly"""

    manipulator: ManipulatorConfig = Field(..., title="Manipulator configuration")
    probes: List[ProbeConfig] = Field(..., title="Probe configurations")

    modules: Optional[List[MISModuleConfig]] = Field(
        default=None,
        title="Modules",
        description=("Configurations for conveniently tracking manipulator modules, e.g. on the New Scale dome."),
    )


class FiberAssemblyConfig(DeviceConfig):
    """Inserted fiber photometry probe recorded in a stream"""

    manipulator: ManipulatorConfig = Field(..., title="Manipulator configuration")
    probes: List[ProbeConfig] = Field(..., title="Probe configurations")
    patch_cords: List[PatchCordConfig] = Field(default=[], title="Fiber photometry devices")


# MRI CONFIGS


class MRIScan(DeviceConfig):
    """Configuration of a 3D scan"""

    scan_index: int = Field(..., title="Scan index")
    scan_type: ScanType = Field(..., title="Scan type")
    primary_scan: bool = Field(
        ..., title="Primary scan", description="Indicates the primary scan used for downstream analysis"
    )
    scan_sequence_type: MriScanSequence = Field(..., title="Scan sequence")
    rare_factor: Optional[int] = Field(default=None, title="RARE factor")
    echo_time: Decimal = Field(..., title="Echo time")
    echo_time_unit: TimeUnit = Field(..., title="Echo time unit")
    effective_echo_time: Optional[Decimal] = Field(default=None, title="Effective echo time")
    repetition_time: Decimal = Field(..., title="Repetition time")
    repetition_time_unit: TimeUnit = Field(..., title="Repetition time unit")

    # fields required to get correct orientation
    scan_coordinate_system: Optional[CoordinateSystem] = Field(default=None, title="Scanner coordinate system")
    scan_affine_transform: Optional[TRANSFORM_TYPES] = Field(
        default=None, title="MRI Scan affine transform", description="NIFTI sform/qform, Bruker vc_transform, etc"
    )
    subject_position: SubjectPosition = Field(..., title="Subject position")

    # other fields
    resolution: Optional[Scale] = Field(default=None, title="Voxel resolution")
    resolution_unit: Optional[SizeUnit] = Field(default=None, title="Voxel resolution unit")
    additional_scan_parameters: GenericModel = Field(..., title="Parameters")
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
        """Validate that primary scan has scan_affine_transform and resolution fields"""

        if self.primary_scan:
            if not self.scan_affine_transform or not self.resolution:
                raise ValueError("Primary scan must have scan_affine_transform and resolution fields")

        return self


# SURGERY CONFIGS


class CatheterConfig(DeviceConfig):
    """Configuration of a catheter"""

    targeted_structure: MouseAnatomyModel = Field(
        ..., title="Targeted blood vessel", description="Use options from MouseBloodVessels"
    )
