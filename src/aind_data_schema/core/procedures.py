""" schema for various Procedures """

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Set, Union

from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species
from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType
from aind_data_schema_models.units import (
    AngleUnit,
    ConcentrationUnit,
    CurrentUnit,
    MassUnit,
    SizeUnit,
    TimeUnit,
    UnitlessUnit,
    VolumeUnit,
)
from aind_data_schema_models.brain_atlas import CCFStructure
from pydantic import Field, SkipValidation, field_serializer, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated

from aind_data_schema.base import DataCoreModel, DataModel, AwareDatetimeWithDefault
from aind_data_schema.components.devices import FiberProbe, MyomatrixArray
from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.reagent import Reagent


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
    MIDLINE = "Midline"


class SectionOrientation(str, Enum):
    """Orientation of sectioning"""

    CORONAL = "Coronal"
    SAGITTAL = "Sagittal"
    TRANSVERSE = "Transverse"


class SectionStrategy(str, Enum):
    """Section strategy"""

    WHOLE = "Whole Brain"
    HEMI = "Hemi Brain"


class ProtectiveMaterial(str, Enum):
    """Name of material applied to craniotomy"""

    AGAROSE = "Agarose"
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
    MIDLINE = "Midline"


class HeadframeMaterial(str, Enum):
    """Headframe material name"""

    STEEL = "Steel"
    TITANIUM = "Titanium"
    WHITE_ZIRCONIA = "White Zirconia"


class GroundWireMaterial(str, Enum):
    """Ground wire material name"""

    SILVER = "Silver"
    PLATINUM_IRIDIUM = "Platinum iridium"


class VirusPrepType(str, Enum):
    """Type of virus preparation"""

    CRUDE = "Crude"
    PURIFIED = "Purified"


class CatheterMaterial(str, Enum):
    """Type of catheter material"""

    NAKED = "Naked"
    SILICONE = "VAB silicone"
    MESH = "VAB mesh"


class CatheterDesign(str, Enum):
    """Type of catheter design"""

    MAGNETIC = "Magnetic"
    NONMAGNETIC = "Non-magnetic"
    NA = "N/A"


class CatheterPort(str, Enum):
    """Type of catheter port"""

    SINGLE = "Single"
    DOUBLE = "Double"


class SampleType(str, Enum):
    """Sample type"""

    BLOOD = "Blood"
    OTHER = "Other"


class Readout(Reagent):
    """Description of a readout"""

    fluorophore: Fluorophore = Field(..., title="Fluorophore")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Excitation wavelength unit")
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
    concentration: Decimal = Field(..., title="Concentration")
    concentration_unit: ConcentrationUnit = Field(default=ConcentrationUnit.UM, title="Concentration unit")


class HybridizationChainReaction(DataModel):
    """Description of an HCR staining round"""

    round_index: int = Field(..., title="Round index")
    start_time: AwareDatetimeWithDefault = Field(..., title="Round start time")
    end_time: AwareDatetimeWithDefault = Field(..., title="Round end time")
    HCR_probes: List[HCRProbe] = Field(..., title="HCR probes")
    other_probes: List[OligoProbe] = Field(default=[], title="Other probes")
    probe_concentration: Decimal = Field(..., title="Probe concentration (M)")
    probe_concentration_unit: str = Field(default="M", title="Probe concentration unit")
    other_stains: List[Stain] = Field(default=[], title="Other stains")
    instrument_id: str = Field(..., title="Instrument ID")


class HCRSeries(DataModel):
    """Description of series of HCR staining rounds for mFISH"""

    codebook_name: str = Field(..., title="Codebook name")
    number_of_rounds: int = Field(..., title="Number of round")
    hcr_rounds: List[HybridizationChainReaction] = Field(..., title="Hybridization Chain Reaction rounds")
    strip_qc_compatible: bool = Field(..., title="Strip QC compatible")


class Antibody(Reagent):
    """Description of an antibody used in immunolableing"""

    immunolabel_class: ImmunolabelClass = Field(..., title="Immunolabel class")
    fluorophore: Optional[Fluorophore] = Field(default=None, title="Fluorophore")
    mass: Decimal = Field(..., title="Mass of antibody")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")
    notes: Optional[str] = Field(default=None, title="Notes")


