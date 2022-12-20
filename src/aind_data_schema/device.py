""" schema for various Devices """

from pydantic import Field
from enum import Enum
from typing import Optional
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
    IMEC = "imec"
    LEICA = "Leica"
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
    TELEDYNE_FLIR = "Teledyne FLIR"
    THORLABS = "Thorlabs"
    SEMROCK = "Semrock"
    VIEWORKS = "Vieworks"
    VORTRAN = "Vortran"


class DaqChannelType(Enum):
    """DAQ Channel type"""

    DO = "Digital Output"
    AO = "Analog Output"


class DaqChannel(AindModel):
    """Description of a DAQ Channel"""

    index: int = Field(..., title="index")
    type: DaqChannelType = Field(..., title="DAQ channel type")


class DeviceBase(AindModel):
    """Description of a general device"""

    manufacturer: Manufacturer = Field(..., title="Manufacturer")
    serial_number: str = Field(..., title="Serial number")
    model: Optional[str] = Field(None, title="Model")
    notes: Optional[str] = Field(None, title="Notes")


class Device(DeviceBase):
    """Description of a device that communicates with a DAQ"""

    daq_channel: Optional[DaqChannel] = Field(None, title="DAQ channel")


class DAQ(DeviceBase):
    """Description of DAQ system"""

    device_name: str = Field(..., title="PC device name")
    update_frequency: float = Field(
        ..., title="DAQ update frequency (Hz)", units="Hz"
    )
    number_active_channels: int = Field(..., title="Number of active channels")
