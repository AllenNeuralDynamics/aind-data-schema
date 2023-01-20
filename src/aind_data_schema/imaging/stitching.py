""" schema describing imaging acquisition """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field
from pydantic.types import conlist

from ..base import AindCoreModel, AindModel
from tile import Tile


class Stitching(AindCoreModel):
    """Description of an imaging acquisition session"""

    schema_version: str = Field("0.4.0", description="schema version", title="Version", const=True)
    
    tiles: List[Tile] = Field(..., title="Data tiles")
    
