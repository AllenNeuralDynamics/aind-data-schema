""" Measurement and calibration data models """

from aind_data_schema.base import GenericModel, GenericModelType, DataModel, AwareDatetimeWithDefault
from pydantic import Field
from typing import List, Optional
from aind_data_schema.components.reagent import Reagent


class Calibration(DataModel):
    """Generic calibration class"""

    date: AwareDatetimeWithDefault = Field(..., title="Date and time of calibration")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Brief description of what is being calibrated")
    input: GenericModelType = Field(GenericModel(), description="Calibration input", title="inputs")
    output: GenericModelType = Field(GenericModel(), description="Calibration output", title="outputs")
    notes: Optional[str] = Field(default=None, title="Notes")


class Maintenance(DataModel):
    """Generic maintenance class"""

    date: AwareDatetimeWithDefault = Field(..., title="Date and time of maintenance")
    device_name: str = Field(..., title="Device name", description="Must match a device name in rig/instrument")
    description: str = Field(..., title="Description", description="Description on maintenance procedure")
    protocol_id: Optional[str] = Field(default=None, title="Protocol ID")
    reagents: List[Reagent] = Field(default=[], title="Reagents")
    notes: Optional[str] = Field(default=None, title="Notes")
