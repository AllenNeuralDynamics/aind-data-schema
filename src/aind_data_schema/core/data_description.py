"""Generic metadata classes for data"""

import re
import warnings
from typing import List, Literal, Optional

from aind_data_schema_models.data_name_patterns import (
    DataLevel,
    DataRegex,
    Group,
    build_data_name,
    datetime_from_name_string,
)
from aind_data_schema_models.licenses import License
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import Field, SkipValidation, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel
from aind_data_schema.components.identifiers import Person


class Funding(DataModel):
    """Description of funding sources"""

    funder: Organization.ONE_OF = Field(..., title="Funder")
    grant_number: Optional[str] = Field(default=None, title="Grant number")
    fundee: Optional[List[Person]] = Field(
        default=None, title="Fundee", description="Person(s) funded by this mechanism"
    )


class DataDescription(DataCoreModel):
    """Description of a logical collection of data files"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/data_description.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.4.0"]] = Field(default="2.4.0")
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
        description=(
            "When left blank, a name will be generated based on subject_id and creation_time. "
            "Conventionally also used as the name of the data folder."
        ),
        title="Data asset name",
        validate_default=True,
    )
    institution: Organization.ONE_OF = Field(
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
            if m is None:
                raise ValueError(f"name({name}) does not match pattern")
            return dict(
                creation_time=datetime_from_name_string(m.group("c_datetime")),
                label=m.group("label"),
            )
        elif data_level == DataLevel.DERIVED:
            m = re.match(f"{DataRegex.DERIVED.value}", name)
            if m is not None:
                return dict(
                    input=m.group("input"),
                    process_name=m.group("process_name"),
                    creation_time=datetime_from_name_string(m.group("c_datetime")),
                )
            m = re.match(f"{DataRegex.ANALYZED.value}", name)
            if m is not None:
                return dict(
                    project_abbreviation=m.group("project_abbreviation"),
                    analysis_name=m.group("analysis_name"),
                    creation_time=datetime_from_name_string(m.group("c_datetime")),
                )
            raise ValueError(f"name({name}) does not match pattern")
        else:
            raise ValueError(f"DataLevel({data_level}) not supported")

    @model_validator(mode="after")
    def subject_id_when_raw(self):
        """Ensure that a subject_id is provided when data_level is RAW"""
        if self.data_level == DataLevel.RAW and self.subject_id is None:
            raise ValueError("subject_id must be set when data_level is RAW")
        return self

    @model_validator(mode="after")
    def build_name(self):
        """Set the name of data_description when data_level is RAW and the name is empty"""
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
        """Deprecated. Use aind_data_schema.utils.inheritance.derive_data_description_from_raw instead."""
        from aind_data_schema.utils.inheritance import derive_data_description_from_raw

        warnings.warn(
            "DataDescription.from_raw is deprecated. Use "
            "aind_data_schema.utils.inheritance.derive_data_description_from_raw instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return derive_data_description_from_raw(data_description, process_name, source_data, **kwargs)

    @classmethod
    def from_derived(
        cls, data_description: "DataDescription", process_name: str, source_data: Optional[List[str]] = None, **kwargs
    ) -> "DataDescription":
        """Deprecated. Use aind_data_schema.utils.inheritance.derive_data_description_from_derived instead."""
        from aind_data_schema.utils.inheritance import derive_data_description_from_derived

        warnings.warn(
            "DataDescription.from_derived is deprecated. Use "
            "aind_data_schema.utils.inheritance.derive_data_description_from_derived instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return derive_data_description_from_derived(data_description, process_name, source_data, **kwargs)

    @classmethod
    def from_data_description(
        cls, data_description: "DataDescription", process_name: str, source_data: Optional[List[str]] = None, **kwargs
    ) -> "DataDescription":
        """Deprecated. Use aind_data_schema.utils.inheritance.derive_data_description instead."""
        from aind_data_schema.utils.inheritance import derive_data_description

        warnings.warn(
            "DataDescription.from_data_description is deprecated. Use "
            "aind_data_schema.utils.inheritance.derive_data_description instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return derive_data_description(data_description, process_name, source_data, **kwargs)
