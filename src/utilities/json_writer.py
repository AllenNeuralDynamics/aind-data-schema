import argparse, os
from pathlib import Path
from aind_data_schema import DataDescription, Procedures, Processing, Subject
from aind_data_schema.ephys.ephys_rig import EphysRig
from aind_data_schema.ephys.ephys_session import EphysSession
from aind_data_schema.imaging.acquisition import Acquisition
from aind_data_schema.imaging.instrument import Instrument
from aind_data_schema.ophys.ophys_rig import OphysRig
from aind_data_schema.ophys.ophys_session import OphysSession

DEFAULT_FILE_PATH = os.getcwd()

def validate_path(output):

    if not os.path.exists(output):
        Path(output).parent.mkdir(exist_ok=True, parents=True)
    return output

def schema_filename(class_name):
    return ''.join(['_'+i.lower() if i.isupper() else i for i in str]).lstrip('_')

def main(output):

    pydantic_schemas = [
        EphysRig,
        EphysSession,
        Acquisition,
        Instrument,
        OphysRig,
        OphysSession,
        Subject,
        Processing,
        Procedures,
        DataDescription,
    ]

    # validated_output = validate_path(output)

    for schema in pydantic_schemas:
        schema_name = schema.__name__.lower()
        filename = f"{output}/{schema_name}.json"

        with open(filename, "w") as f:
            f.write(schema.schema_json(indent=3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output", default=DEFAULT_FILE_PATH, help="Output directory, defaults to current working directory")
    args = parser.parse_args()

    main(args.output)
