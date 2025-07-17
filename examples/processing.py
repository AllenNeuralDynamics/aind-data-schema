"""example processing"""

from datetime import datetime, timezone

from aind_data_schema.components.identifiers import Code
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
    parameters={"size": 7},
)

p = Processing.create_with_sequential_process_graph(
    pipelines=[
        Code(
            name="Imaging processing pipeline",
            url="https://url/for/pipeline",
            version="0.1.1",
        ),
    ],
    data_processes=[
        DataProcess(
            process_type=ProcessName.IMAGE_TILE_FUSING,
            experimenters=["Dr. Dan"],
            stage=ProcessStage.PROCESSING,
            start_date_time=t,
            end_date_time=t,
            output_path="/path/to/outputs",
            pipeline_name="Imaging processing pipeline",
            code=example_code.model_copy(
                update=dict(
                    parameters={"size": 7},
                )
            ),
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
            process_type=ProcessName.FILE_FORMAT_CONVERSION,
            pipeline_name="Imaging processing pipeline",
            experimenters=["Dr. Dan"],
            stage=ProcessStage.PROCESSING,
            start_date_time=t,
            end_date_time=t,
            output_path="/path/to/outputs",
            code=example_code.model_copy(
                update=dict(
                    parameters={"u": 7, "z": True},
                )
            ),
        ),
        DataProcess(
            process_type=ProcessName.IMAGE_DESTRIPING,
            pipeline_name="Imaging processing pipeline",
            experimenters=["Dr. Dan"],
            stage=ProcessStage.PROCESSING,
            start_date_time=t,
            end_date_time=t,
            output_path="/path/to/output",
            code=example_code.model_copy(
                update=dict(
                    parameters={"a": 2, "b": -2},
                )
            ),
        ),
        DataProcess(
            stage=ProcessStage.ANALYSIS,
            experimenters=["Some Analyzer"],
            process_type=ProcessName.ANALYSIS,
            start_date_time=t,
            end_date_time=t,
            output_path="/path/to/outputs",
            code=example_code.model_copy(
                update=dict(
                    parameters={"size": 7},
                )
            ),
        ),
        DataProcess(
            name="Analysis 2",
            stage=ProcessStage.ANALYSIS,
            experimenters=["Some Analyzer"],
            process_type=ProcessName.ANALYSIS,
            start_date_time=t,
            end_date_time=t,
            output_path="/path/to/outputs",
            code=example_code.model_copy(
                update=dict(
                    parameters={"u": 7, "z": True},
                )
            ),
        ),
    ],
)

if __name__ == "__main__":
    serialized = p.model_dump_json()
    deserialized = Processing.model_validate_json(serialized)
    p.write_standard_file()
