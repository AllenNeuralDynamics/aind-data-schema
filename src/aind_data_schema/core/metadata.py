"""Generic metadata class for Data Asset Records."""

import inspect
from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, get_args
from uuid import UUID, uuid4

from pydantic import Field, PrivateAttr, ValidationError, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import AindCoreModel
from aind_data_schema.core.acquisition import Acquisition
from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.procedures import Procedures
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session
from aind_data_schema.core.subject import Subject


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
    _FILE_EXTENSION = PrivateAttr(default=".nd.json")

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/metadata.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})

    schema_version: Literal["0.1.2"] = Field("0.1.2")
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

    @field_validator(
        "subject",
        "data_description",
        "procedures",
        "session",
        "rig",
        "processing",
        "acquisition",
        "instrument",
        mode="before",
    )
    def validate_core_fields(cls, value, info: ValidationInfo):
        """Don't automatically raise errors if the core models are invalid"""

        # extract field from Optional[<class>] annotation
        field_name = info.field_name
        field_class = [f for f in get_args(cls.model_fields[field_name].annotation) if inspect.isclass(f)][0]

        # If the input is a json object, we will try to create the field
        if isinstance(value, dict):
            try:
                core_model = field_class.model_validate_json(value)
            # If a validation error is raised,
            # we will construct the field without validation.
            except ValidationError:
                core_model = field_class.model_construct(**value)
        else:
            core_model = value
        return core_model

    @model_validator(mode="after")
    def validate_metadata(self):
        """Validator for metadata"""

        all_model_fields = dict()
        for field_name in self.model_fields:
            # The fields we're interested in are optional. We need to extract out the
            # class using the get_args method
            annotation_args = get_args(self.model_fields[field_name].annotation)
            optional_classes = (
                None
                if not annotation_args
                else (
                    [
                        f
                        for f in get_args(self.model_fields[field_name].annotation)
                        if inspect.isclass(f) and issubclass(f, AindCoreModel)
                    ]
                )
            )
            if (
                optional_classes
                and inspect.isclass(optional_classes[0])
                and issubclass(optional_classes[0], AindCoreModel)
            ):
                all_model_fields[field_name] = optional_classes[0]

        # For each model field, check that is present and check if the model
        # is valid. If it isn't valid, still add it, but mark MetadataStatus
        # as INVALID
        metadata_status = MetadataStatus.VALID
        for field_name, model_class in all_model_fields.items():
            if getattr(self, field_name) is not None:
                model = getattr(self, field_name)
                model_contents = model.model_dump()
                try:
                    model_class(**model_contents)
                except ValidationError:
                    metadata_status = MetadataStatus.INVALID
        # For certain required fields, like subject, if they are not present,
        # mark the metadata record as missing
        if self.subject is None:
            metadata_status = MetadataStatus.MISSING
        self.metadata_status = metadata_status
        # return values
        return self
