""" Generic metadata classes for data """

from __future__ import annotations

import re
from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

from pydantic import Field

from .base import AindCoreModel, AindModel, BaseName, BaseNameEnumMeta


class RegexParts(Enum):
    """regular expression components to be re-used elsewhere"""

    DATE = r"\d{4}-\d{2}-\d{2}"
    TIME = r"\d{2}-\d{2}-\d{2}"


class DataRegex(Enum):
    """regular expression patterns for different kinds of data and their properties"""

    DATA = f"^(?P<label>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})$"
    RAW_DATA = (
        f"^(?P<experiment_type>.+?)_(?P<subject_id>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>"
        f"{RegexParts.TIME.value})$"
    )
    DERIVED_DATA = (
        f"^(?P<input>.+?_{RegexParts.DATE.value}_{RegexParts.TIME.value})_(?P<process_name>.+?)_(?P<c_date>"
        f"{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})"
    )
    NO_UNDERSCORES = "^[^_]+$"


class DataLevel(Enum):
    """Data level name"""

    DERIVED_DATA = "derived data"
    RAW_DATA = "raw data"


class Institution(Enum, metaclass=BaseNameEnumMeta):
    """Institution name"""

    AIBS = BaseName(name="Allen Institute for Brain Science", abbreviation="AIBS")
    AIND = BaseName(name="Allen Institute for Neural Dynamics", abbreviation="AIND")
    COLUMBIA = BaseName(name="Columbia University", abbreviation="Columbia")
    HUST = BaseName(name="Huazhong University of Science and Technology", abbreviation="HUST")
    NYU = BaseName(name="New York University", abbreviation="NYU")

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Adds enumNames to institution"""
        field_schema.update(
            enumNames=[e.value.name for e in cls],
        )


class Group(Enum):
    """Data collection group name"""

    BEHAVIOR = "behavior"
    EPHYS = "ephys"
    MSMA = "MSMA"
    OPHYS = "ophys"


class Modality(Enum, metaclass=BaseNameEnumMeta):
    """Data collection modality name"""

    CONFOCAL = BaseName(name="Confocal microscopy", abbreviation="confocal")
    DISPIM = BaseName(name="Dual inverted selective plane illumination microscopy", abbreviation="diSPIM")
    ECEPHYS = BaseName(name="Extracellular electrophysiology", abbreviation="ecephys")
    EPHYS = BaseName(name="Electrophysiology", abbreviation="ephys")
    EXASPIM = BaseName(name="Expansion-assisted selective plane illumination microscopy", abbreviation="exaSPIM")
    FIP = BaseName(name="Frame-projected independent-fiber photometry", abbreviation="FIP")
    FMOST = BaseName(name="Fluorescence micro-optical sectioning tomography", abbreviation="fMOST")
    HSFP = BaseName(name="Hyperspectral fiber photometry", abbreviation="HSFP")
    ICEPHYS = BaseName(name="Intracellular electrophysiology", abbreviation="icephys")
    FIB = BaseName(name="Fiber photometry", abbreviation="fib")
    FISH = BaseName(name="Fluorescence in situ hybridization", abbreviation="fish")
    MESOSPIM = BaseName(name="Mesoscale selective plane illumination microscopy", abbreviation="mesoSPIM")
    MERFISH = BaseName(name="Multiplexed error-robust fluorescence in situ hybridization", abbreviation="merfish")
    MRI = BaseName(name="Magnetic resonance imaging", abbreviation="MRI")
    OPHYS = BaseName(name="Optical physiology", abbreviation="ophys")
    SMARTSPIM = BaseName(name="Smart selective plane illumination microscopy", abbreviation="SmartSPIM")
    SPIM = BaseName(name="Selective plane illumination microscopy", abbreviation="SPIM")

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Adds enumNames to modality"""
        field_schema.update(
            enumNames=[e.value.name for e in cls],
        )


