""" schema for various Devices """

from datetime import datetime
from enum import Enum
from typing import List, Optional

try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal

from pydantic import Field

from .base import AindModel


class SizeUnit(Enum):
    """units for sizes"""

    PX = "pixel"
    IN = "inch"
    CM = "centimeter"
    MM = "millimeter"
    UM = "micrometer"
    NM = "nanometer"
    NONE = "none"


class AngleUnit(Enum):
    """orientation units"""

    DEG = "degree"


class FrequencyUnit(Enum):
    """Frequency units"""

    HZ = "Hertz"


class PowerUnit(Enum):
    """Power units"""

    MW = "milliwatt"
    UW = "microwatt"


class Manufacturer(Enum):
    """Device manufacturer name"""

    ALLIED = "Allied"
    ASI = "Applied Scientific Instrumentation"
    BASLER = "Basler"
    CAMBRIDGE_TECHNOLOGY = "Cambridge Technology"
    CHROMA = "Chroma"
    COHERENT_SCIENTIFIC = "Coherent Scientific"
    CUSTOM = "Custom"
    EALING = "Ealing"
    EDMUND_OPTICS = "Edmund Optics"
    FLIR = "FLIR"
    HAMAMATSU = "Hamamatsu"
    IMEC = "IMEC"
    LEICA = "Leica"
    LG = "LG"
    LIFECANVAS = "LifeCanvas"
    MIGHTY_ZAP = "IR Robot Co"
    MKS_NEWPORT = "MKS Newport"
    MPI = "MPI"
    NATIONAL_INSTRUMENTS = "National Instruments"
    NEW_SCALE_TECHNOLOGIES = "New Scale Technologies"
    NIKON = "Nikon"
    OEPS = "OEPS"
    OLYMPUS = "Olympus"
    OPTOTUNE = "Optotune"
    OTHER = "Other"
    OXXIUS = "Oxxius"
    QUANTIFI = "Quantifi"
    SEMROCK = "Semrock"
    THORLABS = "Thorlabs"
    VIEWORKS = "Vieworks"
    VORTRAN = "Vortran"


class Coupling(Enum):
    """Laser coupling type"""

    FREE_SPACE = "Free-space"
    SMF = "SMF"
    MMF = "MMF"
    OTHER = "Other"


class DataInterface(Enum):
    """Connection between a device and a PC"""

    USB = "USB"
    CAMERALINK = "CameraLink"
    COAX = "Coax"
    PCIE = "PCIe"
    PXI = "PXI"
    ETH = "Ethernet"
    OTHER = "Other"


class FilterType(Enum):
    """Filter type"""

    BANDPASS = "Band pass"
    LONGPASS = "Long pass"
    SHORTPASS = "Short pass"
    MULTIBAND = "Multiband"
    DICHROIC = "Dichroic"
    ND = "Neutral density"
    NOTCH = "Notch"


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

    DO = "Digital Output"
    AO = "Analog Output"
    DI = "Digital Input"
    AI = "Analog Input"


class RelativePosition(AindModel):
    """Set of 6 values describing relative position on a rig"""

    pitch: Optional[float] = Field(None, title="Angle pitch (deg)", units="deg", ge=0, le=360)
    yaw: Optional[float] = Field(None, title="Angle yaw (deg)", units="deg", ge=0, le=360)
    roll: Optional[float] = Field(None, title="Angle roll (deg)", units="deg", ge=0, le=360)
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")

    x: Optional[float] = Field(None, title="Position X (mm)", units="mm")
    y: Optional[float] = Field(None, title="Position Y (mm)", units="mm")
    z: Optional[float] = Field(None, title="Position Z (mm)", units="mm")
    position_unit: SizeUnit = Field(SizeUnit.MM, title="Position unit")

    coordinate_system: Optional[str] = Field(None, title="Description of the coordinate system used")


