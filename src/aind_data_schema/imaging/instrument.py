""" schema describing imaging instrument """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from ..base import AindSchema

from ..device import Device, Manufacturer


class InstrumentType(Enum):
    """Instrument type name"""

    MESOSPIM = "mesoSPIM"
    EXASPIM = "exaSPIM"
    DISPIM = "diSPIM"
    SMARTSPIM = "smartSPIM"
    CONFOCAL = "Confocal"
    TWO_PHOTON = "Two photon"
    OTHER = "Other"


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


class Detector(Device):
    """Description of a detector device"""

    type: CameraType = Field(..., title="Detector type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")


class FilterType(Enum):
    """Filter type name"""

    LONG_PASS = "Long pass"
    BAND_PASS = "Band pass"
    SHORT_PASS = "Short pass"
    MULTIBAND = "Multiband"


class Filter(Device):
    """Description of a filter device"""

    type: FilterType = Field(..., title="Filter Type")
    diameter: float = Field(..., title="Size (mm)", ge=0)
    thickness: float = Field(..., title="Size (mm)", ge=0)
    filter_wheel_index: int = Field(..., title="Filter wheel index")
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
    wavelength: float = Field(
        ..., title="Wavelength (nm)", units="nm", ge=300, le=1000
    )
    max_power: float = Field(..., title=" Maximum power (mW)", units="mW")


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


class ImagingDeviceType(Enum):
    """Imaginge device type name"""

    DIFFUSER = "Diffuser"
    GALVO = "Galvo"
    BEAM_EXPANDER = "Beam expander"
    LASER_COUPLER = "Laser coupler"
    PRISM = "Prism"
    OBJECTIVE = "Objective"
    SLIT = "Slit"
    OTHER = "Other"


class AdditionalImagingDevice(Device):
    """Description of additional devices"""

    type: ImagingDeviceType = Field(..., title="Device type")


class StageAxis(Enum):
    """Direction of motion for motorized stage"""

    DETECTION_AXIS = "Detection axis"
    ILLUMINATION_AXIS = "Illumination axis"
    PERPENDICULAR_AXIS = "Perpendicular axis"


class MotorizedStage(Device):
    """Description of motorized stage"""

    axis: StageAxis = Field(..., title="Axis of stage")
    travel: float = Field(..., title="Travel of device (mm)", units="mm")


class DAQ(Device):
    """Description of DAQ device"""

    device_name: str = Field(..., title="PC device name")
    update_frequency: float = Field(
        ..., title="DAQ update frequency (Hz)", units="Hz"
    )
    number_active_channels: int = Field(..., title="Number of active channels")


class OpticalTable(Device):
    """Description of Optical Table"""

    length: Optional[float] = Field(
        None, title="Length (inches)", units="inches", ge=0
    )
    width: Optional[float] = Field(
        None, title="Width (inches)", units="inches", ge=0
    )
    vibration_control: Optional[bool] = Field(None, title="Vibration control")


class Instrument(AindSchema):
    """Description of an instrument, which is a collection of devices"""

    version: str = Field(
        "0.4.1", description="schema version", title="Version", const=True
    )
    instrument_id: Optional[str] = Field(
        None,
        description="unique identifier for this instrument configuration",
        title="Instrument ID",
    )
    type: InstrumentType = Field(..., title="Instrument type")
    location: str = Field(..., title="Instrument location")
    manufacturer: Manufacturer = Field(..., title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(
        None, title="Temperature control"
    )
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    optical_tables: List[OpticalTable] = Field(None, title="Optical table")
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
    motorized_stages: Optional[List[MotorizedStage]] = Field(
        None, title="Motorized stages", unique_items=True
    )
    daqs: Optional[List[DAQ]] = Field(None, title="DAQ", unique_items=True)
    additional_devices: Optional[List[AdditionalImagingDevice]] = Field(
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
    com_ports: Optional[List[Com]] = Field(
        None, title="COM ports", unique_items=True
    )
    notes: Optional[str] = None
