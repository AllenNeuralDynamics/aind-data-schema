""" example subject """

from aind_data_schema import Subject
import datetime

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

s = Subject(
    species="Mus musculus",
    subject_id="12345",
    sex="Male",
    date_of_birth=t.date(),
    genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
    home_cage_enrichment="other",
    background_strain="C57BL/6J",
)

with open("subject.json", "w") as f:
    f.write(s.json(indent=3))
