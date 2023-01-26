""" schema for various Procedures """

from datetime import date, time
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from .base import AindCoreModel, AindModel
from .device import AngleUnit, SizeUnit


class WeightUnit(Enum):
    """Weight units"""

    G = "gram"


class VolumeUnit(Enum):
    """Volume units"""

    NL = "nanoliter"


class CurrentUnit(Enum):
    """Current units"""

    UA = "microamps"


class Side(Enum):
    """Side of animal"""

    LEFT = "Left"
    RIGHT = "Right"


class ProtectiveMaterial(Enum):
    """Name of material applied to craniotomy"""

    DURAGEL = "Duragel"
    SORTA_CLEAR = "SORTA-clear"
    KWIK_CAST = "Kwik-Cast"
    OTHER = "Other - see notes"


class Anaesthetic(AindModel):
    """Description of an anaestheic"""

    type: str = Field(..., title="Type")
    duration: time = Field(..., title="Duration")
    level: float = Field(..., title="Level (percent)", units="percent", ge=1, le=5)


class Procedure(AindModel):
    """Description of surgical or other procedure performed on a subject"""

    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    animal_weight_prior: Optional[float] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
        units="g",
    )
    animal_weight_post: Optional[float] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
        units="g",
    )
    weight_unit: WeightUnit = Field(WeightUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(None, title="Anaesthesia")
    notes: Optional[str] = Field(None, title="Notes")


class CraniotomyType(Enum):
    """Name of craniotomy Type"""
    VISCTX = "Visual Cortex"
    WHC = "Whole hemisphere craniotomy"
    THREE_MM = "3 mm"
    FIVE_MM = "5 mm"
    OTHER = "Other"


class Craniotomy(Procedure):
    """Description of craniotomy procedure"""

    craniotomy_type: CraniotomyType = Field(..., title="Craniotomy type") 
    craniotomy_hemisphere: Optional[Side] = Field(None, title="Craniotomy hemisphere")
    craniotomy_coordinates_ml: Optional[float] = Field(None, title="Craniotomy coordinate ML (mm)", units="mm")
    craniotomy_coordinates_ap: Optional[float] = Field(None, title="Craniotomy coordinates AP (mm)", units="mm")
    craniotomy_coordinates_unit: SizeUnit = Field(SizeUnit.MM, title="Craniotomy coordinates unit")
    craniotomy_size: float = Field(..., title="Craniotomy size (mm)", units="mm")
    craniotomy_size_unit: SizeUnit = Field(SizeUnit.MM, title="Craniotomy size unit")
    implant_part_number: Optional[str] = Field(None, title="Implant part number")
    dura_removed: Optional[bool] = Field(None, title="Dura removed")
    protective_material: Optional[ProtectiveMaterial] = Field(None, title="Protective material")
    workstation_id: Optional[str] = Field(None, title="Workstation ID")
    recovery_time: Optional[time] = Field(None, title="Recovery time")


class HeadframeMaterial(Enum):
    """Headframe material name"""

    TITANIUM = "Titanium"
    STEEL = "Steel"
    WHITE_ZIRCONIA = "White Zirconia"


class Headframe(Procedure):
    """Description of headframe procedure"""

    headframe_type: str = Field(..., title="Headframe type")
    headframe_part_number: str = Field(..., title="Headframe part number")
    headframe_material: Optional[HeadframeMaterial] = Field(None, title="Headframe material")
    well_part_number: Optional[str] = Field(None, title="Well part number")
    well_type: Optional[str] = Field(None, title="Well type")


class VirusPrepType(Enum):
    """Type of virus preparation"""

    CRUDE = "Crude"
    PURIFIED = "Purified"


class InjectionMaterial(AindModel):
    """Description of injection material"""

    name: str = Field(..., title="Name")
    material_id: Optional[str] = Field(None, title="Material ID")
    full_genome_name: Optional[str] = Field(
        None,
        title="Full genome name",
        description="Full genome for virus construct",
    )
    plasmid_name: Optional[str] = Field(
        None,
        title="Plasmid name",
        description="Short name used to reference the plasmid",
    )
    genome_copy: Optional[float] = Field(None, title="Genome copy")
    titer: Optional[float] = Field(None, title="Titer (gc/mL", units="gc/mL")
    titer_unit: Optional[str] = Field("gc/mL", title="Titer unit")
    prep_lot_number: Optional[str] = Field(None, title="Preparation lot number")
    prep_date: Optional[date] = Field(
        None,
        title="Preparation lot date",
        description="Date this prep lot was titered",
    )
    prep_type: Optional[VirusPrepType] = Field(None, title="Viral prep type")


class Injection(Procedure):
    """Description of an injection procedure"""

    injection_materials: List[InjectionMaterial] = Field(None, title="Injection material", unique_items=True)
    recovery_time: Optional[time] = Field(None, title="Recovery time")
    injection_duration: Optional[time] = Field(None, title="Injection duration")
    workstation_id: Optional[str] = Field(None, title="Workstation ID")
    instrument_id: Optional[str] = Field(None, title="Instrument ID")


class RetroOrbitalInjection(Injection):
    """Description of a retro-orbital injection procedure"""

    injection_type: str = Field("Retro-orbital", title="Injection type", const=True)
    injection_volume: float = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: str = Field("nL", title="Injection volume unit")
    injection_eye: Side = Field(..., title="Injection eye")


class BrainInjection(Injection):
    """Description of a brain injection procedure"""

    injection_hemisphere: Optional[Side] = Field(None, title="Injection hemisphere")
    injection_coordinate_ml: float = Field(..., title="Injection coordinate ML (mm)")
    injection_coordinate_ap: float = Field(..., title="Injection coordinate AP (mm)")
    injection_coordinate_depth: float = Field(..., title="Injection coodinate depth (mm)")
    injection_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Injection coordinate unit")
    injection_angle: float = Field(..., title="Injection angle (deg)", units="deg")
    injection_angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Injection angle unit")


class NanojectInjection(BrainInjection):
    """Description of a nanoject injection procedure"""

    injection_type: str = Field("Nanoject", title="Injection type", const=True)
    injection_volume: float = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class IontophoresisInjection(BrainInjection):
    """Description of an iotophoresis injection procedure"""

    injection_type: str = Field("Iontophoresis", title="Injection type", const=True)
    injection_current: float = Field(..., title="Injection current (μA)", units="μA")
    injection_current_unit: CurrentUnit = Field(CurrentUnit.UA, title="Injection current unit")
    alternating_current: str = Field(..., title="Alternating current")


class IntraCerebellarVentricleInjection(BrainInjection):
    """Description of an interacerebellar ventricle injection"""

    injection_type: str = Field("ICV", title="Injection type", const=True)
    injection_volume: float = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class IntraCisternalMagnaInjection(BrainInjection):
    """Description of an interacisternal magna injection"""

    injection_type: str = Field("ICM", title="Injection type", const=True)
    injection_volume: float = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class MriScanSequence(Enum):
    """MRI scan sequence"""

    RARE = "RARE"


class ScannerLocation(Enum):
    """location of scanner"""

    UW_SLU = "UW SLU"
    FRED_HUTCH = "Fred Hutch"


class MagneticStrength(Enum):
    """Strength of magnet"""

    MRI_7T = 7
    MRI_14T = 14


class MriScan(Procedure):
    """Description of an MRI scan"""

    scan_sequence: MriScanSequence = Field(..., title="Scan sequence")
    scanner_location: Optional[ScannerLocation] = Field(None, title="Scanner location")
    magnetic_strength: Optional[MagneticStrength] = Field(None, title="Magnetic strength (T)", units="T")
    magnetic_strength_unit: str = Field("T", title="Magnetic strength unit")
    resolution: float = Field(..., title="Resolution")


class TissuePrepName(Enum):
    """Tissue preparation type name"""

    PERFUSION = "Perfusion"
    FIXATION = "Fixation"
    DOUBLE_DELIPIDATION = "Double delipidation"
    DCM_DELIPIDATION = "DCM delipidation"
    IMMUNOSTAINING = "Immunostaining"
    GELATION = "Gelation"


class TissuePrep(Procedure):
    """Description of a tissue preparation procedure"""

    name: TissuePrepName = Field(..., title="Name")
    specimen_id: List[str] = Field(..., title="Specimen ID")


class TrainingProtocol(AindModel):
    """Description of an animal training protocol"""

    training_name: str = Field(..., title="Training protocol name")
    protocol_id: str = Field(..., title="Training protocol ID")
    training_protocol_start_date: date = Field(..., title="Training protocol start date")
    training_protocol_end_date: Optional[date] = Field(None, title="Training protocol end date")
    notes: Optional[str] = Field(None, title="Notes")


class ProbeName(Enum):
    """Probe name"""

    PROBE_A = "Probe A"
    PROBE_B = "Probe B"
    PROBE_C = "Probe C"


class FerruleMaterial(Enum):
    """Probe ferrule material type name"""

    CERAMIC = "Ceramic"
    STAINLESS_STEEL = "Stainless steel"


class OphysProbe(AindModel):
    """Description of an ophys probe"""

    name: ProbeName = Field(..., title="Name")
    manufacturer: str = Field(..., title="Manufacturer")
    part_number: str = Field(..., title="Part number")
    core_diameter: float = Field(..., title="Core diameter (μm)", units="μm")
    core_diameter_unit: str = Field("μm", title="Core diameter unit")
    numerical_aperture: float = Field(..., title="Numerical aperture")
    ferrule_material: Optional[FerruleMaterial] = Field(None, title="Ferrule material")
    targeted_structure: str = Field(..., title="Targeted structure")
    stereotactic_coordinate_ap: float = Field(..., title="Stereotactic coordinate A/P (mm)", units="mm")
    stereotactic_coordinate_ml: float = Field(..., title="Stereotactic coodinate M/L (mm)", units="mm")
    stereotactic_coordinate_dv: float = Field(..., title="Stereotactic coordinate D/V (mm)", units="mm")
    stereotactic_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Sterotactic coordinate unit")
    angle: float = Field(..., title="Angle (deg)", units="deg")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")
    notes: Optional[str] = Field(None, title="Notes")


class FiberImplant(Procedure):
    """Description of an implant procedure"""

    probes: List[OphysProbe] = Field(..., title="Ophys Probes", unique_items=True)


class WaterRestriction(AindModel):
    """Description of a water restriction procedure"""

    protocol_id: Optional[str] = Field(None, title="Water restriction protocol number")
    baseline_weight: float = Field(
        ...,
        title="Baseline weight (g)",
        description="Weight at start of water restriction",
    )
    weight_unit: WeightUnit = Field(WeightUnit.G, title="Weight unit")
    start_date: date = Field(..., title="Water restriction start date")
    end_date: date = Field(..., title="Water restriction end date")


class Procedures(AindCoreModel):
    """Description of all procedures performed on a subject"""

    schema_version: str = Field("0.5.4", description="schema version", title="Version", const=True)
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    headframes: Optional[List[Headframe]] = Field(None, title="Headframes", unique_items=True)
    craniotomies: Optional[List[Craniotomy]] = Field(None, title="Craniotomies", unique_items=True)
    mri_scans: Optional[List[MriScan]] = Field(None, title="MRI scans", unique_items=True)
    injections: Optional[
        List[
            Union[
                RetroOrbitalInjection,
                NanojectInjection,
                IontophoresisInjection,
                IntraCerebellarVentricleInjection,
                IntraCisternalMagnaInjection,
            ]
        ]
    ] = Field(None, title="Injections", unique_items=True)
    fiber_implants: Optional[List[FiberImplant]] = Field(None, title="Fiber implants", unique_items=True)
    water_restrictions: Optional[List[WaterRestriction]] = Field(None, title="Water restriction")
    training_protocols: Optional[List[TrainingProtocol]] = Field(None, title="Training protocols", unique_items=True)
    tissue_preparations: Optional[List[TissuePrep]] = Field(None, title="Tissue preparations", unique_items=True)
    other_procedures: Optional[List[Procedure]] = Field(None, title="Other procedures", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
