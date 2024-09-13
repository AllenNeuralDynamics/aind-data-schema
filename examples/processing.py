""" example processing """

from datetime import datetime, timezone, date

from aind_data_schema.core.processing import (
    AnalysisProcess,
    DataProcess,
    PipelineProcess,
    Processing,
    ProcessName,
    ResourceTimestamped,
    ResourceUsage,
)
from aind_data_schema_models.units import MemoryUnit, MemoryValue
from aind_data_schema_models.system_architecture import OperatingSystem, CPUArchitecture

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)


timestamped_cpu_usage = [
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=75.5),
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=80.0),
]

timestamped_gpu_usage = [
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=60.0),
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=65.5),
]

timestamped_ram_usage = [
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=70.0),
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=72.5),
]

timestamped_file_io_usage = [
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=5.5),
    ResourceTimestamped(timestamp=date(2024, 9, 13), usage=6.0),
]

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
                    os=OperatingSystem.UBUNTU_20_04,
                    architecture=CPUArchitecture.X86_64,
                    cpu="Intel Core i7",
                    cpu_cores=8,
                    gpu="NVIDIA GeForce RTX 3080",
                    memory=MemoryValue(value=32.0, unit=MemoryUnit.GB),
                    ram=MemoryValue(value=16.0, unit=MemoryUnit.GB),
                    cpu_usage=timestamped_cpu_usage,
                    gpu_usage=timestamped_gpu_usage,
                    ram_usage=timestamped_ram_usage,
                    file_io_usage=timestamped_file_io_usage,
                    file_io_unit=MemoryUnit.MB,
                ),
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
