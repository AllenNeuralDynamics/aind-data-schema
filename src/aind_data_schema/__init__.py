"""Simple package to demo project structure.
"""
__version__ = "0.0.4"

from .data_description import (
    DataDescription,
    RawDataDescription,
    DerivedDataDescription,
)

__all__ = [DataDescription, RawDataDescription, DerivedDataDescription]
