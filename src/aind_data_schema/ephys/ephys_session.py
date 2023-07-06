""" ephys session description and related objects """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.device import AngleUnit, Coordinates3d, PowerUnit, SizeUnit
from aind_data_schema.stimulus import StimulusPresentation


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

    ml: Decimal = Field(..., title="ML")
    ap: Decimal = Field(..., title="AP")
    dv: Decimal = Field(..., title="DV")
    unit: SizeUnit = Field(SizeUnit.UM, title="Coordinate unit")
    ccf_version: CcfVersion = Field(CcfVersion.CCFv3, title="CCF version")


class DomeModule(AindModel):
    """Movable module that is mounted on the ephys dome insertion system"""

    # required fields
    assembly_name: str = Field(..., title="Assembly name")
    arc_angle: Decimal = Field(..., title="Arc Angle", units="degrees")
    module_angle: Decimal = Field(..., title="Module Angle", units="degrees")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")

    # optional fields
    rotation_angle: Optional[Decimal] = Field(0.0, title="Rotation Angle", units="degrees")
    coordinate_transform: Optional[str] = Field(
        None, title="Transform from local manipulator axes to rig", description="Path to coordinate transform"
    )
    calibration_date: Optional[datetime] = Field(None, title="Date on which coordinate transform was last calibrated")
    notes: Optional[str] = Field(None, title="Notes")


class ManipulatorModule(DomeModule):
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
    power_level: Decimal = Field(..., title="Power level used in this session", units="mW")
    power_unit: PowerUnit = Field(PowerUnit.MW, title="Power unit")


class LaserModule(ManipulatorModule):
    """Laser Module used in a Stream"""

    lasers: List[Laser] = Field(..., title="Active lasers in this module")


class EphysProbe(AindModel):
    """Probes in a EphysProbeModule"""

    name: str = Field(..., title="Ephys probe name (must match rig JSON)")
    other_targeted_structures: Optional[List[str]] = None


class EphysModule(ManipulatorModule):
    """Probe recorded in a Stream"""

    ephys_probes: List[EphysProbe] = Field(..., title="Ephys probes used in this module")


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
    ephys_modules: Optional[List[EphysModule]] = Field(None, title="Ephys modules", unique_items=True)
    laser_modules: Optional[List[LaserModule]] = Field(None, title="Laser modules", unique_items=True)
    daqs: Optional[List[DAQDevice]] = Field(None, title="DAQ devices", unique_items=True)
    cameras: Optional[List[Camera]] = Field(None, title="Cameras", unique_items=True)
    stimulus_presentations: Optional[List[StimulusPresentation]] = Field(None, title="Stimulus")
    notes: Optional[str] = Field(None, title="Notes")


class EphysSession(AindCoreModel):
    """Description of an ephys recording session"""

    schema_version: str = Field("0.4.5", description="schema version", title="Version", const=True)
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: datetime = Field(..., title="Session end time")
    subject_id: str = Field(..., title="Subject ID")
    session_type: SessionType = Field(..., title="Session type")
    session_description: Optional[str] = Field(None, title="Session description")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    stick_microscopes: Optional[List[DomeModule]] = Field(
        ..., title="Stick microscopes", description="Must match stick microscope assemblies in rig file"
    )
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
    notes: Optional[str] = Field(None, title="Notes")
