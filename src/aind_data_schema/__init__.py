"""Simple package to demo project structure.
"""
__version__ = "0.0.3"

from .ephys.ephys_rig import EphysRig
from .ephys.ephys_session import EphysSession

__all__ = [EphysRig, EphysSession]
