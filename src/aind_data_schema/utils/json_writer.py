""" Utility method to write Pydantic schemas to JSON """

import argparse
import os
import sys
from pathlib import Path

import aind_data_schema
from aind_data_schema.base import AindCoreModel

DEFAULT_FILE_PATH = os.getcwd()


class SchemaWriter:
    """Class to write Pydantic schemas to JSON"""

    def __init__(self, args: list):
        self.args = args
        self.configs = self.parse_arguments(args)

    def parse_arguments(self, args: list) -> argparse.Namespace:
        """Parses sys args with argparse"""

        help_message = (
            "Output directory, defaults to current working directory"
        )

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default=DEFAULT_FILE_PATH,
            help=help_message,
        )

        optional_args = parser.parse_args(args)

        return optional_args

    @staticmethod
    def get_schemas():
        """
        Returns child classes of AindCoreModel in aind_data_schema
        """
        aind_data_schema_classes = aind_data_schema.__all__

        for class_name in aind_data_schema_classes:
            model = getattr(aind_data_schema, class_name)

            if AindCoreModel in model.__bases__:
                yield model

    def write_to_json(self):
        """
        Writes Pydantic models to JSON file.
        Parameters
        ----------
        args:
            optional output directory argument. defaults to current working directory
        """
        schemas_to_write = self.get_schemas()
        output_path = self.configs.output
        for schema in schemas_to_write:
            filename = schema.default_filename()
            output_file = Path(output_path) / filename

            with open(output_file, "w") as f:
                f.write(schema.schema_json(indent=3))


def main(args):
    """Writes Pydantic models as JSON"""

    s = SchemaWriter(args)
    s.write_to_json()


if __name__ == "__main__":
    """User defined argument for output directory"""
    sys_args = sys.argv[1:]

    main(sys_args)
