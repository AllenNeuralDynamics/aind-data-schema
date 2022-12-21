# main class
# convert pydantic models to JSON
# executable from CLI - argument is user defined (the directory the user wants to write to)
# default directory is current working directory
# loop through classes in aind_data_schema and write out to a json file
# import argparse
# import json

from aind_data_schema import DataDescription, Procedures, Processing, Subject
from aind_data_schema.ephys.ephys_rig import EphysRig
from aind_data_schema.ephys.ephys_session import EphysSession
from aind_data_schema.imaging.acquisition import Acquisition
from aind_data_schema.imaging.instrument import Instrument
from aind_data_schema.ophys.ophys_rig import OphysRig
from aind_data_schema.ophys.ophys_session import OphysSession


def main():

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

    for schema in pydantic_schemas:
        with open(f"{schema.__name__.lower()}.json", "w+") as f:
            f.write(schema.schema_json(indent=4))


if __name__ == "__main__":
    main()
