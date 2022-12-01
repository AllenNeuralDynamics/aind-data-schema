""" example subject """

from aind_data_schema import Subject
import datetime

now = datetime.datetime.now()

s = Subject(
    species="Mus musculus",
    subject_id="12345",
    sex="Male",
    date_of_birth=now.date(),
    genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
    home_cage_enrichment="other",
    background_strain="C57BL/6J",
)


with open("subject.json", "w") as f:
    f.write(s.json(indent=3))
