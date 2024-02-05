"""Classes to define reagents"""

from datetime import date
from typing import Optional

from pydantic import Field

from aind_data_schema.base import AindModel
from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.organizations import Organization

class Reagent(AindModel):
    """Description of reagent used in procedure"""

    name: str = Field(..., title="Name")
    source: str = Field(..., title="Source")
    rrid: Optional[PIDName] = Field(None, title="Research Resource ID")
    lot_number: Organization.RESEARCH_INSTITUTIONS = Field(..., title="Lot number")
    expiration_date: Optional[date] = Field(None, title="Lot expiration date")
