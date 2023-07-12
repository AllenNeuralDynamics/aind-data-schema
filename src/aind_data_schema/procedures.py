""" schema for various Procedures """

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel, PIDName
from aind_data_schema.device import AngleUnit, SizeUnit
from aind_data_schema.subject import Species


class TimeUnit(Enum):
    """Time units"""

    M = "minute"
    S = "second"
    MS = "millisecond"


class WeightUnit(Enum):
    """Weight units"""

    G = "gram"


class VolumeUnit(Enum):
    """Volume units"""

    NL = "nanoliter"
    UL = "microliter"


class CurrentUnit(Enum):
    """Current units"""

    UA = "microamps"


class SpecimenProcedureName(Enum):
    """Specimen procedure type name"""

    ACTIVE_DELIPIDATION = "Active delipidation"
    CLEARING = "Clearing"
    DCM_DELIPIDATION = "DCM delipidation"
    DOUBLE_DELIPIDATION = "Double delipidation"
    EMBEDDING = "Embedding"
    FIXATION = "Fixation"
    FIXATION_PERMEABILIZATION = "Fixation and permeabilization"
    GELATION = "Gelation"
    HYBRIDIZATION_AMPLIFICATION = "Hybridication and amplification"
    IMMUNOSTAINING = "Immunostaining"
    SOAK = "Soak"
    STORAGE = "Storage"
    STRIPPING = "Stripping"
    OTHER = "Other - see notes"


class Reagent(AindModel):
    """Description of reagents used in procedure"""

    name: str = Field(..., title="Name")
    source: str = Field(..., title="Source")
    rrid: Optional[str] = Field(None, title="Research Resource ID")
    lot_number: str = Field(..., title="Lot number")
    expiration_date: Optional[date] = Field(None, title="Lot expiration date")


class SpecimenProcedure(AindModel):
    """Description of surgical or other procedure performed on a specimen"""

    specimen_id: str = Field(..., title="Specimen ID")
    procedure_type: SpecimenProcedureName = Field(..., title="Procedure type")
    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    reagents: Optional[List[Reagent]] = Field(None, title="Reagents")
    notes: Optional[str] = Field(None, title="Notes")


class StainType(Enum):
    """Stain Types for HCR probes"""

    RNA = "RNA"


class Fluorophore(Enum):
    """Fluorophores used in HCR"""

    ALEXA_546 = "Alexa Fluor 546"
    ALEXA_594 = "Alexa Fluor 594"
    ALEXA_647 = "Alexa Fluor 647"


class Readout(Reagent):
    """Description of a readout"""

    fluorophore: Fluorophore = Field(..., title="Fluorophore")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit = SizeUnit = Field(SizeUnit.NM, title="Excitation wavelength unit")
    stain_type: StainType = Field(..., title="Stain type")


class HCRReadout(Readout):
    """Description of a readout for HCR"""

    initiator_name: str = Field(..., title="Initiator name")


class OligoProbe(Reagent):
    """Description of an oligo probe"""

    species: Species = Field(..., title="Species")
    gene: PIDName = Field(..., title="Gene name, accession number, and registry")
    probe_sequences: List[str] = Field(..., title="Probe sequences")
    readout: Readout = Field(..., title="Readout")
    channel_index: int = Field(..., title="Channel index")


class HCRProbe(OligoProbe):
    """Description of a HCR probe"""

    initiator_name: str = Field(..., title="Initiator name")
    readout: HCRReadout = Field(..., title="Readout")


class HybridizationChainReaction(AindModel):
    """Description of an HCR round"""

    round_index: int = Field(..., title="Round index")
    start_time: datetime = Field(..., title="Round start time")
    end_time: datetime = Field(..., title="Round end time")
    HCR_probes: List[HCRProbe] = Field(..., title="HCR probes")
    other_probes: Optional[List[OligoProbe]] = Field(None, title="Other probes")
    probe_concentration: Decimal = Field(..., title="Probe concentration (M)")
    probe_concentration_unit: str = Field("M", title="Probe concentration unit")
    intrument_id: str = Field(..., title="Instrument ID")


class HCRSeries(SpecimenProcedure):
    """Description of series of HCR rounds for mFISH"""

    codebook_name: str = Field(..., title="Codebook name")
    number_of_rounds: int = Field(..., title="Number of round")
    hcr_rounds: List[HybridizationChainReaction] = Field(..., title="Hybridization Chain Reaction rounds")
    strip_qc_compatible: bool = Field(..., title="Strip QC compatible")


class Side(Enum):
    """Side of animal"""

    LEFT = "Left"
    RIGHT = "Right"


class ProtectiveMaterial(Enum):
    """Name of material applied to craniotomy"""

    DURAGEL = "Duragel"
    KWIK_CAST = "Kwik-Cast"
    SORTA_CLEAR = "SORTA-clear"
    OTHER = "Other - see notes"


