"""Generic metadata class for Data Asset Records."""

from datetime import datetime
from enum import Enum

from pydantic import Extra, Field, root_validator

from aind_data_schema.base import AindCoreModel
from aind_data_schema.subject import Subject
from aind_data_schema.data_description import DataDescription
from aind_data_schema.procedures import Procedures
from aind_data_schema.rig import Rig
from aind_data_schema.session import Session
from aind_data_schema.processing import Processing


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

    class Config:
        """Need to allow for additional fields to append to base model"""

        extra = Extra.allow


class SmartSPIMMetadata(Metadata):
    """The smartSPIM records in the Data Asset Collection require certain metadata."""
    data_description: DataDescription = Field(
        ...,
        title="Data Description",
        description="Description of a logical collection of data files."
    )
    procedures: Procedures = Field(
        ...,
        title="Procedures",
        description="Description of all procedures performed on a subject."
    )
    session: Session = Field(
        ...,
        title="Session",
        description="Description of a session."
    )
    rig: Rig = Field(
        ...,
        title="Rig",
        description="Description of a rig."
    )
    processing: Processing = Field(
        ...,
        title="Processing",
        description="Description of all processes run on data."
    )

    @root_validator
    def validate_institute_subject(cls, v):
        """Validator for Institute mice"""
        subject_id_value = v.get("subject_id")
        subject_value = v.get('subject')
        procedures_value = v.get('procedures')
        if 'AK' in subject_id_value:
            if subject_value is None or procedures_value is None:
                raise ValueError("Both subject and procedures are required "
                                 "when the metadata is describing Allen Institute mice.")
        return v


class EcephysMetadata(Metadata):
    """The ecephys records in the Data Asset Collection require certain metadata."""
    data_description: DataDescription = Field(
        ...,
        title="Data Description",
        description="Description of a logical collection of data files"
    )
    procedures: Procedures = Field(
        ...,
        title="Procedures",
        description="Description of all procedures performed on a subject"
    )
    session: Session = Field(
        ...,
        title="Session",
        description="Description of a session."
    )
    rig: Rig = Field(
        ...,
        title="Rig",
        description="Description of a rig."
    )
    processing: Processing = Field(
        ...,
        title="Processing",
        description="Description of all processes run on data."
    )
