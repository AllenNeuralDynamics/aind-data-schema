""" schema for various Procedures """

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from aind_data_schema_models.brain_atlas import CCFStructure
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species
from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType
from aind_data_schema_models.units import (
    ConcentrationUnit,
    CurrentUnit,
    MassUnit,
    SizeUnit,
    TimeUnit,
    UnitlessUnit,
    VolumeUnit,
)
from pydantic import Field, SkipValidation, field_validator, model_validator
from typing_extensions import Annotated

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel
from aind_data_schema.components.coordinates import Coordinate, CoordinateSystem, Origin
from aind_data_schema.components.devices import FiberProbe, MyomatrixArray
from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.reagent import Reagent
from aind_data_schema.utils.merge import merge_notes
from aind_data_schema.utils.validators import subject_specimen_id_compatibility
from aind_data_schema.utils.exceptions import FieldLengthMismatch


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


class SectionOrientation(str, Enum):
    """Orientation of sectioning"""

    CORONAL = "Coronal"
    SAGITTAL = "Sagittal"
    TRANSVERSE = "Transverse"


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
    WHC = "Whole hemisphere craniotomy"
    CIRCLE = "Circle"
    SQUARE = "Square"
    OTHER = "Other"


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


class InjectionProfile(str, Enum):
    """Injection profile"""

    BOLUS = "Bolus"
    CONTINUOUS = "Continuous"
    PULSED = "Pulsed"


class Readout(Reagent):
    """Description of a readout"""

    fluorophore: Fluorophore = Field(..., title="Fluorophore")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Excitation wavelength unit")
    stain_type: StainType = Field(..., title="Stain type")


class HCRReadout(Readout):
    """Description of a readout for HCR"""

    initiator_name: str = Field(..., title="Initiator name")
    stain_type: StainType = Field(..., title="Stain type")


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


class HCRSeries(DataModel):
    """Description of series of HCR staining rounds for mFISH"""

    codebook_name: str = Field(..., title="Codebook name")
    number_of_rounds: int = Field(..., title="Number of round")
    hcr_rounds: List[HybridizationChainReaction] = Field(..., title="Hybridization Chain Reaction rounds")
    strip_qc_compatible: bool = Field(..., title="Strip QC compatible")
    cell_id: Optional[str] = Field(default=None, title="Cell ID")


class Antibody(Reagent):
    """Description of an antibody used in immunolableing"""

    immunolabel_class: ImmunolabelClass = Field(..., title="Immunolabel class")
    fluorophore: Optional[Fluorophore] = Field(default=None, title="Fluorophore")
    mass: Decimal = Field(..., title="Mass of antibody")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")
    notes: Optional[str] = Field(default=None, title="Notes")


class PlanarSectioning(DataModel):
    """Description of a sectioning procedure performed on the coronal, sagittal, or transverse/axial plane"""

    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Sectioning coordinate system",
        description="Only required if different from the Procedures.coordinate_system",
    )
    targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")
    output_specimen_ids: List[str] = Field(..., title="Output specimen ids", min_length=1)

    section_cuts: List[List[Coordinate]] = Field(
        ...,
        title="Section start and end coordinates",
        min_length=1,
        description="Pair of coordinates for each section cut",
    )
    section_orientation: SectionOrientation = Field(..., title="Sectioning orientation")
    partial_slice: Optional[List[AnatomicalRelative]] = Field(
        default=None,
        title="Partial slice",
        description="If sectioning does not include the entire slice, indicate which part of the slice is retained.",
    )

    @field_validator("section_cuts", mode="after")
    def validate_section_cuts(cls, values):
        """Ensure all inner lists have exactly two coordinates"""
        for cut in values:
            if len(cut) != 2:
                raise ValueError(
                    "Each pair of start and end coordinates in section_cuts must have exactly two coordinates."
                )
        return values

    @model_validator(mode="after")
    def check_coord_id_length(cls, values):
        """Validator for list length of section start coordinates"""

        if not hasattr(values, "section_cuts"):  # pragma: no cover, bypass for testing
            return values

        if (len(values.section_cuts)) != len(values.output_specimen_ids):
            raise FieldLengthMismatch(cls.__name__, ["section_cuts", "output_specimen_ids"])
        return values


