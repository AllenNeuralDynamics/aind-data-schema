""" schema for mostly mouse metadata """

from __future__ import annotations

from datetime import date, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Species(Enum):
    """list of species"""

    MUS_MUSCULUS = "Mus musculus"
    CALLITHRIX_JACCHUS = "Callithrix jacchus"
    MACACA_MULATTA = "Macaca mulatta"
    HOMO_SAPIENS = "Homo sapiens"


class Sex(Enum):
    """TODO"""

    FEMALE = "Female"
    MALE = "Male"


class BackgroundStrain(Enum):
    """TODO"""

    C57BL_6J = "C57BL/6J"
    BALB_c = "BALB/c"


class LightCycle(BaseModel):
    """light cycle modes"""

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
    """TODO"""

    none = "none"
    running_wheel = "running wheel"
    social_housing = "social housing"
    plastic_tube = "plastic tube"
    plastic_shelter = "plastic shelter"
    other = "other"


class Subject(BaseModel):
    """basic description of subject of data collection"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/subject.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field(
        "0.1.0", description="schema version", title="Version", const=True
    )
    species: Species = Field(..., title="Species")
    specimen_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Specimen ID",
    )
    sex: Sex = Field(..., title="Sex")
    date_of_birth: date = Field(..., title="Date of birth")
    genotype: str = Field(
        ...,
        description="Genotype of the animal providing both alleles",
        title="Genotype",
    )
    background_strain: Optional[BackgroundStrain] = Field(
        None, title="Background strain"
    )
    source: Optional[str] = Field(
        None,
        description="If the subject was not bred in house, where was it acquired from.",
        title="Source",
    )
    restrictions: Optional[str] = Field(
        None,
        description="Any restrictions on use or publishing based on specimen source",
        title="Restrictions",
    )
    breeding_group: Optional[str] = Field(None, title="Breeding Group")
    maternal_id: Optional[str] = Field(None, title="Maternal specimen ID")
    maternal_genotype: Optional[str] = Field(None, title="Maternal genotype")
    paternal_id: Optional[str] = Field(None, title="Paternal specimen ID")
    paternal_genotype: Optional[str] = Field(None, title="Paternal genotype")
    light_cycle: LightCycle = Field(..., title="Light cycle")
    home_cage_enrichment: Optional[HomeCageEnrichment] = Field(
        None, title="Home cage enrichment"
    )
    notes: Optional[str] = Field(None, title="Notes")
