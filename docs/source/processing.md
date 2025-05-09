# Processing

The `processing.json` file captures the data processing and analysis steps that have been carried out – mostly for derived data assets. 
This tracks what code was used for each step, when it was run, what the input and outputs where, what parameters were 
set. This includes things like spike sorting, image alignment, cell segmentation. It also includes manual annotation, 
quality control, and data analysis. This file should be appended with each subsequent stage of processing or analysis.

```{literalinclude} ../../examples/processing.py
:language: python
:linenos:

## Model definitions

### `[DataProcess](processing#DataProcess)`

Description of a single processing step

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | `ProcessName` |  |
| `name` | `str` | ('Unique name of the processing step.', ' If not provided, the type will be used as the name.') |
| `stage` | `ProcessStage` |  |
| `code` | {[Code](components/identifiers#Code)} | [Code](components/identifiers#Code) used for processing |
| `experimenters` | List[{[Person](components/identifiers#Person)}] | People responsible for processing |
| `pipeline_name` | `Optional[str]` | Pipeline names must exist in [Processing](processing#Processing).pipelines |
| `start_date_time` | `datetime (timezone-aware)` |  |
| `end_date_time` | `datetime (timezone-aware)` |  |
| `output_path` | `Optional[aind_data_schema.components.wrappers.AssetPath]` | Path to processing outputs, if stored. |
| `output_parameters` | `aind_data_schema.base.Generic[Model](model#Model)` | Output parameters |
| `notes` | `Optional[str]` |  |
| `resources` | Optional[{[ResourceUsage](processing#ResourceUsage)}] |  |


### `[Processing](processing#Processing)`

Description of all processes run on data

| Field | Type | Description |
|-------|------|-------------|
| `data_processes` | List[{[DataProcess](processing#DataProcess)}] |  |
| `pipelines` | Optional[List[{[Code](components/identifiers#Code)}]] | For processing done with pipelines, list the repositories here. Pipelines must use the name field ,and be referenced in the pipeline_name field of a [DataProcess](processing#DataProcess). |
| `notes` | `Optional[str]` |  |
| `dependency_graph` | `Dict[str, List[str]]` | Directed graph of processing step dependencies. Each key is a process name, and the value is a list of process names that are inputs to that process. |


### `[ResourceTimestamped](processing#ResourceTimestamped)`

Description of resource usage at a moment in time

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `datetime (timezone-aware)` |  |
| `usage` | `float` |  |


### `[ResourceUsage](processing#ResourceUsage)`

Description of resources used by a process

| Field | Type | Description |
|-------|------|-------------|
| `os` | `str` |  |
| `architecture` | `str` |  |
| `cpu` | `Optional[str]` |  |
| `cpu_cores` | `Optional[int]` |  |
| `gpu` | `Optional[str]` |  |
| `system_memory` | `Optional[float]` |  |
| `system_memory_unit` | `Optional[MemoryUnit]` |  |
| `ram` | `Optional[float]` |  |
| `ram_unit` | `Optional[MemoryUnit]` |  |
| `cpu_usage` | Optional[List[{[ResourceTimestamped](processing#ResourceTimestamped)}]] |  |
| `gpu_usage` | Optional[List[{[ResourceTimestamped](processing#ResourceTimestamped)}]] |  |
| `ram_usage` | Optional[List[{[ResourceTimestamped](processing#ResourceTimestamped)}]] |  |
| `usage_unit` | `str` |  |
