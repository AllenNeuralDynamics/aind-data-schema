from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union, Literal
from typing_extensions import Annotated

from pydantic import Field, root_validator

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.models.devices import RelativePosition, SpoutSide
from aind_data_schema.models.units import PowerUnit, SizeUnit, TimeUnit


class TriggerType(Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class RewardSolution(Enum):
    """Reward solution name"""

    WATER = "Water"
    OTHER = "Other"


class FiberConnectionConfigs(AindModel):
    """Description for a fiber photometry configuration"""

    patch_cord_name: str = Field(..., title="Patch cord name (must match rig)")
    patch_cord_output_power: Decimal = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(PowerUnit.UW, title="Output power unit")
    fiber_name: str = Field(..., title="Fiber name (must match procedure)")


class DetectorConfigs(AindModel):
    """Description of detector settings"""

    name: str = Field(..., title="Name")
    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")


class LightEmittingDiodeConfigs(AindModel):
    """Description of LED settings"""

    config_type: Literal["LightEmittingDiodeConfigs"] = "LightEmittingDiodeConfigs"
    name: str = Field(..., title="Name")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class LaserConfigs(AindModel):
    """Description of laser settings in a session"""

    config_type: Literal["LaserConfigs"] = "LaserConfigs"
    name: str = Field(..., title="Name", description="Must match rig json")
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class RewardSpoutConfigs(AindModel):
    """Reward spout session information"""

    side: SpoutSide = Field(..., title="Spout side", description="Must match rig")
    starting_position: RelativePosition = Field(..., title="Starting position")
    variable_position: bool = Field(
        ..., title="Variable position", description="True if spout position changes during session as tracked in data"
    )


class EphysProbeConfigs(AindModel):
    """Probes in a EphysProbeModule"""

    name: str = Field(..., title="Ephys probe name (must match rig JSON)")
    other_targeted_structures: List[str] = []


class RewardDeliveryConfigs(AindModel):
    """Description of reward delivery configuration"""

    reward_solution: RewardSolution = Field(..., title="Reward solution", description="If Other use notes")
    reward_spouts: List[RewardSpoutConfigs] = Field(..., title="Reward spouts")
    notes: Optional[str] = Field(None, title="Notes")

    # @root_validator
    # def validate_other(cls, v):
    #     """Validator for other/notes"""
    #
    #     if v.get("reward_solution") == RewardSolution.OTHER and not v.get("notes"):
    #         raise ValueError(
    #             "Notes cannot be empty if reward_solution is Other. Describe the reward_solution in the notes field."
    #         )
    #     return v


LIGHT_SOURCE_CONFIGS = Annotated[Union[LightEmittingDiodeConfigs, LaserConfigs], Field(discriminator="config_type")]
