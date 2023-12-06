""" schema for various Devices """

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from aind_data_schema.base import AindModel, OptionalField, OptionalType
from aind_data_schema.models.coordinates import RelativePosition, Size3d
from aind_data_schema.models.manufacturers import InteruniversityMicroelectronicsCenter, Manufacturer
from aind_data_schema.models.reagent import Reagent
from aind_data_schema.models.units import FrequencyUnit, PowerUnit, SizeUnit, SpeedUnit, TemperatureUnit, UnitlessUnit


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


class ObjectiveType(str, Enum):
    """Objective type for Slap2"""

    REMOTE = "Remote"
    PRIMARY = "Primary"


class CameraTarget(str, Enum):
    """Target of camera"""

    BODY = "Body"
    BOTTOM = "Bottom"
    EYE = "Eye"
    FACE_BOTTOM = "Face bottom"
    FACE_FORWARD = "Face forward"
    FACE_SIDE = "Face side"
    SIDE = "Side"
    TONGUE = "Tongue"
    OTHER = "Other"


class HarpDeviceType(str, Enum):
    """Harp device type"""

    BEHAVIOR = "Behavior"
    CAMERA_CONTROLLER = "Camera Controller"
    LOAD_CELLS = "Load Cells"
    SOUND_BOARD = "Sound Board"
    TIMESTAMP_GENERATOR = "Timestamp Generator"
    INPUT_EXPANDER = "Input Expander"


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


class HeadstageModel(str, Enum):
    """Headstage model name"""

    RHD_16_CH = "Intan RHD 16-channel"
    RHD_32_CH = "Intan RHD 32-channel"
    RHD_64_CH = "Intan RHD 64-channel"


