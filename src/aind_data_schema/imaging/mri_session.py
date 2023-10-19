""" schema for MRI Scan """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, root_validator
from pydantic.typing import Literal

from aind_data_schema.base import AindCoreModel, AindModel, EnumSubset
from aind_data_schema.device import Device
from aind_data_schema.imaging.acquisition import Axis
from aind_data_schema.imaging.tile import Scale3dTransform
from aind_data_schema.procedures import Anaesthetic
from aind_data_schema.processing import ProcessName
from aind_data_schema.utils.units import MassUnit, TimeUnit


class MriScanSequence(Enum):
    """MRI scan sequence"""

    RARE = "RARE"
    OTHER = "Other"


class ScanType(Enum):
    """Type of scan"""

    SETUP = "Set Up"
    SCAN_3D = "3D Scan"


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

    device_type: Literal["Scanner"] = Field("Scanner", const=True, readOnly=True)
    scanner_location: ScannerLocation = Field(..., title="Scanner location")
    magnetic_strength: MagneticStrength = Field(..., title="Magnetic strength (T)", units="T")
    magnetic_strength_unit: str = Field("T", title="Magnetic strength unit")


class MRIScan(AindModel):
    """Description of a 3D scan"""

    scan_type: ScanType = Field(..., title="Scan type")
    primary_scan: bool = Field(
        ..., title="Primary scan", description="Indicates the primary scan used for downstream analysis"
    )
    scan_sequence_type: MriScanSequence = Field(..., title="Scan sequence")
    axes: List[Axis] = Field(..., title="Imaging axes")
    voxel_sizes: Scale3dTransform = Field(
        ..., title="Voxel sizes", description="Size of voxels in order as specified in axes"
    )
    processing_steps: Optional[
        List[
            EnumSubset[
                ProcessName.FIDUCIAL_SEGMENTATION,
                ProcessName.REGISTRATION_TO_TEMPLATE,
                ProcessName.SKULL_STRIPPING,
            ]
        ]
    ]
    echo_time: Decimal = Field(..., title="Echo time (ms)")
    effective_echo_time: Decimal = Field(..., title="Effective echo time (ms)")
    echo_time_unit: TimeUnit = Field(TimeUnit.MS, title="Echo time unit")
    repetition_time: Decimal = Field(..., title="Repetition time (ms)")
    repetition_time_unit: TimeUnit = Field(TimeUnit.MS, title="Repetition time unit")
    additional_scan_parameters: Dict[str, Any] = Field(..., title="Parameters")
    notes: Optional[str] = Field(None, title="Notes")

    @root_validator
    def validate_other(cls, v):
        """Validator for other/notes"""

        if v.get("scan_sequence_type") == MriScanSequence.OTHER and not v.get("notes"):
            raise ValueError(
                "Notes cannot be empty if scan_sequence_type is Other.",
                "Describe the scan_sequence_type in the notes field.",
            )
        return v


class MriSession(AindCoreModel):
    """Description of an MRI scan"""

    schema_version: str = Field("0.1.12", description="schema version", title="Version", const=True)
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
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(None, title="Anaesthesia")
    mri_scanner: Scanner = Field(..., title="MRI scanner")
    scans: List[MRIScan] = Field(..., title="MRI scans")
    notes: Optional[str] = Field(None, title="Notes")
