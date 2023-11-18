""" schema describing imaging instrument """

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import Field, root_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.models.devices import (
    LIGHT_SOURCES,
    AdditionalImagingDevice,
    DAQDevice,
    Detector,
    Device,
    Enclosure,
    Filter,
    ImagingInstrumentType,
    Lamp,
    Laser,
    Lens,
    LightEmittingDiode,
    MotorizedStage,
    Objective,
    OpticalTable,
    ScanningStage,
)
from aind_data_schema.models.manufacturers import Manufacturer

# from aind_data_schema.utils.units import SizeUnit


class Com(AindModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class Instrument(AindCoreModel):
    """Description of an instrument, which is a collection of devices"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/imaging/instrument.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": True})
    schema_version: Literal["0.10.0"] = Field("0.10.0")

    instrument_id: Optional[str] = Field(
        None,
        description="Unique identifier for this instrument. Naming convention: <room>-<apparatus>-<version>",
        title="Instrument ID",
    )
    modification_date: date = Field(..., title="Date of modification")
    instrument_type: ImagingInstrumentType = Field(..., title="Instrument type")
    manufacturer: Manufacturer.ONE_OF = Field(..., title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(None, title="Temperature control")
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    optical_tables: List[OpticalTable] = Field(None, title="Optical table")
    enclosure: Optional[Enclosure] = Field(None, title="Enclosure")
    objectives: List[Objective] = Field(..., title="Objectives")
    detectors: List[Detector] = Field([], title="Detectors")
    light_sources: List[LIGHT_SOURCES] = Field([], title="Light sources")
    lenses: List[Lens] = Field([], title="Lenses")
    fluorescence_filters: List[Filter] = Field([], title="Fluorescence filters")
    motorized_stages: List[MotorizedStage] = Field([], title="Motorized stages")
    scanning_stages: List[ScanningStage] = Field([], title="Scanning motorized stages")
    daqs: List[DAQDevice] = Field([], title="DAQ")
    additional_devices: List[AdditionalImagingDevice] = Field([], title="Additional devices")
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
    com_ports: List[Com] = Field([], title="COM ports")
    notes: Optional[str] = None

    # @root_validator
    # def validate_other(cls, v):
    #     """Validator for other/notes"""
    #
    #     if v.get("instrument_type") == ImagingInstrumentType.OTHER and not v.get("notes"):
    #         raise ValueError(
    #             "Notes cannot be empty if instrument_type is Other. Describe the instrument_type in the notes field."
    #         )
    #
    #     if v.get("manufacturer") == Manufacturer.OTHER and not v.get("notes"):
    #         raise ValueError(
    #             "Notes cannot be empty if manufacturer is Other. Describe the manufacturer in the notes field."
    #         )
    #
    #     return v
