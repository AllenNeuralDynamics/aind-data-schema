""" schema describing imaging acquisition """

from decimal import Decimal
from typing import List, Literal, Optional, Union

from pydantic import Field, SkipValidation, Annotated, model_validator

from aind_data_schema.base import DataCoreModel, DataModel, AwareDatetimeWithDefault, GenericModel, GenericModelType
from aind_data_schema.components.units import VolumeUnit, MassUnit
from aind_data_schema.components.devices import Calibration, Maintenance, Camera, CameraAssembly
from aind_data_schema.components.coordinates import Affine3dTransform
from aind_data_schema.procedures import Anaesthetic
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
    RewardDeliveryConfig,
)
from aind_data_schema.components.stimulus import (
    AuditoryStimulation,
    OlfactoryStimulation,
    OptoStimulation,
    PhotoStimulation,
    VisualStimulation,
)

from aind_data_schema_models.modalities import Modality, StimulusModality

# Define the requirements for each modality
# Define the mapping of modalities to their required device types
# The list of list pattern is used to allow for multiple options within a group, so e.g.
# FIB requires a light config (one of the options) plus a fiber connection config and a fiber module
CONFIG_REQUIREMENTS = {
    Modality.ECEPHYS: [[DomeModule, ManipulatorModule]],
    Modality.FIB: [[LightEmittingDiodeConfig, LaserConfig], [FiberConnectionConfig], [FiberModule]],
    Modality.POPHYS: [[FieldOfView, SlapFieldOfView, Stack]],
    Modality.MRI: [[MRIScan]],
}

# This is ugly but one of the validators was just checking that the cameras were active in the device name list
# so to replace that I'm going to add a validator that searches the instrument to make sure the active_devices
# list contains a valid Camera and/or CameraAssembly. Note that this validator has to go in the `metadata` class
# [TODO]
DEVICE_REQUIREMENTS = {
    Modality.BEHAVIOR_VIDEOS: [[CameraAssembly, Camera]],
}


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

    @model_validator(mode="after")
    def check_modality_config_requirements(cls, v):
        for modality in v.modalities:
            for group in CONFIG_REQUIREMENTS[modality]:
                if not any([any([isinstance(config, device) for device in group]) for config in v.configurations]):
                    raise ValueError(f"Missing required devices for modality {modality} in {v.configurations}")


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
    ] = Field(default=[], title="Device configurations")


class Acquisition(DataCoreModel):
    """Description of an imaging acquisition session"""

    # Meta metadata
    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/acquisition.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.3"]] = Field(default="2.0.3")

    # Acquisition metadata
    subject_id: str = Field(default=..., title="Subject ID")
    specimen_id: Optional[str] = Field(default=None, title="Specimen ID")
    experimenters: List[Person] = Field(
        default=[],
        title="experimenter(s)",
    )
    protocol_id: List[str] = Field(default=[], title="Protocol ID", description="DOI for protocols.io")
    ethics_review_id: Optional[str] = Field(default=None, title="Ethics review ID")
    instrument_id: str = Field(..., title="Instrument ID")

    # Instrument metadata
    calibrations: List[Calibration] = Field(
        default=[],
        title="Calibrations",
        description="List of calibration measurements taken prior to acquisition.",
    )
    maintenance: List[Maintenance] = Field(
        default=[], title="Maintenance", description="List of maintenance on instrument prior to acquisition."
    )

    # Information about the acquisition
    acquisition_start_time: AwareDatetimeWithDefault = Field(..., title="Acquisition start time")
    acquisition_end_time: AwareDatetimeWithDefault = Field(..., title="Acquisition end time")
    acquisition_type: Optional[str] = Field(default=None, title="Acquisition type")
    local_storage_directory: Optional[str] = Field(default=None, title="Local storage directory")
    external_storage_directory: Optional[str] = Field(default=None, title="External storage directory")
    software: Optional[List[Software]] = Field(default=[], title="Acquisition software")
    notes: Optional[str] = Field(default=None, title="Notes")

    # Acquisition data
    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
    )
    stimulus_epochs: List[StimulusEpoch] = Field(default=[], title="Stimulus")

    # Fields coming from session [TODO] figure out how to get rid of these, maybe these are actually a data stream?
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
    active_mouse_platform: bool = Field(
        ..., title="Active mouse platform", description="Is the mouse platform being actively controlled"
    )
    headframe_registration: Optional[Affine3dTransform] = Field(
        default=None, title="Headframe registration", description="MRI transform matrix for headframe"
    )
    reward_delivery: Optional[RewardDeliveryConfig] = Field(default=None, title="Reward delivery")
    reward_consumed_total: Optional[Decimal] = Field(default=None, title="Total reward consumed (mL)")
    reward_consumed_unit: VolumeUnit = Field(default=VolumeUnit.ML, title="Reward consumed unit")

    # [TODO] : validator for subject + specimen ID, compare first six digits

    # [TODO] : modality -> specimen ID validator
