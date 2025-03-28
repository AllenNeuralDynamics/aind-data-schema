""" schema describing imaging acquisition """

from decimal import Decimal
from typing import Annotated, List, Literal, Optional, Union

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import MassUnit, VolumeUnit
from pydantic import Field, SkipValidation, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel, GenericModel, GenericModelType
from aind_data_schema.components.configs import (
    AirPuffConfig,
    DetectorConfig,
    DomeModule,
    FiberAssemblyConfig,
    FieldOfView,
    InVitroImagingConfig,
    LaserConfig,
    LickSpoutConfig,
    LightEmittingDiodeConfig,
    ManipulatorConfig,
    MousePlatformConfig,
    MRIScan,
    PatchCordConfig,
    SlapFieldOfView,
    SpeakerConfig,
    Stack,
    StimulusModality,
)
from aind_data_schema.components.coordinates import CoordinateSystem
from aind_data_schema.components.devices import Camera, CameraAssembly, EphysAssembly, FiberAssembly
from aind_data_schema.components.identifiers import Code, Person, Software
from aind_data_schema.components.measurements import CALIBRATIONS, Maintenance
from aind_data_schema.core.procedures import Anaesthetic
from aind_data_schema.utils.merge import merge_notes, merge_optional_list
from aind_data_schema.utils.validators import subject_specimen_id_compatibility

# Define the requirements for each modality
# Define the mapping of modalities to their required device types
# The list of list pattern is used to allow for multiple options within a group, so e.g.
# FIB requires a light config (one of the options) plus a fiber connection config and a fiber module
CONFIG_REQUIREMENTS = {
    Modality.ECEPHYS: [[DomeModule, ManipulatorConfig]],
    Modality.FIB: [[LightEmittingDiodeConfig, LaserConfig], [PatchCordConfig, FiberAssemblyConfig]],
    Modality.POPHYS: [[FieldOfView, SlapFieldOfView, Stack]],
    Modality.MRI: [[MRIScan]],
}

# This is ugly but one of the validators was just checking that the cameras were active in the device name list
# so to replace that I'm going to add a validator that searches the instrument to make sure the active_devices
# list contains a valid Camera and/or CameraAssembly. Note that this validator has to go in the `metadata` class
MODALITY_DEVICE_REQUIREMENTS = {
    Modality.BEHAVIOR_VIDEOS: [[CameraAssembly, Camera]],
}
CONFIG_DEVICE_REQUIREMENTS = {
    "DomeModule": [EphysAssembly],
    "FiberAssemblyConfig": [FiberAssembly],
}

SPECIMEN_MODALITIES = [Modality.SPIM.abbreviation, Modality.CONFOCAL.abbreviation]


class SubjectDetails(DataModel):
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

    output_parameters: GenericModelType = Field(default=GenericModel(), title="Additional metrics")
    reward_consumed_during_epoch: Optional[Decimal] = Field(default=None, title="Reward consumed during training (uL)")
    reward_consumed_unit: Optional[VolumeUnit] = Field(default=None, title="Reward consumed unit")
    trials_total: Optional[int] = Field(default=None, title="Total trials")
    trials_finished: Optional[int] = Field(default=None, title="Finished trials")
    trials_rewarded: Optional[int] = Field(default=None, title="Rewarded trials")


