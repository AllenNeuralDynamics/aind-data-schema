"""Module for models"""

from datetime import datetime

from pydantic import BaseModel, Extra, Field


class DataAssetRecord(BaseModel):
    """The records in the Data Asset Collection needs to contain certain fields
    to easily query and index the data."""

    code_ocean_id: str = Field(
        ...,
        alias="_id",
        title="Data Asset ID",
        description="The unique id of the data asset.",
    )
    name: str = Field(
        ...,
        alias="_name",
        description="Name of the data asset.",
        title="Data Asset Name",
    )
    created: datetime = Field(
        ...,
        alias="_created",
        title="Created",
        description="The data and time the data asset created.",
    )
    location: str = Field(
        ...,
        alias="_location",
        title="Location",
        description="Current location of the data asset.",
    )

    class Config:
        """Need to allow for additional fields to append to base model"""

        extra = Extra.allow

    @property
    def _id(self):
        """Property for _id"""
        return self.code_ocean_id

    @property
    def _name(self):
        """Property for _name"""
        return self.name

    @property
    def _location(self):
        """Property for _location"""
        return self.location

    @property
    def _created(self):
        """Property for _created"""
        return self.created