class SpecimenProcedure(DataModel):
    """Description of surgical or other procedure performed on a specimen"""

    procedure_type: SpecimenProcedureType = Field(..., title="Procedure type")
    procedure_name: Optional[str] = Field(default=None, title="Procedure name")
    specimen_id: str = Field(..., title="Specimen ID")
    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenters: List[Person] = Field(
        default=[],
        title="experimenter(s)",
    )
    protocol_id: Optional[List[str]] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")

    procedure_details: List[
        Annotated[
            Union[
                HCRSeries,
                Antibody,
                PlanarSectioning,
                Reagent,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(
        default=[],
        title="Procedure details",
        description="",
    )

    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="after")
    def validate_procedure_type(self):
        """Adds a validation check on procedure_type"""

        has_hcr_series = any(isinstance(detail, HCRSeries) for detail in self.procedure_details)
        has_antibodies = any(isinstance(detail, Antibody) for detail in self.procedure_details)
        has_sectioning = any(isinstance(detail, PlanarSectioning) for detail in self.procedure_details)

        if has_hcr_series + has_antibodies + has_sectioning > 1:
            raise AssertionError("SpecimenProcedure.procedure_details should only contain one type of model.")

        if self.procedure_type == SpecimenProcedureType.OTHER and not self.notes:
            raise AssertionError(
                "notes cannot be empty if procedure_type is Other. Describe the procedure in the notes field."
            )
        elif self.procedure_type == SpecimenProcedureType.HYBRIDIZATION_CHAIN_REACTION and not has_hcr_series:
            raise AssertionError("HCRSeries required if procedure_type is HCR.")
        elif self.procedure_type == SpecimenProcedureType.IMMUNOLABELING and not has_antibodies:
            raise AssertionError("Antibody required if procedure_type is Immunolabeling.")
        elif self.procedure_type == SpecimenProcedureType.SECTIONING and not has_sectioning:
            raise AssertionError("Sectioning required if procedure_type is Sectioning.")
        return self


class Anaesthetic(DataModel):
    """Description of an anaesthetic"""

    anaesthetic_type: str = Field(..., title="Type")
    duration: Decimal = Field(..., title="Duration")
    duration_unit: TimeUnit = Field(default=TimeUnit.M, title="Duration unit")
    level: Optional[Decimal] = Field(default=None, title="Level (percent)", ge=1, le=5)


class GenericSurgeryProcedure(DataModel):
    """Description of a surgery procedure performed on a subject"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    description: str = Field(..., title="Description")
    notes: Optional[str] = Field(default=None, title="Notes")


class GenericSubjectProcedure(DataModel):
    """Description of a non-surgical procedure performed on a subject"""

    start_date: date = Field(..., title="Start date")
    experimenters: Optional[List[Person]] = Field(
        default=None,
        title="experimenter(s)",
    )
    ethics_review_id: str = Field(..., title="Ethics review ID")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    description: str = Field(..., title="Description")
    notes: Optional[str] = Field(default=None, title="Notes")


class CatheterImplant(DataModel):
    """Description of a catheter implant procedure"""

    where_performed: Organization.CATHETER_IMPLANT_INSTITUTIONS = Field(..., title="Where performed")
    catheter_material: CatheterMaterial = Field(..., title="Catheter material")
    catheter_design: CatheterDesign = Field(..., title="Catheter design")
    catheter_port: CatheterPort = Field(..., title="Catheter port")
    targeted_structure: MouseAnatomyModel = Field(
        ..., title="Targeted blood vessel", description="Use options from MouseBloodVessels"
    )


class Craniotomy(DataModel):
    """Description of craniotomy procedure"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    craniotomy_type: CraniotomyType = Field(..., title="Craniotomy type")

    position: Optional[Union[Coordinate, List[AnatomicalRelative]]] = Field(default=None, title="Craniotomy position")

    size: Optional[float] = Field(default=None, title="Craniotomy size", description="Diameter or side length")
    size_unit: Optional[SizeUnit] = Field(default=None, title="Craniotomy size unit")

    protective_material: Optional[ProtectiveMaterial] = Field(default=None, title="Protective material")
    implant_part_number: Optional[str] = Field(default=None, title="Implant part number")
    dura_removed: Optional[bool] = Field(default=None, title="Dura removed")

    @model_validator(mode="after")
    def check_position(cls, values):
        """Ensure a position is provided for certain craniotomy types"""

        POS_REQUIRED = [CraniotomyType.CIRCLE, CraniotomyType.SQUARE, CraniotomyType.WHC]

        if values.craniotomy_type in POS_REQUIRED and not values.position:
            raise ValueError(f"Craniotomy.position must be provided for craniotomy type {values.craniotomy_type}")
        return values

    @model_validator(mode="after")
    def validate_size(cls, values):
        """Ensure that size is provided for certain craniotomy types"""

        SIZE_REQUIRED = [CraniotomyType.CIRCLE, CraniotomyType.SQUARE]

        if values.craniotomy_type in SIZE_REQUIRED and not values.size:
            raise ValueError(f"Craniotomy.size must be provided for craniotomy type {values.craniotomy_type}")
        return values


class Headframe(DataModel):
    """Description of headframe procedure"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    headframe_type: str = Field(..., title="Headframe type")
    headframe_part_number: str = Field(..., title="Headframe part number")
    headframe_material: Optional[HeadframeMaterial] = Field(default=None, title="Headframe material")
    well_part_number: Optional[str] = Field(default=None, title="Well part number")
    well_type: Optional[str] = Field(default=None, title="Well type")


class GroundWireImplant(DataModel):
    """Ground wire implant procedure"""

    ground_electrode_location: MouseAnatomyModel = Field(..., title="Location of ground electrode")
    ground_wire_hole: Optional[int] = Field(
        default=None, title="Ground wire hole", description="For SHIELD implants, the hole number for the ground wire"
    )
    ground_wire_material: Optional[GroundWireMaterial] = Field(default=None, title="Ground wire material")
    ground_wire_diameter: Optional[Decimal] = Field(default=None, title="Ground wire diameter")
    ground_wire_diameter_unit: Optional[SizeUnit] = Field(default=None, title="Ground wire diameter unit")


class TarsVirusIdentifiers(DataModel):
    """TARS data for a viral prep"""

    virus_tars_id: Optional[str] = Field(default=None, title="Virus ID, usually begins 'AiV'")
    plasmid_tars_alias: Optional[List[str]] = Field(
        default=None,
        title="List of plasmid aliases",
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
        title="Effective titer",
        description="Final titer of viral material, accounting for mixture/diliution",
    )
    titer_unit: Optional[str] = Field(default="gc/mL", title="Titer unit", description="For example, gc/mL")


class NonViralMaterial(Reagent):
    """Description of a non-viral injection material"""

    material_type: Literal["Reagent"] = Field(default="Reagent", title="Injection material type")
    concentration: Optional[float] = Field(
        default=None, title="Concentration", description="Must provide concentration unit"
    )
    concentration_unit: Optional[str] = Field(
        default=None, title="Concentration unit", description="For example, mg/mL"
    )


class InjectionDynamics(DataModel):
    """Description of the volume and rate of an injection"""

    profile: InjectionProfile = Field(..., title="Injection profile")

    volume: Optional[Decimal] = Field(default=None, title="Injection volume")
    volume_unit: Optional[VolumeUnit] = Field(default=None, title="Injection volume unit")

    rate: Optional[Decimal] = Field(default=None, title="Injection rate")
    rate_unit: Optional[VolumeUnit] = Field(default=None, title="Injection rate unit")

    duration: Optional[Decimal] = Field(default=None, title="Injection duration")
    duration_unit: Optional[TimeUnit] = Field(default=None, title="Injection duration unit")

    injection_current: Optional[Decimal] = Field(default=None, title="Injection current (uA)")
    injection_current_unit: Optional[CurrentUnit] = Field(default=None, title="Injection current unit")
    alternating_current: Optional[str] = Field(default=None, title="Alternating current")

    @model_validator(mode="after")
    def check_volume_or_current(cls, values):
        """Check that either volume or injection_current is provided"""
        if not values.volume and not values.injection_current:
            raise ValueError("Either volume or injection_current must be provided.")
        return values


class Injection(DataModel):
    """Description of an injection procedure"""

    injection_materials: List[
        Annotated[Union[ViralMaterial, NonViralMaterial], Field(..., discriminator="material_type")]
    ] = Field(..., title="Injection material", min_length=1)
    targeted_structure: Optional[MouseAnatomyModel] = Field(
        default=None, title="Injection target", description="Use InjectionTargets"
    )
    relative_position: Optional[List[AnatomicalRelative]] = Field(default=None, title="Relative position")

    dynamics: List[InjectionDynamics] = Field(
        ..., title="Injection dynamics", description="List of injection events, one per location/depth"
    )
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")


class BrainInjection(Injection):
    """Description of a brain injection procedure"""

    coordinates: List[Coordinate] = Field(..., title="Injection coordinate")
    targeted_structure: Optional[CCFStructure.ONE_OF] = Field(default=None, title="Injection targeted brain structure")

    @model_validator(mode="after")
    def check_lengths(values):
        """Validator for list length of injection volumes and depths"""

        dynamics_len = len(values.dynamics)
        coords_len = len(values.coordinates)

        if dynamics_len != coords_len:
            raise ValueError("Unmatched list sizes for injection volumes and coordinate depths")
        return values


class SampleCollection(DataModel):
    """Description of a single sample collection"""

    sample_type: SampleType = Field(..., title="Sample type")
    time: AwareDatetimeWithDefault = Field(..., title="Collection time")
    collection_volume: Decimal = Field(..., title="Collection volume")
    collection_volume_unit: VolumeUnit = Field(..., title="Collection volume unit")
    collection_method: Optional[str] = Field(default=None, title="Collection method for terminal collection")


class TrainingProtocol(DataModel):
    """Description of an animal training protocol"""

    training_name: str = Field(..., title="Training protocol name")
    protocol_id: Optional[str] = Field(default=None, title="Training protocol ID")
    start_date: date = Field(..., title="Training protocol start date")
    end_date: Optional[date] = Field(default=None, title="Training protocol end date")
    notes: Optional[str] = Field(default=None, title="Notes")


class OphysProbe(DataModel):
    """Description of an implanted ophys probe"""

    ophys_probe: FiberProbe = Field(..., title="Fiber probe")
    targeted_structure: CCFStructure.ONE_OF = Field(..., title="Targeted structure")

    coordinate: Coordinate = Field(..., title="Stereotactic coordinate")


class FiberImplant(DataModel):
    """Description of an implant procedure"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    probes: List[OphysProbe] = Field(..., title="Ophys Probes")


class WaterRestriction(DataModel):
    """Description of a water restriction procedure"""

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
    """Description of a contact on a myomatrix thread"""

    body_part: MouseAnatomyModel = Field(..., title="Body part of contact insertion", description="Use MouseBodyParts")
    relative_position: AnatomicalRelative = Field(
        ..., title="Relative position", description="Position relative to procedures coordinate system"
    )
    muscle: MouseAnatomyModel = Field(..., title="Muscle of contact insertion", description="Use MouseEmgMuscles")
    in_muscle: bool = Field(..., title="In muscle")


class MyomatrixThread(DataModel):
    """Description of a thread of a myomatrix array"""

    ground_electrode_location: MouseAnatomyModel = Field(
        ..., title="Location of ground electrode", description="Use GroundWireLocations"
    )
    contacts: List[MyomatrixContact] = Field(..., title="Contacts")


class MyomatrixInsertion(DataModel):
    """Description of a Myomatrix array insertion for EMG"""

    ground_electrode: GroundWireImplant = Field(..., title="Ground electrode")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    myomatrix_array: MyomatrixArray = Field(..., title="Myomatrix array")
    threads: List[MyomatrixThread] = Field(..., title="Array threads")


class Perfusion(DataModel):
    """Description of a perfusion procedure that creates a specimen"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    output_specimen_ids: List[str] = Field(
        ...,
        title="Specimen ID",
        description="IDs of specimens resulting from this procedure.",
    )

    @field_validator("output_specimen_ids", mode="before")
    def validate_output_specimen_ids(cls, values: List[str]):
        """Sort specimen IDs"""
        return sorted(values)


class Surgery(DataModel):
    """Description of subject procedures performed at one time"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
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

    # Coordinate system
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Surgery coordinate system",
        description="Only use this field when different from the Procedures.coordinate_system",
    )

    # Measured coordinates
    measured_coordinates: Optional[Dict[Origin, Coordinate]] = Field(
        default=None,
        title="Measured coordinates",
        description="Coordinates measured during the procedure, for example Bregma and Lambda",
    )

    procedures: List[
        Annotated[
            Union[
                CatheterImplant,
                Craniotomy,
                FiberImplant,
                Headframe,
                BrainInjection,
                Injection,
                MyomatrixInsertion,
                GenericSurgeryProcedure,
                Perfusion,
                SampleCollection,
            ],
            Field(discriminator="object_type"),
        ]
    ] = Field(title="Procedures", min_length=1)
    notes: Optional[str] = Field(default=None, title="Notes")


class Procedures(DataCoreModel):
    """Description of all procedures performed on a subject"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/procedures.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})

    schema_version: SkipValidation[Literal["2.0.20"]] = Field(default="2.0.20")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    subject_procedures: List[
        Annotated[
            Union[Surgery, TrainingProtocol, WaterRestriction, GenericSubjectProcedure],
            Field(discriminator="object_type"),
        ]
    ] = Field(default=[], title="Subject Procedures")
    specimen_procedures: List[SpecimenProcedure] = Field(default=[], title="Specimen Procedures")

    # Coordinate system
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Coordinate System",
        description="Required when coordinates are provided in the procedures",
    )

    notes: Optional[str] = Field(default=None, title="Notes")

    @field_validator("specimen_procedures", mode="after")
    def validate_identical_specimen_ids(cls, v, values):
        """Validate that all specimen_id fields are identical in the specimen_procedures"""

        if v:
            specimen_ids = [spec_proc.specimen_id for spec_proc in v]

            if any(spec_id != specimen_ids[0] for spec_id in specimen_ids):
                raise ValueError("All specimen_id must be identical in the specimen_procedures.")

        return v

    @model_validator(mode="after")
    def validate_subject_specimen_ids(values):
        """Validate that the subject_id and specimen_id match"""

        # Return if no specimen procedures
        if values.specimen_procedures:
            subject_id = values.subject_id
            specimen_ids = [spec_proc.specimen_id for spec_proc in values.specimen_procedures]

            if any(not subject_specimen_id_compatibility(subject_id, spec_id) for spec_id in specimen_ids):
                raise ValueError("specimen_id must be an extension of the subject_id.")

        return values

    def __add__(self, other: "Procedures") -> "Procedures":
        """Combine two Procedures objects"""

        if not self.schema_version == other.schema_version:
            raise ValueError("Schema versions must match to combine Procedures")

        if not self.subject_id == other.subject_id:
            raise ValueError("Subject IDs must match to combine Procedures objects.")

        return Procedures(
            subject_id=self.subject_id,
            subject_procedures=self.subject_procedures + other.subject_procedures,
            specimen_procedures=self.specimen_procedures + other.specimen_procedures,
            notes=merge_notes(self.notes, other.notes),
        )