class Sectioning(DataModel):
    """Description of a sectioning procedure"""

    procedure_type: Literal["Sectioning"] = "Sectioning"
    number_of_slices: int = Field(..., title="Number of slices")
    output_specimen_ids: List[str] = Field(..., title="Output specimen ids", min_length=1)
    section_orientation: SectionOrientation = Field(..., title="Sectioning orientation")
    section_thickness: Decimal = Field(..., title="Section thickness")
    section_thickness_unit: SizeUnit = Field(default=SizeUnit.MM, title="Section thickness unit")
    section_distance_from_reference: Decimal = Field(..., title="Section distance from reference")
    section_distance_unit: SizeUnit = Field(default=SizeUnit.MM, title="Distance unit")
    reference_location: CoordinateReferenceLocation = Field(..., title="Reference location for distance measurement")
    section_strategy: SectionStrategy = Field(..., title="Slice strategy")
    targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")

    @field_validator("output_specimen_ids")
    def check_output_id_length(cls, v, info: ValidationInfo):
        """Validator for list of output specimen ids"""

        output_id_len = len(v)
        expected_len = info.data["number_of_slices"]

        if output_id_len != expected_len:
            raise AssertionError("List of output specimen ids does not match the number of slices.")
        return v


class SpecimenProcedure(DataModel):
    """Description of surgical or other procedure performed on a specimen"""

    procedure_type: SpecimenProcedureType = Field(..., title="Procedure type")
    procedure_name: Optional[str] = Field(
        default=None, title="Procedure name", description="Name to clarify specific procedure used as needed"
    )
    specimen_id: str = Field(..., title="Specimen ID")
    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenters: List[Person] = Field(
        default=[],
        title="experimenter(s)",
    )
    protocol_id: List[str] = Field(..., title="Protocol ID", description="DOI for protocols.io")
    reagents: List[Reagent] = Field(default=[], title="Reagents")
    hcr_series: Optional[HCRSeries] = Field(default=None, title="HCR Series")
    antibodies: Optional[List[Antibody]] = Field(default=None, title="Immunolabeling")
    sectioning: Optional[Sectioning] = Field(default=None, title="Sectioning")
    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="after")
    def validate_procedure_type(self):
        """Adds a validation check on procedure_type"""

        if self.procedure_type == SpecimenProcedureType.OTHER and not self.notes:
            raise AssertionError(
                "notes cannot be empty if procedure_type is Other. Describe the procedure in the notes field."
            )
        elif self.procedure_type == SpecimenProcedureType.HYBRIDIZATION_CHAIN_REACTION and not self.hcr_series:
            raise AssertionError("hcr_series cannot be empty if procedure_type is HCR.")
        elif self.procedure_type == SpecimenProcedureType.IMMUNOLABELING and not self.antibodies:
            raise AssertionError("antibodies cannot be empty if procedure_type is Immunolabeling.")
        return self


class Anaesthetic(DataModel):
    """Description of an anaesthetic"""

    type: str = Field(..., title="Type")
    duration: Decimal = Field(..., title="Duration")
    duration_unit: TimeUnit = Field(default=TimeUnit.M, title="Duration unit")
    level: Optional[Decimal] = Field(default=None, title="Level (percent)", ge=1, le=5)


class OtherSubjectProcedure(DataModel):
    """Description of non-surgical procedure performed on a subject"""

    procedure_type: Literal["Other Subject Procedure"] = "Other Subject Procedure"
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    description: str = Field(..., title="Description")
    notes: Optional[str] = Field(default=None, title="Notes")


class CatheterImplant(DataModel):
    """Description of a catheter implant procedure"""

    procedure_type: Literal["Catheter Implant"] = "Catheter implant"
    where_performed: Organization.CATHETER_IMPLANT_INSTITUTIONS = Field(..., title="Where performed")
    catheter_material: CatheterMaterial = Field(..., title="Catheter material")
    catheter_design: CatheterDesign = Field(..., title="Catheter design")
    catheter_port: CatheterPort = Field(..., title="Catheter port")
    targeted_structure: MouseAnatomyModel = Field(
        ..., title="Targeted blood vessel", description="Use options from MouseBloodVessels"
    )


class Craniotomy(DataModel):
    """Description of craniotomy procedure"""

    procedure_type: Literal["Craniotomy"] = "Craniotomy"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    craniotomy_type: CraniotomyType = Field(..., title="Craniotomy type")
    craniotomy_hemisphere: Optional[Side] = Field(default=None, title="Craniotomy hemisphere")
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        default=None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda"
    )
    bregma_to_lambda_unit: SizeUnit = Field(default=SizeUnit.MM, title="Bregma to lambda unit")
    implant_part_number: Optional[str] = Field(default=None, title="Implant part number")
    dura_removed: Optional[bool] = Field(default=None, title="Dura removed")
    protective_material: Optional[ProtectiveMaterial] = Field(default=None, title="Protective material")
    recovery_time: Optional[Decimal] = Field(default=None, title="Recovery time")
    recovery_time_unit: Optional[TimeUnit] = Field(default=None, title="Recovery time unit")


