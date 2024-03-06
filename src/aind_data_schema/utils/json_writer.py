""" Utility method to write Pydantic schemas to JSON """

import argparse
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Iterator

from aind_data_schema import core
from aind_data_schema.base import AindCoreModel

# Import all modules in core package
for mod in core.__loader__.get_resource_reader().contents():
    if "__" not in mod:
        importlib.import_module(f"aind_data_schema.core.{mod.replace('.py','')}")


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

        parser.add_argument(
            "--attach-version",
            action="store_true",
            help="Add extra directory with schema version number",
        )
        parser.set_defaults(attach_version=False)

        optional_args = parser.parse_args(args)

        return optional_args

    @staticmethod
    def get_schemas() -> Iterator[AindCoreModel]:
        """
        Returns Iterator of AindCoreModel classes
        """

        for model in AindCoreModel.__subclasses__():
            yield model

    def write_to_json(self) -> None:
        """
        Writes Pydantic models to JSON file.
        """
        schemas_to_write = self.get_schemas()
        output_path = self.configs.output
        for schema in schemas_to_write:
            filename = schema.default_filename()
            file_extension = "".join(Path(filename).suffixes)
            schema_filename = filename.replace(file_extension, "_schema.json")
            if self.configs.attach_version:
                schema_version = schema.model_construct().schema_version
                model_directory_name = schema_filename.replace("_schema.json", "")
                sub_directory = Path(output_path) / model_directory_name / schema_version
                output_file = sub_directory / schema_filename
            else:
                output_file = Path(output_path) / schema_filename

            if not os.path.exists(output_file.parent):
                os.makedirs(output_file.parent)

            with open(output_file, "w") as f:
                schema_json: dict = schema.model_json_schema()
                schema_json_str: str = json.dumps(schema_json, indent=3)
                f.write(schema_json_str)


if __name__ == "__main__":
    """User defined argument for output directory"""
    sys_args = sys.argv[1:]
    s = SchemaWriter(sys_args)
    s.write_to_json()
