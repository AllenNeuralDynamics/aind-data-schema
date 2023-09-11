""" Generic metadata classes for data """

from __future__ import annotations

import re
from datetime import date, datetime, time
from enum import Enum
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
    RAW_DATA = (
        f"^(?P<project_abbreviation>.+?)_(?P<subject_id>.+?)_(?P<c_date>{RegexParts.DATE.value})_(?P<c_time>"
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


class Modality(Enum, metaclass=BaseNameEnumMeta):
    """Data collection modality name"""

    BEHAVIOR_VIDEOS = BaseName(name="Behavior videos", abbreviation="behavior-videos")
    CONFOCAL = BaseName(name="Confocal microscopy", abbreviation="confocal")
    DISPIM = BaseName(
        name="Dual inverted selective plane illumination microscopy",
        abbreviation="diSPIM",
    )
    ECEPHYS = BaseName(name="Extracellular electrophysiology", abbreviation="ecephys")
    EPHYS = BaseName(name="Electrophysiology", abbreviation="ephys")
    EXASPIM = BaseName(
        name="Expansion-assisted selective plane illumination microscopy",
        abbreviation="exaSPIM",
    )
    FIP = BaseName(name="Frame-projected independent-fiber photometry", abbreviation="FIP")
    FMOST = BaseName(name="Fluorescence micro-optical sectioning tomography", abbreviation="fMOST")
    HSFP = BaseName(name="Hyperspectral fiber photometry", abbreviation="HSFP")
    ICEPHYS = BaseName(name="Intracellular electrophysiology", abbreviation="icephys")
    FIB = BaseName(name="Fiber photometry", abbreviation="fib")
    FISH = BaseName(name="Fluorescence in situ hybridization", abbreviation="fish")
    MESOSPIM = BaseName(
        name="Mesoscale selective plane illumination microscopy",
        abbreviation="mesoSPIM",
    )
    MERFISH = BaseName(
        name="Multiplexed error-robust fluorescence in situ hybridization",
        abbreviation="merfish",
    )
    MPOPHYS = BaseName(name="Multiplane optical physiology", abbreviation="multiplane-ophys")
    MRI = BaseName(name="Magnetic resonance imaging", abbreviation="MRI")
    OPHYS = BaseName(name="Optical physiology", abbreviation="ophys")
    SLAP = BaseName(name="Scanned line projection", abbreviation="slap")
    SMARTSPIM = BaseName(name="Smart selective plane illumination microscopy", abbreviation="SmartSPIM")
    SPIM = BaseName(name="Selective plane illumination microscopy", abbreviation="SPIM")
    SPOPHYS = BaseName(name="Single plane optical physiology", abbreviation="single-plane-ophys")
    TRAINED_BEHAVIOR = BaseName(name="Trained behavior", abbreviation="trained-behavior")


class ExperimentType(Enum):
    """Abbreviated name for data collection technique. This is deprecated and will be removed in a future version."""

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
    MPOPHYS = Modality.MPOPHYS.value.abbreviation
    SLAP = Modality.SLAP.value.abbreviation
    SMARTSPIM = Modality.SMARTSPIM.value.abbreviation
    SPOPHYS = Modality.SPOPHYS.value.abbreviation
    TRAINED_BEHAVIOR = Modality.TRAINED_BEHAVIOR.value.abbreviation
    OTHER = "Other"


class Project(Enum, metaclass=BaseNameEnumMeta):
    ECEPHYS = BaseName(name="Electrophysiology Platform Development", abbreviation="ecephys-dev")
    SLAP2 = BaseName(name="SLAP2 Platform Development", abbreviation="slap2-dev")
    BEHAVIOR = BaseName(name="Behavior Platform Development", abbreviation="behavior-dev")
    MMOD = BaseName(name="Multiplexed Neuromodulation", abbreviation="mmod")
    CTLUT = BaseName(name="Cell Type Lookup Table", abbreviation="ctlut")
    OITEST = BaseName(name="Optical physiology indicator testing", abbreviation="oitest")
    ACTVAL = BaseName(name="Converting value into action", abbreviation="actval")
    COGFLEX = BaseName(name="Cognitive flexibility in patch foraging", abbreviation="cogflex")
    BCI = BaseName(name="Brain computer interface", abbreviation="bci")
    NEFUNC = BaseName(name="Test function differences of NE neurons", abbreviation="nefunc")
    NMSYS = BaseName(name="Molecular and projection-defined diversity of neuromodulator systems", abbreviation="nmsys")
    NMDYN = BaseName(name="Neuromodulation dynamics", abbreviation="nmdyn")
    DISCNM = BaseName(name="Discovery - Neuromodulation", abbreviation="disc-nm")
    DISCBWD = BaseName(name="Discovery - Brain wide dynamics", abbreviation="disc-bwd")
    TIM1 = BaseName(name="AIND Thalamus U19 - Project 1", abbreviation="tim1")
    TIM2 = BaseName(name="AIND Thalamus U19 - Project 2", abbreviation="tim2")
    TIM4 = BaseName(name="AIND Thalamus U19 - Project 4", abbreviation="tim4")
    # 122-01-002-20 - AIND Thalamus U19 - DSC
    TIMMC = BaseName(name="AIND Thalamus U19 - Molecular core", abbreviation="timmc")
    EXASPIM = BaseName(name="Neural Dynamics - Glaser R00", abbreviation="exaspim-dev")
    # 122-01-005-10 - AIND Svoboda DeepMind Collab
    BRAINSTEM = BaseName(name="AIND Brainstem RF1", abbreviation="brainstem")
    HSFP = BaseName(name="AIND Hagihara HFSP", abbreviation="hsfp")
    # 122-01-007-10 - AIND Svoboda HHMI
    # 122-01-008-10 - AIND CZI Acquisition Software
    # 122-01-009-10 - AIND Kaspar MBF
    # 122-01-009-20 - AIND Amarante F32
    # 122-01-010-20 - AIND Poo Simons BTI
    # 122-01-011-20 - AIND Cohen JHU R01 Transferred Subaward
    # 122-01-012-20 AIND RF1 Functions of locus coeruleus
    # 102-01-040-20 - CTY BRAIN UG3/UH3 Genetic Viral Tools
    # 102-01-057-20 - CTY BRAIN BG AAV Toolbox
    GENTOOLS = BaseName(name="Cell Type Genetic Tools", abbreviation="gentools")
    # 102-01-002-20 - TH Grant - Task Molecular Core
    # 102-04-007-10 - CTY Targeted CNS Gene Therapy
    # 102-04-009-10 - Task:Dravet
    # 121-01-025-20 - U01 Bridging Func & Morph
    LMFISH = BaseName(name="Learning & mFISH", abbreviation="lmfish")
    V1OMFISH = BaseName(name="v1omFISH", abbreviation="v1omfish")


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

    funder: Institution = Field(..., title="Funder")
    grant_number: Optional[str] = Field(None, title="Grant number")
    fundee: Optional[str] = Field(None, title="Fundee", description="Person(s) funded by this mechanism")


class RelatedData(AindModel):
    """Description of related data asset"""

    related_data_path: str = Field(..., title="Related data path")
    relation: str = Field(..., title="Relation", description="Relation of data to this asset")


class DataDescription(AindCoreModel):
    """Description of a logical collection of data files"""

    schema_version: str = Field("0.8.0", title="Schema Version", const=True)
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
    project: Project = Field(
        ..., description="A set of coordinated activities intended to achieve one or more objectives", title="Project"
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

    # deprecated fields
    experiment_type: ExperimentType = Field(
        None,
        description="An abbreviated name for the experimental technique used to collect this data. This is DEPRECATED and will be removed in a future version.",
        title="Experiment Type",
    )
    project_name: Optional[str] = Field(
        None,
        description="A name for a set of coordinated activities intended to achieve one or more objectives. This is DEPRECATED and will be removed in a future version.",
        title="Project Name",
    )
    project_id: Optional[str] = Field(
        None,
        description="A database or other identifier for a project. This is DEPRECATED and will be removed in a future version.",
        title="Project ID",
    )

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

        utcnow = datetime.utcnow()
        creation_time = utcnow.time() if kwargs.get("creation_time") is None else kwargs["creation_time"]
        creation_date = utcnow.date() if kwargs.get("creation_date") is None else kwargs["creation_date"]

        return cls(
            creation_time=creation_time,
            creation_date=creation_date,
            process_name=process_name,
            institution=get_or_default("institution"),
            funding_source=get_or_default("funding_source"),
            group=get_or_default("group"),
            investigators=get_or_default("investigators"),
            project=get_or_default("project"),
            restrictions=get_or_default("restrictions"),
            modality=get_or_default("modality"),
            subject_id=get_or_default("subject_id"),
            related_data=get_or_default("related_data"),
            data_summary=get_or_default("data_summary"),
            input_data_name=data_description.name,
            # deprecated fields
            project_name=get_or_default("project_name"),
            project_id=get_or_default("project_id"),
            experiment_type=get_or_default("experiment_type"),
        )


class RawDataDescription(DataDescription):
    """A logical collection of data files as acquired from a rig or instrument"""

    data_level: DataLevel = Field(
        DataLevel.RAW_DATA,
        description="level of processing that data has undergone",
        title="Data Level",
        const=True,
    )

    def __init__(self, project_abbreviation, subject_id, **kwargs):
        """Construct a raw data description"""

        project = None
        for p in Project:
            if p.value.abbreviation == project_abbreviation:
                project = p

        super().__init__(
            label=f"{project.value.abbreviation}_{subject_id}",
            project=project,
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
            project_abbreviation=m.group("project_abbreviation"),
            subject_id=m.group("subject_id"),
            creation_date=creation_date,
            creation_time=creation_time,
        )
