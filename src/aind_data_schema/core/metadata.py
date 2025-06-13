"""Generic metadata class for Data Asset Records."""

import inspect
import json
import logging
import warnings
from typing import Dict, Literal, Optional, get_args

from aind_data_schema_models.modalities import Modality
from pydantic import (
    ConfigDict,
    Field,
    PrivateAttr,
    SkipValidation,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)

from aind_data_schema.base import DataCoreModel
from aind_data_schema.components.identifiers import DatabaseIdentifiers
from aind_data_schema.core.acquisition import Acquisition
from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.model import Model
from aind_data_schema.core.procedures import Injection, Procedures, Surgery
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.quality_control import QualityControl
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
    "model",
]

# Files present must include at least one of these "file set" keys,
# and all files listed in any of the matched sets
REQUIRED_FILE_SETS = {
    "subject": [
        "data_description",
        "procedures",
        "instrument",
        "acquisition",
    ],
    "processing": ["data_description"],
    "model": ["data_description"],
}


class Metadata(DataCoreModel):
    """The records in the Data Asset Collection needs to contain certain fields
    to easily query and index the data."""

    model_config = ConfigDict(extra="ignore")

    # Special file name extension to distinguish this json file from others
    # The models base on this schema will be saved to metadata.nd.json as
    # default
    _FILE_EXTENSION = PrivateAttr(default=".nd.json")

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/metadata.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.67"]] = Field(default="2.0.67")
    name: str = Field(
        ...,
        description="Name of the data asset.",
        title="Data Asset Name",
    )
    location: str = Field(
        ...,
        title="Location",
        description="Current location of the data asset.",
    )
    other_identifiers: Optional[DatabaseIdentifiers] = Field(
        default=None, title="Other identifiers", description="Links to the data asset on secondary platforms."
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
    model: Optional[Model] = Field(
        default=None, title="Model", description="Description of a machine learning model trained on data."
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
                logging.warning(f"Error in validating {field_name}: {e}")
                core_model = field_class.model_construct(**value)
        else:
            core_model = value
        return core_model

    @model_validator(mode="after")
    def validate_expected_files_by_modality(self):
        """Validator warns users if required files are missing"""

        validated = False
        for file in REQUIRED_FILE_SETS.keys():
            if getattr(self, file):
                for file in REQUIRED_FILE_SETS[file]:
                    if not getattr(self, file):
                        warnings.warn(f"Metadata missing required file: {file}")
                validated = True
        if not validated:
            warnings.warn(
                f"Metadata must contain at least one of the following files: {list(REQUIRED_FILE_SETS.keys())}"
            )

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

    @model_validator(mode="after")
    @classmethod
    def validate_acquisition_active_devices(cls, values):
        """Ensure that all Acquisition.data_streams.active_devices exist in either the instrument or procedures."""

        active_devices = []

        if values.acquisition:
            for data_stream in values.acquisition.data_streams:
                active_devices.extend(data_stream.active_devices)

        device_names = []

        if values.instrument:
            for component in values.instrument.components:
                device_names.append(component.name)
        if values.procedures:
            device_names.extend(values.procedures.get_implanted_device_names())

        # Check if all active devices are in the available devices
        if not all(device in device_names for device in active_devices):
            missing_devices = set(active_devices) - set(device_names)
            raise ValueError(
                f"Active devices '{missing_devices}' were not found in either the Instrument.components or "
                f"in an individual procedure's implanted_device field."
            )

        return values

    @model_validator(mode="after")
    def validate_acquisition_connections(self):
        """Validate for Acquisition.data_streams.connections that all connections map between devices either in the
        instrument OR procedures"""

        device_names = []

        if self.instrument:
            for component in self.instrument.components:
                device_names.append(component.name)
        if self.procedures:
            device_names.extend(self.procedures.get_implanted_device_names())

        # Check if all connection devices are in the available devices
        if self.acquisition:
            data_streams = self.acquisition.data_streams
            for data_stream in data_streams:
                for connection in data_stream.connections:
                    if not all(device in device_names for device in connection.device_names):
                        raise ValueError(
                            f"Connection '{connection}' contains devices not found in instrument or procedures."
                        )

        return self


def create_metadata_json(
    name: str,
    location: str,
    core_jsons: Dict[str, Optional[dict]],
    other_identifiers: Optional[dict] = None,
) -> dict:
    """Creates a Metadata dict from dictionary of core schema fields."""
    # Extract basic parameters and non-corrupt core schema fields

    params = {
        "name": name,
        "location": location,
    }
    if other_identifiers is not None:
        params["other_identifiers"] = other_identifiers
    core_fields = dict()
    for key, value in core_jsons.items():
        if key in CORE_FILES and value is not None:
            core_fields[key] = value
    # Create Metadata object and convert to JSON
    # If there are any validation errors, still create it
    try:
        metadata = Metadata.model_validate(params | core_fields)
        metadata_json = json.loads(metadata.model_dump_json(by_alias=True))
    except Exception as e:
        logging.warning(f"Issue with metadata construction! {e.args}")
        metadata = Metadata.model_validate(params)
        metadata_json = json.loads(metadata.model_dump_json(by_alias=True))
        for key, value in core_fields.items():
            metadata_json[key] = value
    return metadata_json
