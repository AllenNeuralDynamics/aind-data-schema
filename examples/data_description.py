""" example data description """

from aind_data_schema import RawDataDescription
from aind_data_schema.data_description import Funding
import datetime

now = datetime.datetime.now()
s = RawDataDescription(
    modality="ecephys",
    subject_id="12345",
    creation_date=now.date(),
    creation_time=now.time(),
    institution="AIND",
    funding_source=[Funding(funder="AIND")],
)

with open("data_description.json", "w") as f:
    f.write(s.json(indent=3))
