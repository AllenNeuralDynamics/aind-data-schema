"""Module for generating erd diagrams"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

import erdantic as erd

from aind_data_schema.utils.aind_utils import aind_core_models


class ErdGenerator:
    """Class to build erdantic diagrams"""

    _DEFAULT_CLASSES_TO_GENERATE = None
    _DEFAULT_OUTPUT_DIRECTORY = os.getcwd()

    def __init__(
        self,
        classes_to_generate: Optional[List[str]] = _DEFAULT_CLASSES_TO_GENERATE,
        output_directory: Path = Path(_DEFAULT_OUTPUT_DIRECTORY),
    ) -> None:
        """
        Initialize erd diagram generator class
        Parameters
        ----------
        classes_to_generate : Optional[List[str]]
          Names of classes to generate diagrams for. Defaults to all
          AindCoreModels.
        output_directory : Path
          Directory to write the diagrams to. Defaults to current working dir.
        """

        self.classes_to_generate = classes_to_generate
        self.output_directory = output_directory

    @classmethod
    def from_args(cls, args: list):
        """
        Constructs class from list of arguments.
        Parameters
        ----------
        args : list

        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-o",
            "--output-directory",
            required=False,
            default=cls._DEFAULT_OUTPUT_DIRECTORY,
            help="Directory to write the diagrams to. Default is current working directory.",
        )
        parser.add_argument(
            "-c",
            "--classes-to-generate",
            nargs="+",
            required=False,
            default=cls._DEFAULT_CLASSES_TO_GENERATE,
            help="List of AindCoreModel subclasses to generate diagrams for. Defaults to all of them.",
        )
        optional_args = parser.parse_args(args)
        return cls(
            classes_to_generate=optional_args.classes_to_generate, output_directory=Path(optional_args.output_directory)
        )

    def generate_erd_diagrams(self) -> None:
        """
        Write erdantic diagrams to output directory,
        """
        for model in aind_core_models():
            if self.classes_to_generate is None or model.__name__ in self.classes_to_generate:
                file_name = model.__name__ + ".png"
                diagram = erd.create(model)
                diagram.draw(self.output_directory / file_name)
        return None


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    erd_gen = ErdGenerator.from_args(sys_args)
    erd_gen.generate_erd_diagrams()
