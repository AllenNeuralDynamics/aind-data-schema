from typing import Iterator
import aind_data_schema
from aind_data_schema.base import AindCoreModel
import erdantic as erd


class ErdDiagramGenerator:
    """Class to build erdantic diagrams"""

    def __init__(self, classes_to_generate: list) -> None:
        """
        Initialize erd diagram generator class
        input: list of AindCoreModel modules you would like to generate erd diagrams for
        if list is empty, will generate erd diagrams for all modules loaded in aind_data_schema.__all__
        """

        # os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

        self.loaded_modules = list(self._get_schemas())
        
        if not classes_to_generate: # if empty list passed in, generate erd docs for all modules
            self.classes_to_generate = self.loaded_modules
        else:
            self.classes_to_generate = [module for module in self.loaded_modules if module.__name__ in classes_to_generate]


    def generate_aind_core_model_diagrams(self):
        for module in self.loaded_modules:
            self.generate_erd_diagram(module)


    def generate_requested_classes(self):
        for module in self.classes_to_generate:
            self.generate_erd_diagram(module)


    def generate_erd_diagram(self, module):
        diagram = erd.create(module)
        diagram.draw("ERD_diagrams/" + module.__name__ + '.png')


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
