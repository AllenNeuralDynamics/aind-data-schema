import inspect
import sys
from typing import Iterator

import aind_data_schema
from aind_data_schema.base import AindCoreModel


class AindUtils:

    def __init__(self) -> None:
        pass

    def _get_classes():
        """Searches for all imported classes which utilize the AindCoreModel class, and returns those modules in a list"""

        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj): # for all classes
                yield obj


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
