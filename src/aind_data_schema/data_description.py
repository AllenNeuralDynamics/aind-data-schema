""" Generic metadata classes for data """

from __future__ import annotations

import re
from datetime import date, datetime, time
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, root_validator, PrivateAttr
from .base import AindSchema


class RegexParts(Enum):
    """regular expression components to be re-used elsewhere"""

    DATE = r"\d{4}-\d{2}-\d{2}"
    TIME = r"\d{2}-\d{2}-\d{2}"


class DataRegex(Enum):
    """regular expression patterns for different kinds of data and their properties"""

    DATA = f"^(?P<label>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})$"
    RAW_DATA = f"^(?P<modality>.+?)_(?P<subject_id>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})$"
    DERIVED_DATA = f"^(?P<input>.+?_{RegexParts.DATE.value}_{RegexParts.TIME.value})_(?P<process_name>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})"
    NO_UNDERSCORES = "^[^_]+$"


class DataLevel(Enum):
    """Data level name"""

    RAW_DATA = "raw data"
    DERIVED_DATA = "derived data"


class Institution(Enum):
    """Institution name"""

    AIND = "AIND"
    AIBS = "AIBS"
    HUST = "HUST"


class Group(Enum):
    """Data collection group name"""

    EPHYS = "ephys"
    OPHYS = "ophys"
    MSMA = "MSMA"
    BEHAVIOR = "behavior"


class Modality(Enum):
    """Data collection modality name"""

    ECEPHYS = "ecephys"
    EXASPIM = "ExASPIM"
    SMARTSPIM = "SmartSPIM"
    MESOSPIM = "mesoSPIM"
    OPHYS = "ophys"
    FMOST = "fMOST"


def datetime_to_name_string(d, t):
    """Take a date and time object, format it a as string"""
    ds = d.strftime("%Y-%m-%d")
    ts = t.strftime("%H-%M-%S")
    return f"{ds}_{ts}"


def datetime_from_name_string(d, t):
    """Take date and time strings, generate date and time objects"""
    return (
        datetime.strptime(d, "%Y-%m-%d").date(),
        datetime.strptime(t, "%H-%M-%S").time(),
    )


def build_data_name(label, creation_date, creation_time):
    """Construct a valid data description name"""
    dt_str = datetime_to_name_string(creation_date, creation_time)
    return f"{label}_{dt_str}"


class Funding(BaseModel):
    """Description of funding sources"""

    funder: str = Field(..., title="Funder")
    grant_number: Optional[str] = Field(None, title="Grant number")
    fundee: Optional[str] = Field(
        None, title="Fundee", description="Person(s) funded by this mechanism"
    )


class DataDescription(AindSchema):
    """Description of a logical collection of data files"""

    schema_version: str = Field("0.2.0", title="Schema Version", const=True)
    license: str = Field("CC-BY-4.0", title="License", const=True)

    creation_time: time = Field(
        ...,
        description="Time in UTC that data files were created, used to uniquely identify the data",
        title="Creation Time",
    )
    creation_date: date = Field(
        ...,
        description="Date in UTC that data files were created, used to uniquely identify the data",
        title="Creation Date",
    )
    name: str = Field(
        ...,
        description="Name of data, conventionally also the name of the directory containing all data and metadata",
        title="Name",
    )
    institution: Institution = Field(
        ...,
        description="An established society, corporation, foundation or other organization that collected this data",
        title="Institution",
    )
    funding_source: List[Funding] = Field(
        ...,
        title="Funding source",
        description="Funding sources. If internal label as Institution.",
    )
    data_level: DataLevel = Field(
        ...,
        description="level of processing that data has undergone",
        title="Data Level",
    )
    group: Optional[Group] = Field(
        None,
        description="A short name for the group of individuals that collected this data",
        title="Group",
    )
    project_name: Optional[str] = Field(
        None,
        description="A name for a set of coordinated activities intended to achieve one or more objectives",
        title="Project Name",
    )
    project_id: Optional[str] = Field(
        None,
        description="A database or other identifier for a project",
        title="Project ID",
    )
    restrictions: Optional[str] = Field(
        None,
        description="Detail any restrictions on publishing or sharing these data",
        title="Restrictions",
    )
    _label: str = PrivateAttr()

    def __init__(self, label=None, **kwargs):
        """Construct a generic data description"""
        super().__init__(_label=label, **kwargs)

    @root_validator(pre=True)
    def build_fields(cls, values):
        """build name"""
        values["name"] = build_data_name(
            label=values["_label"],
            creation_date=values["creation_date"],
            creation_time=values["creation_time"],
        )
        return values

    @classmethod
    def from_name(cls, name, **kwargs):
        """construct a DataDescription from a name string"""
        m = re.match(f"{DataRegex.DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return cls(
            label=m.group("label"),
            creation_date=creation_date,
            creation_time=creation_time,
            **kwargs,
        )


class DerivedDataDescription(DataDescription):
    """A logical collection of data files derived via processing"""

    input_data: DataDescription
    process_name: str

    @root_validator(pre=True)
    def build_fields(cls, values):
        """build name, process_name, and data_level fields"""

        d = values["input_data"]
        name = (
            build_data_name(d.process_name, d.creation_date, d.creation_time)
            if isinstance(d, DerivedDataDescription)
            else d.name
        )
        process_name = values["process_name"]
        values["name"] = build_data_name(
            label=f"{name}_{process_name}",
            creation_date=values["creation_date"],
            creation_time=values["creation_time"],
        )
        values["data_level"] = DataLevel.DERIVED_DATA
        return values

    @classmethod
    def from_name(cls, name, **kwargs):
        """build DerivedDataDescription from a name"""

        # look for input data name
        m = re.match(f"{DataRegex.DERIVED_DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        # data asset with inputs
        input_data = DataDescription.from_name(
            m.group("input"), data_level=DataLevel.DERIVED_DATA, **kwargs
        )

        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return cls(
            process_name=m.group("process_name"),
            creation_date=creation_date,
            creation_time=creation_time,
            input_data=input_data,
            **kwargs,
        )


class RawDataDescription(DataDescription):
    """A logical collection of data files as acquired from a rig or instrument"""

    modality: str = Field(
        ...,
        regex=DataRegex.NO_UNDERSCORES.value,
        description="A short name for the specific manner, characteristic, pattern of application, or the employment of any technology or formal procedure to generate data for a study",
        title="Modality",
    )
    subject_id: str = Field(
        ...,
        regex=DataRegex.NO_UNDERSCORES.value,
        description="Unique identifier for the subject of data acquisition",
    )

    @root_validator(pre=True)
    def build_fields(cls, values):
        """compute the label, name, and data_level fields"""
        values["name"] = build_data_name(
            label=f'{values["modality"]}_{values["subject_id"]}',
            creation_date=values["creation_date"],
            creation_time=values["creation_time"],
        )
        values["data_level"] = DataLevel.RAW_DATA
        return values

    @classmethod
    def from_name(cls, name, **kwargs):
        """construct from a name string"""

        m = re.match(f"{DataRegex.RAW_DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return cls(
            modality=m.group("modality"),
            subject_id=m.group("subject_id"),
            creation_date=creation_date,
            creation_time=creation_time,
            **kwargs,
        )
