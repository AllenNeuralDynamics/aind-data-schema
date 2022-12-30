""" schema for various Devices """

from pydantic import Field
from enum import Enum
from datetime import datetime
from typing import Optional, List
from .base import AindModel

class Manufacturer(Enum):
    """Device manufacturer name"""

    ASI = "Applied Scientific Instrumentation"
    CAMBRIDGE_TECHNOLOGY = "Cambridge Technology"
    CHROMA = "Chroma"
    COHERENT_SCIENTIFIC = "Coherent Scientific"
    CUSTOM = "Custom"
    EALING = "Ealing"
    EDMUND_OPTICS = "Edmund Optics"
    HAMAMATSU = "Hamamatsu"
    LEICA = "Leica"
    LIFECANVAS = "LifeCanvas"
    MIGHTY_ZAP = "IR Robot Co"
    MKS_NEWPORT = "MKS Newport"
    MPI = "MPI"
    NATIONAL_INSTRUMENTS = "National Instruments"
    NIKON = "Nikon"
    OEPS = "OEPS"
    OLYMPUS = "Olympus"
    OPTOTUNE = "Optotune"
    OTHER = "Other"
    OXXIUS = "Oxxius"
    SEMROCK = "Semrock"
    THORLABS = "Thorlabs"
    VIEWORKS = "Vieworks"
    VORTRAN = "Vortran"


class LensManufacturer(Enum):
    """Camera manufacturer"""

    EDMUND_OPTICS = "Edmund Optics"
    BASLER = "Basler"
    THORLABS = "Thorlabs"


class FilterManufacturer(Enum):
    """Filter manufacturer"""

    EDMUND_OPTICS = "Edmund Optics"
    SEMROCK = "Semrock"
    THORLABS = "Thorlabs"


class LaserManufacturer(Enum):
    """Laser manufacturer"""

    COHERENT_SCIENTIFIC = "Coherent Scientific"
    HAMAMATSU = "Hamamatsu"
    OXXIUS = "Oxxius"
    QUANTIFI = "Quantifi"


class CameraManufacturer(Enum):
    """Camera manufacturer"""

    ALLIED = "Allied"
    FLIR = "FLIR"
    BASLER = "Basler"
    EDMUND_OPTICS = "Edmund Optics"
    THORLABS = "Thorlabs"


class DaqManufacturer(Enum):
    """DAQ manufacturer"""

    NI = "NI"
    IMEC = "imec"
    OEPS = "OEPS"


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

    BANDPASS = "Bandpass"
    LONGPASS = "Longpass"
    SHORTPASS = "Shortpass"
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
    angle_pitch: Optional[float] = Field(
        None, title="Angle pitch (deg)", units="deg", ge=0, le=360
    )
    angle_yaw: Optional[float] = Field(
        None, title="Angle yaw (deg)", units="deg", ge=0, le=360
    )
    angle_roll: Optional[float] = Field(
        None, title="Angle roll (deg)", units="deg", ge=0, le=360
    )
    position_x: Optional[float] = Field(None, title="Position X")
    position_y: Optional[float] = Field(None, title="Position Y")
    position_z: Optional[float] = Field(None, title="Position Z")
    coordinate_system: Optional[str] = Field(None, title="Description of the coordinate system used")


