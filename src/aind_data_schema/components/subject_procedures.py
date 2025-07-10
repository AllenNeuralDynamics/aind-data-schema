"""Subject procedures module for AIND data schema"""

from datetime import date
from typing import Dict, List, Optional

from aind_data_schema_models.coordinates import Origin
from aind_data_schema_models.units import MassUnit, UnitlessUnit, VolumeUnit
from pydantic import Field

from aind_data_schema.base import DataModel, DiscriminatedList
from aind_data_schema.components.coordinates import CoordinateSystem, Translation
from aind_data_schema.components.identifiers import Code
from aind_data_schema.components.injection_procedures import Injection
from aind_data_schema.components.surgery_procedures import (
    Anaesthetic,
    BrainInjection,
    CatheterImplant,
    Craniotomy,
    GenericSurgeryProcedure,
    Headframe,
    MyomatrixInsertion,
    Perfusion,
    ProbeImplant,
    SampleCollection,
)


class GenericSubjectProcedure(DataModel):
    """Description of a non-surgical procedure performed on a subject"""

    start_date: date = Field(..., title="Start date")
    experimenters: Optional[List[str]] = Field(
        default=None,
        title="experimenter(s)",
    )
    ethics_review_id: str = Field(..., title="Ethics review ID")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    description: str = Field(..., title="Description")
    notes: Optional[str] = Field(default=None, title="Notes")


class TrainingProtocol(DataModel):
    """Description of an animal training protocol"""

    training_name: str = Field(..., title="Training protocol name")
    protocol_id: Optional[str] = Field(default=None, title="Training protocol ID")
    start_date: date = Field(..., title="Training protocol start date")
    end_date: Optional[date] = Field(default=None, title="Training protocol end date")
    curriculum_code: Optional[Code] = Field(
        default=None,
        title="Curriculum code",
        description="Code describing the directed graph used for the training curriculum",
    )
    notes: Optional[str] = Field(default=None, title="Notes")


class WaterRestriction(DataModel):
    """Description of a water restriction procedure"""

    ethics_review_id: str = Field(..., title="Ethics review ID")
    target_fraction_weight: int = Field(..., title="Target fraction weight (%)")
    target_fraction_weight_unit: UnitlessUnit = Field(default=UnitlessUnit.PERCENT, title="Target fraction weight unit")
    minimum_water_per_day: float = Field(..., title="Minimum water per day (mL)")
    minimum_water_per_day_unit: VolumeUnit = Field(default=VolumeUnit.ML, title="Minimum water per day unit")
    baseline_weight: float = Field(
        ...,
        title="Baseline weight (g)",
        description="Weight at start of water restriction",
    )
    weight_unit: MassUnit = Field(default=MassUnit.G, title="Weight unit")
    start_date: date = Field(..., title="Water restriction start date")
    end_date: Optional[date] = Field(default=None, title="Water restriction end date")


class Surgery(DataModel):
    """Description of subject procedures performed at one time"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    start_date: date = Field(..., title="Start date")
    experimenters: Optional[List[str]] = Field(
        default=None,
        title="experimenter(s)",
    )
    ethics_review_id: Optional[str] = Field(default=None, title="Ethics review ID")
    animal_weight_prior: Optional[float] = Field(
        default=None, title="Animal weight (g)", description="Animal weight before procedure"
    )
    animal_weight_post: Optional[float] = Field(
        default=None, title="Animal weight (g)", description="Animal weight after procedure"
    )
    weight_unit: MassUnit = Field(default=MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(default=None, title="Anaesthesia")
    workstation_id: Optional[str] = Field(default=None, title="Workstation ID")

    # Coordinate system
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Surgery coordinate system",
        description=(
            "Only required when the Surgery.coordinate_system " "is different from the Procedures.coordinate_system"
        ),
    )  # note: exact field name is used by a validator

    # Measured coordinates
    measured_coordinates: Optional[Dict[Origin, Translation]] = Field(
        default=None,
        title="Measured coordinates",
        description="Coordinates measured during the procedure, for example Bregma and Lambda",
    )

    procedures: DiscriminatedList[
        CatheterImplant
        | Craniotomy
        | ProbeImplant
        | Headframe
        | BrainInjection
        | Injection
        | MyomatrixInsertion
        | GenericSurgeryProcedure
        | Perfusion
        | SampleCollection
    ] = Field(title="Procedures", min_length=1)
    notes: Optional[str] = Field(default=None, title="Notes")
