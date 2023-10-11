""" example processing """
import datetime

from aind_data_schema import Processing
from aind_data_schema.processing import AnalysisProcess, DataProcess, PipelineProcess, ProcessName

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

p = Processing(
    processing_pipeline=PipelineProcess(
        processor_full_name="Some Processor",
        pipeline_url="https://url/for/pipeline",
        pipeline_version="0.1.1",
        data_processes=[
            DataProcess(
                name=ProcessName.IMAGE_TILE_FUSING,
                software_version="0.0.1",
                start_date_time=t,
                end_date_time=t,
                input_location="/path/to/inputs",
                output_location="/path/to/outputs",
                code_version="0.1",
                code_url="https://github.com/abcd",
                parameters={"size": 7},
            ),
            DataProcess(
                name=ProcessName.FILE_CONVERSION,
                software_version="0.0.1",
                start_date_time=t,
                end_date_time=t,
                input_location="/path/to/inputs",
                output_location="/path/to/outputs",
                code_version="0.1",
                code_url="https://github.com/asdf",
                parameters={"u": 7, "z": True},
            ),
            DataProcess(
                name=ProcessName.IMAGE_DESTRIPING,
                software_version="0.2.1",
                start_date_time=t,
                end_date_time=t,
                input_location="/path/to/input",
                output_location="/path/to/output",
                code_version="0.3",
                code_url="https://github.com/fdsa",
                parameters={"a": 2, "b": -2},
            ),
        ],
    ),
    analyses=[
        AnalysisProcess(
            analyst_full_name="Some Analyzer",
            description="some description",
            name="Analysis",
            software_version="0.0.1",
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code_version="0.1",
            code_url="https://github.com/abcd",
            parameters={"size": 7},
        ),
        AnalysisProcess(
            analyst_full_name="Some Analyzer",
            description="some description",
            name="Analysis",
            software_version="0.0.1",
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code_version="0.1",
            code_url="https://github.com/asdf",
            parameters={"u": 7, "z": True},
        ),
    ],
)
p.write_standard_file()
