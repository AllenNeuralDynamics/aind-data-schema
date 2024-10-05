""" Generic metadata classes for data """

import re
from datetime import datetime
from typing import Any, List, Literal, Optional

from aind_data_schema_models.data_name_patterns import (
    DataLevel,
    DataRegex,
    Group,
    build_data_name,
    datetime_from_name_string,
)
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.platforms import Platform
from pydantic import Field, model_validator

from aind_data_schema.base import AindCoreModel, AindModel, AwareDatetimeWithDefault


class Funding(AindModel):
    """Description of funding sources"""

    funder: Organization.FUNDERS = Field(..., title="Funder")
    grant_number: Optional[str] = Field(default=None, title="Grant number")
    fundee: Optional[str] = Field(default=None, title="Fundee", description="Person(s) funded by this mechanism")


class RelatedData(AindModel):
    """Description of related data asset"""

    related_data_path: str = Field(..., title="Related data path")
    relation: str = Field(..., title="Relation", description="Relation of data to this asset")


class DataDescription(AindCoreModel):
    """Description of a logical collection of data files"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/data_description.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.1"] = Field("1.0.1")
    license: Literal["CC-BY-4.0"] = Field("CC-BY-4.0", title="License")

    platform: Platform.ONE_OF = Field(
        ...,
        description="Name for a standardized primary data collection system",
        title="Platform",
    )
    subject_id: str = Field(
        ...,
        pattern=DataRegex.NO_UNDERSCORES.value,
        description="Unique identifier for the subject of data acquisition",
        title="Subject ID",
    )
    creation_time: AwareDatetimeWithDefault = Field(
        ...,
        description="Time that data files were created, used to uniquely identify the data",
        title="Creation Time",
    )
    label: Optional[str] = Field(
        default=None,
        description="A short name for the data, used in file names and labels",
        title="Label",
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
        description="level of processing that data has undergone",
        title="Data Level",
    )
    group: Optional[Group] = Field(
        default=None,
        description="A short name for the group of individuals that collected this data",
        title="Group",
    )
    investigators: List[PIDName] = Field(
        ...,
        description="Full name(s) of key investigators (e.g. PI, lead scientist, contact person)",
        title="Investigators",
        min_length=1,
    )
    project_name: Optional[str] = Field(
        default=None,
        pattern=DataRegex.NO_SPECIAL_CHARS_EXCEPT_SPACE.value,
        description="A name for a set of coordinated activities intended to achieve one or more objectives.",
        title="Project Name",
    )
    restrictions: Optional[str] = Field(
        default=None,
        description="Detail any restrictions on publishing or sharing these data",
        title="Restrictions",
    )
    modality: List[Modality.ONE_OF] = Field(
        ...,
        description="A short name for the specific manner, characteristic, pattern of application, or the employment"
        "of any technology or formal procedure to generate data for a study",
        title="Modality",
    )
    related_data: List[RelatedData] = Field(
        default=[],
        title="Related data",
        description="Path and description of data assets associated with this asset (eg. reference images)",
    )
    data_summary: Optional[str] = Field(
        default=None, title="Data summary", description="Semantic summary of experimental goal"
    )

    @classmethod
    def parse_name(cls, name):
        """Decompose a DataDescription name string into component parts"""
        m = re.match(f"{DataRegex.DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            label=m.group("label"),
            creation_time=creation_time,
        )

    @model_validator(mode="after")
    def build_name(self):
        """sets the name of the file"""
        if self.label is not None and self.name is None:
            self.name = build_data_name(self.label, creation_datetime=self.creation_time)
        elif self.name is None:
            raise ValueError("Either label or name must be set")
        return self


class DerivedDataDescription(DataDescription):
    """A logical collection of data files derived via processing"""

    input_data_name: str
    data_level: Literal[DataLevel.DERIVED] = Field(
        default=DataLevel.DERIVED, description="level of processing that data has undergone", title="Data Level"
    )
    process_name: Optional[str] = Field(
        default=None,
        pattern=DataRegex.NO_SPECIAL_CHARS.value,
        description="Name of the process that created the data",
        title="Process name",
    )

    @classmethod
    def parse_name(cls, name):
        """decompose DerivedDataDescription name into parts"""

        # look for input data name
        m = re.match(f"{DataRegex.DERIVED.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            process_name=m.group("process_name"),
            creation_time=creation_time,
            input_data_name=m.group("input"),
        )

    @model_validator(mode="after")
    def build_name(self):
        """sets the name of the file"""
        if self.process_name:
            self.name = build_data_name(
                f"{self.input_data_name}_{self.process_name}", creation_datetime=self.creation_time
            )
        else:
            self.name = build_data_name(f"{self.input_data_name}", creation_datetime=self.creation_time)
        return self

    @classmethod
    def from_data_description(cls, data_description: DataDescription, process_name: str, **kwargs):
        """
        Create a DerivedDataDescription from a DataDescription object.

        Parameters
        ----------
        data_description : DataDescription
            The DataDescription object to use as the base for the Derived
        process_name : str
            Name of the process that created the data
        kwargs
            DerivedDataDescription fields can be explicitly set and will override
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
                return getattr(DerivedDataDescription.model_fields.get(field_name), "default")

        creation_time = datetime.utcnow() if kwargs.get("creation_time") is None else kwargs["creation_time"]

        return cls(
            creation_time=creation_time,
            process_name=process_name,
            institution=get_or_default("institution"),
            funding_source=get_or_default("funding_source"),
            group=get_or_default("group"),
            investigators=get_or_default("investigators"),
            restrictions=get_or_default("restrictions"),
            modality=get_or_default("modality"),
            platform=get_or_default("platform"),
            project_name=get_or_default("project_name"),
            subject_id=get_or_default("subject_id"),
            related_data=get_or_default("related_data"),
            data_summary=get_or_default("data_summary"),
            input_data_name=data_description.name,
        )


