"""Module for pidname definitions"""

from typing import Optional

from pydantic import Field

from aind_data_schema.base import AindModel


class BaseName(AindModel):
    """A simple model associating a name with an abbreviation"""

    name: str = Field(..., title="Name")
    abbreviation: Optional[str] = Field(None, title="Abbreviation")


class PIDName(BaseName):
    """
    Model for associate a name with a persistent identifier (PID),
    the registry for that PID, and abbreviation for that registry
    """

    registry: Optional[BaseName] = Field(None, title="Registry")
    registry_identifier: Optional[str] = Field(None, title="Registry identifier")
