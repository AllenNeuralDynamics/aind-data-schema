""" schema for mostly mouse metadata """

from datetime import date as date_type
from datetime import time
from enum import Enum
from typing import List, Literal, Optional

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from aind_data_schema.base import AindCoreModel, AindModel


class Sex(str, Enum):
    """Subject sex name"""

    FEMALE = "Female"
    MALE = "Male"


class BackgroundStrain(str, Enum):
    """Animal background strain name"""

    BALB_c = "BALB/c"
    C57BL_6J = "C57BL/6J"


class HomeCageEnrichment(str, Enum):
    """Materials provided in animal home cage"""

    NONE = "None"
    PLASTIC_SHELTER = "Plastic shelter"
    PLASTIC_TUBE = "Plastic tube"
    RUNNING_WHEEL = "Running wheel"
    OTHER = "Other"


class LightCycle(AindModel):
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


class WellnessReport(AindModel):
    """Wellness report on animal health"""

    date: date_type = Field(..., title="Date")
    report: str = Field(..., title="Report")


class Housing(AindModel):
    """Description of subject housing"""

    cage_id: Optional[str] = Field(default=None, title="Cage ID")
    room_id: Optional[str] = Field(default=None, title="Room ID")
    light_cycle: Optional[LightCycle] = Field(default=None, title="Light cycle")
    home_cage_enrichment: List[HomeCageEnrichment] = Field(default=[], title="Home cage enrichment")
    cohoused_subjects: List[str] = Field(
        default=[],
        title="Co-housed subjects",
        description="List of IDs of other subjects housed in same cage",
    )


class BreedingInfo(AindModel):
    """Description of breeding info for subject"""

    breeding_group: str = Field(..., title="Breeding Group")
    maternal_id: str = Field(..., title="Maternal specimen ID")
    maternal_genotype: str = Field(..., title="Maternal genotype")
    paternal_id: str = Field(..., title="Paternal specimen ID")
    paternal_genotype: str = Field(..., title="Paternal genotype")


class Subject(AindCoreModel):
    """Description of a subject of data collection"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/subject.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.0"] = Field("1.0.0")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    sex: Sex = Field(..., title="Sex")
    date_of_birth: date_type = Field(..., title="Date of birth")
    genotype: Optional[str] = Field(
        default=None,
        description="Genotype of the animal providing both alleles",
        title="Genotype",
    )
    species: Species.ONE_OF = Field(..., title="Species")
    alleles: List[PIDName] = Field(default=[], title="Alleles", description="Allele names and persistent IDs")
    background_strain: Optional[BackgroundStrain] = Field(default=None, title="Background strain")
    breeding_info: Optional[BreedingInfo] = Field(default=None, title="Breeding Info")
    source: Organization.SUBJECT_SOURCES = Field(
        ...,
        description="Where the subject was acquired from. If bred in-house, use Allen Institute.",
        title="Source",
    )
    rrid: Optional[PIDName] = Field(
        default=None,
        description="RRID of mouse if acquired from supplier",
        title="RRID",
    )
    restrictions: Optional[str] = Field(
        default=None,
        description="Any restrictions on use or publishing based on subject source",
        title="Restrictions",
    )
    wellness_reports: List[WellnessReport] = Field(default=[], title="Wellness Report")
    housing: Optional[Housing] = Field(default=None, title="Housing")
    notes: Optional[str] = Field(default=None, title="Notes")

    @field_validator("source", mode="after")
    def validate_inhouse_breeding_info(cls, v: Organization.ONE_OF, info: ValidationInfo):
        """Validator for inhouse mice breeding info"""

        if v is Organization.AI and info.data.get("breeding_info") is None:
            raise ValueError("Breeding info should be provided for subjects bred in house")

        return v

    @field_validator("species", mode="after")
    def validate_genotype(cls, v: Species.ONE_OF, info: ValidationInfo):
        """Validator for mice genotype"""

        if v is Species.MUS_MUSCULUS and info.data.get("genotype") is None:
            raise ValueError("Full genotype should be provided for mouse subjects")

        return v
