""" Utility method to write Pydantic schemas to JSON """

import argparse
import os
import re

import aind_data_schema
from aind_data_schema.base import AindCoreModel

DEFAULT_FILE_PATH = os.getcwd()


class SchemaWriter:
    """Class to write Pydantic schemas to JSON"""

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
        for schema in schemas_to_write:
            filename = SchemaWriter.schema_filename(schema)
            output_file = f"{args.output}/{filename}"

            with open(output_file, "w") as f:
                f.write(schema.schema_json(indent=3))


def main(args):
    """Writes Pydantic models as JSON"""

    s = SchemaWriter.get_schemas()
    SchemaWriter.write_to_json(s, args)


if __name__ == "__main__":
    """User defined argument for output directory"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_FILE_PATH,
        help="Output directory, defaults to current working directory",
    )
    args = parser.parse_args()

    main(args)
