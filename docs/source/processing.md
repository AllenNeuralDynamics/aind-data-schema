# Processing

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/processing.py)

The `processing.json` file captures the data processing and analysis steps that have been carried out – mostly for derived data assets. This tracks what code was used for each step, when it was run, what the input and outputs where, what parameters were set. This includes things like spike sorting, image alignment, cell segmentation. It also includes manual annotation, quality control, and data analysis.

The processing file should be appended to with each subsequent stage of processing or analysis.

## Example

```{literalinclude} ../../examples/processing.py
:language: python
:linenos:
```

## Core file

### Processing

Description of all processes run on data

| Field | Type | Description |
|-------|------|-------------|
| `data_processes` | List[[DataProcess](processing.md#dataprocess)] |  |
| `pipelines` | Optional[List[[Code](components/identifiers.md#code)]] | For processing done with pipelines, list the repositories here. Pipelines must use the name field ,and be referenced in the pipeline_name field of a DataProcess. |
| `notes` | `Optional[str]` |  |
| `dependency_graph` | `Optional[Dict[str, List[str]]]` | Directed graph of processing step dependencies. Each key is a process name, and the value is a list of process names that are inputs to that process. |


## Model definitions

### DataProcess

Description of a single processing step

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | [ProcessName](aind_data_schema_models/process_names.md#processname) |  |
| `name` | `str` | ('Unique name of the processing step.', ' If not provided, the type will be used as the name.') |
| `stage` | [ProcessStage](processing.md#processstage) |  |
| `code` | [Code](components/identifiers.md#code) | Code used for processing |
| `experimenters` | `List[str]` | People responsible for processing |
| `pipeline_name` | `Optional[str]` | Pipeline names must exist in Processing.pipelines |
| `start_date_time` | `datetime (timezone-aware)` |  |
| `end_date_time` | `Optional[datetime (timezone-aware)]` |  |
| `output_path` | `Optional[AssetPath]` | Path to processing outputs, if stored. |
| `output_parameters` | `dict` | Output parameters |
| `notes` | `Optional[str]` |  |
| `resources` | Optional[[ResourceUsage](processing.md#resourceusage)] |  |


### ProcessStage

Stages of processing

| Name | Value |
|------|-------|
| `PROCESSING` | `Processing` |
| `ANALYSIS` | `Analysis` |


### ResourceTimestamped

Description of resource usage at a moment in time

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `datetime (timezone-aware)` |  |
| `usage` | `float` |  |


### ResourceUsage

Description of resources used by a process

| Field | Type | Description |
|-------|------|-------------|
| `os` | `str` |  |
| `architecture` | `str` |  |
| `cpu` | `Optional[str]` |  |
| `cpu_cores` | `Optional[int]` |  |
| `gpu` | `Optional[str]` |  |
| `system_memory` | `Optional[float]` |  |
| `system_memory_unit` | Optional[[MemoryUnit](aind_data_schema_models/units.md#memoryunit)] |  |
| `ram` | `Optional[float]` |  |
| `ram_unit` | Optional[[MemoryUnit](aind_data_schema_models/units.md#memoryunit)] |  |
| `cpu_usage` | Optional[List[[ResourceTimestamped](processing.md#resourcetimestamped)]] |  |
| `gpu_usage` | Optional[List[[ResourceTimestamped](processing.md#resourcetimestamped)]] |  |
| `ram_usage` | Optional[List[[ResourceTimestamped](processing.md#resourcetimestamped)]] |  |
| `usage_unit` | `str` |  |
