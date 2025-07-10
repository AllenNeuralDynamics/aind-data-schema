"""Components for describing connections between devices"""

from typing import Optional

from pydantic import Field

from aind_data_schema.base import DataModel


class Connection(DataModel):
    """Description of a connection between devices in an instrument"""

    source_device: str = Field(..., title="Source device name")
    source_port: Optional[str] = Field(default=None, title="Source device port index/name")
    target_device: str = Field(..., title="Target device name")
    target_port: Optional[str] = Field(default=None, title="Target device port index/name")
    send_and_receive: bool = Field(
        default=False,
        title="Send and receive",
        description="Whether the connection is bidirectional (send and receive data)",
    )
