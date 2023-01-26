""" ephys session description and related objects """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field

from ..base import AindCoreModel, AindModel
from ..device import PowerUnit, SizeUnit
from .ephys_rig import Coordinates3d


class SessionType(Enum):
    """Session type name"""

    TEST = "Test"
    OPTO = "Optotagging"
    RF_MAPPING = "Receptive field mapping"


class CcfVersion(Enum):
    """CCF version"""

    CCFv3 = "CCFv3"


class CcfCoords(AindModel):
    """Coordinates in CCF template space"""

    ml: float = Field(..., title="ML")
    ap: float = Field(..., title="AP")
    dv: float = Field(..., title="DV")
    unit: SizeUnit = Field(SizeUnit.UM, title="Coordinate unit")
    ccf_version: CcfVersion = Field(CcfVersion.CCFv3, title="CCF version")


class ManipulatorModule(AindModel):
    """A module connected to a 3-axis manipulator"""

    primary_targeted_structure: str = Field(..., title="Targeted structure")
    targeted_ccf_coordinates: Optional[List[CcfCoords]] = Field(
        None,
        title="Targeted CCF coordinates",
    )
    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )


class Laser(AindModel):
    """Laser used in a LaserModule"""

    name: str = Field(..., title="Laser name (must match rig JSON)")
    power_level: float = Field(..., title="Power level used in this session", units="mW")
    power_unit: PowerUnit = Field(PowerUnit.MW, title="Power unit")


class LaserModule(ManipulatorModule):
    """Laser Module used in a Stream"""

    lasers: List[Laser] = Field(..., title="Active lasers in this module")


class EphysProbe(ManipulatorModule):
    """Probe recorded in a Stream"""

    name: str = Field(..., title="Ephys probe name (must match rig JSON)")
    other_targeted_structures: Optional[List[str]] = None


class DAQDevice(AindModel):
    """Data acquisition device recorded in a Stream"""

    name: str = Field(..., title="DAQ device name (must match rig JSON)")


class Camera(AindModel):
    """Camera recorded in a Stream"""

    name: str = Field(..., title="Camera name (must match rig JSON)")


class Stream(AindModel):
    """Stream of data with a start and stop time"""

    stream_start_time: datetime = Field(..., title="Stream start time")
    stream_end_time: datetime = Field(..., title="Stream stop time")
    probes: Optional[List[EphysProbe]] = Field(None, title="Probes", unique_items=True)
    laser_modules: Optional[List[LaserModule]] = Field(None, title="Laser modules", unique_items=True)
    daqs: Optional[List[DAQDevice]] = Field(None, title="DAQ devices", unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title="Cameras", unique_items=True)


class EphysSession(AindCoreModel):
    """Description of an ephys recording session"""

    schema_version: str = Field("0.3.1", description="schema version", title="Version", const=True)
    experimenter_full_name: str = Field(
        ...,
        description="First and last name of the experimenter.",
        title="Experimenter full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    subject_id: str = Field(..., title="Subject ID")
    session_type: SessionType = Field(..., title="Session type")
    session_description: Optional[str] = Field(None, title="Session description")
    stimulus_protocol_id: Optional[str] = Field(None, title="Stimulus protocol ID")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
        unique_items=True,
    )
    ccf_coordinate_transform: Optional[str] = Field(
        None,
        description="Path to file that details the CCF-to-lab coordinate transform",
        title="CCF coordinate transform",
    )
    notes: Optional[str] = None
