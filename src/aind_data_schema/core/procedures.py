""" schema for various Procedures """

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Set, Union

from pydantic import Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.models.devices import FiberProbe
from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.reagent import Reagent
from aind_data_schema.models.species import Species
from aind_data_schema.models.units import (
    AngleUnit,
    ConcentrationUnit,
    CurrentUnit,
    MassUnit,
    SizeUnit,
    TimeUnit,
    VolumeUnit,
    create_unit_with_value,
)


class SpecimenProcedureType(str, Enum):
    """Names for general specimen procedures"""

    DELIPIDATION = "Delipidation"
    CLEARING = "Clearing"
    EMBEDDING = "Embedding"
    FIXATION = "Fixation"
    FIXATION_PERMEABILIZATION = "Fixation and permeabilization"
    GELATION = "Gelation"
    HYBRIDIZATION_AMPLIFICATION = "Hybridication and amplification"
    HCR = "Hybridization Chain Reaction"
    IMMUNOLABELING = "Immunolabeling"
    MOUNTING = "Mounting"
    SECTIONING = "Sectioning"
    SOAK = "Soak"
    STORAGE = "Storage"
    STRIPPING = "Stripping"
    REFRACTIVE_INDEX_MATCHING = "Refractive index matching"
    OTHER = "Other - see notes"


class ImmunolabelClass(str, Enum):
    """Type of antibodies"""

    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    CONJUGATE = "Conjugate"


class StainType(str, Enum):
    """Stain types for probes describing what is being labeled"""

    RNA = "RNA"
    NUCLEAR = "Nuclear"
    FILL = "Fill"


class Fluorophore(str, Enum):
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


class Side(str, Enum):
    """Side of animal"""

    LEFT = "Left"
    RIGHT = "Right"


class ProtectiveMaterial(str, Enum):
    """Name of material applied to craniotomy"""

    DURAGEL = "Duragel"
    KWIK_CAST = "Kwik-Cast"
    SORTA_CLEAR = "SORTA-clear"
    OTHER = "Other - see notes"


class CraniotomyType(str, Enum):
    """Name of craniotomy Type"""

    DHC = "Dual hemisphere craniotomy"
    THREE_MM = "3 mm"
    FIVE_MM = "5 mm"
    VISCTX = "Visual Cortex"
    WHC = "Whole hemisphere craniotomy"
    OTHER = "Other"


class CoordinateReferenceLocation(str, Enum):
    """Name of reference point for Coordinates"""

    BREGMA = "Bregma"
    LAMBDA = "Lambda"


class HeadframeMaterial(str, Enum):
    """Headframe material name"""

    STEEL = "Steel"
    TITANIUM = "Titanium"
    WHITE_ZIRCONIA = "White Zirconia"


class VirusPrepType(str, Enum):
    """Type of virus preparation"""

    CRUDE = "Crude"
    PURIFIED = "Purified"


class Readout(Reagent):
    """Description of a readout"""

    fluorophore: Fluorophore = Field(..., title="Fluorophore")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Excitation wavelength unit")
    stain_type: StainType = Field(..., title="Stain type")


class HCRReadout(Readout):
    """Description of a readout for HCR"""

    initiator_name: str = Field(..., title="Initiator name")


class OligoProbe(Reagent):
    """Description of an oligonucleotide probe"""

    species: Species.ONE_OF = Field(..., title="Species")
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
    # TODO: It might be easier to maintain to avoid dynamic model creation
    concentration: create_unit_with_value("concentration", Decimal, ConcentrationUnit, ConcentrationUnit.UM) = Field(
        ..., title="Concentration (uM)"
    )


class HybridizationChainReaction(AindModel):
    """Description of an HCR staining round"""

    round_index: int = Field(..., title="Round index")
    start_time: datetime = Field(..., title="Round start time")
    end_time: datetime = Field(..., title="Round end time")
    HCR_probes: List[HCRProbe] = Field(..., title="HCR probes")
    other_probes: List[OligoProbe] = Field(default=[], title="Other probes")
    probe_concentration: Decimal = Field(..., title="Probe concentration (M)")
    probe_concentration_unit: str = Field("M", title="Probe concentration unit")
    other_stains: List[Stain] = Field(default=[], title="Other stains")
    instrument_id: str = Field(..., title="Instrument ID")


class HCRSeries(AindModel):
    """Description of series of HCR staining rounds for mFISH"""

    codebook_name: str = Field(..., title="Codebook name")
    number_of_rounds: int = Field(..., title="Number of round")
    hcr_rounds: List[HybridizationChainReaction] = Field(..., title="Hybridization Chain Reaction rounds")
    strip_qc_compatible: bool = Field(..., title="Strip QC compatible")


