# Model

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/model.py)

The Model metadata schema is an extension of the Processing schema tailored to model weights and other data and code artifacts underlying machine learning models - these may be trained on one dataset and evaluated on others, and may be intended to undergo further training iteratively in future versions.

Thus new evaluations and training steps can easily be appended for new model versions. This metadata should be documented for any models that see widespread internal use or public release, in order to facilitate model reuse and document provenance.

## Core file

### Model

Description of a machine learning model including architecture, training, and evaluation details

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Name  |
| `version` | `str` | Version  |
| `example_run_code` | [Code](components/identifiers.md#code) | Example run code (Code to run the model, possibly including example parameters/data) |
| `architecture` | [ModelArchitecture](aind_data_schema_models/system_architecture.md#modelarchitecture) | architecture (Model architecture / type of model) |
| `software_framework` | Optional[[Software](components/identifiers.md#software)] | Software framework  |
| `architecture_parameters` | `Optional[dict]` | Architecture parameters (Parameters of model architecture, such as input signature or number of layers.) |
| `intended_use` | `str` | Intended model use (Semantic description of intended use) |
| `limitations` | `Optional[str]` | Model limitations  |
| `training` | List[[ModelTraining](model.md#modeltraining) or [ModelPretraining](model.md#modelpretraining)] | Training  |
| `evaluations` | List[[ModelEvaluation](model.md#modelevaluation)] | Evaluations  |
| `notes` | `Optional[str]` | Notes  |


## Model definitions

### ModelEvaluation

Description of model evaluation

| Field | Type | Title (Description) |
|-------|------|-------------|
| `process_type` | [ProcessName](aind_data_schema_models/process_names.md#processname) |   |
| `performance` | List[[PerformanceMetric](model.md#performancemetric)] | Evaluation performance  |
| `name` | `str` | Name (('Unique name of the processing step.', ' If not provided, the type will be used as the name.')) |
| `stage` | [ProcessStage](processing.md#processstage) | Processing stage  |
| `code` | [Code](components/identifiers.md#code) | Code (Code used for processing) |
| `experimenters` | `List[str]` | Experimenters (People responsible for processing) |
| `pipeline_name` | `Optional[str]` | Pipeline name (Pipeline names must exist in Processing.pipelines) |
| `start_date_time` | `datetime (timezone-aware)` | Start date time  |
| `end_date_time` | `Optional[datetime (timezone-aware)]` | End date time  |
| `output_path` | `Optional[AssetPath]` | Output path (Path to processing outputs, if stored.) |
| `output_parameters` | `Optional[dict]` | Outputs (Output parameters) |
| `notes` | `Optional[str]` | Notes  |
| `resources` | Optional[[ResourceUsage](processing.md#resourceusage)] | Process resource usage  |


### ModelPretraining

Description of model pretraining

| Field | Type | Title (Description) |
|-------|------|-------------|
| `source_url` | `str` | Pretrained source URL (URL for pretrained weights) |


### ModelTraining

Description of model training

| Field | Type | Title (Description) |
|-------|------|-------------|
| `process_type` | [ProcessName](aind_data_schema_models/process_names.md#processname) |   |
| `train_performance` | List[[PerformanceMetric](model.md#performancemetric)] | Training performance (Performance on training set) |
| `test_performance` | Optional[List[[PerformanceMetric](model.md#performancemetric)]] | Test performance (Performance on test data, evaluated during training) |
| `test_evaluation_method` | `Optional[str]` | Test evaluation method (Approach to cross-validation or Train/test splitting) |
| `name` | `str` | Name (('Unique name of the processing step.', ' If not provided, the type will be used as the name.')) |
| `stage` | [ProcessStage](processing.md#processstage) | Processing stage  |
| `code` | [Code](components/identifiers.md#code) | Code (Code used for processing) |
| `experimenters` | `List[str]` | Experimenters (People responsible for processing) |
| `pipeline_name` | `Optional[str]` | Pipeline name (Pipeline names must exist in Processing.pipelines) |
| `start_date_time` | `datetime (timezone-aware)` | Start date time  |
| `end_date_time` | `Optional[datetime (timezone-aware)]` | End date time  |
| `output_path` | `Optional[AssetPath]` | Output path (Path to processing outputs, if stored.) |
| `output_parameters` | `Optional[dict]` | Outputs (Output parameters) |
| `notes` | `Optional[str]` | Notes  |
| `resources` | Optional[[ResourceUsage](processing.md#resourceusage)] | Process resource usage  |


### PerformanceMetric

Description of a performance metric

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Metric name  |
| `value` | `typing.Any` | Metric value  |
