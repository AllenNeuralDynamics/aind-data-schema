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
    OTHER = "Other"


class DeviceType(Enum):
    """Device type name"""

    DIFFUSER = "Diffuser"
    GALVO = "Galvo"
    BEAM_EXPANDER = "Beam expander"
    LASER_COUPLER = "Laser coupler"
    PRISM = "Prism"
    OBJECTIVE = "Objective"
    SLIT = "Slit"
    OTHER = "Other"


class Device(BaseModel):
    """Description of an general device"""

    manufacturer: Manufacturer = Field(..., title="Manufacturer")
    serial_number: str = Field(..., title="Serial number")
    model: Optional[str] = Field(None, title="Model")
    notes: Optional[str] = Field(None, title="Notes")