class Antibody(Reagent):
    """Description of an antibody used in immunolableing"""

    immunolabel_class: ImmunolabelClass = Field(..., title="Immunolabel class")
    fluorophore: Optional[Fluorophore] = Field(None, title="Fluorophore")
    degree_of_labeling: Optional[Decimal] = Field(None, title="Degree of labeling")
    degree_of_labeling_unit: Literal["Fluorophore per antibody"] = Field(
        "Fluorophore per antibody", title="Degree of labeling unit"
    )
    conjugation_protocol: Optional[str] = Field(
        None, title="Conjugation protocol", description="Only for conjugated anitbody"
    )


class Immunolabeling(AindModel):
    """Description of an immunolabling step"""

    procedure_type: Literal["Immunolabeling"] = "Immunolabeling"
    antibody: Antibody = Field(..., title="Antibody")
    concentration: Decimal = Field(..., title="Concentration")
    concentration_unit: str = Field("ug/ml", title="Concentration unit")


class SpecimenProcedure(AindModel):
    """Description of surgical or other procedure performed on a specimen"""

    procedure_type: SpecimenProcedureType = Field(..., title="Procedure type")
    procedure_name: Optional[str] = Field(
        None, title="Procedure name", description="Name to clarify specific procedure used as needed"
    )
    specimen_id: str = Field(..., title="Specimen ID")
    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    reagents: List[Reagent] = Field(default=[], title="Reagents")
    hcr_series: Optional[HCRSeries] = Field(None, title="HCR Series")
    immunolabeling: Optional[Immunolabeling] = Field(None, title="Immunolabeling")
    notes: Optional[str] = Field(None, title="Notes")

    @model_validator(mode="after")
    def validate_procedure_type(self):
        """Adds a validation check on procedure_type"""

        if self.procedure_type == SpecimenProcedureType.OTHER and not self.notes:
            raise AssertionError(
                "notes cannot be empty if procedure_type is Other. Describe the procedure in the notes field."
            )
        elif self.procedure_type == SpecimenProcedureType.HCR and not self.hcr_series:
            raise AssertionError("hcr_series cannot be empty if procedure_type is HCR.")
        elif self.procedure_type == SpecimenProcedureType.IMMUNOLABELING and not self.immunolabeling:
            raise AssertionError("immunolabeling cannot be empty if procedure_type is Immunolabeling.")
        return self


class Anaesthetic(AindModel):
    """Description of an anaesthetic"""

    type: str = Field(..., title="Type")
    duration: Decimal = Field(..., title="Duration")
    duration_unit: TimeUnit = Field(TimeUnit.M, title="Duration unit")
    level: Decimal = Field(..., title="Level (percent)", ge=1, le=5)


class OtherSubjectProcedure(AindModel):
    """Description of non-surgical procedure performed on a subject"""

    procedure_type: Literal["Other Subject Procedure"] = "Other Subject Procedure"
    protocol_id: Optional[str] = Field(None, title="Protocol ID", description="DOI for protocols.io")
    description: str = Field(..., title="Description")
    notes: Optional[str] = Field(None, title="Notes")


class Craniotomy(AindModel):
    """Description of craniotomy procedure"""

    procedure_type: Literal["Craniotomy"] = "Craniotomy"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    craniotomy_type: CraniotomyType = Field(..., title="Craniotomy type")
    craniotomy_hemisphere: Optional[Side] = Field(None, title="Craniotomy hemisphere")
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda"
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    implant_part_number: Optional[str] = Field(None, title="Implant part number")
    dura_removed: Optional[bool] = Field(None, title="Dura removed")
    protective_material: Optional[ProtectiveMaterial] = Field(None, title="Protective material")
    recovery_time: Optional[Decimal] = Field(None, title="Recovery time")
    recovery_time_unit: TimeUnit = Field(TimeUnit.M, title="Recovery time unit")


class Headframe(AindModel):
    """Description of headframe procedure"""

    procedure_type: Literal["Headframe"] = "Headframe"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    headframe_type: str = Field(..., title="Headframe type")
    headframe_part_number: str = Field(..., title="Headframe part number")
    headframe_material: Optional[HeadframeMaterial] = Field(None, title="Headframe material")
    well_part_number: Optional[str] = Field(None, title="Well part number")
    well_type: Optional[str] = Field(None, title="Well type")


