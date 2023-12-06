"""Module for pidname definitions"""

from pydantic import Field

from aind_data_schema.base import AindModel, OptionalField, OptionalType


class BaseName(AindModel):
    """A simple model associating a name with an abbreviation"""

    name: str = Field(..., title="Name")
    abbreviation: OptionalType[str] = OptionalField(title="Abbreviation")


class PIDName(BaseName):
    """
    Model for associate a name with a persistent identifier (PID),
    the registry for that PID, and abbreviation for that registry
    """

    registry: OptionalType[BaseName] = OptionalField(title="Registry")
    registry_identifier: OptionalType[str] = OptionalField(title="Registry identifier")
