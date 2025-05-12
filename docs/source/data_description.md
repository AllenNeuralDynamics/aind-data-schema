# Data description

The `data_description.json` file tracks administrative information about a data asset, including affiliated researchers/organizations, projects,
data modalities, dates of collection, and more.

## Example

```{literalinclude} ../../examples/data_description.py
:language: python
:linenos:
```

## Model definitions

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
| `funding_source` | List[[Funding](#funding)] | Funding source. If internal funding, select 'Allen Institute' |
| `data_level` | [DataLevel](aind_data_schema_models/data_name_patterns.md#datalevel) | level of processing that data has undergone |
| `group` | Optional[[Group](aind_data_schema_models/data_name_patterns.md#group)] | A short name for the group of individuals that collected this data |
| `investigators` | List[[Person](components/identifiers.md#person)] | Full name(s) of key investigators (e.g. PI, lead scientist, contact person) |
| `project_name` | `str` | A name for a set of coordinated activities intended to achieve one or more objectives. |
| `restrictions` | `Optional[str]` | Detail any restrictions on publishing or sharing these data |
| `modalities` | List[[Modality](aind_data_schema_models/modalities.md#modality)] | A short name for the specific manner, characteristic, pattern of application, or the employmentof any technology or formal procedure to generate data for a study |
| `data_summary` | `Optional[str]` | Semantic summary of experimental goal |


### Funding

Description of funding sources

| Field | Type | Description |
|-------|------|-------------|
| `funder` | [Organization](aind_data_schema_models/organizations.md#organization) |  |
| `grant_number` | `Optional[str]` |  |
| `fundee` | Optional[[Person](components/identifiers.md#person)] | Person(s) funded by this mechanism |
