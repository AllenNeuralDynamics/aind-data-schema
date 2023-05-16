import inspect
import sys


class utils:

    def __init__(self) -> None:
        pass

    def find_core_classes():
        """Searches for all imported classes which utilize the AindCoreModel class, and returns those modules in a list"""

        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj): # for all classes
                yield obj