""" schema describing imaging instrument """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Literal, Optional, Set

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel, Constant
from aind_data_schema.device import (
    Coupling,
    DAQDevice,
    DataInterface,
    Device,
    Filter,
    Manufacturer,
    MotorizedStage,
    Objective,
    PowerUnit,
    SizeUnit,
)


class Com(AindModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class CameraType(Enum):
    """Camera type name"""

    CAMERA = "Camera"
    PMT = "PMT"
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


class LightsourceType(Enum):
    """Light source type name"""

    LAMP = "lamp"
    LASER = "laser"
    LED = "LED"
    OTHER = "other"


class Lightsource(Device):
    """Description of lightsource device"""

    type: LightsourceType = Field(..., title="Lightsource Type")
    coupling: Coupling = Field(..., title="Coupling")
    wavelength: float = Field(..., title="Wavelength (nm)", units="nm", ge=300, le=1000)
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    max_power: float = Field(..., title=" Maximum power (mW)", units="mW")
    power_unit: PowerUnit = Field(PowerUnit.MW, title="Power unit")


class ImagingDeviceType(Enum):
    """Imaginge device type name"""

    BEAM_EXPANDER = "Beam expander"
    DIFFUSER = "Diffuser"
    GALVO = "Galvo"
    LASER_COMBINER = "Laser combiner"
    LASER_COUPLER = "Laser coupler"
    PRISM = "Prism"
    OBJECTIVE = "Objective"
    ROTATION_MOUNT = "Rotation mount"
    SLIT = "Slit"
    TUNABLE_LENS = "Tunable lens"
    OTHER = "Other"


class ImagingInstrumentType(Enum):
    """Experiment type name"""

    CONFOCAL = "confocal"
    DISPIM = "diSPIM"
    EXASPIM = "exaSPIM"
    ECEPHYS = "ecephys"
    MESOSPIM = "mesoSPIM"
    OTHER = "Other"
    SMARTSPIM = "SmartSPIM"
    TWO_PHOTON = "Two photon"


class AdditionalImagingDevice(Device):
    """Description of additional devices"""

    type: ImagingDeviceType = Field(..., title="Device type")


class StageAxisDirection(Enum):
    """Direction of motion for motorized stage"""

    DETECTION_AXIS = "Detection axis"
    ILLUMINATION_AXIS = "Illumination axis"
    PERPENDICULAR_AXIS = "Perpendicular axis"


class StageAxisName(Enum):
    """Axis names for motorized stages as configured by hardware"""

    X = "X"
    Y = "Y"
    Z = "Z"


class ScanningStage(MotorizedStage):
    """Description of a scanning motorized stages"""

    stage_axis_direction: StageAxisDirection = Field(..., title="Direction of stage axis")
    stage_axis_name: StageAxisName = Field(..., title="Name of stage axis")


class OpticalTable(Device):
    """Description of Optical Table"""

    length: Optional[float] = Field(None, title="Length (inches)", units="inches", ge=0)
    width: Optional[float] = Field(None, title="Width (inches)", units="inches", ge=0)
    table_size_unit: SizeUnit = Field(SizeUnit.IN, title="Table size unit")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")


class Instrument(AindCoreModel):
    """Description of an instrument, which is a collection of devices"""

    schema_version: Constant("0.7.1", title="Schema version")
    instrument_id: Optional[str] = Field(
        None,
        description="Unique identifier for this instrument. Naming convention: <room>-<apparatus>-<version>",
        title="Instrument ID",
    )
    instrument_type: ImagingInstrumentType = Field(..., title="Instrument type")
    manufacturer: Manufacturer = Field(..., title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(None, title="Temperature control")
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    optical_tables: List[OpticalTable] = Field(None, title="Optical table")
    objectives: List[Objective] = Field(..., title="Objectives")
    detectors: Optional[List[Detector]] = Field(None, title="Detectors")
    light_sources: Optional[List[Lightsource]] = Field(None, title="Light sources")
    fluorescence_filters: Optional[List[Filter]] = Field(None, title="Fluorescence filters")
    motorized_stages: Optional[List[MotorizedStage]] = Field(None, title="Motorized stages")
    scanning_stages: Optional[List[ScanningStage]] = Field(None, title="Scanning motorized stages")
    daqs: Optional[List[DAQDevice]] = Field(None, title="DAQ")
    additional_devices: Optional[List[AdditionalImagingDevice]] = Field(
        None, title="Additional devices"
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
    com_ports: Optional[List[Com]] = Field(None, title="COM ports")
    notes: Optional[str] = None
