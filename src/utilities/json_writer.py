import argparse, os
from pathlib import Path
from aind_data_schema import DataDescription, Procedures, Processing, Subject
from aind_data_schema.ephys.ephys_rig import EphysRig
from aind_data_schema.ephys.ephys_session import EphysSession
from aind_data_schema.imaging.acquisition import Acquisition
from aind_data_schema.imaging.instrument import Instrument
from aind_data_schema.ophys.ophys_rig import OphysRig
from aind_data_schema.ophys.ophys_session import OphysSession

def _validate_path(output):
    # TO-DO: add validation for user defined path, fix filenames for json files

    # if not os.path.exists(output):
    #     return Path(output).parent.mkdir(exist_ok=True, parents=True)
    return output

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

    validated_output = _validate_path(output)

    for schema in pydantic_schemas:
        filename = f"{validated_output}/{schema.__name__.lower()}.json"

        with open(filename, "w") as f:
            f.write(schema.schema_json(indent=3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output", default=os.getcwd(), help="Output directory, defaults to current working directory")
    args = parser.parse_args()

    main(args.output)
