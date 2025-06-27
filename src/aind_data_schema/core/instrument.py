"""Core Instrument model"""

from datetime import date
from enum import Enum
from typing import Dict, List, Literal, Optional

from aind_data_schema_models.modalities import Modality
from pydantic import Field, SkipValidation, field_validator, model_validator

from aind_data_schema.base import DataCoreModel, DataModel, DiscriminatedList
from aind_data_schema.components.coordinates import CoordinateSystem
from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    AirPuffDevice,
    Arena,
    Camera,
    CameraAssembly,
    CameraTarget,
    Computer,
    DAQDevice,
    Detector,
    Device,
    DigitalMicromirrorDevice,
    Disc,
    Enclosure,
    EphysAssembly,
    FiberAssembly,
    FiberPatchCord,
    Filter,
    HarpDevice,
    Lamp,
    Laser,
    LaserAssembly,
    Lens,
    LickSpout,
    LickSpoutAssembly,
    LightEmittingDiode,
    Microscope,
    Monitor,
    MotorizedStage,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OpenEphysAcquisitionBoard,
    PockelsCell,
    PolygonalScanner,
    Scanner,
    ScanningStage,
    Speaker,
    Treadmill,
    Tube,
    Wheel,
)
from aind_data_schema.components.measurements import CALIBRATIONS
from aind_data_schema.utils.validators import recursive_get_all_names

# Define the mapping of modalities to their required device types
# The list of list pattern is used to allow for multiple options within a group, so e.g.
# FIB requires a light (one of the options) plus a detector and a patch cord
DEVICES_REQUIRED = {
    Modality.ECEPHYS.abbreviation: [EphysAssembly],
    Modality.FIB.abbreviation: [[Laser, LightEmittingDiode, Lamp], [Detector], [FiberPatchCord]],
    Modality.POPHYS.abbreviation: [[Laser], [Detector], [Objective]],
    Modality.SLAP.abbreviation: [[Laser], [Detector], [Objective], [DigitalMicromirrorDevice], [Microscope]],
    Modality.BEHAVIOR_VIDEOS.abbreviation: [CameraAssembly],
    Modality.BEHAVIOR.abbreviation: [[LickSpoutAssembly]],
    Modality.SPIM.abbreviation: [[Laser], [Objective], [ScanningStage]],
}


class ConnectionDirection(str, Enum):
    """Direction of a connection"""

    SEND = "Send"
    RECEIVE = "Receive"
    SEND_AND_RECEIVE = "Send and receive"


class ConnectionData(DataModel):
    """Configuration data for a device connection including direction and port information"""

    direction: Optional[ConnectionDirection] = Field(default=None, title="Connection direction")
    port: Optional[str] = Field(default=None, title="Connection port index/name")


class Connection(DataModel):
    """Description of a connection between devices in an instrument"""

    device_names: List[str] = Field(..., title="Names of connected devices")
    connection_data: Dict[str, ConnectionData] = Field(default={}, title="Connection data")

    @model_validator(mode="after")
    def validate_connection_data(cls, self):
        """Check that all keys in connection_data exist in device_names"""
        for key in self.connection_data.keys():
            if key not in self.device_names:
                raise ValueError(f"Connection data key '{key}' does not exist in device names")

        return self


