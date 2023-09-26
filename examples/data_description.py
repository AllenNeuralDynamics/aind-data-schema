""" example data description """
from datetime import datetime

from aind_data_schema.data_description import Funding, Institution, Modality, Platform, RawDataDescription

d = RawDataDescription(
    modality=[Modality.ECEPHYS, Modality.BEHAVIOR_VIDEOS],
    platform=Platform.ECEPHYS,
    subject_id="12345",
    creation_time=datetime(2022, 2, 21, 16, 30, 1),
    institution=Institution.AIND,
    investigators=["Jane Smith"],
    funding_source=[Funding(funder=Institution.AI)],
)

d.write_standard_file()
