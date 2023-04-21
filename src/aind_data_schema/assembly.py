from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal

from pydantic import Field

from .base import AindModel

from device import WaterDelivery, Tube, Treadmill, Disc, Camera, Lens, Filter, RelativePosition


class BehaviorPlatform(WaterDelivery):
    """Behavior platform including water delivery system and track wheel"""
    track_wheel: Union[Tube, Treadmill, Disc] = Field(..., title="Track wheel type")

class CameraAssembly(AindModel):
    """Named assembly of a camera and lens (and optionally a filter)"""

    # required fields
    camera_assembly_name: str = Field(..., title="Name of this camera assembly")
    camera: Camera = Field(..., title="Camera")
    lens: Lens = Field(..., title="Lens")

    # optional fields
    filter: Optional[Filter] = Field(None, title="Filter")
    position: Optional[RelativePosition] = Field(None, title="Relative position of this assembly")