""" schema describing imaging instrument """

from datetime import date
from typing import List, Literal, Optional

from aind_data_schema_models.organizations import Organization
from pydantic import Field, ValidationInfo, field_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.components.devices import (
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


class Com(AindModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class Instrument(AindCoreModel):
    """Description of an instrument, which is a collection of devices"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/instrument.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.1"] = Field("1.0.1")

    instrument_id: Optional[str] = Field(
        default=None,
        description="Unique instrument identifier, name convention: <room>-<apparatus name>-<date modified YYYYMMDD>",
        title="Instrument ID",
    )
    modification_date: date = Field(..., title="Date of modification")
    instrument_type: ImagingInstrumentType = Field(..., title="Instrument type")
    manufacturer: Organization.ONE_OF = Field(..., title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(default=None, title="Temperature control")
    humidity_control: Optional[bool] = Field(default=None, title="Humidity control")
    optical_tables: List[OpticalTable] = Field(default=[], title="Optical table")
    enclosure: Optional[Enclosure] = Field(default=None, title="Enclosure")
    objectives: List[Objective] = Field(..., title="Objectives")
    detectors: List[Detector] = Field(default=[], title="Detectors")
    light_sources: List[LIGHT_SOURCES] = Field(default=[], title="Light sources")
    lenses: List[Lens] = Field(default=[], title="Lenses")
    fluorescence_filters: List[Filter] = Field(default=[], title="Fluorescence filters")
    motorized_stages: List[MotorizedStage] = Field(default=[], title="Motorized stages")
    scanning_stages: List[ScanningStage] = Field(default=[], title="Scanning motorized stages")
    additional_devices: List[AdditionalImagingDevice] = Field(default=[], title="Additional devices")
    calibration_date: Optional[date] = Field(
        default=None,
        description="Date of most recent calibration",
        title="Calibration date",
    )
    calibration_data: Optional[str] = Field(
        default=None,
        description="Path to calibration data from most recent calibration",
        title="Calibration data",
    )
    com_ports: List[Com] = Field(default=[], title="COM ports")
    daqs: List[DAQDevice] = Field(default=[], title="DAQ")
    notes: Optional[str] = Field(default=None, validate_default=True)

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
        if info.data.get("manufacturer") == Organization.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if manufacturer is Other. Describe the manufacturer in the notes field."
            )
        return value
