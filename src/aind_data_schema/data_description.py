""" Generic metadata classes for data """

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum, EnumMeta
from typing import Any, List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel, BaseName, BaseNameEnumMeta, PIDName, Registry


class RegexParts(Enum):
    """regular expression components to be re-used elsewhere"""

    DATE = r"\d{4}-\d{2}-\d{2}"
    TIME = r"\d{2}-\d{2}-\d{2}"


class DataRegex(Enum):
    """regular expression patterns for different kinds of data and their properties"""

    DATA = f"^(?P<label>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})$"
    RAW = (
        f"^(?P<platform_abbreviation>.+?)_(?P<subject_id>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>"
        f"{RegexParts.TIME.value})$"
    )
    DERIVED = (
        f"^(?P<input>.+?_{RegexParts.DATE.value}_{RegexParts.TIME.value})_(?P<process_name>.+?)_(?P<c_date>"
        f"{RegexParts.DATE.value})_(?P<c_time>{RegexParts.TIME.value})"
    )
    NO_UNDERSCORES = "^[^_]+$"


class DataLevel(Enum):
    """Data level name"""

    DERIVED = "derived"
    RAW = "raw"


class Institution(Enum, metaclass=BaseNameEnumMeta):
    """Institution name"""

    AI = PIDName(
        name="Allen Institute",
        abbreviation="AI",
        registry=Registry.ROR,
        registry_identifier="03cpe7c52",
    )
    AIBS = PIDName(
        name="Allen Institute for Brain Science",
        abbreviation="AIBS",
        registry=Registry.ROR,
        registry_identifier="00dcv1019",
    )
    AIND = PIDName(
        name="Allen Institute for Neural Dynamics",
        abbreviation="AIND",
        registry=Registry.ROR,
        registry_identifier="04szwah67",
    )
    COLUMBIA = PIDName(
        name="Columbia University",
        abbreviation="Columbia",
        registry=Registry.ROR,
        registry_identifier="00hj8s172",
    )
    JAX = PIDName(name="Jackson Laboratory", abbreviation="JAX", registry=Registry.ROR, registry_identifier="021sy4w91")
    HUST = PIDName(
        name="Huazhong University of Science and Technology",
        abbreviation="HUST",
        registry=Registry.ROR,
        registry_identifier="00p991c53",
    )
    NINDS = PIDName(
        name="National Institute of Neurological Disorders and Stroke",
        abbreviation="NINDS",
        registry=Registry.ROR,
        registry_identifier="01s5ya894",
    )
    NYU = PIDName(
        name="New York University",
        abbreviation="NYU",
        registry=Registry.ROR,
        registry_identifier="0190ak572",
    )
    SIMONS = PIDName(
        name="Simons Foundation",
        registry=Registry.ROR,
        registry_identifier="01cmst727",
    )


class Group(Enum):
    """Data collection group name"""

    BEHAVIOR = "behavior"
    EPHYS = "ephys"
    MSMA = "MSMA"
    OPHYS = "ophys"


class AbbreviationEnumMeta(EnumMeta):
    """Allows to create complicated enum based on abbreviation."""

    def __call__(cls, value, *args, **kw):
        """Allow enum to be set by a string."""
        if isinstance(value, str):
            abbr = {member.value.abbreviation: member for member in cls}
            if abbr.get(value) is None:
                value = getattr(cls, value.upper())
            else:
                value = abbr[value]
        return super().__call__(value, *args, **kw)

    def __modify_schema__(cls, field_schema):
        """Adds enumNames to schema"""
        field_schema.update(
            enumNames=[e.value.name for e in cls],
        )


class Modality(Enum, metaclass=AbbreviationEnumMeta):
    """Data collection modality name"""

    BEHAVIOR_VIDEOS = BaseName(name="Behavior videos", abbreviation="behavior-videos")
    CONFOCAL = BaseName(name="Confocal microscopy", abbreviation="confocal")
    ECEPHYS = BaseName(name="Extracellular electrophysiology", abbreviation="ecephys")
    FMOST = BaseName(name="Fluorescence micro-optical sectioning tomography", abbreviation="fMOST")
    ICEPHYS = BaseName(name="Intracellular electrophysiology", abbreviation="icephys")
    FIB = BaseName(name="Fiber photometry", abbreviation="fib")
    MERFISH = BaseName(
        name="Multiplexed error-robust fluorescence in situ hybridization",
        abbreviation="merfish",
    )
    MRI = BaseName(name="Magnetic resonance imaging", abbreviation="MRI")
    POPHYS = BaseName(name="Planar optical physiology", abbreviation="ophys")
    SLAP = BaseName(name="Scanned line projection imaging", abbreviation="slap")
    SPIM = BaseName(name="Selective plane illumination microscopy", abbreviation="SPIM")
    TRAINED_BEHAVIOR = BaseName(name="Trained behavior", abbreviation="trained-behavior")


