"""Generic metadata class for Data Asset Records."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import Field, root_validator, validate_model, validator

from aind_data_schema.base import AindCoreModel
from aind_data_schema.data_description import DataDescription
from aind_data_schema.imaging.acquisition import Acquisition
from aind_data_schema.imaging.instrument import Instrument
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


class ExternalPlatforms(Enum):
    """External Platforms of Data Assets."""

    CODEOCEAN = "Code Ocean"


class Metadata(AindCoreModel):
    """The records in the Data Asset Collection needs to contain certain fields
    to easily query and index the data."""

    # Special file name extension to distinguish this json file from others
    # The models base on this schema will be saved to metadata.nd.json as
    # default
    _DEFAULT_FILE_EXTENSION = ".nd.json"

    schema_version: str = Field("0.0.6", description="schema version", title="Version", const=True)

    id: UUID = Field(
        default_factory=uuid4,
        alias="_id",
        title="Data Asset ID",
        description="The unique id of the data asset.",
    )
    name: str = Field(
        ...,
        description="Name of the data asset.",
        title="Data Asset Name",
    )
    # We'll set created and last_modified defaults using the root_validator
    # to ensure they're synced on creation
    created: datetime = Field(
        default_factory=datetime.utcnow,
        title="Created",
        description="The utc date and time the data asset created.",
    )
    last_modified: datetime = Field(
        default_factory=datetime.utcnow,
        title="Last Modified",
        description="The utc date and time that the data asset was last modified.",
    )
    location: str = Field(
        ...,
        title="Location",
        description="Current location of the data asset.",
    )
    metadata_status: MetadataStatus = Field(
        default=MetadataStatus.UNKNOWN, title=" Metadata Status", description="The status of the metadata."
    )
    external_links: List[Dict[ExternalPlatforms, str]] = Field(
        default=[], title="External Links", description="Links to the data asset on different platforms."
    )
    # We can make the AindCoreModel fields optional for now and do more
    # granular validations using validators. We may have some older data
    # assets in S3 that don't have metadata attached. We'd still like to
    # index that data, but we can flag those instances as MISSING or UNKNOWN
    subject: Optional[Subject] = Field(
        None,
        title="Subject",
        description="Subject of data collection.",
    )
    data_description: Optional[DataDescription] = Field(
        None, title="Data Description", description="A logical collection of data files."
    )
    procedures: Optional[Procedures] = Field(
        None, title="Procedures", description="All procedures performed on a subject."
    )
    session: Optional[Session] = Field(None, title="Session", description="Description of a session.")
    rig: Optional[Rig] = Field(None, title="Rig", description="Rig.")
    processing: Optional[Processing] = Field(None, title="Processing", description="All processes run on data.")
    acquisition: Optional[Acquisition] = Field(None, title="Acquisition", description="Imaging acquisition session")
    instrument: Optional[Instrument] = Field(
        None, title="Instrument", description="Instrument, which is a collection of devices"
    )

    @validator(
        "subject",
        "data_description",
        "procedures",
        "session",
        "rig",
        "processing",
        "acquisition",
        "instrument",
        pre=True,
    )
    def validate_core_fields(cls, value, field):
        """Don't automatically raise errors if the core models are invalid"""
        if isinstance(value, dict):
            core_model = field.type_.construct(**value)
        else:
            core_model = value
        return core_model

    @root_validator(pre=False)
    def validate_metadata(cls, values):
        """Validator for metadata"""

        # There's a simpler way to do this if we drop support for py37
        all_model_fields = []
        for field_name in cls.__fields__:
            field_to_check = cls.__fields__[field_name]
            try:
                if issubclass(field_to_check.type_, AindCoreModel):
                    all_model_fields.append(field_to_check)
            except TypeError:
                # Type errors in python3.7 when using issubclass on type
                # generics
                pass

        # For each model field, check that is present and check if the model
        # is valid. If it isn't valid, still add it, but mark MetadataStatus
        # as INVALID
        metadata_status = MetadataStatus.VALID
        for model_field in all_model_fields:
            model_class = model_field.type_
            model_name = model_field.name
            if values.get(model_name) is not None:
                model = values[model_name]
                # Since pre=False, the dictionaries get converted to models
                # upstream
                model_contents = model.dict()
                *_, validation_error = validate_model(model_class, model_contents)
                if validation_error:
                    model_instance = model_class.construct(**model_contents)
                    metadata_status = MetadataStatus.INVALID
                else:
                    model_instance = model_class(**model_contents)
                values[model_name] = model_instance
        # For certain required fields, like subject, if they are not present,
        # mark the metadata record as missing
        if values.get("subject") is None:
            metadata_status = MetadataStatus.MISSING
        values["metadata_status"] = metadata_status
        return values
