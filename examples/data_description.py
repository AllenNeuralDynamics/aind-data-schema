""" example data description """
from datetime import date, time

from aind_data_schema import RawDataDescription
from aind_data_schema.data_description import Funding

d = RawDataDescription(
    modality="ecephys",
    subject_id="12345",
    creation_date=date(2022, 2, 21),
    creation_time=time(16, 30, 1),
    institution="AIND",
    funding_source=[Funding(funder="AIND")],
)

d.write_standard_file()
