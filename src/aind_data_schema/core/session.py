""" Schemas for Physiology and/or Behavior Sessions """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import (
    AngleUnit,
    FrequencyUnit,
    MassUnit,
    PowerUnit,
    SizeUnit,
    SoundIntensityUnit,
    TimeUnit,
    VolumeUnit,
)
from aind_data_schema_models.brain_atlas import CCFStructure
from pydantic import Field, SkipValidation, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated

from aind_data_schema.base import (
    DataCoreModel,
    GenericModel,
    GenericModelType,
    DataModel,
    AwareDatetimeWithDefault,
)
from aind_data_schema.components.coordinates import (
    Affine3dTransform,
    CcfCoords,
    Coordinates3d,
    Rotation3dTransform,
    Scale3dTransform,
    Translation3dTransform,
)
from aind_data_schema.components.devices import Calibration, Maintenance, RelativePosition, Scanner, SpoutSide
from aind_data_schema.components.identifiers import Person, Software, Code
from aind_data_schema.components.stimulus import (
    AuditoryStimulation,
    OlfactoryStimulation,
    OptoStimulation,
    PhotoStimulation,
    VisualStimulation,
)
from aind_data_schema.components.tile import Channel
from aind_data_schema.core.procedures import Anaesthetic, CoordinateReferenceLocation




class Session(DataCoreModel):
    """Description of a physiology and/or behavior session"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/session.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.3"]] = Field(default="2.0.3")
    protocol_id: List[str] = Field(default=[], title="Protocol ID", description="DOI for protocols.io")
    experimenters: List[Person] = Field(
        default=[],
        title="experimenter(s)",
    )
    session_start_time: AwareDatetimeWithDefault = Field(..., title="Session start time")
    session_end_time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Session end time")
    session_type: str = Field(..., title="Session type")
    instrument_id: str = Field(..., title="Instrument ID")
    ethics_review_id: Optional[str] = Field(default=None, title="Ethics review ID")
    calibrations: List[Calibration] = Field(
        default=[],
        title="Calibrations",
        description="Calibrations of instrument devices prior to session",
    )
    maintenance: List[Maintenance] = Field(
        default=[],
        title="Maintenance",
        description="Maintenance of instrument devices prior to session",
    )
    subject_id: str = Field(..., title="Subject ID")
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
    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
    )
    stimulus_epochs: List[StimulusEpoch] = Field(default=[], title="Stimulus")
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
    notes: Optional[str] = Field(default=None, title="Notes")
