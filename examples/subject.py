""" example subject """
import os
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

dir_path = os.path.dirname(os.path.realpath(__file__))
s.write_to_json(dir_path)
