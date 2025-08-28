""" schema for various Devices """

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional
import warnings

from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.devices import (
    BinMode,
    CameraChroma,
    CameraTarget,
    Cooling,
    Coupling,
    DaqChannelType,
    DataInterface,
    DetectorType,
    DeviceDriver,
    FerruleMaterial,
    FilterType,
    ImagingDeviceType,
    ImmersionMedium,
    LickSensorType,
    MyomatrixArrayType,
    ObjectiveType,
    ProbeModel,
    StageAxisDirection,
)
from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import (
    FrequencyUnit,
    MagneticFieldUnit,
    SizeUnit,
    SpeedUnit,
    TemperatureUnit,
    UnitlessUnit,
    VoltageUnit,
)
from pydantic import Field, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import DataModel, Discriminated, GenericModel
from aind_data_schema.components.coordinates import TRANSFORM_TYPES, AxisName, CoordinateSystem, Scale
from aind_data_schema.components.identifiers import Software


class CatheterMaterial(str, Enum):
    """Type of catheter material"""

    NAKED = "Naked"
    SILICONE = "VAB silicone"
    MESH = "VAB mesh"


class CatheterPort(str, Enum):
    """Type of catheter port"""

    SINGLE = "Single"
    DOUBLE = "Double"


class CatheterDesign(str, Enum):
    """Type of catheter design"""

    MAGNETIC = "Magnetic"
    NONMAGNETIC = "Non-magnetic"
    NA = "N/A"


class Device(DataModel):
    """Generic device"""

    name: str = Field(..., title="Device name")
    serial_number: Optional[str] = Field(default=None, title="Serial number")
    manufacturer: Optional[Organization.ONE_OF] = Field(default=None, title="Manufacturer")
    model: Optional[str] = Field(default=None, title="Model")

    # Additional fields
    additional_settings: Optional[GenericModel] = Field(default=None, title="Additional parameters")
    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="after")
    @classmethod
    def validate_manufacturer_notes(cls, values):
        """Ensure that notes are not empty if manufacturer is 'other'"""

        if hasattr(values, "manufacturer") and values.manufacturer is not None:
            manufacturer = values.manufacturer
            notes = values.notes

            if manufacturer == Organization.OTHER and not notes:
                raise ValueError("Device.notes cannot be empty if manufacturer is 'other'")

        return values


class DevicePosition(DataModel):
    """Position class for devices"""

    relative_position: List[AnatomicalRelative] = Field(..., title="Relative position")

    # Position
    coordinate_system: Optional[CoordinateSystem] = Field(default=None, title="Device coordinate system")
    transform: Optional[TRANSFORM_TYPES] = Field(
        default=None,
        title="Device to instrument transform",
        description="Position and orientation of the device in the instrument coordinate system",
    )

    @model_validator(mode="after")
    @classmethod
    def validate_transform_and_cs(cls, values):
        """Ensure that transform and coordinate system are either both set or both unset"""
        transform = values.transform
        coordinate_system = values.coordinate_system

        if (transform is None) != (coordinate_system is None):
            raise ValueError(
                "DevicePosition.transform and DevicePosition.coordinate_system"
                " must either both be set or both be unset."
            )

        return values


class Catheter(Device):
    """Description of a catheter device"""

    catheter_material: CatheterMaterial = Field(..., title="Catheter material")
    catheter_design: CatheterDesign = Field(..., title="Catheter design")
    catheter_port: CatheterPort = Field(..., title="Catheter port")


class Computer(Device):
    """Description of a computer"""

    operating_system: Optional[str] = Field(default=None, title="Operating system")