class Device(AindModel):
    """Generic device"""

    name: Optional[str] = Field(None, title="Device name")
    serial_number: Optional[str] = Field(None, title="Serial number")
    manufacturer: Optional[Manufacturer] = Field(None, title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    notes: Optional[str] = Field(None, title="Notes")


class Camera(Device):
    """Device that acquires images and streams them to a computer"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: Literal[
        Manufacturer.ALLIED.value,
        Manufacturer.BASLER.value,
        Manufacturer.EDMUND_OPTICS.value,
        Manufacturer.FLIR.value,
        Manufacturer.THORLABS.value,
        Manufacturer.OTHER.value,
    ]
    computer_name: str = Field(..., title="Name of computer receiving data from this camera")
    max_frame_rate: float = Field(..., title="Maximum frame rate (Hz)", units="Hz")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    pixel_width: int = Field(..., title="Width of the sensor in pixels", units="Pixels")
    pixel_height: int = Field(..., title="Height of the sensor in pixels", units="Pixels")
    size_unit: SizeUnit = Field(SizeUnit.PX, title="Size unit")
    chroma: CameraChroma = Field(..., title="Color or Monochrome")

    # optional fields
    sensor_format: Optional[str] = Field(None, title="Size of the sensor")
    format_unit: Optional[str] = Field(None, title="Format unit")
    recording_software: Optional[str] = Field(None, title="Software used to acquire camera data")


class Lens(Device):
    """Lens used to focus light onto a camera sensor"""

    # required fields
    manufacturer: Literal[Manufacturer.EDMUND_OPTICS.value, Manufacturer.THORLABS.value, Manufacturer.OTHER.value]

    # optional fields
    focal_length: Optional[float] = Field(None, title="Focal length of the lens", units="mm")
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
    manufacturer: Literal[
        Manufacturer.EDMUND_OPTICS.value,
        Manufacturer.CHROMA.value,
        Manufacturer.SEMROCK.value,
        Manufacturer.THORLABS.value,
        Manufacturer.OTHER.value,
    ]

    # optional fields
    diameter: Optional[float] = Field(None, title="Diameter (mm)", units="mm")
    diameter_unit: SizeUnit = Field(SizeUnit.MM, title="Diameter unit")
    thickness: Optional[float] = Field(None, title="Thickness (mm)", ge=0)
    thickness_unit: SizeUnit = Field(SizeUnit.MM, title="Thickness unit")
    filter_wheel_index: Optional[int] = Field(None, title="Filter wheel index")
    cut_off_frequency: Optional[int] = Field(None, title="Cut-off frequency (Hz)")
    cut_off_frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Cut off frequency unit")
    cut_on_frequency: Optional[int] = Field(None, title="Cut-on frequency (Hz)")
    cut_on_frequency_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Cut on frequency unit")
    description: Optional[str] = Field(
        None, title="Description", description="More details about filter properties and where/how it is being used"
    )


class CameraAssembly(AindModel):
    """Named assembly of a camera and lens (and optionally a filter)"""

    # required fields
    camera_assembly_name: str = Field(..., title="Name of this camera assembly")
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
    sample_rate: Optional[float] = Field(None, title="DAQ channel sample rate (Hz)", units="Hz")
    sample_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Sample rate unit")
    event_based_sampling: Optional[bool] = Field(
        False, title="Set to true if DAQ channel is sampled at irregular intervals"
    )


class DAQDevice(Device):
    """Data acquisition device containing multiple I/O channels"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    manufacturer: Literal[
        Manufacturer.NATIONAL_INSTRUMENTS.value,
        Manufacturer.IMEC.value,
        Manufacturer.OEPS.value,
        Manufacturer.OTHER.value,
    ]
    computer_name: str = Field(..., title="Name of computer controlling this DAQ")

    # optional fields
    channels: Optional[List[DAQChannel]] = Field(None, title="DAQ channels")


class Laser(Device):
    """Laser module with a specific wavelength (may be a sub-component of a larger assembly)"""

    # required fields
    manufacturer: Literal[
        Manufacturer.COHERENT_SCIENTIFIC.value,
        Manufacturer.HAMAMATSU.value,
        Manufacturer.OXXIUS.value,
        Manufacturer.QUANTIFI.value,
        Manufacturer.OTHER.value,
    ]
    wavelength: int = Field(..., title="Wavelength (nm)", units="nm")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")

    # optional fields
    maximum_power: Optional[float] = Field(None, title="Maximum power (mW)", units="mW")
    power_unit: PowerUnit = Field(PowerUnit.MW, title="Power unit")
    coupling: Optional[Coupling] = Field(None, title="Coupling")
    coupling_efficiency: Optional[float] = Field(
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
