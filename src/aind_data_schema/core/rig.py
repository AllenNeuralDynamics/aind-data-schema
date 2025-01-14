"""Core Rig model"""

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
RIG_ID_PATTERN = r"^[a-zA-Z0-9]+_[a-zA-Z0-9-]+_\d{8}$"


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


class Rig(DataCoreModel):
    """Description of a rig"""

    # metametadata
    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/rig.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["1.0.5"]] = Field(default="1.0.5")

    # rig definition
    rig_id: str = Field(
        ...,
        description="Unique rig identifier, name convention: <room>-<apparatus name>-<date modified YYYYMMDD>",
        title="Rig ID",
        pattern=RIG_ID_PATTERN,
    )
    mouse_platform: Optional[MOUSE_PLATFORMS] = Field(default=None, title="Mouse platform")
    modification_date: date = Field(..., title="Date of modification")
    calibrations: Optional[List[Calibration]] = Field(default=None, title="Full calibration of devices")
    ccf_coordinate_transform: Optional[str] = Field(
        default=None,
        title="CCF coordinate transform",
        description="Path to file that details the CCF-to-lab coordinate transform",
    )
    origin: Optional[Origin] = Field(default=None, title="Origin point for rig position transforms")
    rig_axes: Optional[List[Axis]] = Field(default=None, title="Rig axes", min_length=3, max_length=3)
    modalities: Set[Modality.ONE_OF] = Field(..., title="Modalities")
    com_ports: List[Com] = Field(default=[], title="COM ports")
    instrument_type: Optional[ImagingInstrumentType] = Field(default=None, title="Instrument type")
    manufacturer: Optional[Organization.ONE_OF] = Field(default=None, title="Instrument manufacturer")
    temperature_control: Optional[bool] = Field(default=None, title="Temperature control")
    notes: Optional[str] = Field(default=None, title="Notes")

    connections: List[Connection] = Field(
        default=[],
        title="Connections",
        description="List of all connections between devices in the rig",
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
        """validate that all connections map between devices that actually exist
        """
        device_names = [device.name for device in info.data.get("components", [])]

        for connection in value:
            for device_name in connection.device_names:
                if device_name not in device_names:
                    raise ValueError(
                        f"Device name validation error: '{device_name}' is not part of the rig."
                    )

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

    @field_validator("modalities", mode="after")
    def validate_modalities(cls, value: Set[Modality.ONE_OF], info: ValidationInfo) -> Set[Modality.ONE_OF]:
        """Validate that devices exist for the modalities specified"""

        type_mapping = {
            Modality.ECEPHYS.abbreviation: [EphysAssembly],
            Modality.FIB.abbreviation: [
                [Laser, LightEmittingDiode, Lamp],
                [Detector],
                [Patch]
            ],
            Modality.POPHYS.abbreviation: [
                [Laser, LightEmittingDiode, Lamp],
                [Detector],
                [Objective]
            ],
            Modality.SLAP.abbreviation: [
                [Laser, LightEmittingDiode, Lamp],
                [Detector],
                [Objective]
            ],
            Modality.BEHAVIOR_VIDEOS.abbreviation: [CameraAssembly],
            Modality.BEHAVIOR.abbreviation: [Olfactometer, RewardDelivery, Speaker, Monitor],
        }

        errors = []

        for modality in value:
            if modality.abbreviation in type_mapping:
                for device_type in type_mapping[modality.abbreviation]:
                    if not any(isinstance(component, device) for device in device_type for component in info.data.get("components", [])):
                        errors.append(
                            f"Device type validation error: No device of type {device_type} is part of the rig."
                        )

        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)

        return value
