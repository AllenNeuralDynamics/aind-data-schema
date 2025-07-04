""" example subject """

from datetime import datetime, timezone

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.species import Species, Strain

from aind_data_schema.core.subject import Subject
from aind_data_schema.components.subjects import BreedingInfo, Housing, Sex, MouseSubject

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

s = Subject(
    subject_id="123456",
    subject_details=MouseSubject(
        species=Species.HOUSE_MOUSE,
        strain=Strain.C57BL_6J,
        sex=Sex.MALE,
        date_of_birth=t.date(),
        source=Organization.AI,
        breeding_info=BreedingInfo(
            breeding_group="Emx1-IRES-Cre(ND)",
            maternal_id="546543",
            maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
            paternal_id="232323",
            paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
        ),
        genotype="Emx1-IRES-Cre/wt;Camk2a-tTA/wt;Ai93(TITL-GCaMP6f)/wt",
        housing=Housing(home_cage_enrichment=["Running wheel"], cage_id="123"),
    ),
)

if __name__ == "__main__":
    serialized = s.model_dump_json()
    deserialized = Subject.model_validate_json(serialized)
    deserialized.write_standard_file()