class Instrument(DataCoreModel):
    """Description of an instrument"""

    # metametadata
    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/instrument.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.34"]] = Field(default="2.0.34")

    # instrument definition
    location: Optional[str] = Field(default=None, title="Location", description="Location of the instrument")
    instrument_id: str = Field(
        ...,
        description="Unique instrument identifier",
        title="Instrument ID",
    )
    modification_date: date = Field(
        ...,
        title="Date of modification",
        description="Date of the last change to the instrument, hardware addition/removal, calibration, etc.",
    )
    modalities: List[Modality.ONE_OF] = Field(
        ...,
        title="Modalities",
        description="List of all possible modalities that the instrument is capable of acquiring",
    )
    calibrations: Optional[List[CALIBRATIONS]] = Field(
        default=None,
        title="Calibrations",
        description="List of calibration measurements takend during instrument setup and maintenance",
    )

    # coordinate system
    coordinate_system: CoordinateSystem = Field(
        ...,
        title="Coordinate system",
        description="Origin and axis definitions for determining the position of the instrument's components",
    )  # note: exact field name is used by a validator

    # instrument details
    temperature_control: Optional[bool] = Field(
        default=None, title="Temperature control", description="Does the instrument maintain a constant temperature?"
    )
    notes: Optional[str] = Field(default=None, title="Notes")

    connections: List[Connection] = Field(
        default=[],
        title="Connections",
        description="List of all connections between devices in the instrument",
    )

    components: DiscriminatedList[
        Monitor
        | Olfactometer
        | LickSpout
        | LickSpoutAssembly
        | AirPuffDevice
        | Speaker
        | CameraAssembly
        | Enclosure
        | EphysAssembly
        | FiberAssembly
        | LaserAssembly
        | FiberPatchCord
        | Laser
        | LightEmittingDiode
        | Lamp
        | Detector
        | Camera
        | Objective
        | Scanner
        | Filter
        | Lens
        | DigitalMicromirrorDevice
        | PolygonalScanner
        | PockelsCell
        | HarpDevice
        | NeuropixelsBasestation
        | OpenEphysAcquisitionBoard
        | MotorizedStage
        | ScanningStage
        | AdditionalImagingDevice
        | Disc
        | Wheel
        | Tube
        | Treadmill
        | Arena
        | DAQDevice
        | Computer
        | Microscope
        | Device
    ] = Field(
        ...,
        title="Components",
        description="List of all devices in the instrument",
    )

    @classmethod
    def get_component_names(cls, instrument: "Instrument") -> List[str]:
        """Get the name field of all components, recurse into assemblies."""

        names = []
        for component in instrument.components:
            names.extend(recursive_get_all_names(component))
        names = [name for name in names if name is not None]

        return names

    @field_validator("modalities", mode="before")
    def validate_modalities(cls, value: List[Modality.ONE_OF]) -> List[Modality.ONE_OF]:
        """Sort modalities"""
        return sorted(value, key=lambda x: x["abbreviation"] if isinstance(x, dict) else x.abbreviation)

    @model_validator(mode="after")
    def validate_cameras_other(self):
        """check if any CameraAssemblies contain an 'other' field"""

        if self.notes is None:
            for component in self.components:
                if isinstance(component, CameraAssembly) and component.target == CameraTarget.OTHER:
                    raise ValueError(
                        f"Notes cannot be empty if a camera target contains an 'Other' field. "
                        f"Describe the camera target from ({component.name}) in the notes field"
                    )

        return self

    @model_validator(mode="after")
    @classmethod
    def validate_connections(cls, self):
        """validate that all connections map between devices that actually exist"""
        device_names = Instrument.get_component_names(self)

        for connection in self.connections:
            for device_name in connection.device_names:
                if device_name not in device_names:
                    raise ValueError(f"Device name validation error: '{device_name}' is not part of the instrument.")

        return self

    @model_validator(mode="after")
    def validate_modality_device_dependencies(cls, value):
        """
        Validate that devices exist for the modalities specified.

        Args:
            cls: The class being validated.
            value: The set of modalities to validate.
            info: Validation information, including other fields.

        Returns:
            The validated set of modalities.

        Raises:
            ValueError: If a required device type is missing for any modality.
        """

        # Return if there are no modalities listed, this is for testing
        if len(value.modalities) == 0:
            return value  # pragma: no cover

        # Retrieve the components from the validation info
        components = value.components
        errors = []

        # Validate each modality
        for modality in value.modalities:
            required_device_groups = DEVICES_REQUIRED.get(modality.abbreviation)
            if not required_device_groups:
                # Skip modalities that don't require validation
                continue  # pragma: no cover

            # Check each group of required devices
            for required_group in required_device_groups:
                if not isinstance(required_group, list):
                    required_group = [required_group]

                # Check if at least one required device is present
                if not any(
                    any(isinstance(component, device_type) for device_type in required_group)
                    for component in components
                ):
                    errors.append(
                        f"Device type validation error: modality '{modality.abbreviation}' "
                        "requires at least one device of type(s) "
                    )
                    errors.append(
                        f"{', '.join(device.__name__ for device in required_group)} " "in the instrument components."
                    )

        # Raise an error if there are validation issues
        if errors:
            raise ValueError("\n".join(errors))

        return value
