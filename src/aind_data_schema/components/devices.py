""" schema for various Devices """

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import (
    FrequencyUnit,
    PowerUnit,
    SizeUnit,
    SpeedUnit,
    TemperatureUnit,
    UnitlessUnit,
    VoltageUnit,
)
from pydantic import Field, ValidationInfo, field_validator, model_validator
from typing_extensions import Annotated

from aind_data_schema.base import GenericModel, GenericModelType, DataModel, AwareDatetimeWithDefault
from aind_data_schema.components.coordinates import Position, RelativePosition, Scale
from aind_data_schema.components.reagent import Reagent


class ImagingDeviceType(str, Enum):
    """Imaginge device type name"""

    BEAM_EXPANDER = "Beam expander"
    SAMPLE_CHAMBER = "Sample Chamber"
    DIFFUSER = "Diffuser"
    GALVO = "Galvo"
    LASER_COMBINER = "Laser combiner"
    LASER_COUPLER = "Laser coupler"
    PRISM = "Prism"
    OBJECTIVE = "Objective"
    ROTATION_MOUNT = "Rotation mount"
    SLIT = "Slit"
    TUNABLE_LENS = "Tunable lens"
    OTHER = "Other"


class ImagingInstrumentType(str, Enum):
    """Experiment type name"""

    CONFOCAL = "confocal"
    DISPIM = "diSPIM"
    EXASPIM = "exaSPIM"
    ECEPHYS = "ecephys"
    MESOSPIM = "mesoSPIM"
    OTHER = "Other"
    SMARTSPIM = "SmartSPIM"
    TWO_PHOTON = "Two photon"


class StageAxisDirection(str, Enum):
    """Direction of motion for motorized stage"""

    DETECTION_AXIS = "Detection axis"
    ILLUMINATION_AXIS = "Illumination axis"
    PERPENDICULAR_AXIS = "Perpendicular axis"


class StageAxisName(str, Enum):
    """Axis names for motorized stages as configured by hardware"""

    X = "X"
    Y = "Y"
    Z = "Z"


class DeviceDriver(str, Enum):
    """DeviceDriver name"""

    OPENGL = "OpenGL"
    VIMBA = "Vimba"
    NVIDIA = "Nvidia Graphics"


class Coupling(str, Enum):
    """Laser coupling type"""

    FREE_SPACE = "Free-space"
    MMF = "Multi-mode fiber"
    SMF = "Single-mode fiber"
    OTHER = "Other"


class DataInterface(str, Enum):
    """Connection between a device and a PC"""

    CAMERALINK = "CameraLink"
    COAX = "Coax"
    ETH = "Ethernet"
    PCIE = "PCIe"
    PXI = "PXI"
    USB = "USB"
    OTHER = "Other"


class FilterType(str, Enum):
    """Filter type"""

    BANDPASS = "Band pass"
    DICHROIC = "Dichroic"
    LONGPASS = "Long pass"
    MULTIBAND = "Multiband"
    ND = "Neutral density"
    NOTCH = "Notch"
    SHORTPASS = "Short pass"


class FilterSize(int, Enum):
    """Filter size value"""

    FILTER_SIZE_25 = 25
    FILTER_SIZE_32 = 32


class LensSize(int, Enum):
    """Lens size value"""

    LENS_SIZE_1 = 1
    LENS_SIZE_2 = 2


class CameraChroma(str, Enum):
    """Color vs. black & white"""

    COLOR = "Color"
    BW = "Monochrome"


class DaqChannelType(str, Enum):
    """DAQ Channel type"""

    AI = "Analog Input"
    AO = "Analog Output"
    DI = "Digital Input"
    DO = "Digital Output"


class ImmersionMedium(str, Enum):
    """Immersion medium name"""

    AIR = "air"
    MULTI = "multi"
    OIL = "oil"
    PBS = "PBS"
    WATER = "water"
    OTHER = "other"
    EASYINDEX = "easy index"
    ECI = "ethyl cinnimate"
    ACB = "aqueous clearing buffer"


