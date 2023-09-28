"""Module for models"""

from datetime import datetime
from enum import Enum

from pydantic import Extra, Field

from aind_data_schema.base import AindCoreModel


class MetadataStatus(Enum):
    """Status of Metadata"""

    VALID = "Valid"
    INVALID = "Invalid"
    MISSING = "Missing"
    UNKNOWN = "Unknown"


class DataAsset(AindCoreModel):
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

    class Config:
        """Need to allow for additional fields to append to base model"""

        extra = Extra.allow
