# Processing

The `processing.json` file captures the data processing and analysis steps that have been carried out – mostly for derived data assets. 
This tracks what code was used for each step, when it was run, what the input and outputs where, what parameters were 
set. This includes things like spike sorting, image alignment, cell segmentation. It also includes manual annotation, 
quality control, and data analysis. This file should be appended with each subsequent stage of processing or analysis.

## Example

```{literalinclude} ../../examples/processing.py
:language: python
:linenos:
```

## Model definitions

### DataProcess

Description of a single processing step

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | {ProcessName} |  |
| `name` | `str` | ('Unique name of the processing step.', ' If not provided, the type will be used as the name.') |
| `stage` | [ProcessStage](#processstage) |  |
| `code` | [Code](components/identifiers.md#code) | Code used for processing |
| `experimenters` | List[[Person](components/identifiers.md#person)] | People responsible for processing |
| `pipeline_name` | `Optional[str]` | Pipeline names must exist in Processing.pipelines |
| `start_date_time` | `datetime (timezone-aware)` |  |
| `end_date_time` | `datetime (timezone-aware)` |  |
| `output_path` | `Optional[aind_data_schema.components.wrappers.AssetPath]` | Path to processing outputs, if stored. |
| `output_parameters` | `aind_data_schema.base.GenericModel` | Output parameters |
| `notes` | `Optional[str]` |  |
| `resources` | Optional[[ResourceUsage](#resourceusage)] |  |


### Enum

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.

| Name | Value |
|------|-------|



### MemoryUnit

Computer memory units

| Name | Value |
|------|-------|
| `B` | `Byte` |
| `KB` | `Kilobyte` |
| `MB` | `Megabyte` |
| `GB` | `Gigabyte` |
| `TB` | `Terabyte` |
| `PB` | `Petabyte` |
| `EB` | `Exabyte` |


### ProcessName

Process names

| Name | Value |
|------|-------|
| `ANALYSIS` | `Analysis` |
| `COMPRESSION` | `Compression` |
| `DENOISING` | `Denoising` |
| `EPHYS_CURATION` | `Ephys curation` |
| `EPHYS_POSTPROCESSING` | `Ephys postprocessing` |
| `EPHYS_PREPROCESSING` | `Ephys preprocessing` |
| `EPHYS_VISUALIZATION` | `Ephys visualization` |
| `FIDUCIAL_SEGMENTATION` | `Fiducial segmentation` |
| `FILE_FORMAT_CONVERSION` | `File format conversion` |
| `FLUORESCENCE_EVENT_DETECTION` | `Fluorescence event detection` |
| `IMAGE_ATLAS_ALIGNMENT` | `Image atlas alignment` |
| `IMAGE_BACKGROUND_SUBTRACTION` | `Image background subtraction` |
| `IMAGE_CELL_CLASSIFICATION` | `Image cell classification` |
| `IMAGE_CELL_QUANTIFICATION` | `Image cell quantification` |
| `IMAGE_CELL_SEGMENTATION` | `Image cell segmentation` |
| `IMAGE_CROSS_IMAGE_ALIGNMENT` | `Image cross-image alignment` |
| `IMAGE_DESTRIPING` | `Image destriping` |
| `IMAGE_FLAT_FIELD_CORRECTION` | `Image flat-field correction` |
| `IMAGE_IMPORTING` | `Image importing` |
| `IMAGE_MIP_VISUALIZATION` | `Image mip visualization` |
| `IMAGE_RADIAL_CORRECTION` | `Image radial correction` |
| `IMAGE_SPOT_DETECTION` | `Image spot detection` |
| `IMAGE_SPOT_SPECTRAL_UNMIXING` | `Image spot spectral unmixing` |
| `IMAGE_THRESHOLDING` | `Image thresholding` |
| `IMAGE_TILE_ALIGNMENT` | `Image tile alignment` |
| `IMAGE_TILE_FUSING` | `Image tile fusing` |
| `IMAGE_TILE_PROJECTION` | `Image tile projection` |
| `MODEL_EVALUATION` | `Model evaluation` |
| `MODEL_TRAINING` | `Model training` |
| `NEUROPIL_SUBTRACTION` | `Neuropil subtraction` |
| `OTHER` | `Other` |
| `PIPELINE` | `Pipeline` |
| `SIMULATION` | `Simulation` |
| `SKULL_STRIPPING` | `Skull stripping` |
| `SPATIAL_TIMESERIES_DEMIXING` | `Spatial timeseries demixing` |
| `SPIKE_SORTING` | `Spike sorting` |
| `VIDEO_ROI_CLASSIFICATION` | `Video ROI classification` |
| `VIDEO_ROI_CROSS_SESSION_MATCHING` | `Video ROI cross session matching` |
| `VIDEO_ROI_SEGMENTATION` | `Video ROI segmentation` |
| `VIDEO_ROI_TIMESERIES_EXTRACTION` | `Video ROI timeseries extraction` |
| `VIDEO_MOTION_CORRECTION` | `Video motion correction` |
| `VIDEO_PLANE_DECROSSTALK` | `Video plane decrosstalk` |
| `DF_F_ESTIMATION` | `dF/F estimation` |


### ProcessStage

Stages of processing

| Name | Value |
|------|-------|
| `PROCESSING` | `Processing` |
| `ANALYSIS` | `Analysis` |


### Processing

Description of all processes run on data

| Field | Type | Description |
|-------|------|-------------|
| `data_processes` | List[[DataProcess](#dataprocess)] |  |
| `pipelines` | Optional[List[[Code](components/identifiers.md#code)]] | For processing done with pipelines, list the repositories here. Pipelines must use the name field ,and be referenced in the pipeline_name field of a DataProcess. |
| `notes` | `Optional[str]` |  |
| `dependency_graph` | `Dict[str, List[str]]` | Directed graph of processing step dependencies. Each key is a process name, and the value is a list of process names that are inputs to that process. |


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
| `cpu_usage` | Optional[List[[ResourceTimestamped](#resourcetimestamped)]] |  |
| `gpu_usage` | Optional[List[[ResourceTimestamped](#resourcetimestamped)]] |  |
| `ram_usage` | Optional[List[[ResourceTimestamped](#resourcetimestamped)]] |  |
| `usage_unit` | `str` |  |


### UnitlessUnit

Unitless options

| Name | Value |
|------|-------|
| `PERCENT` | `percent` |
| `FC` | `fraction of cycle` |