class TarsVirusIdentifiers(AindModel):
    """TARS data for a viral prep"""

    virus_tars_id: Optional[str] = Field(None, title="Virus ID, usually begins 'AiV'")
    plasmid_tars_alias: Optional[str] = Field(
        None,
        title="Plasmid alias",
        description="Alias used to reference the plasmid, usually begins 'AiP'",
    )
    prep_lot_number: str = Field(..., title="Preparation lot number")
    prep_date: Optional[date] = Field(
        None,
        title="Preparation lot date",
        description="Date this prep lot was titered",
    )
    prep_type: Optional[VirusPrepType] = Field(None, title="Viral prep type")
    prep_protocol: Optional[str] = Field(None, title="Prep protocol")


class ViralMaterial(AindModel):
    """Description of viral material for injections"""

    material_type: Literal["Virus"] = Field("Virus", title="Injection material type")
    name: str = Field(
        ...,
        title="Full genome name",
        description="Full genome for virus construct",
    )
    tars_identifiers: Optional[TarsVirusIdentifiers] = Field(
        None, title="TARS IDs", description="TARS database identifiers"
    )
    addgene_id: Optional[PIDName] = Field(None, title="Addgene id", description="Registry must be Addgene")
    titer: Optional[int] = Field(
        None,
        title="Effective titer (gc/mL)",
        description="Final titer of viral material, accounting for mixture/diliution",
    )
    titer_unit: str = Field("gc/mL", title="Titer unit")


class NonViralMaterial(Reagent):
    """Description of a non-viral injection material"""

    material_type: Literal["Reagent"] = Field("Reagent", title="Injection material type")
    concentration: Optional[Decimal] = Field(None, title="Concentration", description="Must provide concentration unit")
    concentration_unit: str = Field(default="mg/mL", title="Concentration unit")


class Injection(AindModel):
    """Description of an injection procedure"""

    injection_materials: Annotated[
        List[Union[ViralMaterial, NonViralMaterial]],
        Field(title="Injection material", min_length=1, discriminator="material_type"),
    ] = []
    recovery_time: Optional[Decimal] = Field(None, title="Recovery time")
    recovery_time_unit: TimeUnit = Field(TimeUnit.M, title="Recovery time unit")
    injection_duration: Optional[Decimal] = Field(None, title="Injection duration")
    injection_duration_unit: TimeUnit = Field(TimeUnit.M, title="Injection duration unit")
    instrument_id: Optional[str] = Field(None, title="Instrument ID")
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")


class RetroOrbitalInjection(Injection):
    """Description of a retro-orbital injection procedure"""

    procedure_type: Literal["Retro-orbital injection"] = "Retro-orbital injection"
    injection_volume: Decimal = Field(..., title="Injection volume (uL)")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.UL, title="Injection volume unit")
    injection_eye: Side = Field(..., title="Injection eye")


class IntraperitonealInjection(Injection):
    """Description of an intraperitoneal injection procedure"""

    procedure_type: Literal["Intraperitoneal injection"] = "Intraperitoneal injection"
    injection_volume: Decimal = Field(..., title="Injection volume (uL)")
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.UL, title="Injection volume unit")


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
        None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda"
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    injection_angle: Decimal = Field(..., title="Injection angle (deg)")
    injection_angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Injection angle unit")
    targeted_structure: Optional[str] = Field(None, title="Injection targeted brain structure")
    injection_hemisphere: Optional[Side] = Field(None, title="Injection hemisphere")


class NanojectInjection(BrainInjection):
    """Description of a nanoject injection procedure"""

    procedure_type: Literal["Nanoject injection"] = "Nanoject injection"
    injection_volume: List[Decimal] = Field(
        ...,
        title="Injection volume (nL)",
        description="Injection volume, one value per location",
    )
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")

    @field_validator("injection_volume")
    def check_dv_and_vol_list_lengths(cls, v, info: ValidationInfo):
        """Validator for list length of injection volumes and depths"""

        injection_vol_len = len(v)
        coords_len = len(info.data["injection_coordinate_depth"])

        if injection_vol_len != coords_len:
            raise AssertionError("Unmatched list sizes for injection volumes and coordinate depths")
        return v


class IontophoresisInjection(BrainInjection):
    """Description of an iotophoresis injection procedure"""

    procedure_type: Literal["Iontophoresis injection"] = "Iontophoresis injection"
    injection_current: Decimal = Field(..., title="Injection current (uA)")
    injection_current_unit: CurrentUnit = Field(CurrentUnit.UA, title="Injection current unit")
    alternating_current: str = Field(..., title="Alternating current")


