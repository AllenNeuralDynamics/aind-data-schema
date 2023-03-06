""" schema for MRI Scan """

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import Field

from ..base import AindModel
from ..procedures import WeightUnit, Anaesthetic


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


class MriScan(AindModel):
    """Description of an MRI scan"""

    describedBy: str = Field(
        "https://github.com/AllenNeuralDynamics/data_schema/blob/main/schemas/ephys/mri_session.py",
        description="The URL reference to the schema.",
        title="Described by",
        const=True,
    )
    schema_version: str = Field("0.0.1", description="schema version", title="Version", const=True)
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )
    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    protocol_id: str = Field(..., title="Protocol ID", description="DOI for protocols.io")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    animal_weight_prior: Optional[float] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
        units="g",
    )
    animal_weight_post: Optional[float] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
        units="g",
    )
    weight_unit: WeightUnit = Field(WeightUnit.G, title="Weight unit")
    anaesthesia: Optional[Anaesthetic] = Field(None, title="Anaesthesia")
    scan_sequence: MriScanSequence = Field(..., title="Scan sequence")
    scanner_location: ScannerLocation = Field(..., title="Scanner location")
    magnetic_strength: MagneticStrength = Field(..., title="Magnetic strength (T)", units="T")
    magnetic_strength_unit: str = Field("T", title="Magnetic strength unit")
    resolution: float = Field(..., title="Resolution")
    notes: Optional[str] = Field(None, title="Notes")