class Platform(Enum, metaclass=AbbreviationEnumMeta):
    """Name for standardized data collection system that can collect one or more data modalities."""

    BEHAVIOR = BaseName(name="Behavior platform", abbreviation="behavior")
    CONFOCAL = BaseName(name="Confocal microscopy platform", abbreviation="confocal")
    ECEPHYS = BaseName(name="Electrophysiology platform", abbreviation="ecephys")
    EXASPIM = BaseName(name="ExaSPIM platform", abbreviation="exaSPIM")
    FIP = BaseName(name="Frame-projected independent-fiber photometry platform", abbreviation="FIP")
    HCR = BaseName(name="Hybridization chain reaction platform", abbreviation="HCR")
    HSFP = BaseName(name="Hyperspectral fiber photometry platform", abbreviation="HSFP")
    MESOSPM = BaseName(name="MesoSPIM platform", abbreviation="mesoSPIM")
    MERFISH = BaseName(name="MERFISH platform", abbreviation="MERFISH")
    MRI = BaseName(name="Magnetic resonance imaging platform", abbreviation="MRI")
    MULTIPLANE_OPHYS = BaseName(name="Multiplane optical physiology platform", abbreviation="multiplane-ophys")
    SINGLE_PLANE_OPHYS = BaseName(name="Single-plane optical physiology platform", abbreviation="single-plane-ophys")
    SLAP2 = BaseName(name="SLAP2 platform", abbreviation="SLAP2")
    SMARTSPIM = BaseName(name="SmartSPIM platform", abbreviation="SmartSPIM")


def datetime_to_name_string(dt):
    """Take a date and time object, format it a as string"""
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def datetime_from_name_string(d, t):
    """Take date and time strings, generate date and time objects"""
    d = datetime.strptime(d, "%Y-%m-%d").date()
    t = datetime.strptime(t, "%H-%M-%S").time()
    return datetime.combine(d, t)


def build_data_name(label, creation_datetime):
    """Construct a valid data description name"""
    dt_str = datetime_to_name_string(creation_datetime)
    return f"{label}_{dt_str}"


class Funding(AindModel):
    """Description of funding sources"""

    funder: Institution = Field(..., title="Funder")
    grant_number: Optional[str] = Field(None, title="Grant number")
    fundee: Optional[str] = Field(None, title="Fundee", description="Person(s) funded by this mechanism")


class RelatedData(AindModel):
    """Description of related data asset"""

    related_data_path: str = Field(..., title="Related data path")
    relation: str = Field(..., title="Relation", description="Relation of data to this asset")


class DataDescription(AindCoreModel):
    """Description of a logical collection of data files"""

    schema_version: str = Field("0.10.1", title="Schema Version", const=True)
    license: str = Field("CC-BY-4.0", title="License", const=True)

    creation_time: datetime = Field(
        ...,
        description="Time that data files were created, used to uniquely identify the data",
        title="Creation Time",
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

    funding_source: List[Funding] = Field(
        ...,
        title="Funding source",
        description="Funding source. If internal funding, select 'Allen Institute'",
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
        [],
        description="Full name(s) of key investigators (e.g. PI, lead scientist, contact person)",
        title="Investigators",
    )
    platform: Platform = Field(
        ...,
        description="Name for a standardized primary data collection system",
        title="Platform",
    )
    project_name: Optional[str] = Field(
        None,
        description="A name for a set of coordinated activities intended to achieve one or more objectives.",
        title="Project Name",
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
                creation_datetime=self.creation_time,
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


class DerivedDataDescription(DataDescription):
    """A logical collection of data files derived via processing"""

    input_data_name: str
    data_level: DataLevel = Field(
        DataLevel.DERIVED,
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
        m = re.match(f"{DataRegex.DERIVED.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        return dict(
            process_name=m.group("process_name"),
            creation_time=creation_time,
            input_data_name=m.group("input"),
        )

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
                return getattr(DerivedDataDescription.__fields__.get(field_name), "default")

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

    data_level: DataLevel = Field(
        DataLevel.RAW,
        description="level of processing that data has undergone",
        title="Data Level",
        const=True,
    )

    def __init__(self, platform, subject_id, **kwargs):
        """Construct a raw data description"""

        if isinstance(platform, dict):
            platform_abbreviation = platform.get("abbreviation")
        else:
            platform_abbreviation = platform.value.abbreviation

        super().__init__(
            label=f"{platform_abbreviation}_{subject_id}",
            platform=platform,
            subject_id=subject_id,
            **kwargs,
        )

    @classmethod
    def parse_name(cls, name):
        """Decompose raw description name into component parts"""

        m = re.match(f"{DataRegex.RAW.value}", name)

        if m is None:
            raise ValueError(f"name({name}) does not match pattern")

        creation_time = datetime_from_name_string(m.group("c_date"), m.group("c_time"))

        platform_abbreviation = m.group("platform_abbreviation")
        platform = Platform(platform_abbreviation)

        return dict(
            platform=platform,
            subject_id=m.group("subject_id"),
            creation_time=creation_time,
        )
