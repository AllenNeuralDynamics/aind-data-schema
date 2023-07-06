"""Class for holding generic helper functions that are usable within many packages"""
import inspect
import sys
from typing import Iterator, Optional, Type

from aind_data_schema.base import AindCoreModel


def get_classes(module: Optional[str] = None) -> list:
    """
    Searches for all imported classes and returns those modules in a list
    Parameters
    ----------
    module : Optional[str]
      Name of module to check. If None, weill return calling namespace's imports. Defaults to None.

    Returns
    -------
    list
      List of tuples of class name and class.

    """
    if not module:
        frm = inspect.currentframe().f_back  # Get frame for most recent level of scope (function caller level of scope)
        return inspect.getmembers(sys.modules[frm.f_globals["__name__"]], inspect.isclass)  # getmem for caller scope
    else:
        return inspect.getmembers(sys.modules[module], inspect.isclass)  # getmem for passed __name__ scope


def aind_core_models() -> Iterator[Type[AindCoreModel]]:
    """
    Returns Iterator of AindCoreModel classes
    """
    for model in AindCoreModel.__subclasses__():
        yield model
