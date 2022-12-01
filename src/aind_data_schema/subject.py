""" schema for mostly mouse metadata """

from __future__ import annotations

from datetime import date, time
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from .base import AindSchema


class Species(Enum):
    """Species latin name"""

    MUS_MUSCULUS = "Mus musculus"
    CALLITHRIX_JACCHUS = "Callithrix jacchus"
    MACACA_MULATTA = "Macaca mulatta"
    HOMO_SAPIENS = "Homo sapiens"


class Sex(Enum):
    """Subject sex name"""

    FEMALE = "Female"
    MALE = "Male"


class BackgroundStrain(Enum):
    """Animal background strain name"""

    C57BL_6J = "C57BL/6J"
    BALB_c = "BALB/c"


class LightCycle(BaseModel):
    """Description of vivarium light cycle times"""

    lights_on_time: time = Field(
        ...,
        description="Time in UTC that lights were turned on",
        title="Lights on time",
    )
    lights_off_time: time = Field(
        ...,
        description="Time in UTC that lights were turned off",
        title="Lights off time",
    )


class HomeCageEnrichment(Enum):
    """Materials provided in animal home cage"""

    NONE = "none"
    RUNNING_WHEEL = "running wheel"
    SOCIAL_HOUSING = "social housing"
    PLASTIC_TUBE = "plastic tube"
    PLASTIC_SHELTER = "plastic shelter"
    OTHER = "other"


class WellnessReport(BaseModel):
    """Wellness report on animal health"""

    date: date = Field(..., title="Date")
    report: str = Field(..., title="Report")


class MgiAlleleId(BaseModel):
    """Mouse Genome Informatics IDs for genotype alleles"""

    allele_name: str = Field(..., title="Name")
    mgi_id: str = Field(..., title="MGI ID")


class Subject(AindSchema):
    """Description of a subject of data collection"""

    schema_version: str = Field(
        "0.2.2", description="schema version", title="Version", const=True
    )
    species: Species = Field(..., title="Species")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    sex: Sex = Field(..., title="Sex")
    date_of_birth: date = Field(..., title="Date of birth")
    genotype: str = Field(
        ...,
        description="Genotype of the animal providing both alleles",
        title="Genotype",
    )
    mgi_allele_ids: Optional[List[MgiAlleleId]] = Field(
        None, title="MGI allele ids"
    )
    background_strain: Optional[BackgroundStrain] = Field(
        None, title="Background strain"
    )
    source: Optional[str] = Field(
        None,
        description="If the subject was not bred in house, where was it acquired from.",
        title="Source",
    )
    rrid: Optional[str] = Field(
        None,
        description="RRID of mouse if acquired from supplier",
        title="RRID",
    )
    restrictions: Optional[str] = Field(
        None,
        description="Any restrictions on use or publishing based on subject source",
        title="Restrictions",
    )
    breeding_group: Optional[str] = Field(None, title="Breeding Group")
    maternal_id: Optional[str] = Field(None, title="Maternal specimen ID")
    maternal_genotype: Optional[str] = Field(None, title="Maternal genotype")
    paternal_id: Optional[str] = Field(None, title="Paternal specimen ID")
    paternal_genotype: Optional[str] = Field(None, title="Paternal genotype")
    light_cycle: Optional[LightCycle] = Field(None, title="Light cycle")
    home_cage_enrichment: Optional[HomeCageEnrichment] = Field(
        None, title="Home cage enrichment"
    )
    wellness_reports: Optional[List[WellnessReport]] = Field(
        None, title="Wellness Report"
    )
    notes: Optional[str] = Field(None, title="Notes")
