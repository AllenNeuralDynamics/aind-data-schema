""" schema for MRI Scan """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel
from aind_data_schema.device import Device
from aind_data_schema.imaging.acquisition import Axis
from aind_data_schema.imaging.tile import Scale3dTransform
from aind_data_schema.procedures import Anaesthetic, WeightUnit


class MriScanSequence(Enum):
    """MRI scan sequence"""

    RARE = "RARE"


class ScannerLocation(Enum):
    """location of scanner"""

    FRED_HUTCH = "Fred Hutch"
    UW_SLU = "UW SLU"


class MagneticStrength(Enum):
    """Strength of magnet"""

    MRI_7T = 7
    MRI_14T = 14


class Scanner(Device):
    """Description of a MRI Scanner"""

    scanner_location: ScannerLocation = Field(..., title="Scanner site location")
    magnetic_strength: MagneticStrength = Field(..., title="Magnetic strength (T)", units="T")
    magnetic_strength_unit: str = Field("T", title="Magnetic strength unit")


class MriSession(AindCoreModel):
    """Description of an MRI scan"""

    schema_version: str = Field("0.1.3", description="schema version", title="Version", const=True)
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: Optional[datetime] = Field(None, title="Session end time")
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
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
    scan_sequence: MriScanSequence = Field(..., title="Scan sequence")
    mri_scanner: Scanner = Field(..., title="MRI scanner")
    axes: List[Axis] = Field(..., title="Imaging axes")
    voxel_sizes: Scale3dTransform = Field(
        ..., title="Voxel sizes", description="Size of voxels in order as specified in axes"
    )
    notes: Optional[str] = Field(None, title="Notes")
