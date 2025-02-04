"""Generic metadata class for Data Asset Records."""

import inspect
import json
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Literal, Optional, get_args
from uuid import UUID, uuid4

from aind_data_schema_models.modalities import ExpectedFiles, FileRequirement
from aind_data_schema_models.platforms import Platform
from pydantic import (
    Field,
    PrivateAttr,
    SkipValidation,
    ValidationError,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_validator,
)

from aind_data_schema.base import AindCoreModel, is_dict_corrupt, AwareDatetimeWithDefault
from aind_data_schema.core.acquisition import Acquisition
from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.procedures import Injection, Procedures, Surgery
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.quality_control import QualityControl
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session
from aind_data_schema.core.subject import Subject
from aind_data_schema.utils.compatibility_check import RigSessionCompatibility

CORE_FILES = [
    "subject",
    "data_description",
    "procedures",
    "session",
    "rig",
    "processing",
    "acquisition",
    "instrument",
    "quality_control",
]


class MetadataStatus(str, Enum):
    """Status of Metadata"""

    VALID = "Valid"
    INVALID = "Invalid"
    MISSING = "Missing"
    UNKNOWN = "Unknown"


class ExternalPlatforms(str, Enum):
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
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["1.1.2"]] = Field(default="1.1.2")
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
    created: AwareDatetimeWithDefault = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        title="Created",
        description="The utc date and time the data asset created.",
    )
    last_modified: AwareDatetimeWithDefault = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
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
    external_links: Dict[ExternalPlatforms, List[str]] = Field(
        default=dict(), title="External Links", description="Links to the data asset on different platforms."
    )
    # We can make the AindCoreModel fields optional for now and do more
    # granular validations using validators. We may have some older data
    # assets in S3 that don't have metadata attached. We'd still like to
    # index that data, but we can flag those instances as MISSING or UNKNOWN
    subject: Optional[Subject] = Field(
        default=None,
        title="Subject",
        description="Subject of data collection.",
    )
    data_description: Optional[DataDescription] = Field(
        default=None, title="Data Description", description="A logical collection of data files."
    )
    procedures: Optional[Procedures] = Field(
        default=None, title="Procedures", description="All procedures performed on a subject."
    )
    session: Optional[Session] = Field(default=None, title="Session", description="Description of a session.")
    rig: Optional[Rig] = Field(default=None, title="Rig", description="Rig.")
    processing: Optional[Processing] = Field(default=None, title="Processing", description="All processes run on data.")
    acquisition: Optional[Acquisition] = Field(
        default=None, title="Acquisition", description="Imaging acquisition session"
    )
    instrument: Optional[Instrument] = Field(
        default=None, title="Instrument", description="Instrument, which is a collection of devices"
    )
    quality_control: Optional[QualityControl] = Field(
        default=None, title="Quality Control", description="Description of quality metrics for a data asset"
    )

    @field_validator(
        *CORE_FILES,
        mode="before",
    )
    def validate_core_fields(cls, value, info: ValidationInfo):
        """Don't automatically raise errors if the core models are invalid"""

        # extract field from Optional[<class>] annotation
        field_name = info.field_name
        field_class = [f for f in get_args(cls.model_fields[field_name].annotation) if inspect.isclass(f)][0]

        if isinstance(value, dict):
            try:
                core_model = field_class.model_validate(value)
            except ValidationError as e:
                print(f"Error in validating {field_name}: {e}")
                core_model = field_class.model_construct(**value)
        else:
            core_model = value
        return core_model

    @field_validator("last_modified", mode="after")
    def validate_last_modified(cls, value, info: ValidationInfo):
        """Convert last_modified field to UTC from other timezones"""
        return value.astimezone(timezone.utc)

    @field_serializer("last_modified")
    def serialize_last_modified(value) -> str:
        """Serialize last_modified field"""
        return value.isoformat().replace("+00:00", "Z")

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
                except ValidationError as e:
                    print(f"Error in {field_name}: {e}")
                    metadata_status = MetadataStatus.INVALID
        # For certain required fields, like subject, if they are not present,
        # mark the metadata record as missing
        if self.subject is None:
            metadata_status = MetadataStatus.MISSING
        self.metadata_status = metadata_status
        # return values
        return self

    @model_validator(mode="after")
    def validate_expected_files_by_modality(self):
        """Validator checks that all required/excluded files match the metadata model"""
        if self.data_description:
            modalities = self.data_description.modality

            requirement_dict = {}

            for modality in modalities:
                abbreviation = modality.abbreviation.replace("-", "_").upper()

                for file in CORE_FILES:
                    #  For each field, check if this is a required/excluded file
                    file_requirement = getattr(getattr(ExpectedFiles, abbreviation), file)

                    if file not in requirement_dict:
                        requirement_dict[file] = (abbreviation, file_requirement)
                    else:
                        (prev_modality, prev_requirement) = requirement_dict[file]

                        if (file_requirement == FileRequirement.REQUIRED) or (
                            file_requirement == FileRequirement.OPTIONAL
                            and prev_requirement == FileRequirement.EXCLUDED
                        ):
                            # override, required wins over all else, and optional wins over excluded
                            requirement_dict[file] = (abbreviation, file_requirement)

            for file in CORE_FILES:
                # Unpack modality
                (requirement_modality, file_requirement) = requirement_dict[file]

                # Check required case
                if file_requirement == FileRequirement.REQUIRED and not getattr(self, file):
                    raise ValueError(f"{requirement_modality} metadata missing required file: {file}")

                # Check excluded case
                if file_requirement == FileRequirement.EXCLUDED and getattr(self, file):
                    raise ValueError(f"{requirement_modality} metadata includes excluded file: {file}")

        return self

    @model_validator(mode="after")
    def validate_smartspim_metadata(self):
        """Validator for smartspim metadata"""

        if (
            self.data_description
            and self.data_description.platform == Platform.SMARTSPIM
            and self.procedures
            and any(
                isinstance(surgery, Injection) and getattr(surgery, "injection_materials", None) is None
                for subject_procedure in self.procedures.subject_procedures
                if isinstance(subject_procedure, Surgery)
                for surgery in subject_procedure.procedures
            )
        ):
            raise ValueError("Injection is missing injection_materials.")

        return self

    @model_validator(mode="after")
    def validate_ecephys_metadata(self):
        """Validator for metadata"""
        if (
            self.data_description
            and self.data_description.platform == Platform.ECEPHYS
            and self.procedures
            and any(
                isinstance(surgery, Injection) and getattr(surgery, "injection_materials", None) is None
                for subject_procedure in self.procedures.subject_procedures
                if isinstance(subject_procedure, Surgery)
                for surgery in subject_procedure.procedures
            )
        ):
            raise ValueError("Injection is missing injection_materials.")
        return self

    @model_validator(mode="after")
    def validate_rig_session_compatibility(self):
        """Validator for metadata"""
        if self.rig and self.session:
            check = RigSessionCompatibility(self.rig, self.session)
            check.run_compatibility_check()
        return self


