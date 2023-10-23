"""Generic metadata class for Data Asset Records."""

import re
from datetime import datetime
from enum import Enum

from pydantic import Field, root_validator

from aind_data_schema.base import AindCoreModel
from aind_data_schema.data_description import DataDescription, DataRegex, Platform
from aind_data_schema.procedures import Procedures
from aind_data_schema.processing import Processing
from aind_data_schema.rig import Rig
from aind_data_schema.session import Session
from aind_data_schema.subject import Subject


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
        None,
        title="Subject",
        description="Description of a subject of data collection.",
    )
    data_description: DataDescription = Field(
        None, title="Data Description", description="Description of a logical collection of data files."
    )
    procedures: Procedures = Field(
        None, title="Procedures", description="Description of all procedures performed on a subject."
    )
    session: Session = Field(None, title="Session", description="Description of a session.")
    rig: Rig = Field(None, title="Rig", description="Description of a rig.")
    processing: Processing = Field(None, title="Processing", description="Description of all processes run on data.")

    @root_validator(pre=True)
    def validate_metadata_completeness(cls, v):
        """Validator for complete metadata"""
        name_value = v.get("name")
        match = re.match(str(DataRegex.RAW.value), str(name_value))
        if match:
            platform_abbreviation = match.group("platform_abbreviation")
            subject_id = match.group("subject_id")

            if "AK" in subject_id:
                complete_metadata = ["subject", "data_description", "session", "rig", "processing"]
            else:
                complete_metadata = ["subject", "procedures", "data_description", "session", "rig", "processing"]

            missing_fields = [field for field in complete_metadata if v.get(field) is None]
            if (
                Platform.ECEPHYS.value.abbreviation == platform_abbreviation
                or Platform.SMARTSPIM.value.abbreviation == platform_abbreviation
            ) and missing_fields:
                v["metadata_status"] = "MISSING"
                raise ValueError(f"Missing metadata: {', '.join(missing_fields)}")

        return v
