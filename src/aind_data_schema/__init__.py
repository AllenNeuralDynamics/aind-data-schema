"""Simple package to demo project structure.
"""
__version__ = "0.0.3"

from aind_data_schema.imaging.acquisition import Acquisition
from aind_data_schema.imaging.instrument import Instrument, Microscope

__all__ = [Acquisition, Instrument, Microscope]
