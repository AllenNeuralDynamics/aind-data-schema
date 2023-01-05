import argparse
import json
import os

import aind_data_schema
from aind_data_schema.base import AindCoreModel

DEFAULT_FILE_PATH = os.getcwd()

class SchemaWriter:
    """ Class to write Pydantic schemas to JSON """

    def __init__(self, args):
        self.output = args.output

    @staticmethod
    def get_schemas():

        aind_data_schema_classes = aind_data_schema.__all__

        for class_name in aind_data_schema_classes:
            model = getattr(aind_data_schema, class_name)

            if AindCoreModel in model.__bases__:
                yield model


    # TO-DO: helper function for filename, fix argparse for output directory

    def write_to_json(self):
        schemas_to_write = SchemaWriter.get_schemas()

        for schema in schemas_to_write:
            s = schema.schema()
            filename = f"{DEFAULT_FILE_PATH}/{schema.__name__}.json"

            with open(filename, "w") as f:
                f.write(schema.schema_json(indent=3))

def main():
    s = SchemaWriter.get_schemas()
    SchemaWriter.write_to_json(s)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-o",
    #     "--output",
    #     default=DEFAULT_FILE_PATH,
    #     help="Output directory, defaults to current working directory",
    # )
    # args = parser.parse_args()

    main()
