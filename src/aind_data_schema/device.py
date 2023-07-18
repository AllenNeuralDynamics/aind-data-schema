""" schema for various Devices """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindModel, BaseName, BaseNameEnumMeta, EnumSubset, PIDName


class SizeUnit(Enum):
    """units for sizes"""

    CM = "centimeter"
    IN = "inch"
    MM = "millimeter"
    NM = "nanometer"
    UM = "micrometer"
    PX = "pixel"
    NONE = "none"


class AngleUnit(Enum):
    """orientation units"""

    DEG = "degree"


class FrequencyUnit(Enum):
    """Frequency units"""

    HZ = "Hertz"


class PowerUnit(Enum):
    """Power units"""

    UW = "microwatt"
    MW = "milliwatt"


class DeviceDriver(Enum):
    """DeviceDriver name"""

    OPENGL = "OpenGL"
    VIMBA = "Vimba"
    NVIDIA = "Nvidia Graphics"


class Manufacturer(Enum, metaclass=BaseNameEnumMeta):
    """Device manufacturer name"""

    ALLIED = PIDName(name="Allied")
    ASI = PIDName(
        name="Applied Scientific Instrumentation",
        abbreviation="ASI",
    )
    BASLER = PIDName(name="Basler")
    CAMBRIDGE_TECHNOLOGY = PIDName(name="Cambridge Technology")
    CHROMA = PIDName(name="Chroma")
    COHERENT_SCIENTIFIC = PIDName(
        name="Coherent Scientific",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="031tysd23",
    )
    COMPUTAR = PIDName(name="Computar")
    CUSTOM = PIDName(name="Custom")
    DORIC = PIDName(
        name="Doric",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="059n53q30",
    )
    EALING = PIDName(name="Ealing")
    EDMUND_OPTICS = PIDName(
        name="Edmund Optics",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="01j1gwp17",
    )
    AILIPU = PIDName(name="Ailipu Technology Co")
    FLIR = PIDName(
        name="Teledyne FLIR",
        abbreviation="FLIR",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="01j1gwp17",
    )
    HAMAMATSU = PIDName(
        name="Hamamatsu",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="03natb733",
    )
    IMAGING_SOURCE = PIDName(name="The Imaging Source")
    IMEC = PIDName(
        name="Interuniversity Microelectronics Center",
        abbreviation="IMEC",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="02kcbn207",
    )
    JULABO = PIDName(name="Julabo")
    LEICA = PIDName(name="Leica")
    LG = PIDName(
        name="LG",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="02b948n83",
    )
    LIFECANVAS = PIDName(name="LifeCanvas")
    MIGHTY_ZAP = PIDName(name="IR Robot Co")
    MKS_NEWPORT = PIDName(
        name="MKS Newport",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="00k17f049",
    )
    MPI = PIDName(name="MPI", abbreviation="MPI")
    NATIONAL_INSTRUMENTS = PIDName(
        name="National Instruments",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="026exqw73",
    )
    NEW_SCALE_TECHNOLOGIES = PIDName(name="New Scale Technologies")
    NIKON = PIDName(
        name="Nikon",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="0280y9h11",
    )
    OEPS = PIDName(
        name="Open Ephys Production Site",
        abbreviation="OEPS",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="007rkz355",
    )
    OLYMPUS = PIDName(
        name="Olympus",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="02vcdte90",
    )
    OPTOTUNE = PIDName(name="Optotune")
    OXXIUS = PIDName(name="Oxxius")
    PRIZMATIX = PIDName(name="Prizmatix")
    QUANTIFI = PIDName(name="Quantifi")
    SEMROCK = PIDName(name="Semrock")
    THORLABS = PIDName(
        name="Thorlabs",
        registry=BaseName(name="Research Organization Registry", abbreviation="ROR"),
        registry_identifier="04gsnvb07",
    )
    TMC = PIDName(name="Technical Manufacturing Corporation", abbreviation="TMC")
    VIEWORKS = PIDName(name="Vieworks")
    VORTRAN = PIDName(name="Vortran")
    OTHER = PIDName(name="Other")


