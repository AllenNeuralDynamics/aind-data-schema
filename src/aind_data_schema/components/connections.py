"""Components for describing connections between devices"""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import Field, model_validator

from aind_data_schema.base import DataModel


class ConnectionDirection(str, Enum):
    """Direction of a connection"""

    SEND = "Send"
    RECEIVE = "Receive"
    SEND_AND_RECEIVE = "Send and receive"


class ConnectionData(DataModel):
    """Configuration data for a device connection including direction and port information"""

    direction: Optional[ConnectionDirection] = Field(default=None, title="Connection direction")
    port: Optional[str] = Field(default=None, title="Connection port index/name")


class Connection(DataModel):
    """Description of a connection between devices in an instrument"""

    device_names: List[str] = Field(..., title="Names of connected devices")
    connection_data: Dict[str, ConnectionData] = Field(default={}, title="Connection data")

    @model_validator(mode="after")
    def validate_connection_data(cls, self):
        """Check that all keys in connection_data exist in device_names"""
        for key in self.connection_data.keys():
            if key not in self.device_names:
                raise ValueError(f"Connection data key '{key}' does not exist in device names")

        return self
