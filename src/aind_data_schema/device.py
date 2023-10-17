""" schema for various Devices """

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic.typing import Literal

from aind_data_schema.base import AindModel, EnumSubset
from aind_data_schema.coordinates import RelativePosition
from aind_data_schema.manufacturers import Manufacturer
from aind_data_schema.procedures import Reagent
from aind_data_schema.utils.units import FrequencyUnit, PowerUnit, SizeUnit, TemperatureUnit


class DeviceDriver(Enum):
    """DeviceDriver name"""

    OPENGL = "OpenGL"
    VIMBA = "Vimba"
    NVIDIA = "Nvidia Graphics"


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


class Device(AindModel):
    """Generic device"""

    device_type: str  # Needs to be set by child classes that inherits
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


class Calibration(AindModel):
    """Generic calibration class"""

    calibration_date: datetime = Field(..., title="Date and time of calibration")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: Optional[Dict[str, Any]] = Field({}, description="Calibration input", title="inputs")
    output: Optional[Dict[str, Any]] = Field({}, description="Calibration output", title="outputs")
    notes: Optional[str] = Field(None, title="Notes")


class Maintenance(AindModel):
    """Generic maintenance class"""

    maintenance_date: datetime = Field(..., title="Date and time of maintenance")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: Optional[str] = Field(None, title="Protocol ID")
    reagents: Optional[List[Reagent]] = Field(None, title="Reagents")
    notes: Optional[str] = Field(None, title="Notes")


class Camera(Device):
    """Device that acquires images and streams them to a computer"""

    device_type: Literal["Camera"] = Field("Camera", const=True, readOnly=True)
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


class Filter(Device):
    """Filter used in a light path"""

    device_type: Literal["Filter"] = Field("Filter", const=True, readOnly=True)
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
        None,
        title="Description",
        description="More details about filter properties and where/how it is being used",
    )


