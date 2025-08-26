# Data description

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/data_description.py)

The `data_description.json` file tracks administrative information about a data asset, including affiliated researchers/organizations, projects, data modalities, dates of collection, and more.

## Uniqueness

Every data asset is uniquely identified by its `DataDescription.name` field, which combines the `subject_id` and acquisition `session_end_time`. You can group data assets together using the `DataDescription.tags: List[str]`. Tags should be shared across assets within experiments. **Do not repeat information in the tags that already exists elsewhere in the metadata**, for example modalities should never be included in tags.

## Example

```{literalinclude} ../../examples/data_description.py
:language: python
:linenos:
```

## Core file

### DataDescription

Description of a logical collection of data files

| Field | Type | Description |
|-------|------|-------------|
| `license` | [License](aind_data_schema_models/licenses.md#license) |  |
| `subject_id` | `Optional[str]` | Unique identifier for the subject of data acquisition |
| `creation_time` | `datetime (timezone-aware)` | Time that data files were created, used to uniquely identify the data |
| `tags` | `Optional[List[str]]` | Descriptive strings to help categorize and search for data |
| `name` | `Optional[str]` | Name of data, conventionally also the name of the directory containing all data and metadata |
| `institution` | [Organization](aind_data_schema_models/organizations.md#organization) | An established society, corporation, foundation or other organization that collected this data |
| `funding_source` | List[[Funding](data_description.md#funding)] | Funding source. If internal funding, select 'Allen Institute' |
| `data_level` | [DataLevel](aind_data_schema_models/data_name_patterns.md#datalevel) | Level of processing that data has undergone |
| `group` | Optional[[Group](aind_data_schema_models/data_name_patterns.md#group)] | A short name for the group of individuals that collected this data |
| `investigators` | List[[Person](components/identifiers.md#person)] | Full name(s) of key investigators (e.g. PI, lead scientist, contact person) |
| `project_name` | `str` | A name for a set of coordinated activities intended to achieve one or more objectives. |
| `restrictions` | `Optional[str]` | Detail any restrictions on publishing or sharing these data |
| `modalities` | List[[Modality](aind_data_schema_models/modalities.md#modality)] | A short name for the specific manner, characteristic, pattern of application, or the employment of any technology or formal procedure to generate data for a study |
| `source_data` | `Optional[List[str]]` | For derived assets, list the source data asset names used to create this data |
| `data_summary` | `Optional[str]` | Semantic summary of experimental goal |


## Model definitions

### Funding

Description of funding sources

| Field | Type | Description |
|-------|------|-------------|
| `funder` | [Organization](aind_data_schema_models/organizations.md#organization) |  |
| `grant_number` | `Optional[str]` |  |
| `fundee` | Optional[List[[Person](components/identifiers.md#person)]] | Person(s) funded by this mechanism |