class Anaesthetic(AindModel):
    """Description of an anaestheic"""

    type: str = Field(..., title="Type")
    duration: Decimal = Field(..., title="Duration")
    duration_unit: TimeUnit = Field(TimeUnit.M, title="Duration unit")
    level: Decimal = Field(..., title="Level (percent)", units="percent", ge=1, le=5)


class SubjectProcedure(AindModel):
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
    animal_weight_prior: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
        units="g",
    )
    animal_weight_post: Optional[Decimal] = Field(
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

    THREE_MM = "3 mm"
    FIVE_MM = "5 mm"
    VISCTX = "Visual Cortex"
    WHC = "Whole hemisphere craniotomy"
    OTHER = "Other"


class CoordinateReferenceLocation(Enum):
    """Name of reference point for Coordinates"""

    BREGMA = "Bregma"
    LAMBDA = "Lambda"


class Craniotomy(SubjectProcedure):
    """Description of craniotomy procedure"""

    procedure_type: str = Field("Craniotomy", title="Procedure type", const=True)
    craniotomy_type: CraniotomyType = Field(..., title="Craniotomy type")
    craniotomy_hemisphere: Optional[Side] = Field(None, title="Craniotomy hemisphere")
    craniotomy_coordinates_ml: Optional[Decimal] = Field(None, title="Craniotomy coordinate ML (mm)", units="mm")
    craniotomy_coordinates_ap: Optional[Decimal] = Field(None, title="Craniotomy coordinates AP (mm)", units="mm")
    craniotomy_coordinates_unit: SizeUnit = Field(SizeUnit.MM, title="Craniotomy coordinates unit")
    craniotomy_coordinates_reference: Optional[CoordinateReferenceLocation] = Field(
        None, title="Craniotomy coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda", units="mm"
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    craniotomy_size: Decimal = Field(..., title="Craniotomy size (mm)", units="mm")
    craniotomy_size_unit: SizeUnit = Field(SizeUnit.MM, title="Craniotomy size unit")
    implant_part_number: Optional[str] = Field(None, title="Implant part number")
    dura_removed: Optional[bool] = Field(None, title="Dura removed")
    protective_material: Optional[ProtectiveMaterial] = Field(None, title="Protective material")
    workstation_id: Optional[str] = Field(None, title="Workstation ID")
    recovery_time: Optional[Decimal] = Field(None, title="Recovery time")
    recovery_time_unit: Optional[TimeUnit] = Field(TimeUnit.M, title="Recovery time unit")


class HeadframeMaterial(Enum):
    """Headframe material name"""

    STEEL = "Steel"
    TITANIUM = "Titanium"
    WHITE_ZIRCONIA = "White Zirconia"


class Headframe(SubjectProcedure):
    """Description of headframe procedure"""

    procedure_type: str = Field("Headframe", title="Procedure type", const=True)
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
    genome_copy: Optional[Decimal] = Field(None, title="Genome copy")
    titer: Optional[Decimal] = Field(None, title="Titer (gc/mL)", units="gc/mL")
    titer_unit: Optional[str] = Field("gc/mL", title="Titer unit")
    prep_lot_number: Optional[str] = Field(None, title="Preparation lot number")
    prep_date: Optional[date] = Field(  #
        None,
        title="Preparation lot date",
        description="Date this prep lot was titered",
    )
    prep_type: Optional[VirusPrepType] = Field(None, title="Viral prep type")
    prep_protocol: Optional[str] = Field(None, title="Prep protocol")


class Injection(SubjectProcedure):
    """Description of an injection procedure"""

    injection_materials: List[InjectionMaterial] = Field(None, title="Injection material", unique_items=True)
    recovery_time: Optional[Decimal] = Field(None, title="Recovery time")
    recovery_time_unit: Optional[TimeUnit] = Field(TimeUnit.M, title="Recovery time unit")
    injection_duration: Optional[Decimal] = Field(None, title="Injection duration")
    injection_duration_unit: Optional[TimeUnit] = Field(TimeUnit.M, title="Injection duration unit")
    workstation_id: Optional[str] = Field(None, title="Workstation ID")
    instrument_id: Optional[str] = Field(None, title="Instrument ID")


class RetroOrbitalInjection(Injection):
    """Description of a retro-orbital injection procedure"""

    procedure_type: str = Field("Retro-orbital injection", title="Procedure type", const=True)
    injection_volume: Decimal = Field(..., title="Injection volume (uL)", units="uL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.UL, title="Injection volume unit")
    injection_eye: Side = Field(..., title="Injection eye")


class BrainInjection(Injection):
    """Description of a brain injection procedure"""

    injection_coordinate_ml: Decimal = Field(..., title="Injection coordinate ML (mm)")
    injection_coordinate_ap: Decimal = Field(..., title="Injection coordinate AP (mm)")
    injection_coordinate_depth: Decimal = Field(..., title="Injection coodinate depth (mm)")
    injection_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Injection coordinate unit")
    injection_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        None, title="Injection coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda", units="mm"
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    injection_angle: Decimal = Field(..., title="Injection angle (deg)", units="deg")
    injection_angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Injection angle unit")
    targeted_structure: Optional[str] = Field(None, title="Injection targeted brain structure")

    injection_hemisphere: Optional[Side] = Field(None, title="Injection hemisphere")


class NanojectInjection(BrainInjection):
    """Description of a nanoject injection procedure"""

    procedure_type: str = Field("Nanoject injection", title="Procedure type", const=True)
    injection_volume: Decimal = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class IontophoresisInjection(BrainInjection):
    """Description of an iotophoresis injection procedure"""

    procedure_type: str = Field("Iontophoresis injection", title="Procedure type", const=True)
    injection_current: Decimal = Field(..., title="Injection current (μA)", units="μA")
    injection_current_unit: CurrentUnit = Field(CurrentUnit.UA, title="Injection current unit")
    alternating_current: str = Field(..., title="Alternating current")


class IntraCerebellarVentricleInjection(BrainInjection):
    """Description of an interacerebellar ventricle injection"""

    procedure_type: str = Field("ICV injection", title="Procedure type", const=True)
    injection_volume: Decimal = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class IntraCisternalMagnaInjection(BrainInjection):
    """Description of an interacisternal magna injection"""

    procedure_type: str = Field("ICM injection", title="Procedure type", const=True)
    injection_volume: Decimal = Field(..., title="Injection volume (nL)", units="nL")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class TrainingProtocol(AindModel):
    """Description of an animal training protocol"""

    procedure_type: str = Field("Training", title="Procedure type", const=True)
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
    PROBE_D = "Probe D"


class FerruleMaterial(Enum):
    """Probe ferrule material type name"""

    CERAMIC = "Ceramic"
    STAINLESS_STEEL = "Stainless steel"


class OphysProbe(AindModel):
    """Description of an ophys probe"""

    name: ProbeName = Field(..., title="Name")
    manufacturer: str = Field(..., title="Manufacturer")
    part_number: str = Field(..., title="Part number")
    core_diameter: Decimal = Field(..., title="Core diameter (μm)", units="μm")
    core_diameter_unit: str = Field("μm", title="Core diameter unit")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    ferrule_material: Optional[FerruleMaterial] = Field(None, title="Ferrule material")
    targeted_structure: str = Field(..., title="Targeted structure")
    stereotactic_coordinate_ap: Decimal = Field(..., title="Stereotactic coordinate A/P (mm)", units="mm")
    stereotactic_coordinate_ml: Decimal = Field(..., title="Stereotactic coodinate M/L (mm)", units="mm")
    stereotactic_coordinate_dv: Decimal = Field(..., title="Stereotactic coordinate D/V (mm)", units="mm")
    stereotactic_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Sterotactic coordinate unit")
    stereotactic_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        None, title="Stereotactic coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda", units="mm"
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    angle: Decimal = Field(..., title="Angle (deg)", units="deg")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")
    notes: Optional[str] = Field(None, title="Notes")


class FiberImplant(SubjectProcedure):
    """Description of an implant procedure"""

    procedure_type: str = Field("Fiber implant", title="Procedure type")
    probes: List[OphysProbe] = Field(..., title="Ophys Probes", unique_items=True)


class WaterRestriction(AindModel):
    """Description of a water restriction procedure"""

    procedure_type: str = Field("Water restriction", title="Procedure type", const=True)
    protocol_id: Optional[str] = Field(None, title="Water restriction protocol number")
    baseline_weight: Decimal = Field(
        ...,
        title="Baseline weight (g)",
        description="Weight at start of water restriction",
    )
    weight_unit: WeightUnit = Field(WeightUnit.G, title="Weight unit")
    start_date: date = Field(..., title="Water restriction start date")
    end_date: date = Field(..., title="Water restriction end date")


class Perfusion(SubjectProcedure):
    """Description of a perfusion procedure that creates a specimen"""

    procedure_type: str = Field("Perfusion", title="Procedure type", const=True)
    output_specimen_ids: List[str] = Field(
        ...,
        title="Specimen ID",
        description="IDs of specimens resulting from this procedure.",
        unique_items=True,
    )


class Procedures(AindCoreModel):
    """Description of all procedures performed on a subject"""

    schema_version: str = Field("0.8.2", description="schema version", title="Version", const=True)
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    subject_procedures: Optional[
        List[
            Union[
                Headframe,
                Craniotomy,
                RetroOrbitalInjection,
                NanojectInjection,
                IontophoresisInjection,
                IntraCerebellarVentricleInjection,
                IntraCisternalMagnaInjection,
                FiberImplant,
                WaterRestriction,
                TrainingProtocol,
                Perfusion,
                SubjectProcedure,
            ]
        ]
    ] = Field([], title="Subject Procedures", unique_items=True)
    specimen_procedures: Optional[
        List[
            Union[
                HCRSeries,
                SpecimenProcedure,
            ]
        ]
    ] = Field([], title="Specimen Procedures", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")
