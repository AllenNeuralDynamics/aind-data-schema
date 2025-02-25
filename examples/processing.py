""" example processing """

from datetime import datetime, timezone

from aind_data_schema.components.identifiers import Person, Code
from aind_data_schema.core.processing import (
    DataProcess,
    Processing,
    ProcessName,
    ProcessStage,
    ResourceTimestamped,
    ResourceUsage,
)
from aind_data_schema_models.units import MemoryUnit
from aind_data_schema_models.system_architecture import OperatingSystem, CPUArchitecture

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)


cpu_usage_list = [
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=75.5),
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=80.0),
]

gpu_usage_list = [
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=60.0),
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=65.5),
]

ram_usage_list = [
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=70.0),
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=72.5),
]

file_io_usage_list = [
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=5.5),
    ResourceTimestamped(timestamp=datetime(2024, 9, 13, tzinfo=timezone.utc), usage=6.0),
]

example_code = Code(
    url="https://github.com/abcd",
    version="0.1",
)

p = Processing(
    data_processes=[
        DataProcess(
            experimenters=[Person(name="Dr. Dan")],
            name=ProcessName.PIPELINE,
            pipeline_steps=[
                ProcessName.IMAGE_TILE_FUSING,
                ProcessName.FILE_FORMAT_CONVERSION,
                ProcessName.IMAGE_DESTRIPING,
            ],
            stage=ProcessStage.PROCESSING,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            start_date_time=t,
            end_date_time=t,
            code=Code(
                url="https://url/for/pipeline",
                version="0.1.1",
            )
        ),
        DataProcess(
            name=ProcessName.IMAGE_TILE_FUSING,
            experimenters=[Person(name="Dr. Dan")],
            stage=ProcessStage.PROCESSING,
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code=example_code,
            parameters={"size": 7},
            resources=ResourceUsage(
                os=OperatingSystem.UBUNTU_20_04,
                architecture=CPUArchitecture.X86_64,
                cpu="Intel Core i7",
                cpu_cores=8,
                gpu="NVIDIA GeForce RTX 3080",
                system_memory=32.0,
                system_memory_unit=MemoryUnit.GB,
                ram=16.0,
                ram_unit=MemoryUnit.GB,
                cpu_usage=cpu_usage_list,
                gpu_usage=gpu_usage_list,
                ram_usage=ram_usage_list,
            ),
        ),
        DataProcess(
            name=ProcessName.FILE_FORMAT_CONVERSION,
            experimenters=[Person(name="Dr. Dan")],
            stage=ProcessStage.PROCESSING,
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code=example_code,
            parameters={"u": 7, "z": True},
        ),
        DataProcess(
            name=ProcessName.IMAGE_DESTRIPING,
            experimenters=[Person(name="Dr. Dan")],
            stage=ProcessStage.PROCESSING,
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/input",
            output_location="/path/to/output",
            code=example_code,
            parameters={"a": 2, "b": -2},
        ),
        DataProcess(
            stage=ProcessStage.ANALYSIS,
            experimenters=[Person(name="Some Analyzer")],
            name=ProcessName.ANALYSIS,
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code=example_code,
            parameters={"size": 7},
        ),
        DataProcess(
            stage=ProcessStage.ANALYSIS,
            experimenters=[Person(name="Some Analyzer")],
            name=ProcessName.ANALYSIS,
            start_date_time=t,
            end_date_time=t,
            input_location="/path/to/inputs",
            output_location="/path/to/outputs",
            code=example_code,
            parameters={"u": 7, "z": True},
        ),
    ]
)
serialized = p.model_dump_json()
deserialized = Processing.model_validate_json(serialized)
p.write_standard_file()