class Coupling(Enum):
    """Laser coupling type"""

    FREE_SPACE = "Free-space"
    MMF = "Multi-mode fiber"
    SMF = "Single-mode fiber"
    OTHER = "Other"


class DataInterface(Enum):
    """Connection between a device and a PC"""

    CAMERALINK = "CameraLink"
    COAX = "Coax"
    ETH = "Ethernet"
    PCIE = "PCIe"
    PXI = "PXI"
    USB = "USB"
    OTHER = "Other"


class FilterType(Enum):
    """Filter type"""

    BANDPASS = "Band pass"
    DICHROIC = "Dichroic"
    LONGPASS = "Long pass"
    MULTIBAND = "Multiband"
    ND = "Neutral density"
    NOTCH = "Notch"
    SHORTPASS = "Short pass"


class FilterSize(Enum):
    """Filter size value"""

    FILTER_SIZE_25 = 25
    FILTER_SIZE_32 = 32


class LensSize(Enum):
    """Lens size value"""

    LENS_SIZE_1 = 1
    LENS_SIZE_2 = 2


class CameraChroma(Enum):
    """Color vs. black & white"""

    COLOR = "Color"
    BW = "Monochrome"


class DaqChannelType(Enum):
    """DAQ Channel type"""

    AI = "Analog Input"
    AO = "Analog Output"
    DI = "Digital Input"
    DO = "Digital Output"


class RelativePosition(AindModel):
    """Set of 6 values describing relative position on a rig"""

    pitch: Optional[Decimal] = Field(None, title="Angle pitch (deg)", units="deg", ge=0, le=360)
    yaw: Optional[Decimal] = Field(None, title="Angle yaw (deg)", units="deg", ge=0, le=360)
    roll: Optional[Decimal] = Field(None, title="Angle roll (deg)", units="deg", ge=0, le=360)
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")

    x: Optional[Decimal] = Field(None, title="Position X (mm)", units="mm")
    y: Optional[Decimal] = Field(None, title="Position Y (mm)", units="mm")
    z: Optional[Decimal] = Field(None, title="Position Z (mm)", units="mm")
    position_unit: SizeUnit = Field(SizeUnit.MM, title="Position unit")

    coordinate_system: Optional[str] = Field(None, title="Description of the coordinate system used")


class Size2d(AindModel):
    """2D size of an object"""

    width: int = Field(..., title="Width")
    height: int = Field(..., title="Height")
    unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")


class Orientation3d(AindModel):
    """3D orientation of an object"""

    pitch: Decimal = Field(..., title="Angle pitch", ge=0, le=360)
    yaw: Decimal = Field(..., title="Angle yaw", ge=0, le=360)
    roll: Decimal = Field(..., title="Angle roll", ge=0, le=360)
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class ModuleOrientation2d(AindModel):
    """2D module orientation of an object"""

    arc_angle: Decimal = Field(..., title="Arc angle")
    module_angle: Decimal = Field(..., title="Module angle")
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class ModuleOrientation3d(AindModel):
    """3D module orientation of an object"""

    arc_angle: Decimal = Field(..., title="Arc angle")
    module_angle: Decimal = Field(..., title="Module angle")
    rotation_angle: Decimal = Field(..., title="Rotation angle")
    unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")


class Coordinates3d(AindModel):
    """Coordinates in a 3D grid"""

    x: Decimal = Field(..., title="Position X")
    y: Decimal = Field(..., title="Position Y")
    z: Decimal = Field(..., title="Position Z")
    unit: SizeUnit = Field(SizeUnit.UM, title="Position unit")


