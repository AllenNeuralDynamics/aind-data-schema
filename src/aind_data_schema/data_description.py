""" Generic metadata classes for data """

from __future__ import annotations

import re
from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

from pydantic import Field

from .base import AindCoreModel, AindModel


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


class Funding(AindModel):
    """Description of funding sources"""

    funder: str = Field(..., title="Funder")
    grant_number: Optional[str] = Field(None, title="Grant number")
    fundee: Optional[str] = Field(
        None, title="Fundee", description="Person(s) funded by this mechanism"
    )


class DataDescription(AindCoreModel):
    """Description of a logical collection of data files"""

    schema_version: str = Field("0.3.0", title="Schema Version", const=True)
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

    def __init__(self, label, **kwargs):
        """Construct a generic data description"""
        name = build_data_name(
            label=label,
            creation_date=kwargs["creation_date"],
            creation_time=kwargs["creation_time"],
        )

        super().__init__(name=name, **kwargs)

    @classmethod
    def parse_name(cls, name):
        """Decompose a DataDescription name string into component parts"""
        m = re.match(f"{DataRegex.DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return dict(
            label=m.group("label"),
            creation_date=creation_date,
            creation_time=creation_time,
        )

    @classmethod
    def from_name(cls, name, **kwargs):
        """construct a DataDescription from a name string"""
        d = cls.parse_name(name)

        return cls(**d, **kwargs)


class DerivedDataDescription(DataDescription):
    """A logical collection of data files derived via processing"""

    input_data_name: str
    data_level: DataLevel = Field(
        DataLevel.DERIVED_DATA,
        description="level of processing that data has undergone",
        title="Data Level",
        const=True,
    )

    def __init__(self, process_name, **kwargs):
        """Construct a derived data description"""
        input_data_name = kwargs["input_data_name"]
        super().__init__(label=f"{input_data_name}_{process_name}", **kwargs)

    @classmethod
    def parse_name(cls, name):
        """decompose DerivedDataDescription name into parts"""

        # look for input data name
        m = re.match(f"{DataRegex.DERIVED_DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return dict(
            process_name=m.group("process_name"),
            creation_date=creation_date,
            creation_time=creation_time,
            input_data_name=m.group("input"),
        )

    @classmethod
    def from_name(cls, name, **kwargs):
        """build DerivedDataDescription from a name"""

        d = cls.parse_name(name)

        return cls(**d, **kwargs)

    @classmethod
    def from_data_description(cls, input_data, process_name, **kwargs):
        """Build a DerivedDataDescription from an input DataDescription"""

        if input_data.data_level == DataLevel.DERIVED_DATA:
            name_len = len(input_data.input_data_name) + 1
            input_data_name = input_data.name[name_len:]
        else:
            input_data_name = input_data.name

        return cls(
            input_data_name=input_data_name,
            process_name=process_name,
            subject_id=input_data.subject_id,
            modality=input_data.modality,
            **kwargs,
        )


class RawDataDescription(DataDescription):
    """A logical collection of data files as acquired from a rig or instrument"""

    data_level: DataLevel = Field(
        DataLevel.RAW_DATA,
        description="level of processing that data has undergone",
        title="Data Level",
        const=True,
    )

    def __init__(self, **kwargs):
        """Construct a raw data description"""
        modality = kwargs["modality"]
        subject_id = kwargs["subject_id"]
        super().__init__(label=f"{modality}_{subject_id}", **kwargs)

    @classmethod
    def parse_name(cls, name):
        """Decompose raw data description name into component parts"""

        m = re.match(f"{DataRegex.RAW_DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return dict(
            modality=m.group("modality"),
            subject_id=m.group("subject_id"),
            creation_date=creation_date,
            creation_time=creation_time,
        )

    @classmethod
    def from_name(cls, name, **kwargs):
        """construct from a name string"""

        d = cls.parse_name(name)

        return cls(**d, **kwargs)
