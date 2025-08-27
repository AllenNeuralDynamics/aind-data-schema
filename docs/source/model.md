# Model

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/model.py)

The Model metadata schema is an extension of the Processing schema tailored to model weights and other data and code artifacts underlying machine learning models - these may be trained on one dataset and evaluated on others, and may be intended to undergo further training iteratively in future versions.

Thus new evaluations and training steps can easily be appended for new model versions. This metadata should be documented for any models that see widespread internal use or public release, in order to facilitate model reuse and document provenance.

## Core file

### Model

Description of a machine learning model including architecture, training, and evaluation details

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `version` | `str` |  |
| `example_run_code` | [Code](components/identifiers.md#code) | Code to run the model, possibly including example parameters/data |
| `architecture` | [ModelArchitecture](aind_data_schema_models/system_architecture.md#modelarchitecture) | Model architecture / type of model |
| `software_framework` | Optional[[Software](components/identifiers.md#software)] |  |
| `architecture_parameters` | `dict` | Parameters of model architecture, such as input signature or number of layers. |
| `intended_use` | `str` | Semantic description of intended use |
| `limitations` | `Optional[str]` |  |
| `training` | List[[ModelTraining](model.md#modeltraining) or [ModelPretraining](model.md#modelpretraining)] |  |
| `evaluations` | List[[ModelEvaluation](model.md#modelevaluation)] |  |
| `notes` | `Optional[str]` |  |


## Model definitions

### ModelEvaluation

Description of model evaluation

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | [ProcessName](aind_data_schema_models/process_names.md#processname) |  |
| `performance` | List[[PerformanceMetric](model.md#performancemetric)] |  |
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


### ModelPretraining

Description of model pretraining

| Field | Type | Description |
|-------|------|-------------|
| `source_url` | `str` | URL for pretrained weights |


### ModelTraining

Description of model training

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | [ProcessName](aind_data_schema_models/process_names.md#processname) |  |
| `train_performance` | List[[PerformanceMetric](model.md#performancemetric)] | Performance on training set |
| `test_performance` | Optional[List[[PerformanceMetric](model.md#performancemetric)]] | Performance on test data, evaluated during training |
| `test_evaluation_method` | `Optional[str]` | Approach to cross-validation or Train/test splitting |
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


### PerformanceMetric

Description of a performance metric

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `value` | `typing.Any` |  |
