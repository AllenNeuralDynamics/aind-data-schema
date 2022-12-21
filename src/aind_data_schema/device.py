""" schema for various Devices """

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import AindModel


class Manufacturer(Enum):
    """Device manufacturer name"""

    THORLABS = "Thorlabs"
    OPTOTUNE = "Optotune"
    CAMBRIDGE_TECHNOLOGY = "Cambridge Technology"
    NIKON = "Nikon"
    EDMUND_OPTICS = "Edmund Optics"
    EALING = "Ealing"
    HAMAMATSU = "Hamamatsu"
    OLYMPUS = "Olympus"
    LEICA = "Leica"
    LIFECANVAS = "LifeCanvas"
    CUSTOM = "Custom"
    CHROMA = "Chroma"
    SEMROCK = "Semrock"
    NEUROPIXELS = "Neuropixels"
    MPI = "MPI"
    VORTRAN = "Vortran"
    COHERENT_SCIENTIFIC = "Coherent Scientific"
    MKS_NEWPORT = "MKS Newport"
    ASI = "Applied Scientific Instrumentation"
    MIGHTY_ZAP = "IR Robot Co"
    VIEWORKS = "Vieworks"
    OXXIUS = "Oxxius"
    NATIONAL_INSTRUMENTS = "National Instruments"
    OTHER = "Other"


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
