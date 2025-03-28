"""Core Instrument model"""

from datetime import date
from enum import Enum
from typing import Dict, List, Literal, Optional, Set, Union

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import Field, SkipValidation, ValidationInfo, field_serializer, field_validator, model_validator
from typing_extensions import Annotated

from aind_data_schema.base import DataCoreModel, DataModel
from aind_data_schema.components.coordinates import CoordinateSystem
from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    AirPuffDevice,
    Arena,
    CameraAssembly,
    CameraTarget,
    DAQDevice,
    Detector,
    Device,
    DigitalMicromirrorDevice,
    Disc,
    Enclosure,
    EphysAssembly,
    FiberAssembly,
    Filter,
    HarpDevice,
    Lamp,
    Laser,
    LaserAssembly,
    Lens,
    LickSpout,
    LickSpoutAssembly,
    LightEmittingDiode,
    Monitor,
    MotorizedStage,
    MousePlatform,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OpenEphysAcquisitionBoard,
    OpticalTable,
    PatchCord,
    PockelsCell,
    PolygonalScanner,
    Scanner,
    ScanningStage,
    Speaker,
    Treadmill,
    Tube,
    Wheel,
    Scanner,
    Computer,
)
from aind_data_schema.components.measurements import CALIBRATIONS
from aind_data_schema.utils.validators import recursive_get_all_names

# Define the mapping of modalities to their required device types
# The list of list pattern is used to allow for multiple options within a group, so e.g.
# FIB requires a light (one of the options) plus a detector and a patch cord
DEVICES_REQUIRED = {
    Modality.ECEPHYS.abbreviation: [EphysAssembly],
    Modality.FIB.abbreviation: [[Laser, LightEmittingDiode, Lamp], [Detector], [PatchCord]],
    Modality.POPHYS.abbreviation: [[Laser], [Detector], [Objective]],
    Modality.SLAP.abbreviation: [[Laser], [Detector], [Objective], [DigitalMicromirrorDevice]],
    Modality.BEHAVIOR_VIDEOS.abbreviation: [CameraAssembly],
    Modality.BEHAVIOR.abbreviation: [[LickSpoutAssembly]],
    Modality.SPIM.abbreviation: [[Laser], [Objective], [ScanningStage]],
}


class ConnectionDirection(str, Enum):
    """Direction of a connection"""

    SEND = "send"
    RECEIVE = "receive"


class ConnectionData(DataModel):
    """Data for a connection"""

    direction: Optional[ConnectionDirection] = Field(default=None, title="Connection direction")
    channel: Optional[str] = Field(default=None, title="Connection channel or port index")


class Connection(DataModel):
    """Connection between two devices"""

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
    schema_version: SkipValidation[Literal["2.0.14"]] = Field(default="2.0.14")

    # instrument definition
    instrument_id: str = Field(
        ...,
        description="Unique instrument identifier, name convention: <room>_<apparatus name>_<date modified YYYYMMDD>",
        title="Instrument ID",
    )
    modification_date: date = Field(..., title="Date of modification")
    modalities: List[Modality.ONE_OF] = Field(..., title="Modalities")
    calibrations: Optional[List[CALIBRATIONS]] = Field(default=None, title="Full calibration of devices")

    # coordinate system
    coordinate_system: CoordinateSystem = Field(..., title="Coordinate system")

    # instrument details
    manufacturer: Optional[Organization.ONE_OF] = Field(default=None, title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(default=None, title="Temperature control")
    notes: Optional[str] = Field(default=None, title="Notes")

    connections: List[Connection] = Field(
        default=[],
        title="Connections",
        description="List of all connections between devices in the instrument",
    )

    components: List[
        Annotated[
            Union[
                Monitor,
                Olfactometer,
                LickSpout,
                LickSpoutAssembly,
                AirPuffDevice,
                Speaker,
                CameraAssembly,
                Enclosure,
                EphysAssembly,
                FiberAssembly,
                LaserAssembly,
                PatchCord,
                Laser,
                LightEmittingDiode,
                Lamp,
                Detector,
                Objective,
                Scanner,
                Filter,
                Lens,
                DigitalMicromirrorDevice,
                PolygonalScanner,
                PockelsCell,
                HarpDevice,
                NeuropixelsBasestation,
                OpenEphysAcquisitionBoard,
                OpticalTable,
                MotorizedStage,
                ScanningStage,
                AdditionalImagingDevice,
                Disc,
                Wheel,
                Tube,
                Treadmill,
                Arena,
                MousePlatform,
                DAQDevice,
                Computer,
                Device,
            ],
            Field(discriminator="object_type"),
        ]
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

    @field_serializer("modalities", when_used="json")
    def serialize_modalities(self, modalities: Set[Modality.ONE_OF]):
        """Dynamically serialize modalities based on their type."""
        return sorted(modalities, key=lambda x: x.get("name") if isinstance(x, dict) else x.name)

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

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("manufacturer") == Organization.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if manufacturer is Other. Describe the manufacturer in the notes field."
            )
        return value

    @model_validator(mode="after")
    def validate_modalities(cls, value):
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