class Headframe(DataModel):
    """Description of headframe procedure"""

    procedure_type: Literal["Headframe"] = "Headframe"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    headframe_type: str = Field(..., title="Headframe type")
    headframe_part_number: str = Field(..., title="Headframe part number")
    headframe_material: Optional[HeadframeMaterial] = Field(default=None, title="Headframe material")
    well_part_number: Optional[str] = Field(default=None, title="Well part number")
    well_type: Optional[str] = Field(default=None, title="Well type")


class ProtectiveMaterialReplacement(DataModel):
    """Description of a protective material replacement procedure in preparation for ephys recording"""

    procedure_type: Literal["Ground wire"] = "Ground wire"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    protective_material: ProtectiveMaterial = Field(
        ..., title="Protective material", description="New material being applied"
    )
    ground_wire_hole: Optional[int] = Field(default=None, title="Ground wire hole")
    ground_wire_material: Optional[GroundWireMaterial] = Field(default=None, title="Ground wire material")
    ground_wire_diameter: Optional[Decimal] = Field(default=None, title="Ground wire diameter")
    ground_wire_diameter_unit: Optional[SizeUnit] = Field(default=None, title="Ground wire diameter unit")
    well_part_number: Optional[str] = Field(default=None, title="Well part number")
    well_type: Optional[str] = Field(default=None, title="Well type")


class TarsVirusIdentifiers(DataModel):
    """TARS data for a viral prep"""

    virus_tars_id: Optional[str] = Field(default=None, title="Virus ID, usually begins 'AiV'")
    plasmid_tars_alias: Optional[str] = Field(
        default=None,
        title="Plasmid alias",
        description="Alias used to reference the plasmid, usually begins 'AiP'",
    )
    prep_lot_number: str = Field(..., title="Preparation lot number")
    prep_date: Optional[date] = Field(
        default=None,
        title="Preparation lot date",
        description="Date this prep lot was titered",
    )
    prep_type: Optional[VirusPrepType] = Field(default=None, title="Viral prep type")
    prep_protocol: Optional[str] = Field(default=None, title="Prep protocol")


class ViralMaterial(DataModel):
    """Description of viral material for injections"""

    material_type: Literal["Virus"] = Field(default="Virus", title="Injection material type")
    name: str = Field(
        ...,
        title="Full genome name",
        description="Full genome for virus construct",
    )
    tars_identifiers: Optional[TarsVirusIdentifiers] = Field(
        default=None, title="TARS IDs", description="TARS database identifiers"
    )
    addgene_id: Optional[PIDName] = Field(default=None, title="Addgene id", description="Registry must be Addgene")
    titer: Optional[int] = Field(
        default=None,
        title="Effective titer (gc/mL)",
        description="Final titer of viral material, accounting for mixture/diliution",
    )
    titer_unit: str = Field(default="gc/mL", title="Titer unit")


class NonViralMaterial(Reagent):
    """Description of a non-viral injection material"""

    material_type: Literal["Reagent"] = Field(default="Reagent", title="Injection material type")
    concentration: Optional[Decimal] = Field(
        default=None, title="Concentration", description="Must provide concentration unit"
    )
    concentration_unit: Optional[str] = Field(
        default=None, title="Concentration unit", description="For example, mg/mL"
    )


class Injection(DataModel):
    """Description of an injection procedure"""

    injection_materials: List[
        Annotated[Union[ViralMaterial, NonViralMaterial], Field(..., discriminator="material_type")]
    ] = Field(..., title="Injection material", min_length=1)
    recovery_time: Optional[Decimal] = Field(default=None, title="Recovery time")
    recovery_time_unit: Optional[TimeUnit] = Field(default=None, title="Recovery time unit")
    injection_duration: Optional[Decimal] = Field(default=None, title="Injection duration")
    injection_duration_unit: Optional[TimeUnit] = Field(default=None, title="Injection duration unit")
    instrument_id: Optional[str] = Field(default=None, title="Instrument ID")
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")


