""" example data description """
from datetime import date, time

from aind_data_schema.data_description import Funding, Institution, Modality, RawDataDescription

d = RawDataDescription(
    modality=Modality.SPIM,
    instrument_type="diSPIM",
    subject_id="12345",
    creation_date=date(2022, 2, 21),
    creation_time=time(16, 30, 1),
    institution=Institution.AIND,
    funding_source=[Funding(funder="AIND")],
)

d.write_standard_file()
