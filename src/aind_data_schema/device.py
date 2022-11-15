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
    OTHER = "Other"
    CHROMA = "Chroma"
    SEMROCK = "Semrock"


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

    type: DeviceType = Field(
        ...,
        description="Type of device. If Other please describe in Notes.",
        title="Type",
    )
    manufacturer: Manufacturer = Field(..., title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    serial_number: Optional[str] = Field(None, title="Serial number")
    notes: Optional[str] = Field(None, title="Notes")
