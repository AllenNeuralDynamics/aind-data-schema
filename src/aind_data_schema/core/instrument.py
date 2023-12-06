""" schema describing imaging instrument """

from datetime import date
from typing import List, Literal, Optional

from pydantic import Field, ValidationInfo, field_validator

from aind_data_schema.base import AindCoreModel, AindModel, OptionalField, OptionalType
from aind_data_schema.models.devices import (
    LIGHT_SOURCES,
    AdditionalImagingDevice,
    DAQDevice,
    Detector,
    Enclosure,
    Filter,
    ImagingInstrumentType,
    Lens,
    MotorizedStage,
    Objective,
    OpticalTable,
    ScanningStage,
)
from aind_data_schema.models.manufacturers import Manufacturer


class Com(AindModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class Instrument(AindCoreModel):
    """Description of an instrument, which is a collection of devices"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/imaging/instrument.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": True})
    schema_version: Literal["0.10.0"] = Field("0.10.0")

    instrument_id: OptionalType[str] = OptionalField(
        description="Unique identifier for this instrument. Naming convention: <room>-<apparatus>-<version>",
        title="Instrument ID",
    )
    modification_date: date = Field(..., title="Date of modification")
    instrument_type: ImagingInstrumentType = Field(..., title="Instrument type")
    manufacturer: Manufacturer.ONE_OF = Field(..., title="Instrument manufacturer")
    temperature_control: OptionalType[bool] = OptionalField(title="Temperature control")
    humidity_control: OptionalType[bool] = OptionalField(title="Humidity control")
    optical_tables: List[OpticalTable] = Field([], title="Optical table")
    enclosure: OptionalType[Enclosure] = OptionalField(title="Enclosure")
    objectives: List[Objective] = Field(..., title="Objectives")
    detectors: List[Detector] = Field([], title="Detectors")
    light_sources: List[LIGHT_SOURCES] = Field([], title="Light sources")
    lenses: List[Lens] = Field([], title="Lenses")
    fluorescence_filters: List[Filter] = Field([], title="Fluorescence filters")
    motorized_stages: List[MotorizedStage] = Field([], title="Motorized stages")
    scanning_stages: List[ScanningStage] = Field([], title="Scanning motorized stages")
    additional_devices: List[AdditionalImagingDevice] = Field([], title="Additional devices")
    calibration_date: OptionalType[date] = OptionalField(
        description="Date of most recent calibration",
        title="Calibration date",
    )
    calibration_data: OptionalType[str] = OptionalField(
        description="Path to calibration data from most recent calibration",
        title="Calibration data",
    )
    com_ports: List[Com] = Field([], title="COM ports")
    daqs: List[DAQDevice] = Field([], title="DAQ")
    notes: OptionalType[str] = OptionalField(validate_default=True)

    @field_validator("daqs", mode="after")
    def validate_device_names(cls, value: List[DAQDevice], info: ValidationInfo) -> List[DAQDevice]:
        """validate that all DAQ channels are connected to devices that
        actually exist
        """
        daqs = value
        all_devices = (
            info.data["motorized_stages"]
            + info.data["scanning_stages"]
            + info.data["light_sources"]
            + info.data["detectors"]
            + info.data["additional_devices"]
            + daqs
        )
        all_device_names = [device.name for device in all_devices]
        for daq in daqs:
            for channel in daq.channels:
                if channel.device_name not in all_device_names:
                    raise ValueError(
                        f"Device name validation error: '{channel.device_name}' "
                        + f"is connected to '{channel.channel_name}' on '{daq.name}', but "
                        + "this device is not part of the rig."
                    )
        return daqs

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("instrument_type") == ImagingInstrumentType.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if instrument_type is Other. Describe the instrument_type in the notes field."
            )
        if info.data.get("manufacturer") == Manufacturer.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if manufacturer is Other. Describe the manufacturer in the notes field."
            )
        return value
