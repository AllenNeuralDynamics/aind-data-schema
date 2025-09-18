"""Schema describing data acquisition metadata and configurations"""

from decimal import Decimal
from typing import Annotated, List, Literal, Optional

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.stimulus_modality import StimulusModality
from aind_data_schema_models.units import MassUnit, VolumeUnit
from aind_data_schema.utils.validators import TimeValidation
from pydantic import Field, SkipValidation, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel, DiscriminatedList, GenericModel
from aind_data_schema.components.configs import (
    AirPuffConfig,
    DetectorConfig,
    EphysAssemblyConfig,
    FiberAssemblyConfig,
    ImagingConfig,
    LaserConfig,
    LickSpoutConfig,
    LightEmittingDiodeConfig,
    ManipulatorConfig,
    MousePlatformConfig,
    MRIScan,
    PatchCordConfig,
    ProbeConfig,
    SampleChamberConfig,
    SlapPlane,
    SpeakerConfig,
)
from aind_data_schema.components.coordinates import CoordinateSystem
from aind_data_schema.components.identifiers import Code
from aind_data_schema.components.measurements import CALIBRATIONS, Maintenance
from aind_data_schema.components.connections import Connection
from aind_data_schema.components.surgery_procedures import Anaesthetic
from aind_data_schema.utils.merge import merge_notes, merge_optional_list
from aind_data_schema.utils.validators import subject_specimen_id_compatibility

# Define the requirements for each modality
# Define the mapping of modalities to their required device types
# The list of list pattern is used to allow for multiple options within a group, so e.g.
# FIB requires a light config (one of the options) plus a fiber connection config and a fiber module
CONFIG_REQUIREMENTS = {
    Modality.ECEPHYS: [[EphysAssemblyConfig, ProbeConfig, ManipulatorConfig]],
    Modality.FIB: [[LightEmittingDiodeConfig, LaserConfig], [PatchCordConfig, FiberAssemblyConfig]],
    Modality.POPHYS: [[ImagingConfig]],
    Modality.MRI: [[MRIScan]],
    Modality.SPIM: [[ImagingConfig], [SampleChamberConfig]],
    Modality.SLAP: [[ImagingConfig], [SlapPlane]],
}

SPECIMEN_MODALITIES = [Modality.SPIM.abbreviation, Modality.CONFOCAL.abbreviation]


