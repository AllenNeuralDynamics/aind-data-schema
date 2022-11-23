""" ephys session description and related objects """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from ..base import AindSchema


class SessionType(Enum):
    """Session type name"""

    TEST = "Test"
    FORAGING_A = "Foraging A"
    SPONTANEOUS = "Spontaneous"
    FORAGING_B = "Foraging B"


class ExpectedDataStream(Enum):
    """Names of data streams to expect in recording"""

    NEUROPIXELS_PROBES = "Neuropixels probes"
    BODY_CAMERA = "Body camera"
    FACE_CAMERA = "Face camera"
    EYE_CAMERA = "Eye camera"
    BONSAI_FILE = "Bonsai file"
    HARP_FILE = "Harp bin file"
    OTHER = "Other"


class CcfVersion(Enum):
    """CCF version"""

    CCFv3 = "CCFv3"


class Coordinates3d(BaseModel):
    """Description of 3d coordinates in mm"""

    x: float = Field(..., title="X (mm)", units="mm")
    y: float = Field(..., title="Y (mm)", units="mm")
    z: float = Field(..., title="Z (mm)", units="mm")


class CcfCoords(BaseModel):
    """Coordinates in CCF template space"""

    ml: float = Field(..., title="ML (um)", units="um")
    ap: float = Field(..., title="AP (um)", units="um")
    dv: float = Field(..., title="DV (um)", units="um")
    ccf_version: CcfVersion = Field(CcfVersion.CCFv3, title="CCF version")


class AngleName(Enum):
    """Euler angle name"""

    XY = "XY"
    XZ = "XZ"
    YZ = "YZ"


class ManipulatorAngles(BaseModel):
    """Description of manipulator angle"""

    name: AngleName = Field(..., title="AngleName")
    value: float = Field(..., title="Value (deg)", units="deg")


class Laser(BaseModel):
    """Description of a laser"""

    name: str = Field(..., title="Name")
    wavelength: int = Field(..., title="Wavelength (nm)", units="nm")
    power: float = Field(..., title="Power (mW)", units="mW")
    targeted_structure: str = Field(..., title="Targeted structure")
    targeted_ccf_coordinates: CcfCoords = Field(
        ...,
        title="Targeted CCF coordinates",
    )

    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )
    manipulator_angles: List[ManipulatorAngles] = Field(
        ..., title="Manipulator angles", unique_items=True
    )


class EphysProbe(BaseModel):
    """Description of an ephys probe"""

    name: str = Field(..., title="Name")
    tip_targeted_structure: str
    other_targeted_structures: Optional[str] = None
    targeted_ccf_coordinates: CcfCoords = Field(
        ...,
        title="Targeted CCF coordinates",
    )

    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )
    manipulator_angles: List[ManipulatorAngles] = Field(
        ..., title="Manipulator angles", unique_items=True
    )


class Stream(BaseModel):
    """Stream of data with a start and stop time"""

    stream_start_time: datetime = Field(..., title="Stream start time")
    stream_stop_time: datetime = Field(..., title="Stream stop time")
    probes: List[EphysProbe] = Field(..., title="Probes", unique_items=True)
    lasers: List[Laser] = Field(..., title="Lasers", unique_items=True)


class EphysSession(AindSchema):
    """Description of an ephys recording session"""

    schema_version: str = Field(
        "0.2.0", description="schema version", title="Version", const=True
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    subject_id: int = Field(..., title="Subject ID")
    session_type: SessionType = Field(..., title="Session type")
    stimulus_protocol_id: Optional[str] = Field(
        None, title="Stimulus protocol ID"
    )
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    expected_data_streams: Optional[List[ExpectedDataStream]] = None
    probe_streams: List[Stream] = Field(
        ..., title="Probe streams", unique_items=True
    )
    coordinate_transform: Optional[str] = Field(
        None,
        description="Path to file that details the coordinate transform.",
        title="Coordinate transform",
    )
    notes: Optional[str] = None
