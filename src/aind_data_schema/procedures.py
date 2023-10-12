""" schema for various Procedures """

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field, root_validator
from pydantic.typing import Annotated

from aind_data_schema.base import AindCoreModel, AindModel, PIDName
from aind_data_schema.subject import Species
from aind_data_schema.utils.units import (
    AngleUnit,
    ConcentrationUnit,
    CurrentUnit,
    MassUnit,
    SizeUnit,
    TimeUnit,
    VolumeUnit,
    create_unit_with_value,
)


class SpecimenProcedureName(Enum):
    """Specimen procedure type name"""

    DELIPIDATION = "Delipidation"
    CLEARING = "Clearing"
    EMBEDDING = "Embedding"
    FIXATION = "Fixation"
    FIXATION_PERMEABILIZATION = "Fixation and permeabilization"
    GELATION = "Gelation"
    HYBRIDIZATION_AMPLIFICATION = "Hybridication and amplification"
    IMMUNOSTAINING = "Immunostaining"
    SOAK = "Soak"
    STORAGE = "Storage"
    STRIPPING = "Stripping"
    REFRACTIVE_INDEX_MATCHING = "Refractive index matching"
    OTHER = "Other - see notes"


class Reagent(AindModel):
    """Description of reagents used in procedure"""

    name: str = Field(..., title="Name")
    source: str = Field(..., title="Source")
    rrid: Optional[PIDName] = Field(None, title="Research Resource ID")
    lot_number: str = Field(..., title="Lot number")
    expiration_date: Optional[date] = Field(None, title="Lot expiration date")


class SpecimenProcedure(AindModel):
    """Description of surgical or other procedure performed on a specimen"""

    specimen_procedure_type: str = Field("SpecimenProcedure", title="SpecimenProcedureType", const=True)
    specimen_id: str = Field(..., title="Specimen ID")
    procedure_name: str = Field(..., title="Procedure name")
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
    """Stain types for probes describing what is being labeled"""

    RNA = "RNA"
    NUCLEAR = "Nuclear"
    FILL = "Fill"


class Fluorophore(Enum):
    """Fluorophores used in HCR and Immunolabeling"""

    ALEXA_405 = "Alexa Fluor 405"
    ALEXA_488 = "Alexa Fluor 488"
    ALEXA_546 = "Alexa Fluor 546"
    ALEXA_568 = "Alexa Fluor 568"
    ALEXA_594 = "Alexa Fluor 594"
    ALEXA_633 = "Alexa Fluor 633"
    ALEXA_647 = "Alexa Fluor 647"
    ATTO_488 = "ATTO 488"
    ATTO_565 = "ATTO 565"
    ATTO_643 = "ATTO 643"
    CY3 = "Cyanine Cy 3"


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
    """Description of an oligonucleotide probe"""

    species: Species = Field(..., title="Species")
    gene: PIDName = Field(..., title="Gene name, accession number, and registry")
    probe_sequences: List[str] = Field(..., title="Probe sequences")
    readout: Readout = Field(..., title="Readout")


class HCRProbe(OligoProbe):
    """Description of an oligo probe used for HCR"""

    initiator_name: str = Field(..., title="Initiator name")
    readout: HCRReadout = Field(..., title="Readout")


class Stain(Reagent):
    """Description of a non-oligo probe stain"""

    stain_type: StainType = Field(..., title="Stain type")
    concentration: create_unit_with_value("concentration", Decimal, ConcentrationUnit, ConcentrationUnit.UM) = Field(
        ..., title="Concentration (uM)"
    )


class HybridizationChainReaction(AindModel):
    """Description of an HCR staining round"""

    round_index: int = Field(..., title="Round index")
    start_time: datetime = Field(..., title="Round start time")
    end_time: datetime = Field(..., title="Round end time")
    HCR_probes: List[HCRProbe] = Field(..., title="HCR probes")
    other_probes: Optional[List[OligoProbe]] = Field(None, title="Other probes")
    probe_concentration: Decimal = Field(..., title="Probe concentration (M)")
    probe_concentration_unit: str = Field("M", title="Probe concentration unit")
    other_stains: Optional[List[Stain]] = Field(None, title="Other stains")
    intrument_id: str = Field(..., title="Instrument ID")


class HCRSeries(SpecimenProcedure):
    """Description of series of HCR staining rounds for mFISH"""

    specimen_procedure_type: str = Field("HCRSeries", title="SpecimenProcedureType", const=True)
    codebook_name: str = Field(..., title="Codebook name")
    number_of_rounds: int = Field(..., title="Number of round")
    hcr_rounds: List[HybridizationChainReaction] = Field(..., title="Hybridization Chain Reaction rounds")
    strip_qc_compatible: bool = Field(..., title="Strip QC compatible")


class ImmunolabelClass(Enum):
    """Type of anitbodies"""

    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    CONJUGATE = "Conjugate"


class Antibody(Reagent):
    """Description of an antibody used in immunolableing"""

    immunolabel_class: ImmunolabelClass = Field(..., title="Immunolabel class")
    fluorophore: Optional[Fluorophore] = Field(None, title="Fluorophore")
    degree_of_labeling: Optional[Decimal] = Field(None, title="Degree of labeling")
    degree_of_labeling_unit: str = Field("Fluorophore per antibody", title="Degree of labeling unit", const=True)
    conjugation_protocol: Optional[str] = Field(
        None, title="Conjugation protocol", description="Only for conjugated anitbody"
    )


