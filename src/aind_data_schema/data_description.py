""" Generic metadata classes for data """

from __future__ import annotations

import re
from datetime import date, datetime, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class RegexParts(Enum):
    """regular expression components to be re-used elsewhere"""

    DATE = r"\d{4}-\d{2}-\d{2}"
    TIME = r"\d{2}-\d{2}-\d{2}"


class DataRegex(Enum):
    """regular expression patterns for different kinds of data and their properties"""

    DATA = f"^(?P<label>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})$"
    RAW_DATA = f"^(?P<modality>.+?)_(?P<subject_id>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})$"
    DERIVED_DATA = f"^(?P<input>.+?_{RegexParts.DATE.value}_{RegexParts.TIME.value})_(?P<label>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})"
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


class DataDescription(BaseModel):
    """Description of a logical collection of data files"""

    schema_version: str = Field("0.1.0", title="Schema Version", const=True)
    license: str = Field("CC-BY-4.0", title="License", const=True)
    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/aind-data-schema/blob/main/schemas/data_description.py",
        title="Described by",
        const=True,
    )

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
    label: str = Field(
        ...,
        description="Label describing provenance of data",
        title="Label",
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

    @root_validator(pre=True)
    def build_fields(cls, values):
        """construct the name field"""
        dt_str = datetime_to_name_string(
            values["creation_date"], values["creation_time"]
        )
        values["name"] = f'{values["label"]}_{dt_str}'
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

    processed_name: Optional[str]

    @root_validator(pre=True)
    def build_fields(cls, values):
        """build name, process_name, and data_level fields"""

        dt_str = datetime_to_name_string(
            values["creation_date"], values["creation_time"]
        )
        d = values["input_data"]
        name = (
            d.processed_name
            if isinstance(d, DerivedDataDescription)
            else d.name
        )
        values["name"] = f'{name}_{values["label"]}_{dt_str}'
        values["processed_name"] = f'{values["label"]}_{dt_str}'
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

        label = m.group("label")
        creation_date, creation_time = datetime_from_name_string(
            m.group("c_date"), m.group("c_time")
        )

        return cls(
            label=label,
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

        dt_str = datetime_to_name_string(
            values["creation_date"], values["creation_time"]
        )
        values["label"] = f'{values["modality"]}_{values["subject_id"]}'
        values["name"] = f'{values["label"]}_{dt_str}'
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
