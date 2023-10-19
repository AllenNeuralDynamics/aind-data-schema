""" schema describing imaging instrument """

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field, root_validator
from pydantic.typing import Annotated, Literal

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.device import (
    DAQDevice,
    Detector,
    Device,
    Filter,
    Lamp,
    Laser,
    Lens,
    LightEmittingDiode,
    MotorizedStage,
    Objective,
)
from aind_data_schema.manufacturers import Manufacturer
from aind_data_schema.utils.units import SizeUnit


class Com(AindModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class ImagingDeviceType(Enum):
    """Imaginge device type name"""

    BEAM_EXPANDER = "Beam expander"
    SAMPLE_CHAMBER = "Sample Chamber"
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

    device_type: Literal["AdditionalImagingDevice"] = Field("AdditionalImagingDevice", const=True, readOnly=True)
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

    device_type: Literal["OpticalTable"] = Field("OpticalTable", const=True, readOnly=True)
    length: Optional[Decimal] = Field(None, title="Length (inches)", units="inches", ge=0)
    width: Optional[Decimal] = Field(None, title="Width (inches)", units="inches", ge=0)
    table_size_unit: SizeUnit = Field(SizeUnit.IN, title="Table size unit")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")


class Instrument(AindCoreModel):
    """Description of an instrument, which is a collection of devices"""

    schema_version: str = Field("0.9.0", description="schema version", title="Version", const=True)
    instrument_id: Optional[str] = Field(
        None,
        description="Unique identifier for this instrument. Naming convention: <room>-<apparatus>-<version>",
        title="Instrument ID",
    )
    modification_date: date = Field(..., title="Date of modification")
    instrument_type: ImagingInstrumentType = Field(..., title="Instrument type")
    manufacturer: Manufacturer = Field(..., title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(None, title="Temperature control")
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    optical_tables: List[OpticalTable] = Field(None, title="Optical table")
    objectives: List[Objective] = Field(..., title="Objectives", unique_items=True)
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    light_sources: Optional[
        Annotated[
            List[Union[Laser, Lamp, LightEmittingDiode]],
            Field(None, title="Light sources", unique_items=True, discriminator="device_type"),
        ]
    ]
    lenses: Optional[List[Lens]] = Field(None, title="Lenses", unique_items=True)
    fluorescence_filters: Optional[List[Filter]] = Field(None, title="Fluorescence filters", unique_items=True)
    motorized_stages: Optional[List[MotorizedStage]] = Field(None, title="Motorized stages", unique_items=True)
    scanning_stages: Optional[List[ScanningStage]] = Field(None, title="Scanning motorized stages", unique_items=True)
    daqs: Optional[List[DAQDevice]] = Field(None, title="DAQ", unique_items=True)
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
    com_ports: Optional[List[Com]] = Field(None, title="COM ports", unique_items=True)
    notes: Optional[str] = None

    @root_validator
    def validate_other(cls, v):
        """Validator for other/notes"""

        if v.get("instrument_type") == ImagingInstrumentType.OTHER and not v.get("notes"):
            raise ValueError(
                "Notes cannot be empty if instrument_type is Other. Describe the instrument_type in the notes field."
            )

        if v.get("manufacturer") == Manufacturer.OTHER and not v.get("notes"):
            raise ValueError(
                "Notes cannot be empty if manufacturer is Other. Describe the manufacturer in the notes field."
            )

        return v
