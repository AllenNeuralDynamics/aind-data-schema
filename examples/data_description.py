""" example data description """

from aind_data_schema import RawDataDescription
from aind_data_schema.data_description import Funding
from datetime import date, time

d = RawDataDescription(
    modality="ecephys",
    subject_id="12345",
    creation_date=date(2022, 2, 21),
    creation_time=time(16, 30, 1),
    institution="AIND",
    funding_source=[Funding(funder="AIND")],
)

with open("data_description.json", "w") as f:
    f.write(d.json(indent=3))
