""" schema describing imaging instrument """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MicroscopeType(Enum):
    """Microscope name"""

    MESOSPIM = "mesoSPIM"
    EXASPIM = "exaSPIM"
    DISPIM = "diSPIM"
    SMARTSPIM = "smartSPIM"
    CONFOCAL = "Confocal"
    TWO_PHOTON = "Two photon"
    OTHER = "Other"


class MicroscopeManufacturer(Enum):
    """Microscope manufacturer name"""

    OLYMPUS = "Olympus"
    LEICA = "Leica"
    LIFECANVAS = "LifeCanvas"
    CUSTOM = "Custom"


class AnalogOutput(BaseModel):
    """Description of analog output"""

    hardware_device: Optional[str] = Field(
        None, title="Controlled hardware device"
    )
    ao_channel: int = Field(..., title="Analog output channel")


class Com(BaseModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class CameraType(Enum):
    """Camera type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class DataInterface(Enum):
    """Data interface name"""

    USB = "USB"
    CAMERALINK = "CameraLink"
    COAX = "Coax"
    OTHER = "other"


class Cooling(Enum):
    """Cooling medium name"""

    AIR = "air"
    WATER = "water"


class Device(BaseModel):
    """Description of a device"""

    type: Optional[str] = Field(
        None, description="Generic device type", title="Type"
    )
    manufacturer: Optional[str] = Field(None, title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    serial_number: Optional[str] = Field(None, title="Serial number")
    notes: Optional[str] = Field(None, title="Notes")


class Detector(Device):
    """Description of a detector device"""

    type: CameraType = Field(..., title="Detector Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")


class FilterType(Enum):
    """Filter type name"""

    LONG_PASS = "Long pass"
    BAND_PASS = "Band pass"
    SHORT_PASS = "Short pass"
    MULTIBAND = "Multiband"


class FilterManufacturer(Enum):
    """Filter manufacturer name"""

    CHROMA = "Chroma"
    SEMROCK = "Semrock"
    OTHER = "Other"


class Filter(Device):
    """Description of a filter device"""

    type: FilterType = Field(..., title="Filter Type")
    manufacturer: FilterManufacturer = Field(..., title="Filter manufacturer")
    diameter: float = Field(..., title="Size (mm)", ge=0)
    thickness: float = Field(..., title="Size (mm)", ge=0)
    description: Optional[str] = Field(
        None, description="Where/how filter is being used", title="Description"
    )


class LightsourceType(Enum):
    """Light source type name"""

    LAMP = "lamp"
    LASER = "laser"
    LED = "LED"
    OTHER = "other"


class Coupling(Enum):
    """Coupling method name"""

    FREE_SPACE = "Free-space"
    SMF = "SMF"
    MMF = "MMF"
    OTHER = "other"


class Lightsource(Device):
    """Description of lightsource device"""

    type: LightsourceType = Field(..., title="Lightsource Type")
    coupling: Coupling = Field(..., title="Coupling")
    wavelength: float = Field(..., title="Wavelength (nm)", ge=300, le=1000)
    max_power: float = Field(..., title=" Maximum power (mW)")
    filter_wheel_index: int = Field(..., title="Filter index")


class Immersion(Enum):
    """Immersion media name"""

    AIR = "air"
    WATER = "water"
    OIL = "oil"
    MULTI = "multi"
    OTHER = "other"


class Objective(Device):
    """Description of an objective device"""

    numerical_aperture: float = Field(..., title="Numerical aperture (in air)")
    magnification: float = Field(..., title="Magnification")
    immersion: Immersion = Field(..., title="Immersion")


class Microscope(Device):
    """Description of a microscope device"""

    type: MicroscopeType = Field(..., title="Microscope type")
    manufacturer: MicroscopeManufacturer = Field(
        ..., title="Microscope manufacturer"
    )
    location: str = Field(..., title="Microscope location")


class Instrument(BaseModel):
    """Description of an instrument, which is a collection of devices"""

    version: str = Field(
        "0.1.0", description="schema version", title="Version", const=True
    )
    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/aind-data-schema/blob/main/src/aind-data-schema/imaging/instrument.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    instrument_id: Optional[str] = Field(
        None,
        description="unique identifier for this instrument configuration",
        title="Instrument ID",
    )
    microscope: Microscope = Field(
        ...,
        title="Microscope information",
    )

    temperature_control: Optional[bool] = Field(
        None, title="Temperature control"
    )
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")
    optical_table_model: Optional[str] = Field(
        None, title="Optical table model"
    )
    optical_table_size: Optional[float] = Field(
        None, title="Optical table size"
    )
    objectives: List[Objective] = Field(
        ..., title="Objectives", unique_items=True
    )
    detectors: List[Detector] = Field(
        ..., title="Detectors", unique_items=True
    )
    light_sources: List[Lightsource] = Field(
        ..., title="Light sources", unique_items=True
    )
    fluorescence_filters: Optional[List[Filter]] = Field(
        None, title="Fluorescence filters", unique_items=True
    )
    motorized_stages: Optional[List[Device]] = Field(
        None, title="Motorized stages", unique_items=True
    )
    additional_devices: Optional[List[Device]] = Field(
        None, title="Additional devices", unique_items=True
    )
    calibration_date: Optional[date] = Field(
        None,
        description="Date of most recent calibration",
        title="Calibration date",
    )
    calibration_data: Optional[str] = Field(
        None,
        description="Path to calibration data from most recent calibration",
        title="Calibration data",
    )
    daq_device_name: Optional[str] = Field(
        None,
        description="DAQ device name as it appears to the PC",
        title="DAQ device name",
    )
    daq_model_name: Optional[str] = Field(
        None, description="DAQ product name", title="DAQ model"
    )
    daq_update_frequency: Optional[float] = Field(
        None, title="DAQ update frequency (Hz)"
    )
    daq_ao_names_to_channel: Optional[List[AnalogOutput]] = Field(
        None, title="DAQ analog outputs", unique_items=True
    )
    com_ports: Optional[List[Com]] = Field(
        None, title="COM ports", unique_items=True
    )
    notes: Optional[str] = None