class RetroOrbitalInjection(Injection):
    """Description of a retro-orbital injection procedure"""

    procedure_type: Literal["Retro-orbital injection"] = "Retro-orbital injection"
    injection_volume: Decimal = Field(..., title="Injection volume (uL)")
    injection_volume_unit: VolumeUnit = Field(default=VolumeUnit.UL, title="Injection volume unit")
    injection_eye: Side = Field(..., title="Injection eye")


class IntraperitonealInjection(Injection):
    """Description of an intraperitoneal injection procedure"""

    procedure_type: Literal["Intraperitoneal injection"] = "Intraperitoneal injection"
    time: Optional[AwareDatetimeWithDefault] = Field(default=None, title="Injection time")
    injection_volume: Decimal = Field(..., title="Injection volume (uL)")
    injection_volume_unit: VolumeUnit = Field(default=VolumeUnit.UL, title="Injection volume unit")


class BrainInjection(Injection):
    """Description of a brain injection procedure"""

    injection_coordinate_ml: Decimal = Field(..., title="Injection coordinate ML (mm)")
    injection_coordinate_ap: Decimal = Field(..., title="Injection coordinate AP (mm)")
    injection_coordinate_depth: List[Decimal] = Field(..., title="Injection coordinate depth (mm)")
    injection_coordinate_unit: SizeUnit = Field(default=SizeUnit.MM, title="Injection coordinate unit")
    injection_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        default=None, title="Injection coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        default=None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda"
    )
    bregma_to_lambda_unit: SizeUnit = Field(default=SizeUnit.MM, title="Bregma to lambda unit")
    injection_angle: Decimal = Field(..., title="Injection angle (deg)")
    injection_angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Injection angle unit")
    targeted_structure: Optional[CCFStructure.ONE_OF] = Field(default=None, title="Injection targeted brain structure")
    injection_hemisphere: Optional[Side] = Field(default=None, title="Injection hemisphere")


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
    injection_current_unit: CurrentUnit = Field(default=CurrentUnit.UA, title="Injection current unit")
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


class SampleCollection(DataModel):
    """Description of a single sample collection"""

    procedure_type: Literal["Sample collection"] = "Sample collection"
    sample_type: SampleType = Field(..., title="Sample type")
    time: AwareDatetimeWithDefault = Field(..., title="Collection time")
    collection_volume: Decimal = Field(..., title="Collection volume")
    collection_volume_unit: VolumeUnit = Field(..., title="Collection volume unit")
    collection_method: Optional[str] = Field(default=None, title="Collection method for terminal collection")


class TrainingProtocol(DataModel):
    """Description of an animal training protocol"""

    procedure_type: Literal["Training"] = "Training"
    training_name: str = Field(..., title="Training protocol name")
    protocol_id: str = Field(..., title="Training protocol ID")
    start_date: date = Field(..., title="Training protocol start date")
    end_date: Optional[date] = Field(default=None, title="Training protocol end date")
    notes: Optional[str] = Field(default=None, title="Notes")


class OphysProbe(DataModel):
    """Description of an implanted ophys probe"""

    ophys_probe: FiberProbe = Field(..., title="Fiber probe")
    targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")
    stereotactic_coordinate_ap: Decimal = Field(..., title="Stereotactic coordinate A/P (mm)")
    stereotactic_coordinate_ml: Decimal = Field(..., title="Stereotactic coordinate M/L (mm)")
    stereotactic_coordinate_dv: Decimal = Field(
        ...,
        title="Stereotactic coordinate D/V (mm)",
    )
    stereotactic_coordinate_unit: SizeUnit = Field(default=SizeUnit.MM, title="Sterotactic coordinate unit")
    stereotactic_coordinate_reference: Optional[CoordinateReferenceLocation] = Field(
        default=None, title="Stereotactic coordinate reference"
    )
    bregma_to_lambda_distance: Optional[Decimal] = Field(
        default=None, title="Bregma to lambda (mm)", description="Distance between bregman and lambda"
    )
    bregma_to_lambda_unit: SizeUnit = Field(default=SizeUnit.MM, title="Bregma to lambda unit")
    angle: Decimal = Field(..., title="Angle (deg)")
    angle_unit: AngleUnit = Field(default=AngleUnit.DEG, title="Angle unit")
    notes: Optional[str] = Field(default=None, title="Notes")


class FiberImplant(DataModel):
    """Description of an implant procedure"""

    procedure_type: Literal["Fiber implant"] = "Fiber implant"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    probes: List[OphysProbe] = Field(..., title="Ophys Probes")


