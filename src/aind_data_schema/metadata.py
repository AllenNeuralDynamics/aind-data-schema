"""Generic metadata class for Data Asset Records."""

import re
from datetime import datetime
from enum import Enum

from pydantic import Field, root_validator, validate_model, ValidationError

from aind_data_schema.base import AindCoreModel
from aind_data_schema.data_description import DataDescription, DataRegex, Platform
from aind_data_schema.procedures import Procedures
from aind_data_schema.processing import Processing
from aind_data_schema.rig import Rig
from aind_data_schema.session import Session
from aind_data_schema.subject import Subject
from aind_data_schema.imaging.instrument import Instrument
from aind_data_schema.imaging.acquisition import Acquisition
from typing import Optional


class MetadataStatus(Enum):
    """Status of Metadata"""

    VALID = "Valid"
    INVALID = "Invalid"
    MISSING = "Missing"
    UNKNOWN = "Unknown"


class Metadata(AindCoreModel):
    """The records in the Data Asset Collection needs to contain certain fields
    to easily query and index the data."""

    id: str = Field(
        ...,
        alias="_id",
        title="Data Asset ID",
        description="The unique id of the data asset.",
    )
    name: str = Field(
        ...,
        description="Name of the data asset.",
        title="Data Asset Name",
    )
    created: datetime = Field(
        ...,
        title="Created",
        description="The data and time the data asset created.",
    )
    last_modified: datetime = Field(
        ..., title="Last Modified", description="The date and time that the data asset was last modified."
    )
    location: str = Field(
        ...,
        title="Location",
        description="Current location of the data asset.",
    )
    metadata_status: MetadataStatus = Field(..., title=" Metadata Status", description="The status of the metadata.")
    schema_version: str = Field("0.0.1", title="Schema Version", const=True)
    subject: Subject = Field(
        ...,
        title="Subject",
        description="Description of a subject of data collection.",
    )
    data_description: Optional[DataDescription] = Field(
        None, title="Data Description", description="Description of a logical collection of data files."
    )
    procedures: Optional[Procedures] = Field(
        None, title="Procedures", description="Description of all procedures performed on a subject."
    )
    session: Optional[Session] = Field(None, title="Session", description="Description of a session.")
    rig: Optional[Rig] = Field(None, title="Rig", description="Description of a rig.")
    processing: Optional[Processing] = Field(None, title="Processing", description="Description of all processes run on data.")
    acquisition: Optional[Acquisition] = Field(
        None, title="Acquisition", description="Description of an imaging acquisition session"
    )
    instrument: Optional[Instrument] = Field(
        None, title="Instrument", description="Description of an instrument, which is a collection of devices"
    )

    @root_validator(pre=True)
    def validate_metadata(cls, v):
        """Validator for metadata"""
        metadata_status = MetadataStatus.VALID
        v_subject = v["subject"]
        if isinstance(v_subject, Subject):
            subject_contents = v_subject.dict()
        elif isinstance(v_subject, dict):
            subject_contents = v_subject
        else:
            raise ValidationError("subject needs to be of type Subject or dictionary.")

        if subject_contents.get("subject_id") is None:
            raise ValidationError("Subject requires subject_id.")

        *_, validation_error = validate_model(
            Subject, subject_contents
        )

        if validation_error:
            subject_model = Subject.construct(**subject_contents)
            metadata_status = MetadataStatus.INVALID
        else:
            subject_model = Subject(**subject_contents)

        v_data_description = v.get("data_description")
        if v_data_description is None:
            data_description_contents = None
        elif isinstance(v_data_description, DataDescription):
            data_description_contents = v_data_description.dict()
        elif isinstance(v_data_description, dict):
            data_description_contents = v_data_description
        else:
            raise ValidationError("data_description needs to be of type DataDescription or dictionary.")

        *_, validation_error = validate_model(
            DataDescription, data_description_contents
        )

        if validation_error:
            data_description_model = DataDescription.construct(**data_description_contents)
            metadata_status = MetadataStatus.INVALID
        else:
            data_description_model = DataDescription(**data_description_contents)

        v["metadata_status"] = metadata_status
        v["subject"] = subject_model
        v["data_description"] = data_description_model
        # name_value = v.get("name")
        # match = re.match(str(DataRegex.RAW.value), str(name_value))
        # if match:
        #     platform_abbreviation = match.group("platform_abbreviation")
        #     subject_id = match.group("subject_id")
        #
        #     complete_metadata = ["subject", "data_description", "processing"]
        #     if "AK" not in subject_id:
        #         complete_metadata.append("procedures")
        #     if Platform.ECEPHYS.value.abbreviation == platform_abbreviation:
        #         complete_metadata.extend(["rig", "session"])
        #     elif Platform.SMARTSPIM.value.abbreviation == platform_abbreviation:
        #         complete_metadata.extend(["acquisition", "instrument"])
        #
        #     missing_fields = [field for field in complete_metadata if v.get(field) is None]
        #     if missing_fields:
        #         v["metadata_status"] = "MISSING"
        #         raise ValueError(f"Missing metadata: {', '.join(missing_fields)}")
        #
        # return v
