""" schema for MRI Scan """

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import Field, ValidationInfo, field_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.core.acquisition import Axis
from aind_data_schema.core.procedures import Anaesthetic
from aind_data_schema.imaging.tile import Scale3dTransform
from aind_data_schema.models.devices import Scanner
from aind_data_schema.models.process_names import ProcessName
from aind_data_schema.models.units import MassUnit, TimeUnit


class MriScanSequence(str, Enum):
    """MRI scan sequence"""

    RARE = "RARE"
    OTHER = "Other"


class ScanType(str, Enum):
    """Type of scan"""

    SETUP = "Set Up"
    SCAN_3D = "3D Scan"


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
    processing_steps: List[
        Literal[
            ProcessName.FIDUCIAL_SEGMENTATION,
            ProcessName.REGISTRATION_TO_TEMPLATE,
            ProcessName.SKULL_STRIPPING,
        ]
    ] = Field([])
    echo_time: Decimal = Field(..., title="Echo time (ms)")
    effective_echo_time: Decimal = Field(..., title="Effective echo time (ms)")
    echo_time_unit: TimeUnit = Field(TimeUnit.MS, title="Echo time unit")
    repetition_time: Decimal = Field(..., title="Repetition time (ms)")
    repetition_time_unit: TimeUnit = Field(TimeUnit.MS, title="Repetition time unit")
    additional_scan_parameters: Dict[str, Any] = Field(..., title="Parameters")
    notes: Optional[str] = Field(None, title="Notes", validate_default=True)

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("scan_sequence_type") == MriScanSequence.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if scan_sequence_type is Other."
                " Describe the scan_sequence_type in the notes field."
            )
        return value


class MriSession(AindCoreModel):
    """Description of an MRI scan"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/mri_session.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.2.8"] = Field("0.2.8")
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
    )
    animal_weight_post: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
    )
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(None, title="Anaesthesia")
    mri_scanner: Scanner = Field(..., title="MRI scanner")
    scans: List[MRIScan] = Field(..., title="MRI scans")
    notes: Optional[str] = Field(None, title="Notes")