class WaterRestriction(DataModel):
    """Description of a water restriction procedure"""

    procedure_type: Literal["Water restriction"] = "Water restriction"
    ethics_review_id: str = Field(..., title="Ethics review ID")
    target_fraction_weight: int = Field(..., title="Target fraction weight (%)")
    target_fraction_weight_unit: UnitlessUnit = Field(default=UnitlessUnit.PERCENT, title="Target fraction weight unit")
    minimum_water_per_day: Decimal = Field(..., title="Minimum water per day (mL)")
    minimum_water_per_day_unit: VolumeUnit = Field(default=VolumeUnit.ML, title="Minimum water per day unit")
    baseline_weight: Decimal = Field(
        ...,
        title="Baseline weight (g)",
        description="Weight at start of water restriction",
    )
    weight_unit: MassUnit = Field(default=MassUnit.G, title="Weight unit")
    start_date: date = Field(..., title="Water restriction start date")
    end_date: Optional[date] = Field(default=None, title="Water restriction end date")


class MyomatrixContact(DataModel):
    """ "Description of a contact on a myomatrix thread"""

    body_part: MouseAnatomyModel = Field(..., title="Body part of contact insertion", description="Use MouseBodyParts")
    side: Side = Field(..., title="Body side")
    muscle: MouseAnatomyModel = Field(..., title="Muscle of contact insertion", description="Use MouseEmgMuscles")
    in_muscle: bool = Field(..., title="In muscle")
    notes: Optional[str] = Field(default=None, title="Notes")


class MyomatrixThread(DataModel):
    """Description of a thread of a myomatrix array"""

    ground_electrode_location: MouseAnatomyModel = Field(
        ..., title="Location of ground electrode", description="Use MouseBodyParts"
    )
    contacts: List[MyomatrixContact] = Field(..., title="Contacts")


class MyomatrixInsertion(DataModel):
    """Description of a Myomatrix array insertion for EMG"""

    procedure_type: Literal["Myomatrix_Insertion"] = "Myomatrix_Insertion"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    myomatrix_array: MyomatrixArray = Field(..., title="Myomatrix array")
    threads: List[MyomatrixThread] = Field(..., title="Array threads")


class Perfusion(DataModel):
    """Description of a perfusion procedure that creates a specimen"""

    procedure_type: Literal["Perfusion"] = "Perfusion"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    output_specimen_ids: Set[str] = Field(
        ...,
        title="Specimen ID",
        description="IDs of specimens resulting from this procedure.",
    )

    @field_serializer("output_specimen_ids", when_used="json")
    def serialize_output_specimen_ids(values: Set[str]):
        """sort specimen ids for JSON serialization"""
        return sorted(values)


class Surgery(DataModel):
    """Description of subject procedures performed at one time"""

    procedure_type: Literal["Surgery"] = "Surgery"
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    start_date: date = Field(..., title="Start date")
    experimenters: Optional[List[Person]] = Field(
        default=None,
        title="experimenter(s)",
    )
    ethics_review_id: Optional[str] = Field(default=None, title="Ethics review ID")
    animal_weight_prior: Optional[Decimal] = Field(
        default=None, title="Animal weight (g)", description="Animal weight before procedure"
    )
    animal_weight_post: Optional[Decimal] = Field(
        default=None, title="Animal weight (g)", description="Animal weight after procedure"
    )
    weight_unit: MassUnit = Field(default=MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(default=None, title="Anaesthesia")
    workstation_id: Optional[str] = Field(default=None, title="Workstation ID")
    procedures: List[
        Annotated[
            Union[
                CatheterImplant,
                Craniotomy,
                FiberImplant,
                Headframe,
                IntraCerebellarVentricleInjection,
                IntraCisternalMagnaInjection,
                IntraperitonealInjection,
                IontophoresisInjection,
                MyomatrixInsertion,
                NanojectInjection,
                OtherSubjectProcedure,
                Perfusion,
                ProtectiveMaterialReplacement,
                RetroOrbitalInjection,
                SampleCollection,
            ],
            Field(discriminator="procedure_type"),
        ]
    ] = Field(title="Procedures", min_length=1)
    notes: Optional[str] = Field(default=None, title="Notes")


class Procedures(DataCoreModel):
    """Description of all procedures performed on a subject"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/procedures.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})

    schema_version: SkipValidation[Literal["2.0.0"]] = Field(default="2.0.0")
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
    ] = Field(default=[], title="Subject Procedures")
    specimen_procedures: List[SpecimenProcedure] = Field(default=[], title="Specimen Procedures")
    notes: Optional[str] = Field(default=None, title="Notes")
