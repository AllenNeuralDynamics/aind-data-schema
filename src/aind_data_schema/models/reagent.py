"""Classes to define reagents"""

from datetime import date

from pydantic import Field

from aind_data_schema.base import AindModel, OptionalField, OptionalType
from aind_data_schema.models.pid_names import PIDName


class Reagent(AindModel):
    """Description of reagent used in procedure"""

    name: str = Field(..., title="Name")
    source: str = Field(..., title="Source")
    rrid: OptionalType[PIDName] = OptionalField(title="Research Resource ID")
    lot_number: str = Field(..., title="Lot number")
    expiration_date: OptionalType[date] = OptionalField(title="Lot expiration date")