class Detector(Device):
    """Description of a generic detector"""

    detector_type: DetectorType = Field(..., title="Detector Type")
    manufacturer: Organization.DETECTOR_MANUFACTURERS
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(default=Cooling.NO_COOLING, title="Cooling")
    frame_rate: Optional[Decimal] = Field(default=None, title="Frame rate (Hz)", description="Frame rate being used")
    frame_rate_unit: Optional[FrequencyUnit] = Field(default=None, title="Frame rate unit")
    immersion: Optional[ImmersionMedium] = Field(default=None, title="Immersion")
    chroma: Optional[CameraChroma] = Field(default=None, title="Camera chroma")
    sensor_width: Optional[int] = Field(default=None, title="Width of the sensor (pixels)")
    sensor_height: Optional[int] = Field(default=None, title="Height of the sensor (pixels)")
    size_unit: SizeUnit = Field(default=SizeUnit.PX, title="Size unit")
    sensor_format: Optional[str] = Field(default=None, title="Sensor format")
    sensor_format_unit: Optional[str] = Field(default=None, title="Sensor format unit")
    bit_depth: Optional[int] = Field(default=None, title="Bit depth")
    bin_mode: BinMode = Field(default=BinMode.NO_BINNING, title="Detector binning mode")
    bin_width: Optional[int] = Field(default=None, title="Bin width")
    bin_height: Optional[int] = Field(default=None, title="Bin height")
    bin_unit: SizeUnit = Field(default=SizeUnit.PX, title="Bin size unit")
    gain: Optional[Decimal] = Field(default=None, title="Gain")
    crop_offset_x: Optional[int] = Field(default=None, title="Crop offset x")
    crop_offset_y: Optional[int] = Field(default=None, title="Crop offset y")
    crop_width: Optional[int] = Field(default=None, title="Crop width")
    crop_height: Optional[int] = Field(default=None, title="Crop width")
    crop_unit: SizeUnit = Field(default=SizeUnit.PX, title="Crop size unit")
    recording_software: Optional[Software] = Field(default=None, title="Recording software")
    driver: Optional[DeviceDriver] = Field(default=None, title="Driver")
    driver_version: Optional[str] = Field(default=None, title="Driver version")

    @model_validator(mode="after")
    def validate_other(self):
        """Validator for other/notes"""

        validation_items = []

        if self.notes is None:
            if self.immersion == ImmersionMedium.OTHER:
                validation_items.append("immersion")

            if self.detector_type == DetectorType.OTHER:
                validation_items.append("detector_type")

            if self.data_interface == DataInterface.OTHER:
                validation_items.append("data_interface")

        if len(validation_items) > 0:
            raise ValueError(
                f"Notes cannot be empty while any of the following fields are set to 'other': {validation_items}"
            )

        return self


class Camera(Detector):
    """Camera Detector"""

    detector_type: DetectorType = Field(default=DetectorType.CAMERA)


class Filter(Device):
    """Filter used in a light path"""

    # required fields
    filter_type: FilterType = Field(..., title="Type of filter")
    manufacturer: Organization.FILTER_MANUFACTURERS

    # optional fields
    cut_off_wavelength: Optional[int] = Field(default=None, title="Cut-off wavelength (nm)")
    cut_on_wavelength: Optional[int] = Field(default=None, title="Cut-on wavelength (nm)")
    center_wavelength: Optional[int | list[int]] = Field(
        default=None,
        title="Center wavelength (nm)",
        description="Single wavelength or list of wavelengths for MULTIBAND or MULTI_NOTCH filters",
    )
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")

    @model_validator(mode="after")
    def validate_multi_filters(self):
        """Check for multiband/multinotch filters and make sure center_wavelength is a list"""

        if self.filter_type in {FilterType.MULTIBAND, FilterType.MULTI_NOTCH}:
            if not isinstance(self.center_wavelength, list):
                raise ValueError(
                    "For multiband or multinotch filters, center_wavelength must be a list of wavelengths."
                )
        else:
            if isinstance(self.center_wavelength, list):
                raise ValueError(
                    "For non-multiband/non-multinotch filters, center_wavelength must be a single wavelength."
                )

        return self


class Lens(Device):
    """Lens"""

    # required fields
    manufacturer: Organization.LENS_MANUFACTURERS


class MotorizedStage(Device):
    """Description of motorized stage"""

    travel: Decimal = Field(..., title="Travel of device (mm)")
    travel_unit: SizeUnit = Field(default=SizeUnit.MM, title="Travel unit")

    # optional fields
    firmware: Optional[Software] = Field(default=None, title="Firmware")


