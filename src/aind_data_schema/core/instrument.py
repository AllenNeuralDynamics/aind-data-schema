"""Core Instrument model"""

from datetime import date
from typing import List, Literal, Optional, Set, Union

from aind_data_schema_models.modalities import Modality
from pydantic import Field, SkipValidation, ValidationInfo, field_serializer, field_validator, model_validator
from typing_extensions import Annotated

from aind_data_schema_models.organizations import Organization
from aind_data_schema.base import DataCoreModel, DataModel
from aind_data_schema.components.coordinates import Axis, Origin
from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    Calibration,
    CameraAssembly,
    CameraTarget,
    DAQDevice,
    Detector,
    Device,
    DigitalMicromirrorDevice,
    Enclosure,
    EphysAssembly,
    FiberAssembly,
    Filter,
    HarpDevice,
    ImagingInstrumentType,
    Lamp,
    Laser,
    LaserAssembly,
    Lens,
    LightEmittingDiode,
    Monitor,
    MotorizedStage,
    MousePlatform,
    NeuropixelsBasestation,
    Objective,
    Olfactometer,
    OpenEphysAcquisitionBoard,
    OpticalTable,
    Patch,
    PockelsCell,
    PolygonalScanner,
    RewardDelivery,
    ScanningStage,
    Speaker,
)

MOUSE_PLATFORMS = Annotated[Union[tuple(MousePlatform.__subclasses__())], Field(discriminator="device_type")]
instrument_id_PATTERN = r"^[a-zA-Z0-9]+_[a-zA-Z0-9-]+_\d{8}$"


class Com(DataModel):
    """Description of a communication system"""

    hardware_name: str = Field(..., title="Controlled hardware device")
    com_port: str = Field(..., title="COM port")


class Connection(DataModel):
    """Connection between two devices"""

    device_names: List[str] = Field(..., title="Names of connected devices")
    inputs: Optional[List[bool]] = Field(default=None, title="Input status")
    outputs: Optional[List[bool]] = Field(default=None, title="Output status")
    channels: Optional[List[int]] = Field(default=None, title="Connection channels")


class Instrument(DataCoreModel):
    """Description of an instrument"""

    # metametadata
    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/inst.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["1.0.5"]] = Field(default="1.0.5")

    # instrument definition
    instrument_id: str = Field(
        ...,
        description="Unique instrument identifier, name convention: <room>_<apparatus name>_<date modified YYYYMMDD>",
        title="Insturment ID",
        pattern=instrument_id_PATTERN,
    )
    mouse_platform: Optional[MOUSE_PLATFORMS] = Field(default=None, title="Mouse platform")
    modification_date: date = Field(..., title="Date of modification")
    calibrations: Optional[List[Calibration]] = Field(default=None, title="Full calibration of devices")
    ccf_coordinate_transform: Optional[str] = Field(
        default=None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    origin: Optional[Origin] = Field(default=None, title="Origin point for instrument position transforms")
    instrument_axes: Optional[List[Axis]] = Field(default=None, title="Instrument axes", min_length=3, max_length=3)
    modalities: Set[Modality.ONE_OF] = Field(..., title="Modalities")
    com_ports: List[Com] = Field(default=[], title="COM ports")
    instrument_type: Optional[ImagingInstrumentType] = Field(default=None, title="Instrument type")
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
                RewardDelivery,
                Speaker,
                CameraAssembly,
                Enclosure,
                EphysAssembly,
                FiberAssembly,
                LaserAssembly,
                Patch,
                Laser,
                LightEmittingDiode,
                Lamp,
                Detector,
                Objective,
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
                DAQDevice,
                Device,  # note that order matters in the Union, DAQDevice and Device should go last
            ],
            Field(discriminator="device_type"),
        ]
    ] = Field(
        default=[],
        title="Components",
        description="List of all devices in the rig",
    )

    @field_serializer("modalities", when_used="json")
    def serialize_modalities(self, modalities: Set[Modality.ONE_OF]):
        """Dynamically serialize modalities based on their type."""
        return sorted(modalities, key=lambda x: x.get("name") if isinstance(x, dict) else x.name)

    @model_validator(mode="after")
    def validate_cameras_other(self):
        """check if any cameras contain an 'other' field"""

        if self.notes is None:
            for component in self.components:
                if isinstance(component, CameraAssembly) and component.camera_target == CameraTarget.OTHER:
                    raise ValueError(
                        f"Notes cannot be empty if a camera target contains an 'Other' field. "
                        f"Describe the camera target from ({component.name}) in the notes field"
                    )

        return self

    @field_validator("connections", mode="after")
    def validate_device_names(cls, value: List[Connection], info: ValidationInfo) -> List[Connection]:
        """validate that all connections map between devices that actually exist"""
        device_names = [device.name for device in info.data.get("components", [])]

        for connection in value:
            for device_name in connection.device_names:
                if device_name not in device_names:
                    raise ValueError(f"Device name validation error: '{device_name}' is not part of the inst.")

        return value

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

        # Return if there are no modalities listed, this is largely for testing
        if len(value.modalities) == 0:
            return value

        # Define the mapping of modalities to their required device types
        # The list of list pattern is used to allow for multiple options within a group, so e.g.
        # FIB requires a light (one of the options) plus a detector and a patch cord
        type_mapping = {
            Modality.ECEPHYS: [EphysAssembly],
            Modality.FIB: [[Laser, LightEmittingDiode, Lamp], [Detector], [Patch]],
            Modality.POPHYS: [[Laser, LightEmittingDiode, Lamp], [Detector], [Objective]],
            Modality.SLAP: [[Laser, LightEmittingDiode, Lamp], [Detector], [Objective]],
            Modality.BEHAVIOR_VIDEOS: [CameraAssembly],
            Modality.BEHAVIOR: [[Olfactometer, RewardDelivery, Speaker, Monitor]],
            Modality.SPIM: [[Objective], [Detector], [ScanningStage], [MotorizedStage]],
        }

        # Retrieve the components from the validation info
        components = value.components
        errors = []

        # Validate each modality
        for modality in value.modalities:
            required_device_groups = type_mapping.get(modality.abbreviation)
            if not required_device_groups:
                # Skip modalities that don't require validation
                continue

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
                        f"Device type validation error: modality '{modality.abbreviation}' requires at least one device of type(s) "
                        f"{', '.join(device.__name__ for device in required_group)} in the rig components."
                    )

        # Raise an error if there are validation issues
        if errors:
            raise ValueError("\n".join(errors))

        return value
