"""Injection procedures for AIND data schema"""

from datetime import date
from enum import Enum
from typing import List, Optional

from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.units import CurrentUnit, TimeUnit, VolumeUnit
from pydantic import Field, model_validator

from aind_data_schema.base import DataModel, DiscriminatedList
from aind_data_schema.components.reagent import Reagent


class VirusPrepType(str, Enum):
    """Type of virus preparation"""

    CRUDE = "Crude"
    PURIFIED = "Purified"


class InjectionProfile(str, Enum):
    """Injection profile"""

    BOLUS = "Bolus"
    CONTINUOUS = "Continuous"
    PULSED = "Pulsed"


class TarsVirusIdentifiers(DataModel):
    """TARS data for a viral prep"""

    virus_tars_id: Optional[str] = Field(default=None, title="Virus ID, usually begins 'AiV'")
    plasmid_tars_alias: Optional[List[str]] = Field(
        default=None,
        title="List of plasmid aliases",
        description="Alias used to reference the plasmid, usually begins 'AiP'",
    )
    prep_lot_number: str = Field(..., title="Preparation lot number")
    prep_date: Optional[date] = Field(
        default=None,
        title="Preparation lot date",
        description="Date this prep lot was titered",
    )
    prep_type: Optional[VirusPrepType] = Field(default=None, title="Viral prep type")
    prep_protocol: Optional[str] = Field(default=None, title="Prep protocol")


class ViralMaterial(DataModel):
    """Description of viral material for injections"""

    name: str = Field(
        ...,
        title="Full genome name",
        description="Full genome for virus construct",
    )
    tars_identifiers: Optional[TarsVirusIdentifiers] = Field(
        default=None, title="TARS IDs", description="TARS database identifiers"
    )
    addgene_id: Optional[PIDName] = Field(default=None, title="Addgene id", description="Registry must be Addgene")
    titer: Optional[int] = Field(
        default=None,
        title="Effective titer",
        description="Final titer of viral material, accounting for mixture/diliution",
    )
    titer_unit: Optional[str] = Field(default="gc/mL", title="Titer unit", description="For example, gc/mL")


class NonViralMaterial(Reagent):
    """Description of a non-viral injection material"""

    concentration: Optional[float] = Field(
        default=None, title="Concentration", description="Must provide concentration unit"
    )
    concentration_unit: Optional[str] = Field(
        default=None, title="Concentration unit", description="For example, mg/mL"
    )


class InjectionDynamics(DataModel):
    """Description of the volume and rate of an injection"""

    profile: InjectionProfile = Field(..., title="Injection profile")

    volume: Optional[float] = Field(default=None, title="Injection volume")
    volume_unit: Optional[VolumeUnit] = Field(default=None, title="Injection volume unit")

    duration: Optional[float] = Field(default=None, title="Injection duration")
    duration_unit: Optional[TimeUnit] = Field(default=None, title="Injection duration unit")

    injection_current: Optional[float] = Field(default=None, title="Injection current (uA)")
    injection_current_unit: Optional[CurrentUnit] = Field(default=None, title="Injection current unit")
    alternating_current: Optional[str] = Field(default=None, title="Alternating current")

    @model_validator(mode="after")
    def check_volume_or_current(cls, values):
        """Check that either volume or injection_current is provided"""
        if not values.volume and not values.injection_current:
            raise ValueError("Either volume or injection_current must be provided.")
        return values


class Injection(DataModel):
    """Description of an injection procedure"""

    injection_materials: DiscriminatedList[ViralMaterial | NonViralMaterial] = Field(
        ..., title="Injection material", min_length=1
    )
    targeted_structure: Optional[MouseAnatomyModel] = Field(
        default=None, title="Injection target", description="Use InjectionTargets"
    )
    relative_position: Optional[List[AnatomicalRelative]] = Field(default=None, title="Relative position")

    dynamics: List[InjectionDynamics] = Field(
        ..., title="Injection dynamics", description="List of injection events, one per location/depth"
    )
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