class ExperimentType(Enum):
    """Abbreviated name for data collection technique"""

    ECEPHYS = Modality.ECEPHYS.value.abbreviation
    EXASPIM = Modality.EXASPIM.value.abbreviation
    CONFOCAL = Modality.CONFOCAL.value.abbreviation
    DISPIM = Modality.DISPIM.value.abbreviation
    FIP = Modality.FIP.value.abbreviation
    FMOST = Modality.FMOST.value.abbreviation
    HSFP = Modality.HSFP.value.abbreviation
    MESOSPIM = Modality.MESOSPIM.value.abbreviation
    MERFISH = Modality.MERFISH.value.abbreviation
    MRI = Modality.MRI.value.abbreviation
    SMARTSPIM = Modality.SMARTSPIM.value.abbreviation
    OTHER = "Other"


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
    fundee: Optional[str] = Field(None, title="Fundee", description="Person(s) funded by this mechanism")


class RelatedData(AindModel):
    """Description of related data asset"""

    related_data_path: str = Field(..., title="Related data path")
    relation: str = Field(..., title="Relation", description="Relation of data to this asset")


class DataDescription(AindCoreModel):
    """Description of a logical collection of data files"""

    schema_version: str = Field("0.6.2", title="Schema Version", const=True)
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
    name: Optional[str] = Field(
        None,
        description="Name of data, conventionally also the name of the directory containing all data and metadata",
        title="Name",
    )
    institution: Institution = Field(
        ...,
        description="An established society, corporation, foundation or other organization that collected this data",
        title="Institution",
    )
    ror_id: Optional[str] = Field(
        None,
        title="ROR ID",
        description="Institution ID from the Research Organization Registry",
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
    investigators: List[str] = Field(
        ...,
        description="Full name(s) of key investigators (e.g. PI, lead scientist, contact person)",
        title="Investigators",
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
    modality: List[Modality] = Field(
        ...,
        description="A short name for the specific manner, characteristic, pattern of application, or the employment"
        "of any technology or formal procedure to generate data for a study",
        title="Modality",
    )
    experiment_type: ExperimentType = Field(
        ...,
        description="An abbreviated name for the experimental technique used to collect this data",
        title="Experiment Type",
    )
    subject_id: str = Field(
        ...,
        regex=DataRegex.NO_UNDERSCORES.value,
        description="Unique identifier for the subject of data acquisition",
        title="Subject ID",
    )
    related_data: Optional[List[RelatedData]] = Field(
        [],
        title="Related data",
        description="Path and description of data assets associated with this asset (eg. reference images)",
    )
    data_summary: Optional[str] = Field(None, title="Data summary", description="Semantic summary of experimental goal")

    def __init__(self, label=None, **kwargs):
        """Construct a generic DataDescription"""

        super().__init__(**kwargs)

        if label is not None:
            self.name = build_data_name(
                label,
                creation_date=self.creation_date,
                creation_time=self.creation_time,
            )

    @classmethod
    def parse_name(cls, name):
        """Decompose a DataDescription name string into component parts"""
        m = re.match(f"{DataRegex.DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            label=m.group("label"),
            creation_date=creation_date,
            creation_time=creation_time,
        )


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

        creation_date, creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            process_name=m.group("process_name"),
            creation_date=creation_date,
            creation_time=creation_time,
            input_data_name=m.group("input"),
        )


class RawDataDescription(DataDescription):
    """A logical collection of data files as acquired from a rig or instrument"""

    data_level: DataLevel = Field(
        DataLevel.RAW_DATA,
        description="level of processing that data has undergone",
        title="Data Level",
        const=True,
    )

    def __init__(self, experiment_type, subject_id, **kwargs):
        """Construct a raw data description"""

        experiment_type = ExperimentType(experiment_type)

        super().__init__(
            label=f"{experiment_type.value}_{subject_id}",
            experiment_type=experiment_type,
            subject_id=subject_id,
            **kwargs,
        )

    @classmethod
    def parse_name(cls, name):
        """Decompose raw data description name into component parts"""

        m = re.match(f"{DataRegex.RAW_DATA.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_date, creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            experiment_type=m.group("experiment_type"),
            subject_id=m.group("subject_id"),
            creation_date=creation_date,
            creation_time=creation_time,
        )
