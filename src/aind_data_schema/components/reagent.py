"""Classes to define reagents"""

from datetime import date
from typing import Optional

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from pydantic import Field

from aind_data_schema.base import AindModel


class Reagent(AindModel):
    """Description of reagent used in procedure"""

    name: str = Field(..., title="Name")
    source: Organization.ONE_OF = Field(..., title="Source")
    rrid: Optional[PIDName] = Field(default=None, title="Research Resource ID")
    lot_number: str = Field(..., title="Lot number")
    expiration_date: Optional[date] = Field(default=None, title="Lot expiration date")
