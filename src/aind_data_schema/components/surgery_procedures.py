"""Surgery procedures components for AIND data schema."""

from enum import Enum
from typing import List, Optional, Union

from aind_data_schema_models.brain_atlas import BrainStructureModel
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import SizeUnit, TimeUnit, VolumeUnit
from pydantic import Field, field_validator, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel
from aind_data_schema.components.configs import CatheterConfig, ProbeConfig
from aind_data_schema.components.coordinates import TRANSFORM_TYPES, Translation
from aind_data_schema.components.devices import Catheter, EphysProbe, FiberProbe, MyomatrixArray
from aind_data_schema.components.injection_procedures import Injection


class ProtectiveMaterial(str, Enum):
    """Name of material applied to craniotomy"""

    AGAROSE = "Agarose"
    DURAGEL = "Duragel"
    KWIK_CAST = "Kwik-Cast"
    SORTA_CLEAR = "SORTA-clear"
    OTHER = "Other - see notes"


class SampleType(str, Enum):
    """Sample type"""

    BLOOD = "Blood"
    OTHER = "Other"


class GroundWireMaterial(str, Enum):
    """Ground wire material name"""

    SILVER = "Silver"
    PLATINUM_IRIDIUM = "Platinum iridium"


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


class CatheterImplant(DataModel):
    """Description of a catheter implant procedure"""

    where_performed: Organization.CATHETER_IMPLANT_INSTITUTIONS = Field(..., title="Where performed")
    implanted_device: Catheter = Field(
        ...,
        title="Implanted device",
    )  # note: exact field name is used by a validator
    device_config: CatheterConfig = Field(
        ...,
        title="Device configuration",
    )  # note: exact field name is used by a validator


class Anaesthetic(DataModel):
    """Description of an anaesthetic"""

    anaesthetic_type: str = Field(..., title="Type")
    duration: float = Field(..., title="Duration")
    duration_unit: TimeUnit = Field(default=TimeUnit.M, title="Duration unit")
    level: Optional[float] = Field(default=None, title="Level (percent)", ge=1, le=5)


class GenericSurgeryProcedure(DataModel):
    """Description of a surgery procedure performed on a subject"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    description: str = Field(..., title="Description")
    notes: Optional[str] = Field(default=None, title="Notes")


class Craniotomy(DataModel):
    """Description of craniotomy procedure"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    craniotomy_type: CraniotomyType = Field(..., title="Craniotomy type")

    coordinate_system_name: Optional[str] = Field(default=None, title="Coordinate system name")
    position: Optional[Union[Translation, List[AnatomicalRelative]]] = Field(default=None, title="Craniotomy position")

    size: Optional[float] = Field(default=None, title="Craniotomy size", description="Diameter or side length")
    size_unit: Optional[SizeUnit] = Field(default=None, title="Craniotomy size unit")

    protective_material: Optional[ProtectiveMaterial] = Field(default=None, title="Protective material")
    implant_part_number: Optional[str] = Field(default=None, title="Implant part number")
    dura_removed: Optional[bool] = Field(default=None, title="Dura removed")

    @model_validator(mode="after")
    def check_system_if_position(cls, values):
        """Ensure that coordinate_system_name is provided if position is provided"""

        if values.position and not values.coordinate_system_name:
            raise ValueError("Craniotomy.coordinate_system_name must be provided if Craniotomy.position is provided")
        return values

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


class ProbeImplant(DataModel):
    """Description of a probe (fiber, ephys) implant procedure"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    implanted_device: Union[EphysProbe, FiberProbe] = Field(
        ...,
        title="Implanted device",
    )  # note: exact field name is used by a validator
    device_config: ProbeConfig = Field(
        ...,
        title="Device configuration",
    )  # note: exact field name is used by a validator


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
    ground_wire_diameter: Optional[float] = Field(default=None, title="Ground wire diameter")
    ground_wire_diameter_unit: Optional[SizeUnit] = Field(default=None, title="Ground wire diameter unit")


class BrainInjection(Injection):
    """Description of an injection procedure into a brain"""

    coordinate_system_name: str = Field(..., title="Coordinate system name")
    coordinates: List[TRANSFORM_TYPES] = Field(..., title="Injection coordinate, depth, and rotation")
    targeted_structure: Optional[BrainStructureModel] = Field(default=None, title="Injection targeted brain structure")

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
    collection_volume: float = Field(..., title="Collection volume")
    collection_volume_unit: VolumeUnit = Field(..., title="Collection volume unit")
    collection_method: Optional[str] = Field(default=None, title="Collection method for terminal collection")


class MyomatrixInsertion(DataModel):
    """Description of a Myomatrix array insertion for EMG"""

    protocol_id: Optional[str] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")

    ground_electrode: GroundWireImplant = Field(..., title="Ground electrode")

    implanted_device: MyomatrixArray = Field(
        ...,
        title="Implanted device",
    )  # note: exact field name is used by a validator


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
