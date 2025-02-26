""" schema describing imaging acquisition """

from decimal import Decimal
from typing import List, Literal, Optional, Union

from aind_data_schema_models.process_names import ProcessName
from pydantic import Field, SkipValidation, field_validator, Annotated
from pydantic_core.core_schema import ValidationInfo

from aind_data_schema.base import DataCoreModel, DataModel, AwareDatetimeWithDefault
from aind_data_schema.components.coordinates import AnatomicalDirection, AxisName, ImageAxis
from aind_data_schema.components.devices import Calibration, ImmersionMedium, Maintenance
from aind_data_schema.components.tile import AcquisitionTile
from aind_data_schema.components.identifiers import Person, Software

from aind_data_schema.components.configs import (
    DomeModule,
    FiberConnectionConfig,
    FiberModule,
    ManipulatorModule,
    DetectorConfig,
    FieldOfView,
    SlapFieldOfView,
    SpeakerConfig,
    LightEmittingDiodeConfig,
    LaserConfig,
    ArenaConfig,
    Stack,
    MRIScan,
)
from aind_data_schema.components.stimulus import (
    AuditoryStimulation,
    OlfactoryStimulation,
    OptoStimulation,
    PhotoStimulation,
    VisualStimulation,
)

from aind_data_schema_models.modalities import Modality, StimulusModality


