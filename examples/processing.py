""" example processing """

import datetime
from aind_data_schema import Processing
from aind_data_schema.processing import DataProcess

now = datetime.datetime.now()

p = Processing(
    pipeline_url="https://url/for/pipeline",
    pipeline_version="0.1.0",
    data_processes=[
        DataProcess(
            name="Merge volume",
            version="0.0.1",
            start_date_time=now,
            end_date_time=now,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code_url="https://github.com/abcd",
            parameters={"size": 7},
        ),
        DataProcess(
            name="OME zarr",
            version="0.0.1",
            start_date_time=now,
            end_date_time=now,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code_url="https://github.com/asdf",
            parameters={"u": 7, "z": True},
        ),
        DataProcess(
            name="Pystripe",
            version="0.2.1",
            start_date_time=now,
            end_date_time=now,
            input_location="/path/to/input",
            output_location="/path/to/output",
            code_url="https://github.com/fdsa",
            parameters={"a": 2, "b": -2},
        ),
    ],
)

with open("processing.json", "w") as f:
    f.write(p.json(indent=3))
