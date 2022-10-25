""" schema describing imaging instrument """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MicroscopeType(Enum):
    """various microscope names"""

    mesoSPIM = "mesoSPIM"
    exaSPIM = "exaSPIM"
    diSPIM = "diSPIM"
    smartSPIM = "smartSPIM"
    Confocal = "Confocal"
    Two_photon = "Two photon"
    Other = "Other"


class MicroscopeManufacturer(Enum):
    """various microscope manufacturers"""

    Olympus = "Olympus"
    Leica = "Leica"
    LifeCanvas = "LifeCanvas"
    Custom = "Custom"


class Ao(BaseModel):
    """TODO"""

    hardware_device: Optional[str] = Field(
        None, title="Controlled hardware device"
    )
    ao_channel: int = Field(..., title="AO channel")


class Com(BaseModel):
    """TODO"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class CameraType(Enum):
    """camera type list"""

    Camera = "Camera"
    PMT = "PMT"
    other = "other"


class DataInterface(Enum):
    """TODO"""

    USB = "USB"
    CameraLink = "CameraLink"
    Coax = "Coax"
    other = "other"


class Cooling(Enum):
    """cooling medium"""

    air = "air"
    water = "water"


class Device(BaseModel):
    """base device description"""

    type: Optional[str] = Field(
        None, description="Generic device type", title="Type"
    )
    manufacturer: Optional[str] = Field(None, title="Manufacturer")
    model: Optional[str] = Field(None, title="Model")
    serial_number: Optional[str] = Field(None, title="Serial number")
    notes: Optional[str] = Field(None, title="Notes")


class Detector(Device):
    """detector device description"""

    type: CameraType = Field(..., title="Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")


class FilterType(Enum):
    """filter types"""

    Long_pass = "Long pass"
    Band_pass = "Band pass"
    Short_pass = "Short pass"
    Multiband = "Multiband"


class FilterManufacturer(Enum):
    """list of filter manufacturers"""

    Chroma = "Chroma"
    Semrock = "Semrock"
    Other = "Other"


class Filter(Device):
    """filter device description"""

    type: FilterType = Field(..., title="Type")
    manufacturer: FilterManufacturer = Field(..., title="Filter manufacturer")
    diameter: float = Field(..., title="Size (mm)")
    thickness: float = Field(..., title="Size (mm)")
    description: Optional[str] = Field(
        None, description="Where/how filter is being used", title="Description"
    )


class LightsourceType(Enum):
    """light source types"""

    lamp = "lamp"
    laser = "laser"
    LED = "LED"
    other = "other"


class Coupling(Enum):
    """TODO"""

    Free_space = "Free-space"
    SMF = "SMF"
    MMF = "MMF"
    other = "other"


class Lightsource(Device):
    """lightsource device information"""

    type: LightsourceType = Field(..., title="Type")
    coupling: Coupling = Field(..., title="Coupling")
    wavelength: float = Field(..., title="Wavelength (nm)")
    max_power: float = Field(..., title=" Maximum power (mW)")
    filter_wheel_index: int = Field(..., title="Filter index")


class Immersion(Enum):
    """immersion media"""

    air = "air"
    water = "water"
    oil = "oil"
    multi = "multi"
    other = "other"


class Objective(Device):
    """objective device information"""

    numerical_aperture: float = Field(..., title="Numerical aperture (in air)")
    magnification: float = Field(..., title="Magnification")
    immersion: Immersion = Field(..., title="Immersion")


class Microscope(Device):
    """microscope device information"""

    type: MicroscopeType = Field(..., title="Microscope type")
    manufacturer: MicroscopeManufacturer = Field(
        ..., title="Microscope manufacturer"
    )
    location: str = Field(..., title="Microscope location")


class Instrument(BaseModel):
    """instrument is a collection of devices, etc"""

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
    daq_ao_names_to_channel: Optional[List[Ao]] = Field(
        None, title="DAQ analog outputs", unique_items=True
    )
    com_ports: Optional[List[Com]] = Field(
        None, title="COM ports", unique_items=True
    )
    notes: Optional[str] = None