class Immunolabeling(SpecimenProcedure):
    """Description of an immunolabling step"""

    specimen_procedure_type: str = Field("Immunolabeling", title="SpecimenProcedureType", const=True)
    antibody: Antibody = Field(..., title="Antibody")
    concentration: Decimal = Field(..., title="Concentration")
    concentration_unit: str = Field("ug/ml", title="Concentration unit")


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
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
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
        None,
        title="Bregma to lambda (mm)",
        description="Distance between bregman and lambda",
        units="mm",
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
    titer: Optional[Decimal] = Field(None, title="Titer (gc/mL)", description="Titer for viral materials")
    titer_unit: Optional[str] = Field("gc/mL", title="Titer unit")
    concentration: Optional[Decimal] = Field(None, title="Concentration", description="Must provide concentration unit")
    concentration_unit: Optional[str] = Field(None, title="Concentration unit")
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

    injection_materials: List[InjectionMaterial] = Field(
        None, title="Injection material", unique_items=True, min_items=1
    )
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
    injection_coordinate_depth: List[Decimal] = Field(..., title="Injection coordinate depth (mm)")
    injection_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Injection coordinate unit")
    injection_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        None, title="Injection coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None,
        title="Bregma to lambda (mm)",
        description="Distance between bregman and lambda",
        units="mm",
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    injection_angle: Decimal = Field(..., title="Injection angle (deg)", units="deg")
    injection_angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Injection angle unit")
    targeted_structure: Optional[str] = Field(None, title="Injection targeted brain structure")

    injection_hemisphere: Optional[Side] = Field(None, title="Injection hemisphere")


class NanojectInjection(BrainInjection):
    """Description of a nanoject injection procedure"""

    procedure_type: str = Field("Nanoject injection", title="Procedure type", const=True)
    injection_volume: List[Decimal] = Field(
        ...,
        title="Injection volume (nL)",
        units="nL",
        description="Injection volume, one value per location",
    )
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")

    @root_validator
    def check_dv_and_vol_list_lengths(cls, v):
        """Validator for list length of injection volumes and depths"""

        injection_vol_len = len(v.get("injection_volume"))
        coords_len = len(v.get("injection_coordinate_depth"))

        if injection_vol_len != coords_len:
            raise ValueError("Unmatched list sizes for injection volumes and coordinate depths")
        return v


class IontophoresisInjection(BrainInjection):
    """Description of an iotophoresis injection procedure"""

    procedure_type: str = Field("Iontophoresis injection", title="Procedure type", const=True)
    injection_current: Decimal = Field(..., title="Injection current (μA)", units="μA")
    injection_current_unit: CurrentUnit = Field(CurrentUnit.UA, title="Injection current unit")
    alternating_current: str = Field(..., title="Alternating current")


class IntraCerebellarVentricleInjection(BrainInjection):
    """Description of an interacerebellar ventricle injection"""

    procedure_type: str = Field("ICV injection", title="Procedure type", const=True)
    injection_volume: List[Decimal] = Field(
        ...,
        title="Injection volume (nL)",
        units="nL",
        description="Injection volume, one value per location",
    )
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class IntraCisternalMagnaInjection(BrainInjection):
    """Description of an interacisternal magna injection"""

    procedure_type: str = Field("ICM injection", title="Procedure type", const=True)
    injection_volume: List[Decimal] = Field(
        ...,
        title="Injection volume (nL)",
        units="nL",
        description="Injection volume, one value per location",
    )
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
    stereotactic_coordinate_ml: Decimal = Field(..., title="Stereotactic coordinate M/L (mm)", units="mm")
    stereotactic_coordinate_dv: Decimal = Field(..., title="Stereotactic coordinate D/V (mm)", units="mm")
    stereotactic_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Sterotactic coordinate unit")
    stereotactic_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        None, title="Stereotactic coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None,
        title="Bregma to lambda (mm)",
        description="Distance between bregman and lambda",
        units="mm",
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
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
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

    schema_version: str = Field("0.9.5", description="schema version", title="Version", const=True)
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    subject_procedures: Optional[
        Annotated[
            List[
                Union[
                    Craniotomy,
                    FiberImplant,
                    Headframe,
                    IntraCerebellarVentricleInjection,
                    IntraCisternalMagnaInjection,
                    IontophoresisInjection,
                    NanojectInjection,
                    Perfusion,
                    RetroOrbitalInjection,
                    TrainingProtocol,
                    WaterRestriction,
                    SubjectProcedure,
                ]
            ],
            Field(title="Subject Procedures", unique_items=True, discriminator="procedure_type"),
        ]
    ] = []
    specimen_procedures: Optional[
        Annotated[
            List[Union[HCRSeries, Immunolabeling, SpecimenProcedure]],
            Field(title="Specimen Procedures", unique_items=True, discriminator="specimen_procedure_type"),
        ]
    ] = []
    notes: Optional[str] = Field(None, title="Notes")
