from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal

from pydantic import Field

from .base import AindModel

from device import  Tube, Treadmill, Disc, Camera, Lens, Filter, Monitor, SizeUnit, AngleUnit, Software

class RelativePosition(AindModel):
    """Set of 6 values describing relative position on a rig"""
    # required fields
    pitch: Optional[float] = Field(None, title="Angle pitch (deg)", units="deg", ge=0, le=360)
    yaw: Optional[float] = Field(None, title="Angle yaw (deg)", units="deg", ge=0, le=360)
    roll: Optional[float] = Field(None, title="Angle roll (deg)", units="deg", ge=0, le=360)
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")

    x: Optional[float] = Field(None, title="Position X (mm)", units="mm")
    y: Optional[float] = Field(None, title="Position Y (mm)", units="mm")
    z: Optional[float] = Field(None, title="Position Z (mm)", units="mm")
    position_unit: SizeUnit = Field(SizeUnit.MM, title="Position unit")

    # optional fields
    coordinate_system: Optional[str] = Field(None, title="Description of the coordinate system used")


class WaterDelivery(AindModel):
    """Description of water delivery system"""

    # required fields
    spout_diameter: str = Field(..., title="Spout diameter", units="mm")
    spout_placement: RelativePosition = Field(..., title="Spout stage placement")
    stage_type: str = Field(..., title="Stage build type")
    calibration: dict = Field(..., title="Water calibration values")
    solenoid_part: str = Field(..., title="Solenoid Part number")

class BehaviorPlatform(AindModel):
    """Behavior platform for a mouse during a session"""
    track_wheel: Union[Tube, Treadmill, Disc] = Field(..., title="Track wheel type")
    
    # optional fields
    stage_software: Optional[Software] = Field(None, title="Stage software")
    water_delivery: Optional[WaterDelivery] = Field(None, title="Water delivery")


class CameraAssembly(AindModel):
    """Named assembly of a camera and lens (and optionally a filter)"""

    # required fields
    camera_assembly_name: str = Field(..., title="Name of this camera assembly")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: Optional[Filter] = Field(None, title="Filter")
    position: Optional[RelativePosition] = Field(None, title="Relative position of this assembly")

class VisualStimulusDisplayAssembly(AindModel):
    """Visual display"""

    # required fields
    monitor: Monitor = Field(..., title= "Monitor")
    viewing_distance: float = Field(..., title="Viewing distance (cm)", units="cm")
    viewing_distance_unit: SizeUnit = Field(SizeUnit.CM, title="Viewing distance unit")

    # optional fields
    position: Optional[RelativePosition] = Field(None, title="Relative position of the monitor")