class DeviceBase(AindModel):
    """Description of a general device"""

    device_name: Optional[str] = Field(None, title="Device name")
    serial_number: Optional[str] = Field(None, title="Serial number")
    device_manufacturer: Optional[Manufacturer] = Field(None, title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    notes: Optional[str] = Field(None, title="Notes")


class Camera(DeviceBase):
    """A device that acquires images and streams them to a PC"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    camera_manufacturer: CameraManufacturer = Field(..., title="Camera manufacturer")
    max_frame_rate: float = Field(..., title="Maximum frame rate (Hz)", units="Hz")
    pixel_width: int = Field(..., title="Width of the sensor in pixels", units="Pixels")
    pixel_height: int = Field(..., title="Height of the sensor in pixels", units="Pixels")
    chroma: CameraChroma = Field(..., title="Color or Monochrome")

    # optional fields
    sensor_format: Optional[str] = Field(None, title='Size of the sensor (e.g. 1/2.9")')
    recording_software: Optional[str] = Field(None, title="Software used to acquire camera data")


class Lens(DeviceBase):
    """A lens used to focus light onto a camera sensor"""

    # required fields
    lens_manufacturer: LensManufacturer = Field(..., title="Lens manufacturer")

    # optional fields
    focal_length: Optional[float] = Field(None, title="Focal length of the lens", units="mm")
    size: Optional[LensSize] = Field(None, title="Size (inches)")
    optimized_wavelength_range: Optional[str] = Field(
        None, title="Optimized wavelength range (nm)"
    )
    max_aperture: Optional[str] = Field(None, title="Max aperture (e.g. f/2)")
    notes: Optional[str] = Field(None, title="Notes")


class Filter(DeviceBase):
    """A filter used in a light path"""

    # required fields
    filter_type: FilterType = Field(..., title="Type of filter")
    filter_manufacturer: FilterManufacturer = Field(..., title="Filter manufacturer")

    # optional fields
    diameter: Optional[FilterSize] = Field(None, title="Size (mm)", units="mm")
    thickness: Optional[float] = Field(None, title="Size (mm)", ge=0)
    filter_wheel_index: Optional[int] = Field(None, title="Filter wheel index")
    cut_off_frequency: Optional[int] = Field(None, title="Cut-off frequency")
    cut_on_frequency: Optional[int] = Field(None, title="Cut-on frequency")
    description: Optional[str] = Field(None, title="Description", 
        description="More details about filter properties and where/how it is being used")


class CameraAssembly(AindModel):
    """An assembly of a camera and lens"""

    # required fields
    camera_assembly_name: str = Field(..., title="Name of this camera assembly")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: Optional[Filter] = Field(None, title="Filter")
    position: Optional[RelativePosition] = Field(None, title="Relative position of this assembly")
    

class DaqChannel(AindModel):
    """Description of a DAQ Channel"""

    # required fields
    channel_name: str = Field(..., title="DAQ channel name")
    device_name: str = Field(..., title="Name of connected device")
    channel_type: DaqChannelType = Field(..., title="DAQ channel type")

    # optional fields
    port: Optional[int] = Field(None, title="DAQ port")
    channel_index: Optional[int] = Field(None, title="DAQ channel index")
    sample_rate: Optional[float] = Field(-1.0, title="DAQ channel sample rate (Hz); -1 = event-based sampling", units="Hz")
    

class DAQ(DeviceBase):
    """A non-camera device that interfaces with a computer"""

    # required fields
    data_interface: DataInterface = Field(..., title="Type of connection to PC")
    daq_manufacturer: DaqManufacturer = Field(..., title="DAQ manufacturer")
    computer_name: str = Field(..., title="Name of computer controlling this DAQ")

    # optional fields
    channels: Optional[List[DaqChannel]] = Field(
        None, title="DAQ channels"
    )


class Laser(DeviceBase):
    """Description of a laser"""
    
    # required fields
    laser_manufacturer: LaserManufacturer = Field(..., title="Laser manufacturer")
    wavelength: int = Field(
        ..., title="Wavelength (nm)", units="nm"
    )

    # optional fields
    item_number: Optional[str] = Field(None, title="Item number")
    maximum_power: Optional[float] = Field(
        None, title="Maximum power (mW)", units="mW"
    )
    coupling: Optional[Coupling] = Field(None, title="Coupling")
    coupling_efficiency: Optional[float] = Field(
        None,
        title="Coupling efficiency (percent)",
        units="percent",
        ge=0,
        le=100,
    )
    calibration_data: Optional[str] = Field(
        None, description="Path to calibration data", title="Calibration data"
    )
    calibration_date: Optional[datetime] = Field(
        None, title="Calibration date"
    )
