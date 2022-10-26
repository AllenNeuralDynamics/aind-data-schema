"""Simple package to demo project structure.
"""
__version__ = "0.0.5"

from .data_description import (
    DataDescription,
    RawDataDescription,
    DerivedDataDescription,
)

from .procedures import Procedures

from .ephys.ephys_rig import EphysRig
from .ephys.ephys_session import EphysSession

__all__ = [
    DataDescription,
    RawDataDescription,
    DerivedDataDescription,
    Procedures,
    EphysRig,
    EphysSession,
]
