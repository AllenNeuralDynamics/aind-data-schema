""" example processing """
import datetime

from aind_data_schema import Processing
from aind_data_schema.processing import DataProcess

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

p = Processing(
    pipeline_url="https://url/for/pipeline",
    pipeline_version="0.1.0",
    data_processes=[
        DataProcess(
            name="Image tile fusing",
            version="0.0.1",
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code_url="https://github.com/abcd",
            parameters={"size": 7},
        ),
        DataProcess(
            name="File format conversion",
            version="0.0.1",
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code_url="https://github.com/asdf",
            parameters={"u": 7, "z": True},
        ),
        DataProcess(
            name="Image destriping",
            version="0.2.1",
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/input",
            output_location="/path/to/output",
            code_url="https://github.com/fdsa",
            parameters={"a": 2, "b": -2},
        ),
    ],
)
p.write_standard_file()
