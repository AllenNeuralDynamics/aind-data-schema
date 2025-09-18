"""Subject species models"""

from datetime import date as date_type
from datetime import time
from enum import Enum
from typing import Annotated, List, Optional

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species, Strain
from pydantic import Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from aind_data_schema.base import DataModel
from aind_data_schema.components.devices import Device
from aind_data_schema.utils.validators import TimeValidation


class Sex(str, Enum):
    """Subject sex name"""

    FEMALE = "Female"
    MALE = "Male"


class HomeCageEnrichment(str, Enum):
    """Materials provided in animal home cage"""

    NO_ENRICHMENT = "No enrichment"
    PLASTIC_SHELTER = "Plastic shelter"
    PLASTIC_TUBE = "Plastic tube"
    RUNNING_WHEEL = "Running wheel"
    OTHER = "Other"


class LightCycle(DataModel):
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


class WellnessReport(DataModel):
    """Wellness report on animal health"""

    date: date_type = Field(..., title="Date")
    report: str = Field(..., title="Report")


class Housing(DataModel):
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


class BreedingInfo(DataModel):
    """Description of breeding info for subject"""

    breeding_group: str = Field(..., title="Breeding Group")
    maternal_id: str = Field(..., title="Maternal specimen ID")
    maternal_genotype: str = Field(..., title="Maternal genotype")
    paternal_id: str = Field(..., title="Paternal specimen ID")
    paternal_genotype: str = Field(..., title="Paternal genotype")


class MouseSubject(DataModel):
    """Description of a mouse subject"""

    sex: Sex = Field(..., title="Sex")
    date_of_birth: Annotated[date_type, TimeValidation.BEFORE] = Field(..., title="Date of birth")
    strain: Strain.ONE_OF = Field(..., title="Strain")
    species: Species.ONE_OF = Field(..., title="Species")
    alleles: List[PIDName] = Field(default=[], title="Alleles", description="Allele names and persistent IDs")
    genotype: str = Field(
        ...,
        description="Genotype of the animal providing both alleles",
        title="Genotype",
    )
    breeding_info: Optional[BreedingInfo] = Field(default=None, title="Breeding Info")
    wellness_reports: List[WellnessReport] = Field(default=[], title="Wellness Report")
    housing: Optional[Housing] = Field(default=None, title="Housing")
    source: Organization.SUBJECT_SOURCES = Field(
        ...,
        description="Where the subject was acquired from. If bred in-house, use Allen Institute.",
        title="Source",
    )
    restrictions: Optional[str] = Field(
        default=None,
        description="Any restrictions on use or publishing based on subject source",
        title="Restrictions",
    )
    rrid: Optional[PIDName] = Field(
        default=None,
        description="RRID of mouse if acquired from supplier",
        title="RRID",
    )

    @field_validator("source", mode="after")
    def validate_inhouse_breeding_info(cls, v: Organization.ONE_OF, info: ValidationInfo):
        """Validator for inhouse mice breeding info"""

        if v is Organization.AI and info.data.get("breeding_info") is None:
            raise ValueError("Breeding info should be provided for subjects bred in house")

        return v

    @model_validator(mode="after")
    def validate_species_strain(value):
        """Ensure that the species and strain.species match"""

        if value.strain:
            if not value.species or value.species.name != value.strain.species:
                raise ValueError("The animal species and it's strain's species do not match")

        return value


class HumanSubject(DataModel):
    """Description of a human subject"""

    sex: Sex = Field(..., title="Sex")
    year_of_birth: int = Field(..., title="Year of birth")
    source: Organization.SUBJECT_SOURCES = Field(
        ...,
        description="Where the subject was acquired from.",
        title="Source",
    )


class CalibrationObject(DataModel):
    """Description of a calibration object"""

    empty: bool = Field(
        default=False, title="Empty", description="Set to true if the calibration was performed with no object."
    )
    description: str = Field(..., title="Description")
    objects: Optional[list[Device]] = Field(
        default=None, title="Objects", description="For calibration objects that are built up from one or more devices."
    )