def create_metadata_json(
    name: str,
    location: str,
    core_jsons: Dict[str, Optional[dict]],
    optional_created: Optional[datetime] = None,
    optional_external_links: Optional[dict] = None,
) -> dict:
    """Creates a Metadata dict from dictionary of core schema fields."""
    # Extract basic parameters and non-corrupt core schema fields
    params = {
        "name": name,
        "location": location,
    }
    if optional_created is not None:
        params["created"] = optional_created
    if optional_external_links is not None:
        params["external_links"] = optional_external_links
    core_fields = dict()
    for key, value in core_jsons.items():
        if key in CORE_FILES and value is not None:
            if is_dict_corrupt(value):
                logging.warning(f"Provided {key} is corrupt! It will be ignored.")
            else:
                core_fields[key] = value
    # Create Metadata object and convert to JSON
    # If there are any validation errors, still create it
    # but set MetadataStatus as Invalid
    try:
        metadata = Metadata.model_validate({**params, **core_fields})
        metadata_json = json.loads(metadata.model_dump_json(by_alias=True))
    except Exception as e:
        logging.warning(f"Issue with metadata construction! {e.args}")
        metadata = Metadata.model_validate(params)
        metadata_json = json.loads(metadata.model_dump_json(by_alias=True))
        for key, value in core_fields.items():
            metadata_json[key] = value
        metadata_json["metadata_status"] = MetadataStatus.INVALID.value
    return metadata_json
