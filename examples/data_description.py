""" example data description """
from datetime import datetime

from aind_data_schema.core.data_description import Funding, RawDataDescription
from aind_data_schema.models.institutions import AI, AIND
from aind_data_schema.models.modalities import BEHAVIOR_VIDEOS, ECEPHYS
from aind_data_schema.models.platforms import ECEPHYS as P_ECEPHYS

d = RawDataDescription(
    modality=[ECEPHYS, BEHAVIOR_VIDEOS],
    platform=P_ECEPHYS,
    subject_id="12345",
    creation_time=datetime(2022, 2, 21, 16, 30, 1),
    institution=AIND,
    investigators=["Jane Smith"],
    funding_source=[Funding(funder=AI)],
)

d.write_standard_file()