class Objective(Device):
    """Description of an objective device"""

    numerical_aperture: Decimal = Field(..., title="Numerical aperture (in air)")
    magnification: Decimal = Field(..., title="Magnification")
    immersion: ImmersionMedium = Field(..., title="Immersion")
    objective_type: Optional[ObjectiveType] = Field(default=None, title="Objective type")

    @field_validator("immersion", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if value == ImmersionMedium.OTHER and not info.data.get("notes"):
            raise ValueError("Notes cannot be empty if immersion is Other. Describe the immersion in the notes field.")

        return value


class CameraAssembly(DevicePosition):
    """Named assembly of a camera and lens (and optionally a filter)"""

    name: str = Field(..., title="Camera assembly name")
    target: CameraTarget = Field(..., title="Camera target")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    filter: Optional[Filter] = Field(default=None, title="Filter")


class DAQChannel(DataModel):
    """Named input or output channel on a DAQ device"""

    # required fields
    channel_name: str = Field(..., title="DAQ channel name")
    channel_type: DaqChannelType = Field(..., title="DAQ channel type")

    # optional fields
    port: Optional[int] = Field(default=None, title="DAQ port")
    channel_index: Optional[int] = Field(
        default=None, title="DAQ channel index", deprecated="Use DAQChannel.port instead"
    )
    sample_rate: Optional[Decimal] = Field(default=None, title="DAQ channel sample rate (Hz)")
    sample_rate_unit: Optional[FrequencyUnit] = Field(default=None, title="Sample rate unit")
    event_based_sampling: Optional[bool] = Field(
        default=None, title="Set to true if DAQ channel is sampled at irregular intervals"
    )

    @field_validator("channel_index", mode="after")
    def deprecated_channel_index(cls, value: Optional[int]) -> Optional[int]:
        """Warn if channel_index is used (deprecated)"""
        if value is not None:
            warnings.warn(
                "DAQChannel.channel_index is deprecated. Use DAQChannel.port instead.",
                DeprecationWarning,
            )
        return value


class DAQDevice(Device):
    """Data acquisition device containing multiple I/O channels"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS

    # optional fields
    channels: List[DAQChannel] = Field(default=[], title="DAQ channels")
    firmware_version: Optional[str] = Field(default=None, title="Firmware version")
    hardware_version: Optional[str] = Field(default=None, title="Hardware version")


class HarpDevice(DAQDevice):
    """DAQ that uses the Harp protocol for synchronization and data transmission"""

    # required fields
    manufacturer: Organization.ONE_OF = Field(default=Organization.OEPS)
    harp_device_type: HarpDeviceType.ONE_OF = Field(..., title="Type of Harp device")
    core_version: Optional[str] = Field(default=None, title="Core version")
    tag_version: Optional[str] = Field(default=None, title="Tag version")
    data_interface: DataInterface = Field(default=DataInterface.USB, title="Data interface")
    is_clock_generator: bool = Field(..., title="Is Clock Generator")

    @field_validator("data_interface", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if value == DataInterface.OTHER and not info.data.get("notes"):
            raise ValueError(
                "Notes cannot be empty if data_interface is Other. Describe the data interface in the notes field."
            )

        return value


class Laser(Device):
    """Laser module with a specific wavelength (may be a sub-component of a larger assembly)"""

    # required fields
    manufacturer: Organization.LASER_MANUFACTURERS
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")

    # optional fields
    coupling: Optional[Coupling] = Field(default=None, title="Coupling")
    coupling_efficiency: Optional[Decimal] = Field(
        default=None,
        title="Coupling efficiency (percent)",
        ge=0,
        le=100,
    )
    coupling_efficiency_unit: Literal["percent"] = Field(default="percent", title="Coupling efficiency unit")


class LightEmittingDiode(Device):
    """Description of a Light Emitting Diode (LED) device"""

    manufacturer: Organization.LED_MANUFACTURERS
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    bandwidth: Optional[int] = Field(default=None, title="Bandwidth (FWHM)")
    bandwidth_unit: Optional[SizeUnit] = Field(default=None, title="Bandwidth unit")


class Lamp(Device):
    """Description of a Lamp lightsource"""

    wavelength_min: Optional[int] = Field(default=None, title="Wavelength minimum (nm)")
    wavelength_max: Optional[int] = Field(default=None, title="Wavelength maximum (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    temperature: Optional[int] = Field(default=None, title="Temperature (K)")
    temperature_unit: Optional[TemperatureUnit] = Field(default=None, title="Temperature unit")


class LightAssembly(DataModel):
    """Named assembly of a light source and lens"""

    # required fields
    name: str = Field(..., title="Light assembly name")
    light: Discriminated[Laser | LightEmittingDiode | Lamp]
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: Optional[Filter] = Field(default=None, title="Filter")


class ProbePort(DataModel):
    """Port for a probe connection"""

    index: int = Field(..., title="One-based port index")
    probes: List[str] = Field(..., title="Names of probes connected to this port")


class NeuropixelsBasestation(DAQDevice):
    """PXI-based Neuropixels DAQ"""

    # required fields
    basestation_firmware_version: str = Field(..., title="Basestation firmware version")
    bsc_firmware_version: str = Field(..., title="Basestation connect board firmware")
    slot: int = Field(..., title="Slot number for this basestation")
    ports: List[ProbePort] = Field(..., title="Basestation ports")

    # fixed values
    data_interface: DataInterface = DataInterface.PXI
    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS = Organization.IMEC


class OpenEphysAcquisitionBoard(DAQDevice):
    """Multichannel electrophysiology DAQ"""

    # required fields
    ports: List[ProbePort] = Field(..., title="Acquisition board ports")

    # fixed values
    data_interface: Literal[DataInterface.USB] = DataInterface.USB
    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS = Field(default=Organization.OEPS)


class Manipulator(Device):
    """Manipulator used on a dome module"""

    manufacturer: Organization.MANIPULATOR_MANUFACTURERS


class FiberPatchCord(Device):
    """Description of a patch cord"""

    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(default=None, title="Photobleaching date")


class LaserAssembly(DataModel):
    """Named assembly combining a manipulator, lasers, collimator, and fibers"""

    name: str = Field(..., title="Laser assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: List[Laser] = Field(..., title="Lasers connected to this module")
    collimator: Device = Field(..., title="Collimator")
    fiber: FiberPatchCord = Field(..., title="Fiber patch")


class EphysProbe(Device):
    """Probe used in an ephys experiment"""

    probe_model: ProbeModel = Field(..., title="Probe model")
    headstage: Optional[Device] = Field(default=None, title="Headstage for this probe")


class EphysAssembly(DataModel):
    """Named assembly for combining a manipulator and ephys probes"""

    name: str = Field(..., title="Ephys assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    probes: List[EphysProbe] = Field(..., title="Probes that are held by this module")


class FiberProbe(Device):
    """Description of a fiber optic probe"""

    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    core_diameter_unit: SizeUnit = Field(default=SizeUnit.UM, title="Core diameter unit")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    ferrule_material: Optional[FerruleMaterial] = Field(default=None, title="Ferrule material")
    active_length: Optional[Decimal] = Field(default=None, title="Active length (mm)", description="Length of taper")
    total_length: Decimal = Field(..., title="Total length (mm)")
    length_unit: SizeUnit = Field(default=SizeUnit.MM, title="Length unit")


class FiberAssembly(DataModel):
    """Module for inserted fiber photometry recording"""

    name: str = Field(..., title="Fiber assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    fibers: List[FiberProbe] = Field(..., title="Probes that are held by this module")


class DigitalMicromirrorDevice(Device):
    """Description of a Digital Micromirror Device (DMD)"""

    max_dmd_patterns: int = Field(..., title="Max DMD patterns")
    double_bounce_design: bool = Field(..., title="Double bounce design")
    invert_pixel_values: bool = Field(..., title="Invert pixel values")
    motion_padding_x: int = Field(..., title="Motion padding X (pixels)")
    motion_padding_y: int = Field(..., title="Motion padding Y (pixels)")
    padding_unit: SizeUnit = Field(default=SizeUnit.PX, title="Padding unit")
    pixel_size: Decimal = Field(..., title="DMD Pixel size")
    pixel_size_unit: SizeUnit = Field(default=SizeUnit.UM, title="Pixel size unit")
    start_phase: Decimal = Field(..., title="DMD Start phase (fraction of cycle)")
    dmd_flip: bool = Field(..., title="DMD Flip")
    dmd_curtain: List[Decimal] = Field(..., title="DMD Curtain")
    dmd_curtain_unit: SizeUnit = Field(default=SizeUnit.PX, title="dmd_curtain_unit")
    line_shear: List[int] = Field(..., title="Line shear (pixels)")
    line_shear_unit: SizeUnit = Field(default=SizeUnit.PX, title="Line shear unit")


class PolygonalScanner(Device):
    """Description of a Polygonal scanner"""

    speed: int = Field(..., title="Speed (rpm)")
    speed_unit: SpeedUnit = Field(default=SpeedUnit.RPM, title="Speed unit")
    number_faces: int = Field(..., title="Number of faces")


class PockelsCell(Device):
    """Description of a Pockels Cell"""

    polygonal_scanner: Optional[str] = Field(
        default=None, title="Polygonal scanner", description="Must match name of Polygonal scanner"
    )
    on_time: Optional[Decimal] = Field(default=None, title="On time (fraction of cycle)")
    off_time: Optional[Decimal] = Field(default=None, title="Off time (fraction of cycle)")
    time_setting_unit: UnitlessUnit = Field(default=UnitlessUnit.FC, title="Time setting unit")
    beam_modulation: Optional[Decimal] = Field(default=None, title="Beam modulation (V)")
    beam_modulation_unit: Optional[VoltageUnit] = Field(default=None, title="Beam modulation unit")


class Enclosure(Device):
    """Description of an enclosure"""

    size: Scale = Field(..., title="Size")
    size_unit: SizeUnit = Field(..., title="Size unit")
    internal_material: Optional[str] = Field(default=None, title="Internal material")
    external_material: str = Field(..., title="External material")
    grounded: bool = Field(..., title="Grounded")
    laser_interlock: bool = Field(..., title="Laser interlock")
    air_filtration: bool = Field(..., title="Air filtration")


class Disc(Device):
    """Description of a running disc (i.e. MindScope Disc)"""

    radius: Decimal = Field(..., title="Radius (cm)", ge=0)
    radius_unit: SizeUnit = Field(default=SizeUnit.CM, title="radius unit")
    output: Optional[DaqChannelType] = Field(default=None, description="analog or digital electronics")
    encoder: Optional[str] = Field(default=None, title="Encoder", description="Encoder hardware type")
    decoder: Optional[str] = Field(default=None, title="Decoder", description="Decoder chip type")
    encoder_firmware: Optional[Software] = Field(
        default=None,
        title="Encoder firmware",
        description="Firmware to read from decoder chip counts",
    )
    surface_material: Optional[str] = Field(default=None, title="Surface material")


class Wheel(Device):
    """Description of a running wheel"""

    radius: Decimal = Field(..., title="Radius (mm)")
    width: Decimal = Field(..., title="Width (mm)")
    size_unit: SizeUnit = Field(default=SizeUnit.MM, title="Size unit")
    encoder: Device = Field(..., title="Encoder")
    pulse_per_revolution: int = Field(..., title="Pulse per revolution")
    magnetic_brake: Device = Field(..., title="Magnetic brake")
    torque_sensor: Device = Field(..., title="Torque sensor")


class Tube(Device):
    """Description of a tube platform"""

    diameter: Decimal = Field(..., title="Diameter", ge=0)
    diameter_unit: SizeUnit = Field(default=SizeUnit.CM, title="Diameter unit")


class Treadmill(Device):
    """Description of treadmill platform"""

    treadmill_width: Decimal = Field(..., title="Width of treadmill (mm)")
    width_unit: SizeUnit = Field(default=SizeUnit.CM, title="Width unit")
    encoder: Optional[Device] = Field(default=None, title="Encoder")
    pulse_per_revolution: Optional[int] = Field(default=None, title="Pulse per revolution")


class Arena(Device):
    """Description of a rectangular arena"""

    size: Scale = Field(..., title="3D Size")
    size_unit: SizeUnit = Field(..., title="Size unit")
    objects_in_arena: List[Device] = Field(default=[], title="Objects in arena")


class Monitor(Device, DevicePosition):
    """Description of visual display for visual stimuli"""

    manufacturer: Organization.MONITOR_MANUFACTURERS
    refresh_rate: int = Field(..., title="Refresh rate (Hz)", ge=60)
    width: int = Field(..., title="Width (pixels)")
    height: int = Field(..., title="Height (pixels)")
    size_unit: SizeUnit = Field(default=SizeUnit.PX, title="Size unit")
    viewing_distance: Decimal = Field(..., title="Viewing distance (cm)")
    viewing_distance_unit: SizeUnit = Field(default=SizeUnit.CM, title="Viewing distance unit")

    contrast: Optional[int] = Field(
        default=None,
        description="Monitor's contrast setting",
        title="Contrast",
        ge=0,
        le=100,
    )
    brightness: Optional[int] = Field(
        default=None,
        description="Monitor's brightness setting",
        title="Brightness",
        ge=0,
        le=100,
    )


class LickSpout(Device):
    """Description of a lick spout"""

    spout_diameter: Decimal = Field(..., title="Spout diameter (mm)")
    spout_diameter_unit: SizeUnit = Field(default=SizeUnit.MM, title="Spout diameter unit")

    solenoid_valve: Device = Field(..., title="Solenoid valve")
    lick_sensor: Device = Field(..., title="Lick sensor")
    lick_sensor_type: Optional[LickSensorType] = Field(default=None, title="Lick sensor type")


class LickSpoutAssembly(DataModel):
    """Description of multiple lick spouts, possibly mounted on a stage"""

    name: str = Field(..., title="Lick spout assembly name")
    lick_spouts: List[LickSpout] = Field(..., title="Water spouts")
    motorized_stage: Optional[MotorizedStage] = Field(default=None, title="Motorized stage")


class AirPuffDevice(Device):
    """Description of an air puff device"""

    diameter: float = Field(..., title="Spout diameter")
    diameter_unit: SizeUnit = Field(..., title="Size unit")


class Speaker(Device, DevicePosition):
    """Description of a speaker for auditory stimuli"""

    manufacturer: Organization.SPEAKER_MANUFACTURERS


class OlfactometerChannelType(Enum):
    """Olfactometer channel types"""

    ODOR = "Odor"
    CARRIER = "Carrier"


class OlfactometerChannel(DataModel):
    """description of a Olfactometer channel"""

    channel_index: int = Field(..., title="Channel index")
    channel_type: OlfactometerChannelType = Field(..., title="Channel type")
    flow_capacity: Literal[100, 1000] = Field(default=100, title="Flow capacity")
    flow_unit: str = Field(default="mL/min", title="Flow unit")


class Olfactometer(HarpDevice):
    """Description of an olfactometer for odor stimuli"""

    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS = Field(default=Organization.CHAMPALIMAUD)

    harp_device_type: HarpDeviceType.ONE_OF = Field(
        HarpDeviceType.OLFACTOMETER, frozen=True, title="Type of Harp device"
    )
    channels: List[OlfactometerChannel]


class AdditionalImagingDevice(Device):
    """Description of additional devices"""

    imaging_device_type: ImagingDeviceType = Field(..., title="Device type")

    @field_validator("imaging_device_type", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if value == ImagingDeviceType.OTHER and not info.data.get("notes"):
            raise ValueError(
                "Notes cannot be empty if imaging_device_type is Other. "
                "Describe the imaging device type in the notes field."
            )

        return value


class ScanningStage(MotorizedStage):
    """Description of a scanning motorized stages"""

    stage_axis_direction: StageAxisDirection = Field(..., title="Direction of stage axis")
    stage_axis_name: AxisName = Field(..., title="Name of stage axis")


class Scanner(Device):
    """Description of a MRI Scanner"""

    magnetic_strength: float = Field(..., title="Magnetic strength (T)")
    magnetic_strength_unit: MagneticFieldUnit = Field(..., title="Magnetic strength unit")


class MyomatrixContact(DataModel):
    """Description of a contact on a myomatrix thread"""

    body_part: MouseAnatomyModel = Field(..., title="Body part of contact insertion", description="Use MouseBodyParts")
    relative_position: AnatomicalRelative = Field(
        ..., title="Relative position", description="Position relative to procedures coordinate system"
    )
    muscle: MouseAnatomyModel = Field(..., title="Muscle of contact insertion", description="Use MouseEmgMuscles")
    in_muscle: bool = Field(..., title="In muscle")


class MyomatrixThread(DataModel):
    """Description of a thread of a myomatrix array"""

    ground_electrode_location: MouseAnatomyModel = Field(
        ..., title="Location of ground electrode", description="Use GroundWireLocations"
    )
    contacts: List[MyomatrixContact] = Field(..., title="Contacts")


class MyomatrixArray(Device):
    """Description of a Myomatrix array"""

    array_type: MyomatrixArrayType = Field(..., title="Array type")
    threads: List[MyomatrixThread] = Field(..., title="Array threads")


class Microscope(Device):
    """Description of a microscope"""
