""" Generic metadata classes for data """

import re
from datetime import datetime, timezone
from typing import Any, List, Literal, Optional

from aind_data_schema_models.data_name_patterns import (
    DataLevel,
    DataRegex,
    Group,
    build_data_name,
    datetime_from_name_string,
    datetime_to_name_string,
)
from aind_data_schema_models.licenses import License
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import Field, SkipValidation, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel
from aind_data_schema.components.identifiers import Person


class Funding(DataModel):
    """Description of funding sources"""

    funder: Organization.FUNDERS = Field(..., title="Funder")
    grant_number: Optional[str] = Field(default=None, title="Grant number")
    fundee: Optional[List[Person]] = Field(
        default=None, title="Fundee", description="Person(s) funded by this mechanism"
    )


class DataDescription(DataCoreModel):
    """Description of a logical collection of data files"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/data_description.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.1.1"]] = Field(default="2.1.1")
    license: License = Field(default=License.CC_BY_40, title="License")

    subject_id: Optional[str] = Field(
        default=None,
        pattern=DataRegex.NO_UNDERSCORES.value,
        description="Unique identifier for the subject of data acquisition",
        title="Subject ID",
    )
    creation_time: AwareDatetimeWithDefault = Field(
        ...,
        description="Time that data files were created, used to uniquely identify the data",
        title="Creation Time",
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="Descriptive strings to help categorize and search for data",
        title="Tags",
    )
    name: Optional[str] = Field(
        default=None,
        description="Name of data, conventionally also the name of the directory containing all data and metadata",
        title="Name",
        validate_default=True,
    )
    institution: Organization.RESEARCH_INSTITUTIONS = Field(
        ...,
        description="An established society, corporation, foundation or other organization that collected this data",
        title="Institution",
    )
    funding_source: List[Funding] = Field(
        ...,
        title="Funding source",
        description="Funding source. If internal funding, select 'Allen Institute'",
        min_length=1,
    )
    data_level: DataLevel = Field(
        ...,
        description="Level of processing that data has undergone",
        title="Data Level",
    )
    group: Optional[Group] = Field(
        default=None,
        description="A short name for the group of individuals that collected this data",
        title="Group",
    )
    investigators: List[Person] = Field(
        ...,
        description="Full name(s) of key investigators (e.g. PI, lead scientist, contact person)",
        title="Investigators",
        min_length=1,
    )
    project_name: str = Field(
        ...,
        pattern=DataRegex.NO_SPECIAL_CHARS_EXCEPT_SPACE.value,
        description="A name for a set of coordinated activities intended to achieve one or more objectives.",
        title="Project Name",
    )
    restrictions: Optional[str] = Field(
        default=None,
        description="Detail any restrictions on publishing or sharing these data",
        title="Restrictions",
    )
    modalities: List[Modality.ONE_OF] = Field(
        ...,
        description="A short name for the specific manner, characteristic, pattern of application, or the employment"
        " of any technology or formal procedure to generate data for a study",
        title="Modalities",
    )
    source_data: Optional[List[str]] = Field(
        default=None,
        description="For derived assets, list the source data asset names used to create this data",
        title="Source data",
    )
    data_summary: Optional[str] = Field(
        default=None, title="Data summary", description="Semantic summary of experimental goal"
    )

    @classmethod
    def parse_name(cls, name, data_level: DataLevel = DataLevel.RAW):
        """Decompose a DataDescription name string into component parts"""

        if data_level == DataLevel.RAW:
            m = re.match(f"{DataRegex.DATA.value}", name)
        elif data_level == DataLevel.DERIVED:
            m = re.match(f"{DataRegex.DERIVED.value}", name)
        else:
            raise ValueError(f"DataLevel({data_level}) not supported")

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_datetime"))

        if data_level == DataLevel.RAW:
            return dict(
                creation_time=creation_time,
                label=m.group("label"),
            )
        elif data_level == DataLevel.DERIVED:
            return dict(
                input=m.group("input"),
                process_name=m.group("process_name"),
                creation_time=creation_time,
            )

    @model_validator(mode="after")
    def subject_id_when_raw(self):
        """Ensure that a subject_id is provided when data_level is RAW"""
        if self.data_level == DataLevel.RAW and self.subject_id is None:
            raise ValueError("subject_id must be set when data_level is RAW")
        return self

    @model_validator(mode="after")
    def build_name(self):
        """sets the name of the file"""
        if self.name is None and self.data_level == DataLevel.RAW:
            self.name = build_data_name(self.subject_id, creation_datetime=self.creation_time)

        # check that the name matches the name regex
        if not re.match(DataRegex.DATA.value, self.name):
            raise ValueError(f"Name({self.name}) does not match allowed Regex pattern")

        return self

    @model_validator(mode="after")
    def source_data_when_raw(self):
        """Ensure that source_data is not provided when data_level is RAW"""
        if self.data_level == DataLevel.RAW and self.source_data is not None:
            raise ValueError("source_data must not be set when data_level is 'raw'")
        return self

    @classmethod
    def from_raw(
        cls, data_description: "DataDescription", process_name: str, source_data: Optional[List[str]] = None, **kwargs
    ) -> "DataDescription":
        """
        Create a DataLevel.DERIVED DataDescription from a DataLevel.RAW DataDescription object.

        Parameters
        ----------
        data_description : DataDescription
            The DataDescription object to use as the base for the Derived
        process_name : str
            Name of the process that created the data
        kwargs
            DataDescription fields can be explicitly set and will override
            values pulled from DataDescription

        """

        def get_or_default(field_name: str) -> Any:
            """
            If the field is set in kwargs, use that value. Otherwise, check if
            the field is set in the DataDescription object. If not, pull from
            the field default value if the field has a default value. Otherwise,
            return None and allow pydantic to raise a Validation Error if field
            is not Optional.
            Parameters
            ----------
            field_name : str
                Name of the field to set

            Returns
            -------
            Any

            """
            if kwargs.get(field_name) is not None:
                return kwargs.get(field_name)
            elif hasattr(data_description, field_name) and getattr(data_description, field_name) is not None:
                return getattr(data_description, field_name)
            else:
                return getattr(DataDescription.model_fields.get(field_name), "default")

        creation_time = (
            datetime.now(tz=timezone.utc) if kwargs.get("creation_time") is None else kwargs["creation_time"]
        )

        if not isinstance(creation_time, datetime):
            raise ValueError(f"creation_time({creation_time}) must be a datetime object")

        # Upgrade name
        original_name = data_description.name
        derived_name = f"{original_name}_{process_name}_{datetime_to_name_string(creation_time)}"
        if not re.match(DataRegex.DERIVED.value, derived_name):  # pragma: no cover
            raise ValueError(f"Derived name({derived_name}) does not match allowed Regex pattern")

        # Upgrade source_data
        if source_data is not None:
            new_source_data = (
                source_data if not data_description.source_data else data_description.source_data + source_data
            )
        else:
            new_source_data = (
                [original_name] if not data_description.source_data else data_description.source_data + [original_name]
            )

        return cls(
            subject_id=get_or_default("subject_id"),
            creation_time=creation_time,
            tags=get_or_default("tags"),
            name=derived_name,
            institution=get_or_default("institution"),
            funding_source=get_or_default("funding_source"),
            data_level=DataLevel.DERIVED,
            group=get_or_default("group"),
            investigators=get_or_default("investigators"),
            project_name=get_or_default("project_name"),
            restrictions=get_or_default("restrictions"),
            modalities=get_or_default("modalities"),
            data_summary=get_or_default("data_summary"),
            source_data=new_source_data,
        )
