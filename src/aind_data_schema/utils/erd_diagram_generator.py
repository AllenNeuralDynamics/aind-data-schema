from typing import Iterator
import aind_data_schema
from aind_data_schema.base import AindCoreModel
import erdantic as erd
import os
from pathlib import Path


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

        if not classes_to_generate:  # if empty list passed in, generate erd docs for all modules
            self.classes_to_generate = self.loaded_modules
        else:
            # List of only models that are present in both loaded_modules and classes_to_generate
            self.classes_to_generate = [
                module for module in self.loaded_modules if module.__name__ in classes_to_generate
            ]

    def generate_aind_core_model_diagrams(self):
        """generate erd diagrams for all models in loaded models"""
        for module in self.loaded_modules:
            self.generate_erd_diagram(module)

    def generate_requested_classes(self):
        """generate erd diagrams for all models in classes_to_generate"""
        for module in self.classes_to_generate:
            self.generate_erd_diagram(module)

    def generate_erd_diagram(self, module, outpath: Path = Path("ERD_diagrams")):
        """
        Code to generate a single erd diagram, given a generic class/model
        ie:
            from xx import yy
            erd = ErdDiagramGenerator()
            erd.generate_erd_diagram(yy)

        Can take output file path as input, otherwise defaults to generic output path
        """

        file_path = outpath / (module.__name__ + ".png")
        diagram = erd.create(module)
        diagram.draw(file_path)

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
