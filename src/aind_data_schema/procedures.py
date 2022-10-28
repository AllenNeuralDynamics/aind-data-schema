""" schema for various Procedures """

from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class ProtectiveMaterial(Enum):
    """material applied post-craniotomy"""

    DURAGEL = "Duragel"
    SORTA_CLEAR = "SORTA-clear"
    KWIK_CAST = "Kwik-Cast"
    OTHER = "Other - see notes"

class Procedure(BaseModel):
    """basic procedure description"""

    type: Optional[str] = Field(
        None, description="Generic device type", title="Procedure"
    )
    date: date = Field(..., title="Date")
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    protocol_id: str = Field(..., title="Protocol ID")
    animal_weight: Optional[float]=Field(None, title="Animal weight (g)")
    notes: Optional[str] = Field(None, title="Notes")

class Craniotomy(Procedure):
    """description of the craniotomy"""

    craniotomy_coordinates_ml: float = Field(
        ..., title="Craniotomy coordinate ML (mm)", units="mm"
    )
    craniotomy_coordinates_ap: float = Field(
        ..., title="Craniotomy coordinates AP (mm)", units="mm"
    )
    craniotomy_size: float = Field(
        ..., title="Craniotomy size (mm)", units="mm"
    )
    implant_part_number: Optional[str] = Field(
        None, title="Implant part number"
    )
    dura_removed: Optional[bool] = Field(None, title="Dura removed")
    protective_material: Optional[ProtectiveMaterial] = Field(
        None, title="Protective material"
    )

class HeadframeMaterial(Enum):
    """headframe materials"""

    TITANIUM = "Titanium"
    STEEL = "Steel"


class Headframe(Procedure):
    """description of headframe procedure"""

    headframe_part_number: str = Field(..., title="Headframe part number")
    headframe_material: HeadframeMaterial = Field(
        ..., title="Headframe material"
    )
    well_part_number: Optional[str] = Field(None, title="Well part number")
    well_type: Optional[str] = Field(None, title="Well type")


class InjectionHemisphere(Enum):
    """brain hemisphere targeted by injection"""

    LEFT = "left"
    RIGHT = "right"


class NanojectInjection(BaseModel):
    """description of nanoject injection"""

    injection_type: str = Field("Nanoject", title="Injection type", const=True)
    injection_volume: float = Field(
        ..., title="Injection volume (nL)", units="nL"
    )


class IontophoresisInjection(BaseModel):
    """description of nanoject injection"""

    injection_type: str = Field(
        "Iontophoresis", title="Injection type", const=True
    )
    injection_current: float = Field(
        ..., title="Injection current (μA)", units="μA"
    )
    alternating_current: str = Field(..., title="Alternating current")


class Injection(Procedure):
    """general description of injection procedure"""

    injection_hemisphere: Optional[InjectionHemisphere] = Field(
        None, title="Injection hemisphere"
    )
    injection_coordinate_ml: float = Field(
        ..., title="Injection coordinate ML (mm)"
    )
    injection_coordinate_ap: float = Field(
        ..., title="Injection coordinate AP (mm)"
    )
    injection_coordinate_depth: float = Field(
        ..., title="Injection coodinate depth (mm)"
    )
    injection_angle: float = Field(
        ..., title="Injection angle (deg)", units="deg"
    )
    injection_virus: str = Field(..., title="Injection virus")
    injection_virus_id: Optional[str] = Field(None, title="Injection virus ID")
    injection_duration: time = Field(..., title="Injection duration")
    injection_class: Union[NanojectInjection, IontophoresisInjection]


class MriScanSequence(Enum):
    """MRI scan sequence"""

    RARE = "RARE"


class ScannerLocation(Enum):
    """location of scanner"""

    UW_SLU = "UW SLU"
    FRED_HUTCH = "Fred Hutch"


class MagneticStrength(Enum):
    """strength of magnet"""

    MRI_7T = 7
    MRI_14T = 14


class MriScan(Procedure):
    """information about MRI scan"""

    scan_sequence: MriScanSequence = Field(..., title="Scan sequence")
    scanner_location: Optional[ScannerLocation] = Field(
        None, title="Scanner location"
    )
    magnetic_strength: Optional[MagneticStrength] = Field(
        None, title="Magnetic strength (T)", units="T"
    )
    resolution: float = Field(..., title="Resolution")
    protocol_id: str = Field(..., title="Protocol ID")