class Lens(Device):
    """Lens used to focus light onto a camera sensor"""

    device_type: Literal["Lens"] = Field("Lens", const=True, readOnly=True)

    # required fields
    manufacturer: EnumSubset[
        Manufacturer.COMPUTAR,
        Manufacturer.EDMUND_OPTICS,
        Manufacturer.HAMAMATSU,
        Manufacturer.INFINITY_PHOTO_OPTICAL,
        Manufacturer.LEICA,
        Manufacturer.MITUTUYO,
        Manufacturer.NIKON,
        Manufacturer.OLYMPUS,
        Manufacturer.SCHNEIDER_KREUZNACH,
        Manufacturer.THORLABS,
        Manufacturer.ZEISS,
        Manufacturer.OTHER,
    ]

    # optional fields
    focal_length: Optional[Decimal] = Field(None, title="Focal length of the lens", units="mm")
    focal_length_unit: SizeUnit = Field(SizeUnit.MM, title="Focal length unit")
    size: Optional[LensSize] = Field(None, title="Size (inches)")
    lens_size_unit: SizeUnit = Field(SizeUnit.IN, title="Lens size unit")
    optimized_wavelength_range: Optional[str] = Field(None, title="Optimized wavelength range (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    max_aperture: Optional[str] = Field(None, title="Max aperture (e.g. f/2)")


class MotorizedStage(Device):
    """Description of motorized stage"""

    device_type: Literal["MotorizedStage"] = Field("MotorizedStage", const=True, readOnly=True)
    travel: Decimal = Field(..., title="Travel of device (mm)", units="mm")
    travel_unit: SizeUnit = Field(SizeUnit.MM, title="Travel unit")

    # optional fields
    firmware: Optional[str] = Field(None, title="Firmware")


class Immersion(Enum):
    """Immersion media name"""

    AIR = "air"
    MULTI = "multi"
    OIL = "oil"
    WATER = "water"
    OTHER = "other"


class Objective(Device):
    """Description of an objective device"""

    device_type: Literal["Objective"] = Field("Objective", const=True, readOnly=True)
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
    device_type: Literal["DAQDevice"] = Field("DAQDevice", const=True, readOnly=True)
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
    device_type: Literal["HarpDevice"] = Field("HarpDevice", const=True, readOnly=True)
    harp_device_type: HarpDeviceType = Field(..., title="Type of Harp device")
    harp_device_version: str = Field(..., title="Device version")

    # fixed values
    manufacturer: Manufacturer = Manufacturer.OEPS
    data_interface: DataInterface = Field("USB", const=True)


class Laser(Device):
    """Laser module with a specific wavelength (may be a sub-component of a larger assembly)"""

    # required fields
    device_type: Literal["Laser"] = Field("Laser", const=True, readOnly=True)
    manufacturer: EnumSubset[
        Manufacturer.COHERENT_SCIENTIFIC,
        Manufacturer.HAMAMATSU,
        Manufacturer.OXXIUS,
        Manufacturer.QUANTIFI,
        Manufacturer.VORTRAN,
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


class LightEmittingDiode(Device):
    """Description of a Light Emitting Diode (LED) device"""

    device_type: Literal["LightEmittingDiode"] = Field("LightEmittingDiode", const=True, readOnly=True)
    manufacturer: EnumSubset[
        Manufacturer.DORIC,
        Manufacturer.PRIZMATIX,
        Manufacturer.THORLABS,
        Manufacturer.OTHER,
    ]
    wavelength: int = Field(..., title="Wavelength (nm)", units="nm")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")


class Lamp(Device):
    """Description of a Lamp lightsource"""

    device_type: Literal["Lamp"] = Field("Lamp", const=True, readOnly=True)
    wavelength_min: Optional[int] = Field(None, title="Wavelength minimum (nm)")
    wavelength_max: Optional[int] = Field(None, title="Wavelength maximum (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    temperature: Optional[int] = Field(None, title="Temperature (K)")
    temperature_unit: TemperatureUnit = Field(TemperatureUnit.K, title="Temperature unit")


class ProbePort(AindModel):
    """Port for a probe connection"""

    index: int = Field(..., title="One-based port index")
    probes: List[str] = Field(..., title="Names of probes connected to this port")


class NeuropixelsBasestation(DAQDevice):
    """PXI-based Neuropixels DAQ"""

    # required fields
    device_type: Literal["NeuropixelsBasestation"] = Field("NeuropixelsBasestation", const=True, readOnly=True)
    basestation_firmware_version: str = Field(..., title="Basestation firmware version")
    bsc_firmware_version: str = Field(..., title="Basestation connect board firmware")
    slot: int = Field(..., title="Slot number for this basestation")
    ports: List[ProbePort] = Field(..., title="Basestation ports")

    # fixed values
    data_interface: DataInterface = Field("PXI", const=True)
    manufacturer: Manufacturer = Field(Manufacturer.IMEC, const=True)


class OpenEphysAcquisitionBoard(DAQDevice):
    """Multichannel electrophysiology DAQ"""

    # required fields
    device_type: Literal["OpenEphysAcquisitionBoard"] = Field("OpenEphysAcquisitionBoard", const=True, readOnly=True)

    ports: List[ProbePort] = Field(..., title="Acquisition board ports")

    # fixed values
    data_interface: DataInterface = Field("USB", const=True)
    manufacturer: Manufacturer = Manufacturer.OEPS


class Manipulator(Device):
    """Manipulator used on a dome module"""

    device_type: Literal["Manipulator"] = Field("Manipulator", const=True, readOnly=True)
    manufacturer: EnumSubset[Manufacturer.NEW_SCALE_TECHNOLOGIES]


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


class ProbeModel(Enum):
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


class HeadstageModel(Enum):
    """Headstage model name"""

    RHD_16_CH = "Intan RHD 16-channel"
    RHD_32_CH = "Intan RHD 32-channel"
    RHD_64_CH = "Intan RHD 64-channel"


class Headstage(Device):
    """Headstage used with an ephys probe"""

    device_type: Literal["Headstage"] = Field("Headstage", const=True, readOnly=True)
    headstage_model: Optional[HeadstageModel] = Field(None, title="Headstage model")


class EphysProbe(Device):
    """Named probe used in an ephys experiment"""

    # required fields
    device_type: Literal["EphysProbe"] = Field("EphysProbe", const=True, readOnly=True)
    probe_model: ProbeModel = Field(..., title="Probe model")

    # optional fields
    lasers: Optional[List[Laser]] = Field(None, title="Lasers connected to this probe")
    headstage: Optional[Headstage] = Field(None, title="Headstage for this probe")


class EphysAssembly(AindModel):
    """Module for electrophysiological recording"""

    ephys_assembly_name: str = Field(..., title="Ephys assembly name")
    manipulator: Manipulator = Field(..., title="Manipulator")
    probes: List[EphysProbe] = Field(..., title="Probes that are held by this module")


class DetectorType(Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class Cooling(Enum):
    """Cooling medium name"""

    AIR = "air"
    WATER = "water"


class BinMode(Enum):
    """Detector binning mode"""

    ADDITIVE = "additive"
    AVERAGE = "average"
    NONE = "none"


class Detector(Device):
    """Description of a generic detector"""

    device_type: Literal["Detector"] = Field("Detector", const=True, readOnly=True)
    detector_type: DetectorType = Field(..., title="Detector Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: Optional[Immersion] = Field(None, title="Immersion")

    chroma: Optional[CameraChroma] = Field(None, title="Camera chroma")
    sensor_width: Optional[int] = Field(None, title="Width of the sensor in pixels")
    sensor_height: Optional[int] = Field(None, title="Height of the sensor in pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit", const=True)
    bit_depth: Optional[int] = Field(None, title="Bit depth")
    bin_mode: Optional[BinMode] = Field(BinMode.NONE, title="Detector binning mode")
    bin_width: Optional[int] = Field(None, title="Bin width")
    bin_height: Optional[int] = Field(None, title="Bin height")
    bin_unit: Optional[SizeUnit] = Field(SizeUnit.PX, title="Bin size unit", const=True)
    gain: Optional[Decimal] = Field(None, title="Gain")
    crop_width: Optional[int] = Field(None, title="Crop width")
    crop_height: Optional[int] = Field(None, title="Crop width")
    crop_unit: Optional[SizeUnit] = Field(SizeUnit.PX, title="Crop size unit", const=True)


class Patch(Device):
    """Description of a patch cord"""

    device_type: Literal["Patch"] = Field("Patch", const=True, readOnly=True)
    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(None, title="Photobleaching date")


class MousePlatform(Device):
    """Description of a mouse platform"""

    device_type: Literal["MousePlatform"] = Field("MousePlatform", const=True, readOnly=True)
    surface_material: Optional[str] = Field(None, title="Surface material")
    date_surface_replaced: Optional[datetime] = Field(None, title="Date surface replaced")


class Disc(MousePlatform):
    """Description of a running disc (i.e. MindScope Disc)"""

    device_type: Literal["Disc"] = Field("Disc", const=True, readOnly=True)
    radius: Decimal = Field(..., title="Radius (cm)", units="cm", ge=0)
    radius_unit: SizeUnit = Field(SizeUnit.CM, title="radius unit")
    output: Optional[DaqChannelType] = Field(None, description="analog or digital electronics")
    encoder: Optional[str] = Field(None, title="Encoder", description="Encoder hardware type")
    decoder: Optional[str] = Field(None, title="Decoder", description="Decoder chip type")
    encoder_firmware: Optional[Software] = Field(
        None,
        title="Encoder firmware",
        description="Firmware to read from decoder chip counts",
    )


class Wheel(MousePlatform):
    """Description of a running wheel"""

    device_type: Literal["Wheel"] = Field("Wheel", const=True, readOnly=True)
    radius: Decimal = Field(..., title="Radius (mm)")
    width: Decimal = Field(..., title="Width (mm)")
    size_unit: SizeUnit = Field(SizeUnit.MM, title="Size unit")
    encoder: Device = Field(..., title="Encoder")
    encoder_output: Optional[DaqChannelType] = Field(None, title="Encoder DAQ channel")
    pulse_per_revolution: int = Field(..., title="Pulse per revolution")
    magnetic_brake: Device = Field(..., title="Magnetic brake")
    brake_output: Optional[DaqChannelType] = Field(None, title="Brake DAQ channel")
    torque_sensor: Device = Field(..., title="Torque sensor")
    torque_output: Optional[DaqChannelType] = Field(None, title="Torque DAQ channel")


class Tube(MousePlatform):
    """Description of a tube platform"""

    device_type: Literal["Tube"] = Field("Tube", const=True, readOnly=True)
    diameter: Decimal = Field(..., title="Diameter", ge=0)
    diameter_unit: SizeUnit = Field(SizeUnit.CM, title="Diameter unit")


class Treadmill(MousePlatform):
    """Description of treadmill platform"""

    device_type: Literal["Treadmill"] = Field("Treadmill", const=True, readOnly=True)
    treadmill_width: Decimal = Field(..., title="Width of treadmill (mm)", units="mm")
    width_unit: SizeUnit = Field(SizeUnit.CM, title="Width unit")


class Monitor(Device):
    """Description of visual display for visual stimuli"""

    device_type: Literal["Monitor"] = Field("Monitor", const=True, readOnly=True)
    manufacturer: EnumSubset[Manufacturer.LG]
    refresh_rate: int = Field(..., title="Refresh rate (Hz)", units="Hz", ge=60)
    width: int = Field(..., title="Width (pixels)", units="pixels")
    height: int = Field(..., title="Height (pixels)", units="pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    viewing_distance: Decimal = Field(..., title="Viewing distance (cm)", units="cm")
    viewing_distance_unit: SizeUnit = Field(SizeUnit.CM, title="Viewing distance unit")
    position: Optional[RelativePosition] = Field(None, title="Relative position of the monitor")
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


class SpoutSide(Enum):
    """Spout sides"""

    LEFT = "Left"
    RIGHT = "Right"
    CENTER = "Center"
    OTHER = "Other"


class RewardSpout(Device):
    """Description of a reward spout"""

    device_type: Literal["RewardSpout"] = Field("RewardSpout", const=True, readOnly=True)
    side: SpoutSide = Field(..., title="Spout side", description="If Other use notes")
    spout_diameter: Decimal = Field(..., title="Spout diameter (mm)")
    spout_diameter_unit: SizeUnit = Field(SizeUnit.MM, title="Spout diameter unit")
    spout_position: Optional[RelativePosition] = Field(None, title="Spout stage position")
    solenoid_valve: Device = Field(..., title="Solenoid valve")
    notes: Optional[str] = Field(None, title="Notes")


class RewardDelivery(AindModel):
    """Description of reward delivery system"""

    device_type: Literal["RewardDelivery"] = Field("RewardDelivery", const=True, readOnly=True)
    stage_type: MotorizedStage = Field(None, title="Motorized stage")
    reward_spouts: List[RewardSpout] = Field(..., title="Water spouts")


class Speaker(Device):
    """Description of a speaker for auditory stimuli"""

    device_type: Literal["Speaker"] = Field("Speaker", const=True, readOnly=True)
    manufacturer: EnumSubset[Manufacturer.TYMPHANY]
    position: Optional[RelativePosition] = Field(None, title="Relative position of the monitor")


class Olfactometer(Device):
    """Description of a olfactometer for odor stimuli"""

    device_type: Literal["Olfactometer"] = Field("Olfactometer", const=True, readOnly=True)
    position: Optional[RelativePosition] = Field(None, title="Relative position of the monitor")
