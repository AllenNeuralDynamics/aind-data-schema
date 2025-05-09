# Model

### `[Model](model#Model)`

Description of an analysis model

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `version` | `str` |  |
| `example_run_code` | {[Code](components/identifiers#Code)} | [Code](components/identifiers#Code) to run the model, possibly including example parameters/data |
| `architecture` | `[Model](model#Model)Architecture` | [Model](model#Model) architecture / type of model |
| `software_framework` | Optional[{[Software](components/identifiers#Software)}] |  |
| `architecture_parameters` | `aind_data_schema.base.Generic[Model](model#Model)` | Parameters of model architecture, such as input signature or number of layers. |
| `intended_use` | `str` | Semantic description of intended use |
| `limitations` | `Optional[str]` |  |
| `training` | List[{[Model](model#Model)Training} | {[Model](model#Model)Pretraining}] |  |
| `evaluations` | List[{[Model](model#Model)Evaluation}] |  |
| `notes` | `Optional[str]` |  |


### `[Model](model#Model)Evaluation`

Description of model evaluation

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | `ProcessName` |  |
| `performance` | List[{[PerformanceMetric](model#PerformanceMetric)}] |  |
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


### `[Model](model#Model)Pretraining`

Description of model pretraining

| Field | Type | Description |
|-------|------|-------------|
| `source_url` | `str` | URL for pretrained weights |


### `[Model](model#Model)Training`

Description of model training

| Field | Type | Description |
|-------|------|-------------|
| `process_type` | `ProcessName` |  |
| `train_performance` | List[{[PerformanceMetric](model#PerformanceMetric)}] | Performance on training set |
| `test_performance` | Optional[List[{[PerformanceMetric](model#PerformanceMetric)}]] | Performance on test data, evaluated during training |
| `test_evaluation_method` | `Optional[str]` | Approach to cross-validation or Train/test splitting |
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


### `[PerformanceMetric](model#PerformanceMetric)`

Description of a performance metric

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `value` | `typing.Any` |  |
