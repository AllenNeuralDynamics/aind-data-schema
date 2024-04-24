""" schema for MRI Scan """

from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional

from pydantic import Field, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import AindCoreModel, AindGenericType, AindModel, AwareDatetimeWithDefault
from aind_data_schema.core.procedures import Anaesthetic
from aind_data_schema.models.coordinates import Rotation3dTransform, Scale3dTransform, Translation3dTransform
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


class SubjectPosition(str, Enum):
    """Subject position"""

    PRONE = "Prone"
    SUPINE = "Supine"


class MRIScan(AindModel):
    """Description of a 3D scan"""

    scan_index: int = Field(..., title="Scan index")
    scan_type: ScanType = Field(..., title="Scan type")
    primary_scan: bool = Field(
        ..., title="Primary scan", description="Indicates the primary scan used for downstream analysis"
    )
    scan_sequence_type: MriScanSequence = Field(..., title="Scan sequence")
    rare_factor: Optional[int] = Field(None, title="RARE factor")
    echo_time: Decimal = Field(..., title="Echo time (ms)")
    effective_echo_time: Optional[Decimal] = Field(None, title="Effective echo time (ms)")
    echo_time_unit: TimeUnit = Field(TimeUnit.MS, title="Echo time unit")
    repetition_time: Decimal = Field(..., title="Repetition time (ms)")
    repetition_time_unit: TimeUnit = Field(TimeUnit.MS, title="Repetition time unit")
    # fields required to get correct orientation
    vc_orientation: Optional[Rotation3dTransform] = Field(None, title="Scan orientation")
    vc_position: Optional[Translation3dTransform] = Field(None, title="Scan position")
    subject_position: SubjectPosition = Field(..., title="Subject position")
    # other fields
    voxel_sizes: Optional[Scale3dTransform] = Field(None, title="Voxel sizes", description="Resolution")
    processing_steps: List[
        Literal[
            ProcessName.FIDUCIAL_SEGMENTATION,
            ProcessName.IMAGE_ATLAS_ALIGNMENT,
            ProcessName.SKULL_STRIPPING,
        ]
    ] = Field([])
    additional_scan_parameters: AindGenericType = Field(..., title="Parameters")
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

    @model_validator(mode="after")
    def validate_primary_scan(self):
        """Validate that primary scan has vc_orientation and vc_position fields"""

        if self.primary_scan:
            if not self.vc_orientation or not self.vc_position or not self.voxel_sizes:
                raise ValueError("Primary scan must have vc_orientation, vc_position, and voxel_sizes fields")

        return self


class MriSession(AindCoreModel):
    """Description of an MRI scan"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/mri_session.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.3.7"] = Field("0.3.7")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    session_start_time: AwareDatetimeWithDefault = Field(..., title="Session start time")
    session_end_time: Optional[AwareDatetimeWithDefault] = Field(None, title="Session end time")
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
