""" Utility method to write Pydantic schemas to JSON """

import argparse
import os
import re
import sys

import aind_data_schema
from aind_data_schema.base import AindCoreModel

DEFAULT_FILE_PATH = os.getcwd()


class SchemaWriter:
    """Class to write Pydantic schemas to JSON"""

    def __init__(self, args: list):
        self.args = args

    def parse_args(self, args: list) -> argparse.Namespace:
        """Parses sys args with argparse"""

        help_message = "Output directory, defaults to current working directory"

        parser = argparse.ArgumentParser()
        
        parser.add_argument(
            "-o",
            "--output",
            default=DEFAULT_FILE_PATH,
            help=help_message,
        )

        optional_args = parser.parse_args()

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

    def schema_filename(class_name):
        """
        Returns filename in snakecase
        """
        name = class_name.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + ".json"

    def write_to_json(self, args):
        """
        Writes Pydantic models to JSON file.
        Parameters
        ----------
        args:
            optional output directory argument. defaults to current working directory
        """
        schemas_to_write = SchemaWriter.get_schemas()

        if len(args) > 1:
            output_path = args[2]
        output_path = DEFAULT_FILE_PATH

        for schema in schemas_to_write:
            filename = SchemaWriter.schema_filename(schema)
            output_file = f"{output_path}/{filename}"

            with open(output_file, "w") as f:
                f.write(schema.schema_json(indent=3))
    


if __name__ == "__main__":
    
    """Writes Pydantic models as JSON"""

    s = SchemaWriter.get_schemas()
    SchemaWriter.write_to_json(s, sys.argv)