class IntraCerebellarVentricleInjection(BrainInjection):
    """Description of an interacerebellar ventricle injection"""

    procedure_type: Literal["ICV injection"] = "ICV injection"
    injection_volume: List[Decimal] = Field(
        ...,
        title="Injection volume (nL)",
        description="Injection volume, one value per location",
    )
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class IntraCisternalMagnaInjection(BrainInjection):
    """Description of an interacisternal magna injection"""

    procedure_type: Literal["ICM injection"] = "ICM injection"
    injection_volume: List[Decimal] = Field(
        ...,
        title="Injection volume (nL)",
        description="Injection volume, one value per location",
    )
    injection_volume_unit: VolumeUnit = Field(VolumeUnit.NL, title="Injection volume unit")


class TrainingProtocol(AindModel):
    """Description of an animal training protocol"""

    procedure_type: Literal["Training"] = "Training"
    training_name: str = Field(..., title="Training protocol name")
    protocol_id: str = Field(..., title="Training protocol ID")
    start_date: date = Field(..., title="Training protocol start date")
    end_date: Optional[date] = Field(None, title="Training protocol end date")
    notes: Optional[str] = Field(None, title="Notes")


class OphysProbe(AindModel):
    """Description of an implanted ophys probe"""

    ophys_probe: FiberProbe = Field(..., title="Fiber probe")
    targeted_structure: str = Field(..., title="Targeted structure")
    stereotactic_coordinate_ap: Decimal = Field(..., title="Stereotactic coordinate A/P (mm)")
    stereotactic_coordinate_ml: Decimal = Field(..., title="Stereotactic coordinate M/L (mm)")
    stereotactic_coordinate_dv: Decimal = Field(
        ...,
        title="Stereotactic coordinate D/V (mm)",
    )
    stereotactic_coordinate_unit: SizeUnit = Field(SizeUnit.MM, title="Sterotactic coordinate unit")
    stereotactic_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        None, title="Stereotactic coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda"
    )
    bregma_to_lambda_unit: SizeUnit = Field(SizeUnit.MM, title="Bregma to lambda unit")
    angle: Decimal = Field(..., title="Angle (deg)")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")
    notes: Optional[str] = Field(None, title="Notes")


class FiberImplant(AindModel):
    """Description of an implant procedure"""

    procedure_type: Literal["Fiber implant"] = "Fiber implant"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    probes: List[OphysProbe] = Field(..., title="Ophys Probes")


class WaterRestriction(AindModel):
    """Description of a water restriction procedure"""

    procedure_type: Literal["Water restriction"] = "Water restriction"
    protocol_id: Optional[str] = Field(None, title="Water restriction protocol number")
    baseline_weight: Decimal = Field(
        ...,
        title="Baseline weight (g)",
        description="Weight at start of water restriction",
    )
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    start_date: date = Field(..., title="Water restriction start date")
    end_date: date = Field(..., title="Water restriction end date")


class Perfusion(AindModel):
    """Description of a perfusion procedure that creates a specimen"""

    procedure_type: Literal["Perfusion"] = "Perfusion"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    output_specimen_ids: Set[str] = Field(
        ...,
        title="Specimen ID",
        description="IDs of specimens resulting from this procedure.",
    )


class Surgery(AindModel):
    """Description of subject procedures performed at one time"""

    procedure_type: Literal["Surgery"] = "Surgery"

    start_date: date = Field(..., title="Start date")
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    animal_weight_prior: Optional[Decimal] = Field(
        None, title="Animal weight (g)", description="Animal weight before procedure"
    )
    animal_weight_post: Optional[Decimal] = Field(
        None, title="Animal weight (g)", description="Animal weight after procedure"
    )
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(None, title="Anaesthesia")
    workstation_id: Optional[str] = Field(None, title="Workstation ID")
    procedures: List[
        Annotated[
            Union[
                Craniotomy,
                FiberImplant,
                Headframe,
                IntraCerebellarVentricleInjection,
                IntraCisternalMagnaInjection,
                IntraperitonealInjection,
                IontophoresisInjection,
                NanojectInjection,
                Perfusion,
                OtherSubjectProcedure,
                RetroOrbitalInjection,
            ],
            Field(discriminator="procedure_type"),
        ]
    ] = Field(title="Procedures", min_length=1)
    notes: Optional[str] = Field(None, title="Notes")


class Procedures(AindCoreModel):
    """Description of all procedures performed on a subject"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/procedures.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})

    schema_version: Literal["0.12.3"] = Field("0.12.3", description="schema version", title="Version")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    subject_procedures: List[
        Annotated[
            Union[Surgery, TrainingProtocol, WaterRestriction, OtherSubjectProcedure],
            Field(discriminator="procedure_type"),
        ]
    ] = Field([], title="Subject Procedures")
    specimen_procedures: List[SpecimenProcedure] = Field([], title="Specimen Procedures")
    notes: Optional[str] = Field(None, title="Notes")