class AcquisitionSubjectDetails(DataModel):
    """Details about the subject during an acquisition"""

    animal_weight_prior: Optional[Decimal] = Field(
        default=None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
    )
    animal_weight_post: Optional[Decimal] = Field(
        default=None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
    )
    weight_unit: MassUnit = Field(default=MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(default=None, title="Anaesthesia")
    mouse_platform_name: str = Field(..., title="Mouse platform")
    reward_consumed_total: Optional[Decimal] = Field(default=None, title="Total reward consumed (mL)")
    reward_consumed_unit: Optional[VolumeUnit] = Field(default=None, title="Reward consumed unit")


class PerformanceMetrics(DataModel):
    """Summary of a StimulusEpoch"""

    output_parameters: GenericModel = Field(default=GenericModel(), title="Additional metrics")
    reward_consumed_during_epoch: Optional[Decimal] = Field(default=None, title="Reward consumed during training (uL)")
    reward_consumed_unit: Optional[VolumeUnit] = Field(default=None, title="Reward consumed unit")
    trials_total: Optional[int] = Field(default=None, title="Total trials")
    trials_finished: Optional[int] = Field(default=None, title="Finished trials")
    trials_rewarded: Optional[int] = Field(default=None, title="Rewarded trials")


class DataStream(DataModel):
    """A set of devices that are acquiring data and their configurations starting and stopping at approximately the
    same time.
    """

    stream_start_time: Annotated[
        AwareDatetimeWithDefault,
        Field(..., title="Stream start time"),
        TimeValidation.BETWEEN,
    ]
    stream_end_time: Annotated[
        AwareDatetimeWithDefault,
        Field(..., title="Stream stop time"),
        TimeValidation.BETWEEN,
    ]
    modalities: List[Modality.ONE_OF] = Field(
        ..., title="Modalities", description="Modalities that are acquired in this stream"
    )
    code: Optional[List[Code]] = Field(default=None, title="Acquisition code")
    notes: Optional[str] = Field(default=None, title="Notes")

    active_devices: List[str] = Field(
        ...,
        title="Active devices",
        description="Device names must match devices in the Instrument",
    )

    configurations: DiscriminatedList[
        LightEmittingDiodeConfig
        | LaserConfig
        | ManipulatorConfig
        | DetectorConfig
        | PatchCordConfig
        | FiberAssemblyConfig
        | MRIScan
        | LickSpoutConfig
        | AirPuffConfig
        | ImagingConfig
        | SlapPlane
        | SampleChamberConfig
        | ProbeConfig
        | EphysAssemblyConfig
    ] = Field(
        ...,
        title="Device configurations",
        description="Configurations are parameters controlling active devices during this stream",
    )

    connections: List[Connection] = Field(
        default=[],
        title="Connections",
        description=(
            "Connections are links between devices that are specific to this acquisition (i.e."
            " not already defined in the Instrument)"
        ),
    )

    @model_validator(mode="after")
    def check_modality_config_requirements(self):
        """Check that the required devices are present for the modalities"""
        for modality in self.modalities:
            if modality not in CONFIG_REQUIREMENTS.keys():
                # No configuration requirements for this modality
                continue  # pragma: no cover

            for group in CONFIG_REQUIREMENTS[modality]:
                if not any(isinstance(config, device_type) for config in self.configurations for device_type in group):
                    # Get the types of all configurations
                    group_types = [device_type.__name__ for device_type in group]
                    config_types = [type(config).__name__ for config in self.configurations]
                    raise ValueError(
                        f"Missing one of required devices {group_types} for modality {modality.name} in {config_types}"
                    )

        return self

    @model_validator(mode="after")
    def check_connections(self):
        """Check that every device in a Connection is present in the active_devices list"""
        for connection in self.connections:
            # Check that both source and target devices are in active_devices
            if (
                connection.source_device not in self.active_devices
                or connection.target_device not in self.active_devices
            ):
                missing_devices = []
                if connection.source_device not in self.active_devices:
                    missing_devices.append(connection.source_device)
                if connection.target_device not in self.active_devices:
                    missing_devices.append(connection.target_device)
                raise ValueError(
                    f"Missing devices in active_devices list for connection "
                    f"from '{connection.source_device}' to '{connection.target_device}': {missing_devices}"
                )

        return self


class StimulusEpoch(DataModel):
    """All stimuli being presented to the subject. starting and stopping at approximately the
    same time. Not all acquisitions have StimulusEpochs.
    """

    stimulus_start_time: Annotated[AwareDatetimeWithDefault, TimeValidation.BETWEEN] = Field(
        ...,
        title="Stimulus start time",
        description="When a specific stimulus begins. This might be the same as the acquisition start time.",
    )
    stimulus_end_time: Annotated[AwareDatetimeWithDefault, TimeValidation.BETWEEN] = Field(
        ...,
        title="Stimulus end time",
        description="When a specific stimulus ends. This might be the same as the acquisition end time.",
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    code: Optional[Code] = Field(
        default=None,
        title="Code or script",
        description=(
            "Custom code/script used to control the behavior/stimulus."
            " Use the Code.parameters field to store stimulus properties"
        ),
    )
    stimulus_modalities: List[StimulusModality] = Field(..., title="Stimulus modalities")
    performance_metrics: Optional[PerformanceMetrics] = Field(default=None, title="Performance metrics")
    notes: Optional[str] = Field(default=None, title="Notes")

    # Devices and configurations
    active_devices: List[str] = Field(
        default=[],
        title="Active devices",
        description="Device names must match devices in the Instrument",
    )
    configurations: DiscriminatedList[SpeakerConfig | LightEmittingDiodeConfig | LaserConfig | MousePlatformConfig] = (
        Field(default=[], title="Device configurations")
    )

    # Training protocol
    training_protocol_name: Optional[str] = Field(
        default=None,
        title="Training protocol name",
        description=(
            "Name of the training protocol used during the acquisition, " "must match a protocol in the Procedures"
        ),
    )
    curriculum_status: Optional[str] = Field(
        default=None,
        title="Curriculum status",
        description="Status within the training protocol curriculum",
    )


class Acquisition(DataCoreModel):
    """Description of data acquisition metadata including streams, stimuli, and experimental setup.

    The acquisition metadata is split into two parallel pieces: the DataStream and the StimulusEpoch.
    At any given moment in time the active DataStream(s) represents all modalities of data being acquired,
    while the StimulusEpoch represents all stimuli being presented."""

    # Meta metadata
    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/acquisition.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.36"]] = Field(default="2.0.36")

    # ID
    subject_id: str = Field(default=..., title="Subject ID", description="Unique identifier for the subject")
    specimen_id: Optional[str] = Field(
        default=None, title="Specimen ID", description="Specimen ID is required for in vitro imaging modalities"
    )

    # Acquisition metadata
    acquisition_start_time: AwareDatetimeWithDefault = Field(..., title="Acquisition start time")
    acquisition_end_time: AwareDatetimeWithDefault = Field(..., title="Acquisition end time")
    experimenters: List[str] = Field(
        default=[],
        title="experimenter(s)",
    )
    protocol_id: Optional[List[str]] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    ethics_review_id: Optional[List[str]] = Field(default=None, title="Ethics review ID")
    instrument_id: str = Field(..., title="Instrument ID", description="Should match the Instrument.instrument_id")
    acquisition_type: str = Field(
        ...,
        title="Acquisition type",
        description=(
            "Descriptive string detailing the type of acquisition, "
            "should be consistent across similar acquisitions for the same experiment."
        ),
    )
    notes: Optional[str] = Field(default=None, title="Notes")

    # Coordinate system
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Coordinate system",
        description=(
            "Origin and axis definitions for determining the configured position of devices during acquisition."
            " Required when coordinates are provided within the Acquisition"
        ),
    )  # note: exact field name is used by a validator

    # Instrument metadata
    calibrations: List[CALIBRATIONS] = Field(
        default=[],
        title="Calibrations",
        description="List of calibration measurements taken prior to acquisition.",
    )
    maintenance: List[Maintenance] = Field(
        default=[], title="Maintenance", description="List of maintenance on instrument prior to acquisition."
    )

    # Acquisition data
    data_streams: List[DataStream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are acquiring data simultaneously. Each acquisition can "
            "include multiple streams. Streams should be split when configurations are changed."
        ),
    )
    stimulus_epochs: List[StimulusEpoch] = Field(
        default=[],
        title="Stimulus",
        description=(
            "A stimulus epoch captures all stimuli being presented during an acquisition."
            " Epochs should be split when the purpose of the stimulus changes."
        ),
    )
    subject_details: Optional[AcquisitionSubjectDetails] = Field(default=None, title="Subject details")

    @model_validator(mode="after")
    def subject_details_if_not_specimen(self):
        """Check that subject details are present if no specimen ID"""
        if not self.specimen_id and not self.subject_details:
            raise ValueError("Subject details are required for in vivo experiments")

        return self

    @model_validator(mode="after")
    def check_subject_specimen_id(self):
        """Check that the subject and specimen IDs match"""
        if self.specimen_id and self.subject_id:
            if not subject_specimen_id_compatibility(self.subject_id, self.specimen_id):
                raise ValueError(f"Expected {self.subject_id} to appear in {self.specimen_id}")

        return self

    @model_validator(mode="after")
    def specimen_required(self):
        """Check if specimen ID is required for in vitro imaging modalities"""

        if not hasattr(self, "data_streams"):  # bypass for testing
            return self

        for stream in self.data_streams:
            if any([modality.abbreviation in SPECIMEN_MODALITIES for modality in stream.modalities]):
                if not self.specimen_id:
                    raise ValueError(f"Specimen ID is required for modalities {stream.modalities}")

        return self

    def __add__(self, other: "Acquisition") -> "Acquisition":
        """Combine two Acquisition objects"""

        # Check for schema version incompability
        if self.schema_version != other.schema_version:
            raise ValueError(
                "Cannot combine Acquisition objects with different schema "
                + f"versions: {self.schema_version} and {other.schema_version}"
            )

        # Check for incompatible key fields
        subj_check = self.subject_id != other.subject_id
        spec_check = self.specimen_id != other.specimen_id
        inst_check = self.instrument_id != other.instrument_id
        exp_type_check = self.acquisition_type != other.acquisition_type
        cs_check = self.coordinate_system != other.coordinate_system
        if any([subj_check, spec_check, inst_check, exp_type_check, cs_check]):
            raise ValueError(
                "Cannot combine Acquisition objects that differ in key fields:\n"
                f"subject_id: {self.subject_id}/{other.subject_id}\n"
                f"specimen_id: {self.specimen_id}/{other.specimen_id}\n"
                f"instrument_id: {self.instrument_id}/{other.instrument_id}\n"
                f"acquisition_type: {self.acquisition_type}/{other.acquisition_type}"
                f"coordinate_system: {self.coordinate_system}/{other.coordinate_system}"
            )

        details_check = self.subject_details and other.subject_details
        if details_check:
            raise ValueError(
                "SubjectDetails cannot be combined in Acquisition. Only a single set of details is allowed."
            )

        # Combine
        experimenters = self.experimenters + other.experimenters
        protocol_id = merge_optional_list(self.protocol_id, other.protocol_id)
        ethics_review_id = merge_optional_list(self.ethics_review_id, other.ethics_review_id)
        calibrations = self.calibrations + other.calibrations
        maintenance = self.maintenance + other.maintenance
        data_streams = self.data_streams + other.data_streams
        stimulus_epochs = self.stimulus_epochs + other.stimulus_epochs

        # Combine notes
        notes = merge_notes(self.notes, other.notes)

        # Handle start and end time
        start_time = min(self.acquisition_start_time, other.acquisition_start_time)
        end_time = max(self.acquisition_end_time, other.acquisition_end_time)

        return Acquisition(
            subject_id=self.subject_id,
            specimen_id=self.specimen_id,
            experimenters=experimenters,
            protocol_id=protocol_id,
            ethics_review_id=ethics_review_id,
            instrument_id=self.instrument_id,
            calibrations=calibrations,
            coordinate_system=self.coordinate_system,
            maintenance=maintenance,
            acquisition_start_time=start_time,
            acquisition_end_time=end_time,
            acquisition_type=self.acquisition_type,
            notes=notes,
            data_streams=data_streams,
            stimulus_epochs=stimulus_epochs,
            subject_details=self.subject_details if self.subject_details else other.subject_details,
        )
