""" Utility method to write Pydantic schemas to JSON """

import argparse
import os
import sys
from pathlib import Path
from typing import Iterator

import aind_data_schema
from aind_data_schema.base import AindCoreModel


class SchemaWriter:
    """Class to write Pydantic schemas to JSON"""

    DEFAULT_FILE_PATH = os.getcwd()

    def __init__(self, args: list) -> None:
        """Initialize schema writer class."""
        self.args = args
        self.configs = self._parse_arguments(args)

    def _parse_arguments(self, args: list) -> argparse.Namespace:
        """Parses sys args with argparse"""

        help_message = "Output directory, defaults to current working directory"

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default=self.DEFAULT_FILE_PATH,
            help=help_message,
        )

        optional_args = parser.parse_args(args)

        return optional_args

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

    def write_to_json(self) -> None:
        """
        Writes Pydantic models to JSON file.
        """
        schemas_to_write = self._get_schemas()
        output_path = self.configs.output
        for schema in schemas_to_write:
            filename = schema.default_filename()
            schema_filename = filename.replace(".json", "_schema.json")
            output_file = Path(output_path) / schema_filename

            with open(output_file, "w") as f:
                f.write(schema.schema_json(indent=3))


if __name__ == "__main__":
    """User defined argument for output directory"""
    sys_args = sys.argv[1:]
    s = SchemaWriter(sys_args)
    s.write_to_json()
