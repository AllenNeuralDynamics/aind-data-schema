""" example data description """
from datetime import datetime

from aind_data_schema.core.data_description import Funding, RawDataDescription
from aind_data_schema.models.modalities import Modality
from aind_data_schema.models.organizations import Organization
from aind_data_schema.models.platforms import Platform

d = RawDataDescription(
    modality=[Modality.ECEPHYS, Modality.BEHAVIOR_VIDEOS],
    platform=Platform.ECEPHYS,
    subject_id="12345",
    creation_time=datetime(2022, 2, 21, 16, 30, 1),
    institution=Organization.AIND,
    investigators=["Jane Smith"],
    funding_source=[Funding(funder=Organization.AI)],
)

d.write_standard_file()
