"""Class for holding generic helper functions that are usable within many packages"""

import inspect
import sys
from typing import Iterator, Type

from aind_data_schema.base import AindCoreModel


def get_classes(module=None) -> list:
    """
    Searches for all imported classes and returns those modules in a list
    Input:
        (1) _get_classes(__name__), where __name__ is from module/scope you wish to check, or
        (2) _get_classeS(), blank to check the calling namespace's imports
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