class RawDataDescription(DataDescription):
    """A logical collection of data files as acquired from a rig or instrument"""

    data_level: Literal[DataLevel.RAW] = Field(
        default=DataLevel.RAW, description="level of processing that data has undergone", title="Data Level"
    )

    @model_validator(mode="after")
    def build_name(self):
        """sets the name of the file"""
        platform_abbreviation = self.platform.abbreviation
        self.name = build_data_name(f"{platform_abbreviation}_{self.subject_id}", creation_datetime=self.creation_time)
        return self

    @classmethod
    def parse_name(cls, name):
        """Decompose raw description name into component parts"""

        m = re.match(f"{DataRegex.RAW.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        platform_abbreviation = m.group("platform_abbreviation")
        platform = Platform.from_abbreviation(platform_abbreviation)

        return dict(
            platform=platform,
            subject_id=m.group("subject_id"),
            creation_time=creation_time,
        )


class AnalysisDescription(DataDescription):
    """A collection of data files as analyzed from an asset"""

    data_level: Literal[DataLevel.DERIVED] = Field(
        DataLevel.DERIVED, description="Level of processing that data has undergone", title="Data Level"
    )
    project_name: str = Field(
        ...,
        pattern=DataRegex.NO_SPECIAL_CHARS.value,
        description="Name of the project the analysis belongs to",
        title="Project name",
    )
    analysis_name: str = Field(
        ...,
        pattern=DataRegex.NO_SPECIAL_CHARS.value,
        description="Name of the analysis performed",
        title="Analysis name",
    )

    @model_validator(mode="after")
    def build_name(self):
        """returns the label of the file"""
        self.name = build_data_name(f"{self.project_name}_{self.analysis_name}", creation_datetime=self.creation_time)
        return self

    @classmethod
    def parse_name(cls, name):
        """Decompose raw Analysis name into component parts"""

        m = re.match(f"{DataRegex.ANALYZED.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            project_abbreviation=m.group("project_abbreviation"),
            analysis_name=m.group("analysis_name"),
            creation_time=creation_time,
        )
