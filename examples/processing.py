""" example processing """

from datetime import datetime, timezone

from aind_data_schema.core.processing import AnalysisProcess, DataProcess, PipelineProcess, Processing, ProcessName, ResourceUsage
from aind_data_schema_models.units import MemoryUnit, MemoryValue, TimeUnit

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

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
                resources=ResourceUsage(
                    os="Ubuntu 20.04",
                    architecture="x86_64",
                    cpu="Intel i7-9700K",
                    cpu_cores=8,
                    gpu="NVIDIA GTX 1080",
                    memory=MemoryValue(value=1, unit=MemoryUnit.TB),
                    ram=MemoryValue(value=32, unit=MemoryUnit.GB),
                    timestamps=[0, 60, 120, 180],
                    timestamp_unit=TimeUnit.S,
                    cpu_usage=[0.0, 0.5, 0.75, 1.0],
                    gpu_usage=[0.0, 0.0, 0.0, 0.0],
                    ram_usage=[0.25, 0.30, 0.45, 0.45],
                    file_io_usage=[100.0, 200.0, 150.0],
                    file_io_unit=MemoryUnit.MB
                )
            ),
            DataProcess(
                name=ProcessName.FILE_FORMAT_CONVERSION,
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
serialized = p.model_dump_json()
deserialized = Processing.model_validate_json(serialized)
p.write_standard_file()