class Device(AindModel):
    """Generic device"""

    name: Optional[str] = Field(None, title="Device name")
    serial_number: Optional[str] = Field(None, title="Serial number")
    manufacturer: Optional[Manufacturer] = Field(None, title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    notes: Optional[str] = Field(None, title="Notes")


class Software(AindModel):
    """Description of generic software"""

    name: str = Field(..., title="Software name")
    version: str = Field(..., title="Software version")
    parameters: Optional[dict] = Field(None, title="Software parameters", additionalProperties={"type": "string"})


class MotorizedStage(Device):
    """Description of motorized stage"""

    travel: Decimal = Field(..., title="Travel of device (mm)", units="mm")
    travel_unit: SizeUnit = Field(SizeUnit.MM, title="Travel unit")

    # optional fields
    firmware: Optional[str] = Field(None, title="Firmware")


class Camera(Device):
    """Device that acquires images and streams them to a computer"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: EnumSubset[
        Manufacturer.AILIPU,
        Manufacturer.ALLIED,
        Manufacturer.BASLER,
        Manufacturer.EDMUND_OPTICS,
        Manufacturer.FLIR,
        Manufacturer.IMAGING_SOURCE,
        Manufacturer.THORLABS,
        Manufacturer.OTHER,
    ]
    computer_name: str = Field(..., title="Name of computer receiving data from this camera")
    max_frame_rate: Decimal = Field(..., title="Maximum frame rate (Hz)", units="Hz")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    pixel_width: int = Field(..., title="Width of the sensor in pixels", units="Pixels")
    pixel_height: int = Field(..., title="Height of the sensor in pixels", units="Pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    chroma: CameraChroma = Field(..., title="Color or Monochrome")

    # optional fields
    sensor_format: Optional[str] = Field(None, title="Size of the sensor")
    format_unit: Optional[str] = Field(None, title="Format unit")
    recording_software: Optional[Software] = Field(None, title="Recording software")
    driver: Optional[DeviceDriver] = Field(None, title="Driver")
    driver_version: Optional[str] = Field(None, title="Driver version")


class Lens(Device):
    """Lens used to focus light onto a camera sensor"""

    # required fields
    manufacturer: EnumSubset[Manufacturer.COMPUTAR, Manufacturer.EDMUND_OPTICS, Manufacturer.THORLABS, Manufacturer.OTHER]

    # optional fields
    focal_length: Optional[Decimal] = Field(None, title="Focal length of the lens", units="mm")
    focal_length_unit: SizeUnit = Field(SizeUnit.MM, title="Focal length unit")
    size: Optional[LensSize] = Field(None, title="Size (inches)")
    lens_size_unit: SizeUnit = Field(SizeUnit.IN, title="Lens size unit")
    optimized_wavelength_range: Optional[str] = Field(None, title="Optimized wavelength range (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    max_aperture: Optional[str] = Field(None, title="Max aperture (e.g. f/2)")


class Filter(Device):
    """Filter used in a light path"""

    # required fields
    filter_type: FilterType = Field(..., title="Type of filter")
    manufacturer: EnumSubset[
        Manufacturer.EDMUND_OPTICS,
        Manufacturer.CHROMA,
        Manufacturer.SEMROCK,
        Manufacturer.THORLABS,
        Manufacturer.OTHER,
    ]

    # optional fields
    diameter: Optional[Decimal] = Field(None, title="Diameter (mm)", units="mm")
    width: Optional[Decimal] = Field(None, title="Width (mm)")
    height: Optional[Decimal] = Field(None, title="Height (mm)")
    size_unit: SizeUnit = Field(SizeUnit.MM, title="Size unit")
    thickness: Optional[Decimal] = Field(None, title="Thickness (mm)", ge=0)
    thickness_unit: SizeUnit = Field(SizeUnit.MM, title="Thickness unit")
    filter_wheel_index: Optional[int] = Field(None, title="Filter wheel index")
    cut_off_wavelength: Optional[int] = Field(None, title="Cut-off wavelength (nm)")
    cut_on_wavelength: Optional[int] = Field(None, title="Cut-on wavelength (nm)")
    center_wavelength: Optional[int] = Field(None, title="Center wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    description: Optional[str] = Field(
        None, title="Description", description="More details about filter properties and where/how it is being used"
    )


class Immersion(Enum):
    """Immersion media name"""

    AIR = "air"
    MULTI = "multi"
    OIL = "oil"
    WATER = "water"
    OTHER = "other"


class Objective(Device):
    """Description of an objective device"""

    numerical_aperture: Decimal = Field(..., title="Numerical aperture (in air)")
    magnification: Decimal = Field(..., title="Magnification")
    immersion: Immersion = Field(..., title="Immersion")


class CameraTarget(Enum):
    """Target of camera"""

    BODY = "Body"
    BOTTOM = "Bottom"
    EYE = "Eye"
    FACE_BOTTOM = "Face bottom"
    FACE_SIDE = "Face side"
    SIDE = "Side"
    TONGUE = "Tongue"
    OTHER = "Other"


class CameraAssembly(AindModel):
    """Named assembly of a camera and lens (and optionally a filter)"""

    # required fields
    camera_assembly_name: str = Field(..., title="Camera assembly name")
    camera_target: CameraTarget = Field(..., title="Camera target")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: Optional[Filter] = Field(None, title="Filter")
    position: Optional[RelativePosition] = Field(None, title="Relative position of this assembly")


class DAQChannel(AindModel):
    """Named input or output channel on a DAQ device"""

    # required fields
    channel_name: str = Field(..., title="DAQ channel name")
    device_name: str = Field(..., title="Name of connected device")
    channel_type: DaqChannelType = Field(..., title="DAQ channel type")

    # optional fields
    port: Optional[int] = Field(None, title="DAQ port")
    channel_index: Optional[int] = Field(None, title="DAQ channel index")
    sample_rate: Optional[Decimal] = Field(None, title="DAQ channel sample rate (Hz)", units="Hz")
    sample_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Sample rate unit")
    event_based_sampling: Optional[bool] = Field(
        False, title="Set to true if DAQ channel is sampled at irregular intervals"
    )


class DAQDevice(Device):
    """Data acquisition device containing multiple I/O channels"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: EnumSubset[
        Manufacturer.NATIONAL_INSTRUMENTS,
        Manufacturer.IMEC,
        Manufacturer.OEPS,
        Manufacturer.OTHER,
    ]
    computer_name: str = Field(..., title="Name of computer controlling this DAQ")

    # optional fields
    channels: Optional[List[DAQChannel]] = Field(None, title="DAQ channels")


