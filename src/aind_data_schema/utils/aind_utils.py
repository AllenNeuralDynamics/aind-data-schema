import inspect
import sys
from typing import Iterator

import aind_data_schema
from aind_data_schema.base import AindCoreModel


class AindUtils:

    def __init__(self) -> None:
        pass

    def _get_classes(self, module = None) -> list:
        """
        Searches for all imported classes and returns those modules in a list
        Input: __name__ of module you wish to check, or blank to check the calling namespace's imports
        """
        if not module:
            frm = inspect.currentframe().f_back
            return inspect.getmembers(sys.modules[frm.f_globals['__name__']], inspect.isclass)
        else: 
            return inspect.getmembers(sys.modules[module], inspect.isclass)


    @staticmethod
    def _get_schemas() -> Iterator[AindCoreModel]:
        """
        Returns Iterator of AindCoreModel classes
        """
        aind_data_schema_classes = aind_data_schema.__all__

        for class_name in aind_data_schema_classes:
            model = getattr(aind_data_schema, class_name)

            if AindCoreModel in model.__bases__:
                yield model