class Stream(DataModel):
    """Data streams with a start and stop time"""

    stream_start_time: AwareDatetimeWithDefault = Field(..., title="Stream start time")
    stream_end_time: AwareDatetimeWithDefault = Field(..., title="Stream stop time")
    modalities: List[Modality.ONE_OF] = Field(..., title="Modalities")
    software: Optional[List[Software]] = Field(default=[], title="Software packages")
    notes: Optional[str] = Field(default=None, title="Notes")

    active_devices: List[str] = Field(..., title="Active devices")

    configurations: List[
        Annotated[
            Union[
                LightEmittingDiodeConfig,
                LaserConfig,
                ManipulatorModule,
                DomeModule,
                DetectorConfig,
                FiberConnectionConfig,
                FiberModule,
                FieldOfView,
                SlapFieldOfView,
                Stack,
                MRIScan,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(..., title="Active devices")

    @staticmethod
    def _validate_ephys_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate ecephys modality has ephys_assemblies and stick_microscopes"""
        if Modality.ECEPHYS in value:
            ephys_modules = info.data["ephys_modules"]
            for k, v in {
                "ephys_modules": ephys_modules,
            }.items():
                if not v:
                    return f"{k} field must be utilized for Ecephys modality"
        return None

    @staticmethod
    def _validate_fib_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate FIB modality has light_sources, detectors, and fiber_connections"""
        if Modality.FIB in value:
            light_source = info.data["light_sources"]
            detector = info.data["detectors"]
            fiber_connections = info.data["fiber_connections"]
            for k, v in {
                "light_sources": light_source,
                "detectors": detector,
                "fiber_connections": fiber_connections,
            }.items():
                if not v:
                    return f"{k} field must be utilized for FIB modality"
        return None

    @staticmethod
    def _validate_pophys_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate POPHYS modality has ophys_fovs and stack_parameters"""
        if Modality.POPHYS in value:
            ophys_fovs = info.data["ophys_fovs"]
            stack_parameters = info.data["stack_parameters"]
            if not ophys_fovs and not stack_parameters:
                return "ophys_fovs field OR stack_parameters field must be utilized for Pophys modality"
        else:
            return None

    @staticmethod
    def _validate_behavior_videos_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate BEHAVIOR_VIDEOS modality has cameras"""
        if Modality.BEHAVIOR_VIDEOS in value and len(info.data["camera_names"]) == 0:
            return "camera_names field must be utilized for Behavior Videos modality"
        else:
            return None

    @staticmethod
    def _validate_mri_modality(value: List[Modality.ONE_OF], info: ValidationInfo) -> Optional[str]:
        """Validate MRI modality has scans"""
        if Modality.MRI in value:
            scans = info.data["mri_scans"]
            if not scans:
                return "mri_scans field must be utilized for MRI modality"
        else:
            return None

    @field_validator("stream_modalities", mode="after")
    def validate_stream_modalities(cls, value: List[Modality.ONE_OF], info: ValidationInfo) -> List[Modality.ONE_OF]:
        """Validate each modality in stream_modalities field has associated data"""
        errors = []
        ephys_errors = cls._validate_ephys_modality(value, info)
        fib_errors = cls._validate_fib_modality(value, info)
        pophys_errors = cls._validate_pophys_modality(value, info)
        behavior_vids_errors = cls._validate_behavior_videos_modality(value, info)
        mri_errors = cls._validate_mri_modality(value, info)

        if ephys_errors is not None:
            errors.append(ephys_errors)
        if fib_errors is not None:
            errors.append(fib_errors)
        if pophys_errors is not None:
            errors.append(pophys_errors)
        if behavior_vids_errors is not None:
            errors.append(behavior_vids_errors)
        if mri_errors is not None:
            errors.append(mri_errors)
        if len(errors) > 0:
            message = "\n     ".join(errors)
            raise ValueError(message)
        return value


class StimulusEpoch(DataModel):
    """Description of stimulus used during session"""

    stimulus_start_time: AwareDatetimeWithDefault = Field(
        ...,
        title="Stimulus start time",
        description="When a specific stimulus begins. This might be the same as the session start time.",
    )
    stimulus_end_time: AwareDatetimeWithDefault = Field(
        ...,
        title="Stimulus end time",
        description="When a specific stimulus ends. This might be the same as the session end time.",
    )
    stimulus_name: str = Field(..., title="Stimulus name")
    code: Optional[Code] = Field(
        default=None,
        title="Code or script",
        description="Custom code or script used to control the behavior/stimulus",
    )
    modalities: List[StimulusModality] = Field(..., title="Stimulus modalities")
    output_parameters: GenericModelType = Field(default=GenericModel(), title="Performance metrics")
    reward_consumed_during_epoch: Optional[Decimal] = Field(default=None, title="Reward consumed during training (uL)")
    reward_consumed_unit: VolumeUnit = Field(default=VolumeUnit.UL, title="Reward consumed unit")
    trials_total: Optional[int] = Field(default=None, title="Total trials")
    trials_finished: Optional[int] = Field(default=None, title="Finished trials")
    trials_rewarded: Optional[int] = Field(default=None, title="Rewarded trials")
    notes: Optional[str] = Field(default=None, title="Notes")

    stimulus_parameters: Optional[
        List[
            Annotated[
                Union[AuditoryStimulation, OptoStimulation, OlfactoryStimulation, PhotoStimulation, VisualStimulation],
                Field(discriminator="object_type"),
            ]
        ]
    ] = Field(default=[], title="Stimulus parameters")

    active_devices = List[str] = Field(..., title="Active devices")

    configurations = List[
        Annotated[
            Union[
                SpeakerConfig,
                LightEmittingDiodeConfig,
                LaserConfig,
                ArenaConfig,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(default=[], title="Active devices")


class Acquisition(DataCoreModel):
    """Description of an imaging acquisition session"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/acquisition.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.3"]] = Field(default="2.0.3")
    protocol_id: List[str] = Field(default=[], title="Protocol ID", description="DOI for protocols.io")
    experimenters: List[Person] = Field(
        default=[],
        title="experimenter(s)",
    )
    subject_id: str = Field(default=None, title="Subject ID")
    specimen_id: Optional[str] = Field(..., title="Specimen ID")
    instrument_id: str = Field(..., title="Instrument ID")
    ethics_review_id: Optional[str] = Field(default=None, title="Ethics review ID")

    calibrations: List[Calibration] = Field(
        default=[],
        title="Calibrations",
        description="List of calibration measurements taken prior to acquisition.",
    )
    maintenance: List[Maintenance] = Field(
        default=[], title="Maintenance", description="List of maintenance on instrument prior to acquisition."
    )
    acquisition_start_time: AwareDatetimeWithDefault = Field(..., title="Acquisition start time")
    acquisition_end_time: AwareDatetimeWithDefault = Field(..., title="Acquisition end time")
    acquisition_type: Optional[str] = Field(default=None, title="Acquisition type")
    local_storage_directory: Optional[str] = Field(default=None, title="Local storage directory")
    external_storage_directory: Optional[str] = Field(default=None, title="External storage directory")

    software: Optional[List[Software]] = Field(default=[], title="Acquisition software")
    notes: Optional[str] = Field(default=None, title="Notes")

    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
    )
    stimulus_epochs: List[StimulusEpoch] = Field(default=[], title="Stimulus")

    # Fields coming from session
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

    # Todo: validator for subject + specimen ID, compare first six digits

    # Todo: modality -> specimen ID validator
