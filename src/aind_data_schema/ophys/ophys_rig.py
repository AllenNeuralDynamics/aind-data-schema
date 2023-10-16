""" Schemas for Ophys Rigs. This is being deprecated after 2023-11-01."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field
from pydantic.typing import Annotated

from aind_data_schema.base import AindCoreModel
from aind_data_schema.device import (
    CameraAssembly,
    CameraChroma,
    DAQDevice,
    DataInterface,
    Device,
    Disc,
    Filter,
    HarpDevice,
    Immersion,
    Laser,
    Lens,
    LightEmittingDiode,
    Monitor,
    Objective,
    RewardDelivery,
    Speaker,
    Treadmill,
    Tube,
)
from aind_data_schema.utils.units import SizeUnit


class DetectorType(Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "PMT"
    OTHER = "other"


class Cooling(Enum):
    """Cooling medium name"""

    AIR = "air"
    WATER = "water"


class BinMode(Enum):
    """Detector binning mode"""

    ADDITIVE = "additive"
    AVERAGE = "average"
    NONE = "none"


class Detector(Device):
    """Description of a generic detector"""

    detector_type: DetectorType = Field(..., title="Detector Type")
    data_interface: DataInterface = Field(..., title="Data interface")
    cooling: Cooling = Field(..., title="Cooling")
    immersion: Optional[Immersion] = Field(None, title="Immersion")

    chroma: Optional[CameraChroma] = Field(None, title="Camera chroma")
    bit_depth: Optional[int] = Field(None, title="Bit depth")
    bin_mode: Optional[BinMode] = Field(BinMode.NONE, title="Detector binning mode")
    bin_width: Optional[int] = Field(None, title="Bin width")
    bin_height: Optional[int] = Field(None, title="Bin height")
    bin_unit: Optional[SizeUnit] = Field(SizeUnit.PX, title="Bin size unit", const=True)
    gain: Optional[Decimal] = Field(None, title="Gain")
    crop_width: Optional[int] = Field(None, title="Crop width")
    crop_height: Optional[int] = Field(None, title="Crop width")
    crop_unit: Optional[SizeUnit] = Field(SizeUnit.PX, title="Crop size unit", const=True)


class Patch(Device):
    """Description of a patch cord"""

    core_diameter: Decimal = Field(..., title="Core diameter (um)")
    numerical_aperture: Decimal = Field(..., title="Numerical aperture")
    photobleaching_date: Optional[date] = Field(None, title="Photobleaching date")


class OphysRig(AindCoreModel):
    """Description of an optical physiology rig. This is being deprecated after 2023-11-01."""

    schema_version: str = Field(
        "0.7.4",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    rig_id: str = Field(..., description="room number_stim apparatus_version", title="Rig ID")
    temperature_control: Optional[bool] = Field(None, title="Temperature control")
    humidity_control: Optional[bool] = Field(None, title="Humidity control")
    vibration_control: Optional[bool] = Field(None, title="Vibration control")
    patch_cords: Optional[List[Patch]] = Field(..., title="Patch cords", unique_items=True)
    light_sources: Optional[
        Annotated[
            List[Union[Laser, LightEmittingDiode]],
            Field(None, title="Light sources", unique_items=True, discriminator="device_type"),
        ]
    ]
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    objectives: Optional[List[Objective]] = Field(None, title="Objectives", unique_items=True)
    filters: Optional[List[Filter]] = Field(None, title="Filters", unique_items=True)
    lenses: Optional[List[Lens]] = Field(None, title="Lenses", unique_items=True)
    cameras: Optional[List[CameraAssembly]] = Field(None, title="Camera assemblies", unique_items=True)
    mouse_platform: Optional[
        Annotated[Union[Tube, Treadmill, Disc], Field(None, title="Mouse platform", discriminator="device_type")]
    ]
    stimulus_devices: Optional[
        Annotated[
            List[Union[Monitor, RewardDelivery, Speaker]],
            Field(None, title="Stimulus devices", unique_items=True, discriminator="device_type"),
        ]
    ]
    daqs: Optional[
        Annotated[
            List[Union[DAQDevice, HarpDevice]],
            Field(None, title="Data acquisition devices", discriminator="device_type"),
        ]
    ]
    additional_devices: Optional[List[Device]] = Field(None, title="Additional devices", unique_items=True)
    light_path_diagram: Optional[str] = Field(
        None,
        description="Path to diagram of the light path.",
        title="Light path diagram",
    )
    notes: Optional[str] = Field(None, title="Notes")
