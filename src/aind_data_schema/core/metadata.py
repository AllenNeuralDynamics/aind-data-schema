"""Generic metadata class for Data Asset Records."""

import inspect
import json
import logging
from datetime import datetime, timezone
from enum import Enum
import warnings
from typing import Dict, List, Literal, Optional, get_args
from uuid import UUID, uuid4

from aind_data_schema_models.modalities import Modality
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

from aind_data_schema.base import DataCoreModel, is_dict_corrupt, AwareDatetimeWithDefault
from aind_data_schema.core.acquisition import Acquisition, MODALITY_DEVICE_REQUIREMENTS, CONFIG_DEVICE_REQUIREMENTS
from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.procedures import Injection, Procedures, Surgery
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.quality_control import QualityControl
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.subject import Subject
from aind_data_schema.utils.compatibility_check import InstrumentAcquisitionCompatibility

CORE_FILES = [
    "subject",
    "data_description",
    "procedures",
    "instrument",
    "processing",
    "acquisition",
    "quality_control",
]

REQUIRED_FILES = [
    "subject",
    "data_description",
    "procedures",
    "instrument",
    "acquisition",
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


class Metadata(DataCoreModel):
    """The records in the Data Asset Collection needs to contain certain fields
    to easily query and index the data."""

    # Special file name extension to distinguish this json file from others
    # The models base on this schema will be saved to metadata.nd.json as
    # default
    _FILE_EXTENSION = PrivateAttr(default=".nd.json")

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/metadata.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.5"]] = Field(default="2.0.5")
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
    # We can make the DataCoreModel fields optional for now and do more
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
    instrument: Optional[Instrument] = Field(
        default=None, title="Instrument", description="Devices used to acquire data."
    )
    processing: Optional[Processing] = Field(default=None, title="Processing", description="All processes run on data.")
    acquisition: Optional[Acquisition] = Field(default=None, title="Acquisition", description="Data acquisition")
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
                        if inspect.isclass(f) and issubclass(f, DataCoreModel)
                    ]
                )
            )
            if (
                optional_classes
                and inspect.isclass(optional_classes[0])
                and issubclass(optional_classes[0], DataCoreModel)
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

    @model_validator(mode="after")
    def validate_expected_files_by_modality(self):
        """Validator warns users if required files are missing"""

        for file in REQUIRED_FILES:
            if not getattr(self, file):
                warnings.warn(f"Metadata missing required file: {file}")

        return self

    @model_validator(mode="after")
    def validate_smartspim_metadata(self):
        """Validator for smartspim metadata"""

        if (
            self.data_description
            and any([modality == Modality.SPIM for modality in self.data_description.modalities])
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
            and any([modality == Modality.ECEPHYS for modality in self.data_description.modalities])
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
    def validate_instrument_acquisition_compatibility(self):
        """Validator for metadata"""
        if self.instrument and self.acquisition:
            check = InstrumentAcquisitionCompatibility(self.instrument, self.acquisition)
            check.run_compatibility_check()
        return self

    def _check_for_device(self, device_type_group):
        """Check if the instrument has a device of a certain type"""
        for component in self.instrument.components:
            if any(isinstance(component, device_type) for device_type in device_type_group):
                return True
        return False

    @model_validator(mode="after")
    def validate_acquisition_modality_requirements(self):
        """Validator for acquisition modality -> device requirements

        For certain modalities in acquisition, check that the instrument has the appropriate components
        """

        if not self.acquisition:
            return self

        # get all modalities from all data_streams
        modalities = [modality for data_stream in self.acquisition.data_streams for modality in data_stream.modalities]
        for modality in modalities:
            if modality in MODALITY_DEVICE_REQUIREMENTS.keys():
                for group in MODALITY_DEVICE_REQUIREMENTS[modality]:
                    if not self._check_for_device(group):
                        requirement = ", ".join(device.__name__ for device in group)
                        raise ValueError(
                            f"Modality '{modality.abbreviation}' requires one " f"of '{requirement}' in instrument"
                        )

        return self

    @model_validator(mode="after")
    def validate_acquisition_config_requirements(self):
        """Validator for acquisition config -> device requirements

        For certain config files in acquisition, check that the instrument has the appropriate devices
        """

        if not self.acquisition:
            return self

        configurations = [
            config for data_stream in self.acquisition.data_streams for config in data_stream.configurations
        ]

        for config in configurations:
            if any(type(config).__name__ == config_type for config_type in CONFIG_DEVICE_REQUIREMENTS.keys()):
                group = CONFIG_DEVICE_REQUIREMENTS[type(config).__name__]
                if not self._check_for_device(group):
                    requirement = ", ".join(device.__name__ for device in group)
                    raise ValueError(
                        f"Configuration '{type(config).__name__}' requires one of '{requirement}' in instrument"
                    )

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
