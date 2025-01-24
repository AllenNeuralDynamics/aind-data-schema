""" example data description """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.data_description import Funding, RawDataDescription

d = RawDataDescription(
    modalities=[Modality.ECEPHYS, Modality.BEHAVIOR_VIDEOS],
    subject_id="12345",
    creation_time=datetime(2022, 2, 21, 16, 30, 1, tzinfo=timezone.utc),
    institution=Organization.AIND,
    investigators=[Person(name="Jane Smith")],
    funding_source=[Funding(funder=Organization.AI)],
)

serialized = d.model_dump_json()
deserialized = RawDataDescription.model_validate_json(serialized)
deserialized.write_standard_file()