class HarpDeviceType(Enum):
    """Harp device type"""

    BEHAVIOR = "Behavior"
    CAMERA_CONTROLLER = "Camera Controller"
    LOAD_CELLS = "Load Cells"
    SOUND_BOARD = "Sound Board"
    TIMESTAMP_GENERATOR = "Timestamp Generator"
    INPUT_EXPANDER = "Input Expander"


class HarpDevice(DAQDevice):
    """DAQ that uses the Harp protocol for synchronization and data transmission"""

    # required fields
    harp_device_type: HarpDeviceType = Field(..., title="Type of Harp device")
    harp_device_version: str = Field(..., title="Device version")

    # fixed values
    manufacturer: Manufacturer = Manufacturer.OEPS
    data_interface: DataInterface = Field("USB", const=True)


class Laser(Device):
    """Laser module with a specific wavelength (may be a sub-component of a larger assembly)"""

    # required fields
    lightsource_type: str = Field("Laser", title="Lightsource type")
    manufacturer: EnumSubset[
        Manufacturer.COHERENT_SCIENTIFIC,
        Manufacturer.HAMAMATSU,
        Manufacturer.OXXIUS,
        Manufacturer.QUANTIFI,
        Manufacturer.OTHER,
    ]
    wavelength: int = Field(..., title="Wavelength (nm)", units="nm")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")

    # optional fields
    maximum_power: Optional[Decimal] = Field(None, title="Maximum power (mW)", units="mW")
    power_unit: PowerUnit = Field(PowerUnit.MW, title="Power unit")
    coupling: Optional[Coupling] = Field(None, title="Coupling")
    coupling_efficiency: Optional[Decimal] = Field(
        None,
        title="Coupling efficiency (percent)",
        units="percent",
        ge=0,
        le=100,
    )
    coupling_efficiency_unit: Optional[str] = Field("percent", title="Coupling efficiency unit")
    item_number: Optional[str] = Field(None, title="Item number")
    calibration_data: Optional[str] = Field(None, description="Path to calibration data", title="Calibration data")
    calibration_date: Optional[datetime] = Field(None, title="Calibration date")


