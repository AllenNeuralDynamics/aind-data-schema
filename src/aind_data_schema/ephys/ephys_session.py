""" ephys session description and related objects """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field
from ..base import AindCoreModel, AindModel


class SessionType(Enum):
    """Session type name"""

    TEST = "Test"
    OPTO = "Optotagging"
    RF_MAPPING = "Receptive field mapping"


class CcfVersion(Enum):
    """CCF version"""

    CCFv3 = "CCFv3"


class Coordinates3d(AindModel):
    """Description of 3d coordinates in mm"""

    x: float = Field(..., title="X (mm)", units="mm")
    y: float = Field(..., title="Y (mm)", units="mm")
    z: float = Field(..., title="Z (mm)", units="mm")


class CcfCoords(AindModel):
    """Coordinates in CCF template space"""

    ml: float = Field(..., title="ML (um)", units="um")
    ap: float = Field(..., title="AP (um)", units="um")
    dv: float = Field(..., title="DV (um)", units="um")
    ccf_version: CcfVersion = Field(CcfVersion.CCFv3, title="CCF version")


class ManipulatorModule(AindModel):
    """A module connected to a 3-axis manipulator"""

    primary_targeted_structure: str = Field(..., title="Targeted structure")
    targeted_ccf_coordinates: Optional[CcfCoords] = Field(
        None,
        title="Targeted CCF coordinates",
    )
    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )

class LaserModule(ManipulatorModule):
    """Laser used in a Stream"""

    name: str = Field(..., title="Laser module name (must match rig JSON)")
    

class EphysProbe(ManipulatorModule):
    """Probe recorded in a Stream"""

    name: str = Field(..., title="Ephys probe name (must match rig JSON)")
    other_targeted_structures: Optional[List[str]] = None
    

class DAQ(AindModel):
    """DAQ recorded in a Stream"""
    
    name: str = Field(..., title="DAQ name (must match rig JSON)")


class Camera(AindModel):
    """Camera recorded in a Stream"""

    name: str = Field(..., title="Camera name (must match rig JSON)")


class Stream(AindModel):
    """Stream of data with a start and stop time"""

    start_time: datetime = Field(..., title="Stream start time")
    end_time: datetime = Field(..., title="Stream stop time")
    probes: List[EphysProbe] = Field(..., title="Probes", unique_items=True)
    lasers: List[LaserModule] = Field(..., title="Lasers", unique_items=True)
    daqs: List[DAQ] = Field(..., title="DAQs", unique_items=True)
    cameras: List[Camera] = Field(..., title="Cameras", unique_items=True)


class EphysSession(AindCoreModel):
    """Description of an ephys recording session"""

    schema_version: str = Field(
        "0.2.1", description="schema version", title="Version", const=True
    )
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    start_time: datetime = Field(..., title="Session start time")
    end_time: datetime = Field(..., title="Session end time")
    subject_id: Optional[int] = Field(1, title="Subject ID; 1 = Test subject")
    session_type: SessionType = Field(..., title="Session type")
    session_description: Optional[str] = Field(
        None, title="Session description"
    )
    stimulus_protocol_id: Optional[str] = Field(
        None, title="Stimulus protocol ID"
    )
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    expected_data_streams: List[Stream] = Field(
        ..., 
        title="Expected data streams", 
        description="A data stream is a collection of devices that are recorded simultaneously. Each session can include multiple streams (e.g., if the manipulators are moved to a new location)",
        unique_items=True
    )
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        description="Path to file that details the CCF-to-lab coordinate transform",
        title="CCF coordinate transform",
    )
    notes: Optional[str] = None
