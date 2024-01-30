""" example subject """

import datetime

from aind_data_schema.core.subject import BreedingInfo, Housing, Sex, Subject
from aind_data_schema.models.organizations import Organization
from aind_data_schema.models.species import Species

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

s = Subject(
    species=Species.MUS_MUSCULUS,
    subject_id="12345",
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
    background_strain="C57BL/6J",
)

s.write_standard_file()
