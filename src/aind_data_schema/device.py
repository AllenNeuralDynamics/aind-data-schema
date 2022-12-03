""" schema for various Devices """

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


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
    NEWPORT = "Newport"
    ASI = "Applied Scientific Instrumentation"
    MIGHTY_ZAP = "IR Robot Co"
    OTHER = "Other"


class DaqChannelType(Enum):
    """DAQ Channel type"""

    DO = "Digital Output"
    AO = "Analog Output"


class DaqChannel(BaseModel):
    """Description of a DAQ Channel"""

    index: int = Field(..., title="index")
    type: DaqChannelType = Field(..., title="DAQ channel type")


class Device(BaseModel):
    """Description of a general device"""

    manufacturer: Manufacturer = Field(..., title="Manufacturer")
    serial_number: str = Field(..., title="Serial number")
    model: Optional[str] = Field(None, title="Model")
    notes: Optional[str] = Field(None, title="Notes")
    daq_channel: Optional[DaqChannel] = Field(None, title="DAQ channel")