class ObjectiveType(str, Enum):
    """Objective type for Slap2"""

    REMOTE = "Remote"
    PRIMARY = "Primary"


class CameraTarget(str, Enum):
    """Target of camera"""

    BODY = "Body"
    BRAIN = "Brain"
    EYE = "Eye"
    FACE = "Face"
    TONGUE = "Tongue"
    OTHER = "Other"


class ProbeModel(str, Enum):
    """Probe model name"""

    MI_ULED_PROBE = "Michigan uLED Probe (Version 1)"
    MP_PHOTONIC_V1 = "MPI Photonic Probe (Version 1)"
    NP_OPTO_DEMONSTRATOR = "Neuropixels Opto (Demonstrator)"
    NP_UHD_FIXED = "Neuropixels UHD (Fixed)"
    NP_UHD_SWITCHABLE = "Neuropixels UHD (Switchable)"
    NP1 = "Neuropixels 1.0"
    NP2_SINGLE_SHANK = "Neuropixels 2.0 (Single Shank)"
    NP2_MULTI_SHANK = "Neuropixels 2.0 (Multi Shank)"
    NP2_QUAD_BASE = "Neuropixels 2.0 (Quad Base)"


class DetectorType(str, Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "Photomultiplier Tube"
    OTHER = "Other"


class Cooling(str, Enum):
    """Cooling medium name"""

    AIR = "Air"
    WATER = "Water"
    NONE = "None"


class BinMode(str, Enum):
    """Detector binning mode"""

    ADDITIVE = "Additive"
    AVERAGE = "Average"
    NONE = "None"


class FerruleMaterial(str, Enum):
    """Fiber probe ferrule material type name"""

    CERAMIC = "Ceramic"
    STAINLESS_STEEL = "Stainless steel"


class SpoutSide(str, Enum):
    """Spout sides"""

    LEFT = "Left"
    RIGHT = "Right"
    CENTER = "Center"
    OTHER = "Other"


class ScannerLocation(str, Enum):
    """location of scanner"""

    FRED_HUTCH = "Fred Hutch"
    UW_SLU = "UW SLU"


class MagneticStrength(int, Enum):
    """Strength of magnet"""

    MRI_7T = 7
    MRI_14T = 14


class LickSensorType(str, Enum):
    """Type of lick sensor"""

    CAPACITIVE = "Capacitive"
    CONDUCTIVE = "Conductive"
    PIEZOELECTIC = "Piezoelectric"


class MyomatrixArrayType(str, Enum):
    """Type of Myomatrix array"""

    INJECTED = "Injected"
    SUTURED = "Sutured"


class Device(DataModel):
    """Generic device"""

    name: str = Field(..., title="Device name")
    serial_number: Optional[str] = Field(default=None, title="Serial number")
    manufacturer: Optional[Organization.ONE_OF] = Field(default=None, title="Manufacturer")
    model: Optional[str] = Field(default=None, title="Model")
    path_to_cad: Optional[str] = Field(
        default=None, title="Path to CAD diagram", description="For CUSTOM manufactured devices"
    )
    port_index: Optional[str] = Field(default=None, title="Port index")
    additional_settings: Optional[GenericModelType] = Field(default=None, title="Additional parameters")
    notes: Optional[str] = Field(default=None, title="Notes")

    # Position information
    position: Optional[Annotated[
        Union[
            Position,
            RelativePosition,
        ], Field(discriminator="object_type")
    ]] = Field(
        default=None,
        title="Position",
        description="Position of the device in the instrument's CoordinateSpace",)


class Software(DataModel):
    """Description of generic software"""

    name: str = Field(..., title="Software name")
    version: str = Field(..., title="Software version")
    url: Optional[str] = Field(default=None, title="URL to commit being used")
    parameters: GenericModelType = Field(GenericModel(), title="Software parameters")


class Calibration(DataModel):
    """Generic calibration class"""

    calibration_date: AwareDatetimeWithDefault = Field(..., title="Date and time of calibration")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: GenericModelType = Field(GenericModel(), description="Calibration input", title="inputs")
    output: GenericModelType = Field(GenericModel(), description="Calibration output", title="outputs")
    notes: Optional[str] = Field(default=None, title="Notes")


class Maintenance(DataModel):
    """Generic maintenance class"""

    maintenance_date: AwareDatetimeWithDefault = Field(..., title="Date and time of maintenance")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID")
    reagents: List[Reagent] = Field(default=[], title="Reagents")
    notes: Optional[str] = Field(default=None, title="Notes")


class Detector(Device):
    """Description of a generic detector"""

    detector_type: DetectorType = Field(..., title="Detector Type")
    manufacturer: Organization.DETECTOR_MANUFACTURERS
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(default=Cooling.NONE, title="Cooling")
    computer_name: Optional[str] = Field(default=None, title="Name of computer receiving data from this camera")
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
    bin_mode: BinMode = Field(default=BinMode.NONE, title="Detector binning mode")
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


class Filter(Device):
    """Filter used in a light path"""

    # required fields
    filter_type: FilterType = Field(..., title="Type of filter")
    manufacturer: Organization.FILTER_MANUFACTURERS

    # optional fields
    diameter: Optional[Decimal] = Field(default=None, title="Diameter (mm)")
    width: Optional[Decimal] = Field(default=None, title="Width (mm)")
    height: Optional[Decimal] = Field(default=None, title="Height (mm)")
    size_unit: SizeUnit = Field(default=SizeUnit.MM, title="Size unit")
    thickness: Optional[Decimal] = Field(default=None, title="Thickness (mm)", ge=0)
    thickness_unit: Optional[SizeUnit] = Field(default=None, title="Thickness unit")
    filter_wheel_index: Optional[int] = Field(default=None, title="Filter wheel index")
    cut_off_wavelength: Optional[int] = Field(default=None, title="Cut-off wavelength (nm)")
    cut_on_wavelength: Optional[int] = Field(default=None, title="Cut-on wavelength (nm)")
    center_wavelength: Optional[int] = Field(default=None, title="Center wavelength (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    description: Optional[str] = Field(
        default=None,
        title="Description",
        description="More details about filter properties and where/how it is being used",
    )


class Lens(Device):
    """Lens"""

    # required fields
    manufacturer: Organization.LENS_MANUFACTURERS

    # optional fields
    focal_length: Optional[Decimal] = Field(default=None, title="Focal length of the lens (mm)")
    focal_length_unit: Optional[SizeUnit] = Field(default=None, title="Focal length unit")
    size: Optional[LensSize] = Field(default=None, title="Size (inches)")
    lens_size_unit: SizeUnit = Field(default=SizeUnit.IN, title="Lens size unit")
    optimized_wavelength_range: Optional[str] = Field(default=None, title="Optimized wavelength range (nm)")
    wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Wavelength unit")
    max_aperture: Optional[str] = Field(default=None, title="Max aperture (e.g. f/2)")


class MotorizedStage(Device):
    """Description of motorized stage"""

    travel: Decimal = Field(..., title="Travel of device (mm)")
    travel_unit: SizeUnit = Field(default=SizeUnit.MM, title="Travel unit")

    # optional fields
    firmware: Optional[str] = Field(default=None, title="Firmware")


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


class CameraAssembly(DataModel):
    """Named assembly of a camera and lens (and optionally a filter)"""

    # required fields
    name: str = Field(..., title="Camera assembly name")
    camera_target: CameraTarget = Field(..., title="Camera target")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: Optional[Filter] = Field(default=None, title="Filter")


class DAQChannel(DataModel):
    """Named input or output channel on a DAQ device"""

    # required fields
    channel_name: str = Field(..., title="DAQ channel name")
    device_name: str = Field(..., title="Name of connected device")
    channel_type: DaqChannelType = Field(..., title="DAQ channel type")

    # optional fields
    port: Optional[int] = Field(default=None, title="DAQ port")
    channel_index: Optional[int] = Field(default=None, title="DAQ channel index")
    sample_rate: Optional[Decimal] = Field(default=None, title="DAQ channel sample rate (Hz)")
    sample_rate_unit: Optional[FrequencyUnit] = Field(default=None, title="Sample rate unit")
    event_based_sampling: Optional[bool] = Field(
        default=None, title="Set to true if DAQ channel is sampled at irregular intervals"
    )


class DAQDevice(Device):
    """Data acquisition device containing multiple I/O channels"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS
    computer_name: str = Field(..., title="Name of computer controlling this DAQ")

    # optional fields
    channels: List[DAQChannel] = Field(default=[], title="DAQ channels")
    firmware_version: Optional[str] = Field(default=None, title="Firmware version")
    hardware_version: Optional[str] = Field(default=None, title="Hardware version")


class HarpDevice(DAQDevice):
    """DAQ that uses the Harp protocol for synchronization and data transmission"""

    # required fields
    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS = Field(default=Organization.OEPS)
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
    maximum_power: Optional[Decimal] = Field(default=None, title="Maximum power (mW)")
    power_unit: PowerUnit = Field(default=PowerUnit.MW, title="Power unit")
    coupling: Optional[Coupling] = Field(default=None, title="Coupling")
    coupling_efficiency: Optional[Decimal] = Field(
        default=None,
        title="Coupling efficiency (percent)",
        ge=0,
        le=100,
    )
    coupling_efficiency_unit: Literal["percent"] = Field(default="percent", title="Coupling efficiency unit")
    item_number: Optional[str] = Field(default=None, title="Item number")


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
    light: Annotated[Union[Laser, LightEmittingDiode, Lamp], Field(discriminator="object_type")]
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
    data_interface: Literal[DataInterface.PXI] = DataInterface.PXI
    manufacturer: Annotated[Union[type(Organization.IMEC)], Field(default=Organization.IMEC, discriminator="name")]


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


class Patch(Device):
    """Description of a patch cord"""

    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(default=None, title="Photobleaching date")


class LaserAssembly(DataModel):
    """Assembly for optogenetic stimulation"""

    name: str = Field(..., title="Laser assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: List[Laser] = Field(..., title="Lasers connected to this module")
    collimator: Device = Field(..., title="Collimator")
    fiber: Patch = Field(..., title="Fiber patch")


class Headstage(Device):
    """Headstage used with an ephys probe"""


class EphysProbe(Device):
    """Named probe used in an ephys experiment"""

    # required fields
    probe_model: ProbeModel = Field(..., title="Probe model")

    # optional fields
    lasers: List[Laser] = Field(default=[], title="Lasers connected to this probe")
    headstage: Optional[Headstage] = Field(default=None, title="Headstage for this probe")


class EphysAssembly(DataModel):
    """Module for electrophysiological recording"""

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
    line_shear_units: SizeUnit = Field(default=SizeUnit.PX, title="Line shear units")


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
    internal_material: str = Field(..., title="Internal material")
    external_material: str = Field(..., title="External material")
    grounded: bool = Field(..., title="Grounded")
    laser_interlock: bool = Field(..., title="Laser interlock")
    air_filtration: bool = Field(..., title="Air filtration")


class MousePlatform(Device):
    """Description of a mouse platform"""

    surface_material: Optional[str] = Field(default=None, title="Surface material")
    date_surface_replaced: Optional[datetime] = Field(default=None, title="Date surface replaced")


class Disc(MousePlatform):
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


class Wheel(MousePlatform):
    """Description of a running wheel"""

    radius: Decimal = Field(..., title="Radius (mm)")
    width: Decimal = Field(..., title="Width (mm)")
    size_unit: SizeUnit = Field(default=SizeUnit.MM, title="Size unit")
    encoder: Device = Field(..., title="Encoder")
    encoder_output: Optional[DAQChannel] = Field(default=None, title="Encoder DAQ channel")
    pulse_per_revolution: int = Field(..., title="Pulse per revolution")
    magnetic_brake: Device = Field(..., title="Magnetic brake")
    brake_output: Optional[DAQChannel] = Field(default=None, title="Brake DAQ channel")
    torque_sensor: Device = Field(..., title="Torque sensor")
    torque_output: Optional[DAQChannel] = Field(default=None, title="Torque DAQ channel")


class Tube(MousePlatform):
    """Description of a tube platform"""

    diameter: Decimal = Field(..., title="Diameter", ge=0)
    diameter_unit: SizeUnit = Field(default=SizeUnit.CM, title="Diameter unit")


class Treadmill(MousePlatform):
    """Description of treadmill platform"""

    treadmill_width: Decimal = Field(..., title="Width of treadmill (mm)")
    width_unit: SizeUnit = Field(default=SizeUnit.CM, title="Width unit")
    encoder: Device = Field(..., title="Encoder")
    pulse_per_revolution: int = Field(..., title="Pulse per revolution")


class Arena(MousePlatform):
    """Description of a rectangular arena"""

    size: Scale = Field(..., title="3D Size")
    objects_in_arena: List[Device] = Field(default=[], title="Objects in arena")


class Monitor(Device):
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


class RewardSpout(Device):
    """Description of a reward spout"""

    side: SpoutSide = Field(..., title="Spout side", description="If Other use notes")
    spout_diameter: Decimal = Field(..., title="Spout diameter (mm)")
    spout_diameter_unit: SizeUnit = Field(default=SizeUnit.MM, title="Spout diameter unit")
    solenoid_valve: Device = Field(..., title="Solenoid valve")
    lick_sensor: Device = Field(..., title="Lick sensor")
    lick_sensor_type: Optional[LickSensorType] = Field(default=None, title="Lick sensor type")
    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="after")
    def validate_other(self):
        """Validator for other/notes"""

        if self.side == SpoutSide.OTHER and self.notes is None:
            raise ValueError(
                "Notes cannot be empty if spout side is Other. " "Describe the spout side in the notes field."
            )

        return self


class RewardDelivery(DataModel):
    """Description of reward delivery system"""

    stage_type: Optional[MotorizedStage] = Field(default=None, title="Motorized stage")
    reward_spouts: List[RewardSpout] = Field(..., title="Water spouts")


class Speaker(Device):
    """Description of a speaker for auditory stimuli"""

    manufacturer: Organization.SPEAKER_MANUFACTURERS


class ChannelType(Enum):
    """Olfactometer channel types"""

    ODOR = "Odor"
    CARRIER = "Carrier"


class OlfactometerChannel(DataModel):
    """description of a Olfactometer channel"""

    channel_index: int = Field(..., title="Channel index")
    channel_type: ChannelType = Field(default=ChannelType.ODOR, title="Channel type")
    flow_capacity: Literal[100, 1000] = Field(default=100, title="Flow capacity")
    flow_unit: str = Field(default="mL/min", title="Flow unit")


class Olfactometer(HarpDevice):
    """Description of an olfactometer for odor stimuli"""

    manufacturer: Organization.DAQ_DEVICE_MANUFACTURERS = Field(default=Organization.CHAMPALIMAUD)
    harp_device_type: Annotated[
        Union[type(HarpDeviceType.OLFACTOMETER)], Field(default=HarpDeviceType.OLFACTOMETER, discriminator="name")
    ]
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
    stage_axis_name: StageAxisName = Field(..., title="Name of stage axis")


class OpticalTable(Device):
    """Description of Optical Table"""

    length: Optional[Decimal] = Field(default=None, title="Length (inches)", ge=0)
    width: Optional[Decimal] = Field(default=None, title="Width (inches)", ge=0)
    table_size_unit: SizeUnit = Field(default=SizeUnit.IN, title="Table size unit")
    vibration_control: Optional[bool] = Field(default=None, title="Vibration control")


class Scanner(Device):
    """Description of a MRI Scanner"""

    scanner_location: ScannerLocation = Field(..., title="Scanner location")
    magnetic_strength: MagneticStrength = Field(..., title="Magnetic strength (T)")
    #  TODO: Check if this should go into the units module.
    magnetic_strength_unit: str = Field(default="T", title="Magnetic strength unit")


class MyomatrixArray(Device):
    """Description of a Myomatrix array"""

    array_type: MyomatrixArrayType = Field(..., title="Array type")