class DataStream(DataModel):
    """Data streams with a start and stop time"""

    stream_start_time: AwareDatetimeWithDefault = Field(..., title="Stream start time")
    stream_end_time: AwareDatetimeWithDefault = Field(..., title="Stream stop time")
    modalities: List[Modality.ONE_OF] = Field(..., title="Modalities")
    software: Optional[List[Software]] = Field(default=[], title="Software packages")
    notes: Optional[str] = Field(default=None, title="Notes")

    active_devices: List[str] = Field(
        ...,
        title="Active devices",
        description="Device names must match devices in the Instrument",
    )

    configurations: List[
        Annotated[
            Union[
                LightEmittingDiodeConfig,
                LaserConfig,
                ManipulatorConfig,
                DomeModule,
                DetectorConfig,
                PatchCordConfig,
                FiberAssemblyConfig,
                FieldOfView,
                SlapFieldOfView,
                Stack,
                MRIScan,
                InVitroImagingConfig,
                LickSpoutConfig,
                AirPuffConfig,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(..., title="Device configurations")

    @model_validator(mode="after")
    def check_modality_config_requirements(self):
        """Check that the required devices are present for the modalities"""
        for modality in self.modalities:
            if modality not in CONFIG_REQUIREMENTS.keys():
                # No configuration requirements for this modality
                continue

            for group in CONFIG_REQUIREMENTS[modality]:
                if not any(isinstance(config, device) for config in self.configurations for device in group):
                    raise ValueError(f"Missing required devices for modality {modality} in {self.configurations}")

        return self


class StimulusEpoch(DataModel):
    """Description of stimulus used during data acquisition"""

    stimulus_start_time: AwareDatetimeWithDefault = Field(
        ...,
        title="Stimulus start time",
        description="When a specific stimulus begins. This might be the same as the acquisition start time.",
    )
    stimulus_end_time: AwareDatetimeWithDefault = Field(
        ...,
        title="Stimulus end time",
        description="When a specific stimulus ends. This might be the same as the acquisition end time.",
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    code: Optional[Code] = Field(
        default=None,
        title="Code or script",
        description="Custom code/script used to control the behavior/stimulus and parameters",
    )
    stimulus_modalities: List[StimulusModality] = Field(..., title="Stimulus modalities")
    summary: Optional[PerformanceMetrics] = Field(default=None, title="Summary")
    notes: Optional[str] = Field(default=None, title="Notes")

    active_devices: List[str] = Field(
        default=[],
        title="Active devices",
        description="Device names must match devices in the Instrument",
    )

    configurations: List[
        Annotated[
            Union[
                SpeakerConfig,
                LightEmittingDiodeConfig,
                LaserConfig,
                MousePlatformConfig,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(default=[], title="Device configurations")


class Acquisition(DataCoreModel):
    """Description of an imaging acquisition"""

    # Meta metadata
    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/acquisition.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.14"]] = Field(default="2.0.14")

    # ID
    subject_id: str = Field(default=..., title="Subject ID")
    specimen_id: Optional[str] = Field(
        default=None, title="Specimen ID", description="Specimen ID is required for in vitro imaging modalities"
    )

    # Acquisition metadata
    acquisition_start_time: AwareDatetimeWithDefault = Field(..., title="Acquisition start time")
    acquisition_end_time: AwareDatetimeWithDefault = Field(..., title="Acquisition end time")
    experimenters: List[Person] = Field(
        default=[],
        title="experimenter(s)",
    )
    protocol_id: List[str] = Field(default=[], title="Protocol ID", description="DOI for protocols.io")
    ethics_review_id: Optional[str] = Field(default=None, title="Ethics review ID")
    instrument_id: str = Field(..., title="Instrument ID")
    experiment_type: str = Field(default=None, title="Experiment type")
    software: Optional[List[Software]] = Field(default=[], title="Acquisition software")
    notes: Optional[str] = Field(default=None, title="Notes")
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Coordinate system",
        description="Required when coordinates are provided within the Acquisition",
    )

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
            "A data stream is a collection of devices that are recorded simultaneously. Each acquisition can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
    )
    stimulus_epochs: List[StimulusEpoch] = Field(default=[], title="Stimulus")
    subject_details: Optional[SubjectDetails] = Field(default=None, title="Subject details")

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
        ethics_check = self.ethics_review_id != other.ethics_review_id
        inst_check = self.instrument_id != other.instrument_id
        exp_type_check = self.experiment_type != other.experiment_type
        if any([subj_check, spec_check, ethics_check, inst_check, exp_type_check]):
            raise ValueError(
                "Cannot combine Acquisition objects that differ in key fields:\n"
                f"subject_id: {self.subject_id}/{other.subject_id}\n"
                f"specimen_id: {self.specimen_id}/{other.specimen_id}\n"
                f"ethics_review_id: {self.ethics_review_id}/{other.ethics_review_id}\n"
                f"instrument_id: {self.instrument_id}/{other.instrument_id}\n"
                f"experiment_type: {self.experiment_type}/{other.experiment_type}"
            )

        details_check = self.subject_details and other.subject_details
        if details_check:
            raise ValueError(
                "SubjectDetails cannot be combined in Acquisition. Only a single set of details is allowed."
            )

        # Combine
        experimenters = self.experimenters + other.experimenters
        protocol_id = self.protocol_id + other.protocol_id
        calibrations = self.calibrations + other.calibrations
        maintenance = self.maintenance + other.maintenance
        software = merge_optional_list(self.software, other.software)
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
            ethics_review_id=self.ethics_review_id,
            instrument_id=self.instrument_id,
            calibrations=calibrations,
            maintenance=maintenance,
            acquisition_start_time=start_time,
            acquisition_end_time=end_time,
            experiment_type=self.experiment_type,
            software=software,
            notes=notes,
            data_streams=data_streams,
            stimulus_epochs=stimulus_epochs,
            subject_details=self.subject_details if self.subject_details else other.subject_details,
        )