class DetectorType(str, Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class Cooling(str, Enum):
    """Cooling medium name"""

    AIR = "air"
    WATER = "water"


class BinMode(str, Enum):
    """Detector binning mode"""

    ADDITIVE = "additive"
    AVERAGE = "average"
    NONE = "none"


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


class MriScanSequence(str, Enum):
    """MRI scan sequence"""

    RARE = "RARE"
    OTHER = "Other"


class ScanType(str, Enum):
    """Type of scan"""

    SETUP = "Set Up"
    SCAN_3D = "3D Scan"


class ScannerLocation(str, Enum):
    """location of scanner"""

    FRED_HUTCH = "Fred Hutch"
    UW_SLU = "UW SLU"


class MagneticStrength(int, Enum):
    """Strength of magnet"""

    MRI_7T = 7
    MRI_14T = 14


class Device(AindModel):
    """Generic device"""

    device_type: str = Field(..., title="Device type")  # Needs to be set by child classes that inherits
    name: OptionalType[str] = OptionalField(title="Device name")
    serial_number: OptionalType[str] = OptionalField(title="Serial number")
    manufacturer: OptionalType[Manufacturer.ONE_OF] = OptionalField(title="Manufacturer")
    model: OptionalType[str] = OptionalField(title="Model")
    path_to_cad: OptionalType[str] = OptionalField(
        title="Path to CAD diagram", description="For CUSTOM manufactured devices"
    )
    notes: OptionalType[str] = OptionalField(title="Notes")


class Software(AindModel):
    """Description of generic software"""

    name: str = Field(..., title="Software name")
    version: str = Field(..., title="Software version")
    url: OptionalType[str] = OptionalField(title="URL to commit being used")
    parameters: Dict[str, Any] = Field(dict(), title="Software parameters")


class Calibration(AindModel):
    """Generic calibration class"""

    calibration_date: datetime = Field(..., title="Date and time of calibration")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: Dict[str, Any] = Field(dict(), description="Calibration input", title="inputs")
    output: Dict[str, Any] = Field(dict(), description="Calibration output", title="outputs")
    notes: OptionalType[str] = OptionalField(title="Notes")


class Maintenance(AindModel):
    """Generic maintenance class"""

    maintenance_date: datetime = Field(..., title="Date and time of maintenance")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: OptionalType[str] = OptionalField(title="Protocol ID")
    reagents: List[Reagent] = Field([], title="Reagents")
    notes: OptionalType[str] = OptionalField(title="Notes")


class Camera(Device):
    """Device that acquires images and streams them to a computer"""

    device_type: Literal["Camera"] = "Camera"
    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: Manufacturer.CAMERA_MANUFACTURERS
    computer_name: str = Field(..., title="Name of computer receiving data from this camera")
    max_frame_rate: Decimal = Field(..., title="Maximum frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    pixel_width: int = Field(..., title="Width of the sensor in pixels")
    pixel_height: int = Field(..., title="Height of the sensor in pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    chroma: CameraChroma = Field(..., title="Color or Monochrome")

    # optional fields
    sensor_format: OptionalType[str] = OptionalField(title="Size of the sensor")
    format_unit: OptionalType[str] = OptionalField(title="Format unit")
    recording_software: OptionalType[Software] = OptionalField(title="Recording software")
    driver: OptionalType[DeviceDriver] = OptionalField(title="Driver")
    driver_version: OptionalType[str] = OptionalField(title="Driver version")


class Filter(Device):
    """Filter used in a light path"""

    device_type: Literal["Filter"] = "Filter"
    # required fields
    filter_type: FilterType = Field(..., title="Type of filter")
    manufacturer: Manufacturer.FILTER_MANUFACTURERS

    # optional fields
    diameter: OptionalType[Decimal] = OptionalField(title="Diameter (mm)")
    width: OptionalType[Decimal] = OptionalField(title="Width (mm)")
    height: OptionalType[Decimal] = OptionalField(title="Height (mm)")
    size_unit: SizeUnit = Field(SizeUnit.MM, title="Size unit")
    thickness: OptionalType[Decimal] = OptionalField(title="Thickness (mm)", ge=0)
    thickness_unit: SizeUnit = Field(SizeUnit.MM, title="Thickness unit")
    filter_wheel_index: OptionalType[int] = OptionalField(title="Filter wheel index")
    cut_off_wavelength: OptionalType[int] = OptionalField(title="Cut-off wavelength (nm)")
    cut_on_wavelength: OptionalType[int] = OptionalField(title="Cut-on wavelength (nm)")
    center_wavelength: OptionalType[int] = OptionalField(title="Center wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    description: OptionalType[str] = OptionalField(
        title="Description",
        description="More details about filter properties and where/how it is being used",
    )


class Lens(Device):
    """Lens used to focus light onto a camera sensor"""

    device_type: Literal["Lens"] = "Lens"

    # required fields
    manufacturer: Manufacturer.LENS_MANUFACTURERS

    # optional fields
    focal_length: OptionalType[Decimal] = OptionalField(title="Focal length of the lens (mm)")
    focal_length_unit: SizeUnit = Field(SizeUnit.MM, title="Focal length unit")
    size: OptionalType[LensSize] = OptionalField(title="Size (inches)")
    lens_size_unit: SizeUnit = Field(SizeUnit.IN, title="Lens size unit")
    optimized_wavelength_range: OptionalType[str] = OptionalField(title="Optimized wavelength range (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    max_aperture: OptionalType[str] = OptionalField(title="Max aperture (e.g. f/2)")


class MotorizedStage(Device):
    """Description of motorized stage"""

    device_type: Literal["Motorized stage"] = "Motorized stage"
    travel: Decimal = Field(..., title="Travel of device (mm)")
    travel_unit: SizeUnit = Field(SizeUnit.MM, title="Travel unit")

    # optional fields
    firmware: OptionalType[str] = OptionalField(title="Firmware")


class Objective(Device):
    """Description of an objective device"""

    device_type: Literal["Objective"] = "Objective"
    numerical_aperture: Decimal = Field(..., title="Numerical aperture (in air)")
    magnification: Decimal = Field(..., title="Magnification")
    immersion: ImmersionMedium = Field(..., title="Immersion")
    objective_type: OptionalType[ObjectiveType] = OptionalField(title="Objective type")


class CameraAssembly(AindModel):
    """Named assembly of a camera and lens (and optionally a filter)"""

    # required fields
    camera_assembly_name: str = Field(..., title="Camera assembly name")
    camera_target: CameraTarget = Field(..., title="Camera target")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: OptionalType[Filter] = OptionalField(title="Filter")
    position: OptionalType[RelativePosition] = OptionalField(title="Relative position of this assembly")


class DAQChannel(AindModel):
    """Named input or output channel on a DAQ device"""

    # required fields
    channel_name: str = Field(..., title="DAQ channel name")
    device_name: str = Field(..., title="Name of connected device")
    channel_type: DaqChannelType = Field(..., title="DAQ channel type")

    # optional fields
    port: OptionalType[int] = OptionalField(title="DAQ port")
    channel_index: OptionalType[int] = OptionalField(title="DAQ channel index")
    sample_rate: OptionalType[Decimal] = OptionalField(title="DAQ channel sample rate (Hz)")
    sample_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Sample rate unit")
    event_based_sampling: OptionalType[bool] = OptionalField(
        title="Set to true if DAQ channel is sampled at irregular intervals"
    )


class DAQDevice(Device):
    """Data acquisition device containing multiple I/O channels"""

    # required fields
    device_type: Literal["DAQ Device"] = "DAQ Device"
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: Manufacturer.DAQ_DEVICE_MANUFACTURERS
    computer_name: str = Field(..., title="Name of computer controlling this DAQ")

    # optional fields
    channels: List[DAQChannel] = Field([], title="DAQ channels")


class HarpDevice(DAQDevice):
    """DAQ that uses the Harp protocol for synchronization and data transmission"""

    # required fields
    device_type: Literal["Harp device"] = "Harp device"
    harp_device_type: HarpDeviceType = Field(..., title="Type of Harp device")
    harp_device_version: str = Field(..., title="Device version")

    # fixed values
    manufacturer: Manufacturer.DAQ_DEVICE_MANUFACTURERS = Field(default=Manufacturer.OEPS)
    data_interface: Literal[DataInterface.USB] = DataInterface.USB


class Laser(Device):
    """Laser module with a specific wavelength (may be a sub-component of a larger assembly)"""

    # required fields
    device_type: Literal["Laser"] = "Laser"
    manufacturer: Manufacturer.LASER_MANUFACTURERS
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")

    # optional fields
    maximum_power: OptionalType[Decimal] = OptionalField(title="Maximum power (mW)")
    power_unit: PowerUnit = Field(PowerUnit.MW, title="Power unit")
    coupling: OptionalType[Coupling] = OptionalField(title="Coupling")
    coupling_efficiency: OptionalType[Decimal] = OptionalField(
        title="Coupling efficiency (percent)",
        ge=0,
        le=100,
    )
    coupling_efficiency_unit: Literal["percent"] = Field("percent", title="Coupling efficiency unit")
    item_number: OptionalType[str] = OptionalField(title="Item number")


class LightEmittingDiode(Device):
    """Description of a Light Emitting Diode (LED) device"""

    device_type: Literal["Light emitting diode"] = "Light emitting diode"
    manufacturer: Manufacturer.LED_MANUFACTURERS
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")


class Lamp(Device):
    """Description of a Lamp lightsource"""

    device_type: Literal["Lamp"] = "Lamp"
    wavelength_min: OptionalType[int] = OptionalField(title="Wavelength minimum (nm)")
    wavelength_max: OptionalType[int] = OptionalField(title="Wavelength maximum (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    temperature: OptionalType[int] = OptionalField(title="Temperature (K)")
    temperature_unit: TemperatureUnit = Field(TemperatureUnit.K, title="Temperature unit")


class ProbePort(AindModel):
    """Port for a probe connection"""

    index: int = Field(..., title="One-based port index")
    probes: List[str] = Field(..., title="Names of probes connected to this port")


class NeuropixelsBasestation(DAQDevice):
    """PXI-based Neuropixels DAQ"""

    # required fields
    device_type: Literal["Neuropixels basestation"] = "Neuropixels basestation"
    basestation_firmware_version: str = Field(..., title="Basestation firmware version")
    bsc_firmware_version: str = Field(..., title="Basestation connect board firmware")
    slot: int = Field(..., title="Slot number for this basestation")
    ports: List[ProbePort] = Field(..., title="Basestation ports")

    # fixed values
    data_interface: Literal[DataInterface.PXI] = DataInterface.PXI
    manufacturer: InteruniversityMicroelectronicsCenter = Field(Manufacturer.IMEC, json_schema_extra={"const": True})


class OpenEphysAcquisitionBoard(DAQDevice):
    """Multichannel electrophysiology DAQ"""

    # required fields
    device_type: Literal["Open Ephys Acquisition Board"] = "Open Ephys Acquisition Board"
    ports: List[ProbePort] = Field(..., title="Acquisition board ports")

    # fixed values
    data_interface: Literal[DataInterface.USB] = DataInterface.USB
    manufacturer: Manufacturer.DAQ_DEVICE_MANUFACTURERS = Field(default=Manufacturer.OEPS)


class Manipulator(Device):
    """Manipulator used on a dome module"""

    device_type: Literal["Manipulator"] = "Manipulator"
    manufacturer: Manufacturer.MANIPULATOR_MANUFACTURERS


class StickMicroscopeAssembly(AindModel):
    """Stick microscope used to monitor probes during insertion"""

    scope_assembly_name: str = Field(..., title="Scope assembly name")
    camera: Camera = Field(..., title="Camera for this module")
    lens: Lens = Field(..., title="Lens for this module")


class LaserAssembly(AindModel):
    """Assembly for optogenetic stimulation"""

    laser_assembly_name: str = Field(..., title="Laser assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    lasers: List[Laser] = Field(..., title="Lasers connected to this module")


class Headstage(Device):
    """Headstage used with an ephys probe"""

    device_type: Literal["Headstage"] = "Headstage"
    headstage_model: OptionalType[HeadstageModel] = OptionalField(title="Headstage model")


class EphysProbe(Device):
    """Named probe used in an ephys experiment"""

    # required fields
    device_type: Literal["Ephys probe"] = "Ephys probe"
    probe_model: ProbeModel = Field(..., title="Probe model")

    # optional fields
    lasers: List[Laser] = Field([], title="Lasers connected to this probe")
    headstage: OptionalType[Headstage] = OptionalField(title="Headstage for this probe")


class EphysAssembly(AindModel):
    """Module for electrophysiological recording"""

    ephys_assembly_name: str = Field(..., title="Ephys assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    probes: List[EphysProbe] = Field(..., title="Probes that are held by this module")


class Detector(Device):
    """Description of a generic detector"""

    device_type: Literal["Detector"] = "Detector"
    detector_type: DetectorType = Field(..., title="Detector Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: OptionalType[ImmersionMedium] = OptionalField(title="Immersion")
    chroma: OptionalType[CameraChroma] = OptionalField(title="Camera chroma")
    sensor_width: OptionalType[int] = OptionalField(title="Width of the sensor in pixels")
    sensor_height: OptionalType[int] = OptionalField(title="Height of the sensor in pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    bit_depth: OptionalType[int] = OptionalField(title="Bit depth")
    bin_mode: BinMode = Field(BinMode.NONE, title="Detector binning mode")
    bin_width: OptionalType[int] = OptionalField(title="Bin width")
    bin_height: OptionalType[int] = OptionalField(title="Bin height")
    bin_unit: SizeUnit = Field(SizeUnit.PX, title="Bin size unit")
    gain: OptionalType[Decimal] = OptionalField(title="Gain")
    crop_width: OptionalType[int] = OptionalField(title="Crop width")
    crop_height: OptionalType[int] = OptionalField(title="Crop width")
    crop_unit: SizeUnit = Field(SizeUnit.PX, title="Crop size unit")


class FiberProbe(Device):
    """Description of a fiber optic probe"""

    device_type: Literal["Fiber optic probe"] = "Fiber optic probe"
    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    #  TODO: Check if this should be an enum?
    core_diameter_unit: str = Field("um", title="Core diameter unit")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    ferrule_material: OptionalType[FerruleMaterial] = OptionalField(title="Ferrule material")
    active_length: OptionalType[Decimal] = OptionalField(title="Active length (mm)", description="Length of taper")
    total_length: Decimal = Field(..., title="Total length (mm)")
    length_unit: SizeUnit = Field(SizeUnit.MM, title="Length unit")


class Patch(Device):
    """Description of a patch cord"""

    device_type: Literal["Patch"] = "Patch"
    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    photobleaching_date: OptionalType[date] = OptionalField(title="Photobleaching date")


class FiberAssembly(AindModel):
    """Module for inserted fiber photometry recording"""

    fiber_assembly_name: str = Field(..., title="Ephys assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    fibers: List[FiberProbe] = Field(..., title="Probes that are held by this module")


class DigitalMicromirrorDevice(Device):
    """Description of a Digital Micromirror Device (DMD)"""

    device_type: Literal["Digital Micromirror Device"] = "Digital Micromirror Device"
    max_dmd_patterns: int = Field(..., title="Max DMD patterns")
    double_bounce_design: bool = Field(..., title="Double bounce design")
    invert_pixel_values: bool = Field(..., title="Invert pixel values")
    motion_padding_x: int = Field(..., title="Motion padding X (pixels)")
    motion_padding_y: int = Field(..., title="Motion padding Y (pixels)")
    padding_unit: SizeUnit = Field(SizeUnit.PX, title="Padding unit")
    pixel_size: Decimal = Field(..., title="DMD Pixel size")
    pixel_size_unit: SizeUnit = Field(SizeUnit.UM, title="Pixel size unit")
    start_phase: Decimal = Field(..., title="DMD Start phase (fraction of cycle)")
    dmd_flip: bool = Field(..., title="DMD Flip")
    dmd_curtain: List[Decimal] = Field(..., title="DMD Curtain")
    dmd_curtain_unit: SizeUnit = Field(SizeUnit.PX, title="dmd_curtain_unit")
    line_shear: List[int] = Field(..., title="Line shear (pixels)")
    line_shear_units: SizeUnit = Field(SizeUnit.PX, title="Line shear units")


class PolygonalScanner(Device):
    """Description of a Polygonal scanner"""

    device_type: Literal["Polygonal Scanner"] = "Polygonal Scanner"
    speed: int = Field(..., title="Speed (rpm)")
    speed_unit: SpeedUnit = Field(SpeedUnit.RPM, title="Speed unit")
    number_faces: int = Field(..., title="Number of faces")


class PockelsCell(Device):
    """Description of a Pockels Cell"""

    device_type: Literal["Pockels Cell"] = "Pockels Cell"
    polygonal_scanner: str = Field(..., title="Polygonal scanner", description="Must match name of Polygonal scanner")
    on_time: Decimal = Field(..., title="On time (fraction of cycle)")
    off_time: Decimal = Field(..., title="Off time (fraction of cycle)")
    time_setting_unit: UnitlessUnit = Field(UnitlessUnit.FC, title="time setting unit")


class Enclosure(Device):
    """Description of an enclosure"""

    device_type: Literal["Enclosure"] = "Enclosure"
    size: Size3d = Field(..., title="Size")
    internal_material: str = Field(..., title="Internal material")
    external_material: str = Field(..., title="External material")
    grounded: bool = Field(..., title="Grounded")
    laser_interlock: bool = Field(..., title="Laser interlock")
    air_filtration: bool = Field(..., title="Air filtration")


class MousePlatform(Device):
    """Description of a mouse platform"""

    device_type: Literal["Mouse platform"] = "Mouse platform"
    surface_material: OptionalType[str] = OptionalField(title="Surface material")
    date_surface_replaced: OptionalType[datetime] = OptionalField(title="Date surface replaced")


class Disc(MousePlatform):
    """Description of a running disc (i.e. MindScope Disc)"""

    device_type: Literal["Disc"] = "Disc"
    radius: Decimal = Field(..., title="Radius (cm)", ge=0)
    radius_unit: SizeUnit = Field(SizeUnit.CM, title="radius unit")
    output: OptionalType[DaqChannelType] = OptionalField(description="analog or digital electronics")
    encoder: OptionalType[str] = OptionalField(title="Encoder", description="Encoder hardware type")
    decoder: OptionalType[str] = OptionalField(title="Decoder", description="Decoder chip type")
    encoder_firmware: OptionalType[Software] = OptionalField(
        title="Encoder firmware",
        description="Firmware to read from decoder chip counts",
    )


class Wheel(MousePlatform):
    """Description of a running wheel"""

    device_type: Literal["Wheel"] = "Wheel"
    radius: Decimal = Field(..., title="Radius (mm)")
    width: Decimal = Field(..., title="Width (mm)")
    size_unit: SizeUnit = Field(SizeUnit.MM, title="Size unit")
    encoder: Device = Field(..., title="Encoder")
    encoder_output: OptionalType[DaqChannelType] = OptionalField(title="Encoder DAQ channel")
    pulse_per_revolution: int = Field(..., title="Pulse per revolution")
    magnetic_brake: Device = Field(..., title="Magnetic brake")
    brake_output: OptionalType[DaqChannelType] = OptionalField(title="Brake DAQ channel")
    torque_sensor: Device = Field(..., title="Torque sensor")
    torque_output: OptionalType[DaqChannelType] = OptionalField(title="Torque DAQ channel")


class Tube(MousePlatform):
    """Description of a tube platform"""

    device_type: Literal["Tube"] = "Tube"
    diameter: Decimal = Field(..., title="Diameter", ge=0)
    diameter_unit: SizeUnit = Field(SizeUnit.CM, title="Diameter unit")


class Treadmill(MousePlatform):
    """Description of treadmill platform"""

    device_type: Literal["Treadmill"] = "Treadmill"
    treadmill_width: Decimal = Field(..., title="Width of treadmill (mm)")
    width_unit: SizeUnit = Field(SizeUnit.CM, title="Width unit")


class Monitor(Device):
    """Description of visual display for visual stimuli"""

    device_type: Literal["Monitor"] = "Monitor"
    manufacturer: Manufacturer.MONITOR_MANUFACTURERS
    refresh_rate: int = Field(..., title="Refresh rate (Hz)", ge=60)
    width: int = Field(..., title="Width (pixels)")
    height: int = Field(..., title="Height (pixels)")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    viewing_distance: Decimal = Field(..., title="Viewing distance (cm)")
    viewing_distance_unit: SizeUnit = Field(SizeUnit.CM, title="Viewing distance unit")
    position: OptionalType[RelativePosition] = OptionalField(title="Relative position of the monitor")
    contrast: OptionalType[int] = OptionalField(
        description="Monitor's contrast setting",
        title="Contrast",
        ge=0,
        le=100,
    )
    brightness: OptionalType[int] = OptionalField(
        description="Monitor's brightness setting",
        title="Brightness",
        ge=0,
        le=100,
    )


class RewardSpout(Device):
    """Description of a reward spout"""

    device_type: Literal["Reward spout"] = "Reward spout"
    side: SpoutSide = Field(..., title="Spout side", description="If Other use notes")
    spout_diameter: Decimal = Field(..., title="Spout diameter (mm)")
    spout_diameter_unit: SizeUnit = Field(SizeUnit.MM, title="Spout diameter unit")
    spout_position: OptionalType[RelativePosition] = OptionalField(title="Spout stage position")
    solenoid_valve: Device = Field(..., title="Solenoid valve")
    notes: OptionalType[str] = OptionalField(title="Notes")


class RewardDelivery(AindModel):
    """Description of reward delivery system"""

    device_type: Literal["Reward delivery"] = "Reward delivery"
    stage_type: MotorizedStage = Field(None, title="Motorized stage")
    reward_spouts: List[RewardSpout] = Field(..., title="Water spouts")


class Speaker(Device):
    """Description of a speaker for auditory stimuli"""

    device_type: Literal["Speaker"] = "Speaker"
    manufacturer: Manufacturer.SPEAKER_MANUFACTURERS
    position: OptionalType[RelativePosition] = OptionalField(title="Relative position of the monitor")


class Olfactometer(Device):
    """Description of an olfactometer for odor stimuli"""

    device_type: Literal["Olfactometer"] = "Olfactometer"
    position: OptionalType[RelativePosition] = OptionalField(title="Relative position of the monitor")


class AdditionalImagingDevice(Device):
    """Description of additional devices"""

    device_type: Literal["AdditionalImagingDevice"] = "AdditionalImagingDevice"
    type: ImagingDeviceType = Field(..., title="Device type")


class ScanningStage(MotorizedStage):
    """Description of a scanning motorized stages"""

    stage_axis_direction: StageAxisDirection = Field(..., title="Direction of stage axis")
    stage_axis_name: StageAxisName = Field(..., title="Name of stage axis")


class OpticalTable(Device):
    """Description of Optical Table"""

    device_type: Literal["OpticalTable"] = "OpticalTable"
    length: OptionalType[Decimal] = OptionalField(title="Length (inches)", ge=0)
    width: OptionalType[Decimal] = OptionalField(title="Width (inches)", ge=0)
    table_size_unit: SizeUnit = Field(SizeUnit.IN, title="Table size unit")
    vibration_control: OptionalType[bool] = OptionalField(title="Vibration control")


class Scanner(Device):
    """Description of a MRI Scanner"""

    device_type: Literal["Scanner"] = "Scanner"
    scanner_location: ScannerLocation = Field(..., title="Scanner location")
    magnetic_strength: MagneticStrength = Field(..., title="Magnetic strength (T)")
    #  TODO: Check if this should go into the units module
    magnetic_strength_unit: str = Field("T", title="Magnetic strength unit")


MOUSE_PLATFORMS = Annotated[Union[tuple(MousePlatform.__subclasses__())], Field(discriminator="device_type")]
STIMULUS_DEVICES = Annotated[Union[Monitor, Olfactometer, RewardDelivery, Speaker], Field(discriminator="device_type")]
RIG_DAQ_DEVICES = Annotated[
    Union[HarpDevice, NeuropixelsBasestation, OpenEphysAcquisitionBoard, DAQDevice], Field(discriminator="device_type")
]
LIGHT_SOURCES = Annotated[Union[Laser, LightEmittingDiode, Lamp], Field(discriminator="device_type")]
