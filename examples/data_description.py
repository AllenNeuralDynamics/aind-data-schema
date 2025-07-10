""" example data description """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.data_name_patterns import DataLevel

from aind_data_schema.core.data_description import Funding, DataDescription
from aind_data_schema.components.identifiers import Person

d = DataDescription(
    modalities=[Modality.ECEPHYS, Modality.BEHAVIOR_VIDEOS],
    subject_id="123456",
    creation_time=datetime(2022, 2, 21, 16, 30, 1, tzinfo=timezone.utc),
    institution=Organization.AIND,
    investigators=[Person(name="Daniel Birman", registry_identifier="0000-0003-3748-6289")],  # Include ORCID IDs
    funding_source=[Funding(funder=Organization.AI)],
    project_name="Example project",
    data_level=DataLevel.RAW,
)

if __name__ == "__main__":
    serialized = d.model_dump_json()
    deserialized = DataDescription.model_validate_json(serialized)
    deserialized.write_standard_file()
