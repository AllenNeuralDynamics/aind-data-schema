""" example subject """

import datetime

from aind_data_schema.core.subject import Housing, Sex, Subject, BreedingInfo
from aind_data_schema.models.species import Species
from aind_data_schema.models.institutions import Institution

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

s = Subject(
    species=Species.MUS_MUSCULUS,
    subject_id="12345",
    sex=Sex.MALE,
    date_of_birth=t.date(),
    source=Institution.AI,
    breeding_info=BreedingInfo(),
    genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
    housing=Housing(home_cage_enrichment=["Running wheel"], cage_id="123"),
    background_strain="C57BL/6J",
)

s.write_standard_file()