class LightEmittingDiode(Device):
    """Description of a Light Emitting Diode (LED) device"""

    lightsource_type: str = Field("LED", title="Lightsource type")
    manufacturer: EnumSubset[
        Manufacturer.DORIC,
        Manufacturer.PRIZMATIX,
        Manufacturer.THORLABS,
        Manufacturer.OTHER,
    ]
    wavelength: int = Field(..., title="Wavelength (nm)", units="nm")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")


class MousePlatform(Device):
    """Description of a mouse platform"""

    surface_material: Optional[str] = Field(None, title="Surface material")
    date_surface_replaced: Optional[datetime] = Field(None, title="Date surface replaced")


class Disc(MousePlatform):
    """Description of a running disc"""

    platform_type: str = Field("Disc", title="Platform type", const=True)
    radius: Decimal = Field(..., title="Radius (cm)", units="cm", ge=0)
    radius_unit: SizeUnit = Field(SizeUnit.CM, title="radius unit")
    output: Optional[DaqChannelType] = Field(None, description="analog or digital electronics")
    encoder: Optional[str] = Field(None, title="Encoder", description="Encoder hardware type")
    decoder: Optional[str] = Field(None, title="Decoder", description="Decoder chip type")
    encoder_firmware: Optional[Software] = Field(
        None, title="Encoder firmware", description="Firmware to read from decoder chip counts"
    )


class Tube(MousePlatform):
    """Description of a tube platform"""

    platform_type: str = Field("Tube", title="Platform type", const=True)
    diameter: Decimal = Field(..., title="Diameter", ge=0)
    diameter_unit: SizeUnit = Field(SizeUnit.CM, title="Diameter unit")


class Treadmill(MousePlatform):
    """Description of treadmill platform"""

    platform_type: str = Field("Treadmill", title="Platform type", const=True)
    treadmill_width: Decimal = Field(..., title="Width of treadmill (mm)", units="mm")
    width_unit: SizeUnit = Field(SizeUnit.CM, title="Width unit")


class Monitor(Device):
    """Visual display"""

    # required fields
    manufacturer: EnumSubset[Manufacturer.LG]
    refresh_rate: int = Field(..., title="Refresh rate (Hz)", units="Hz", ge=60)
    width: int = Field(..., title="Width (pixels)", units="pixels")
    height: int = Field(..., title="Height (pixels)", units="pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    viewing_distance: Decimal = Field(..., title="Viewing distance (cm)", units="cm")

    # optional fields
    contrast: Optional[int] = Field(
        ...,
        description="Monitor's contrast setting",
        title="Contrast",
        ge=0,
        le=100,
    )
    brightness: Optional[int] = Field(
        ...,
        description="Monitor's brightness setting",
        title="Brightness",
        ge=0,
        le=100,
    )


class WaterDelivery(AindModel):
    """Description of water delivery system"""

    # required fields
    spout_diameter: str = Field(..., title="Spout diameter (mm)")
    spout_diameter_unit: SizeUnit = Field(SizeUnit.MM, title="Spout diameter unit")
    spout_position: RelativePosition = Field(..., title="Spout stage position")
    water_calibration_values: Dict[str, Any] = Field(..., title="Water calibration values")

    # optional fields
    stage_type: Optional[MotorizedStage] = Field(None, title="Motorized stage")


class MousePlatform(AindModel):
    """Behavior platform for a mouse during a session"""

    track_wheel: Union[Tube, Treadmill, Disc] = Field(..., title="Track wheel type")

    # optional fields
    stage_software: Optional[Software] = Field(None, title="Stage software")
    water_delivery: Optional[WaterDelivery] = Field(None, title="Water delivery")


class VisualStimulusDisplayAssembly(AindModel):
    """Visual display"""

    # required fields
    monitor: Monitor = Field(..., title="Monitor")
    viewing_distance: Decimal = Field(..., title="Viewing distance (cm)", units="cm")
    viewing_distance_unit: SizeUnit = Field(SizeUnit.CM, title="Viewing distance unit")

    # optional fields
    position: Optional[RelativePosition] = Field(None, title="Relative position of the monitor")