class TissuePrepName(Enum):
    """type of tissue prep"""

    PERFUSION = "Perfusion"
    FIXATION = "Fixation"
    DOUBLE_DELIPIDATION = "Double delipidation"
    DCM_DELIPIDATION = "DCM delipidation"
    IMMUNOSTAINING = "Immunostaining"
    GELATION = "Gelation"


class TissuePrep(BaseModel):
    """information about tissue prep procedure"""

    name: TissuePrepName = Field(..., title="Name")
    date_started: date = Field(..., title="Date-time procedure started")
    date_ended: date = Field(None, title="Date-time procedure ended")
    experimenter_full_name: str = Field(
        None,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    protocol_id: str = Field(..., title="Protocol ID")
    notes: Optional[str] = None


class TrainingProtocol(BaseModel):
    """information about training procedures"""

    protocol_id: str = Field(..., title="Training protocol ID")
    training_protocol_start_date: date = Field(
        ..., title="Training protocol start date"
    )
    training_protocol_end_date: Optional[date] = Field(
        None, title="Training protocol end date"
    )
    notes: Optional[str] = Field(None, title="Notes")


class ProbeName(Enum):
    """name of probe"""

    PROBE_A = "Probe A"
    PROBE_B = "Probe B"
    PROBE_C = "Probe C"


class FerruleMaterial(Enum):
    """probe material"""

    CERAMIC = "Ceramic"
    STAINLESS_STEEL = "Stainless steel"


class Probe(BaseModel):
    """description of probe"""

    name: ProbeName = Field(..., title="Name")
    manufacturer: str = Field(..., title="Manufacturer")
    part_number: str = Field(..., title="Part number")
    core_diameter: float = Field(..., title="Core diameter (μm)", units="μm")
    numerical_aperture: float = Field(..., title="Numerical aperture")
    ferrule_material: Optional[FerruleMaterial] = Field(
        None, title="Ferrule material"
    )
    targeted_structure: str = Field(..., title="Targeted structure")
    stereotactic_coordinate_ap: float = Field(
        ..., title="Stereotactic coordinate A/P (mm)", units="mm"
    )
    stereotactic_coordinate_ml: float = Field(
        ..., title="Stereotactic coodinate M/L (mm)", units="mm"
    )
    stereotactic_coordinate_dv: float = Field(
        ..., title="Stereotactic coordinate D/V (mm)", units="mm"
    )
    angle: float = Field(..., title="Angle (deg)", units="deg")
    notes: Optional[str] = Field(None, title="Notes")


class Implant(Procedure):
    """description of implant procedure"""

    probes: List[Probe] = Field(..., title="Probes", unique_items=True)


class WaterRestriction(BaseModel):
    """description of water restriction procedure"""

    protocol_id: Optional[str] = Field(
        None, title="Water restriction protocol number"
    )
    baseline_weight: float = Field(..., title="Baseline weight (g)", description="Weight at start of water restriction")
    start_date: date = Field(
        ..., title="Water restriction start date"
    )
    end_date: date = Field(..., title="Water restriction end date")


class Procedures(BaseModel):
    """description of all procedures applied to subject"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/aind-data-schema/blob/main/src/aind-data-schema/procedures.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field(
        "0.3.1", description="schema version", title="Version", const=True
    )
    specimen_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Specimen ID",
    )
    headframes: Optional[List[Headframe]] = Field(
        None, title="Headframes", unique_items=True
    )
    craniotomies: Optional[List[Craniotomy]] = Field(
        None, title="Craniotomies", unique_items=True
    )
    mri_scans: Optional[List[MriScan]] = Field(
        None, title="MRI scans", unique_items=True
    )
    injections: Optional[List[Injection]] = Field(
        None, title="Injections", unique_items=True
    )
    fiber_implants: Optional[List[Implant]] = Field(
        None, title="Fiber implants", unique_items=True
    )
    water_restriction: Optional[WaterRestriction] = Field(
        None, title="Water restriction"
    )
    training_protocols: Optional[List[TrainingProtocol]] = Field(
        None, title="Training protocols", unique_items=True
    )
    tissue_preparations: Optional[List[TissuePrep]] = Field(
        None, title="Tissue preparations", unique_items=True
    )
    notes: Optional[str] = Field(None, title="Notes")
