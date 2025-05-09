# Data description

The `data_description.json` file tracks administrative information about a data asset, including affiliated researchers/organizations, projects,
data modalities, dates of collection, and more.

```{literalinclude} ../../examples/data_description.py
:language: python
:linenos:
```

## Model definitions

### `[DataDescription](data_description#DataDescription)`

Description of a logical collection of data files

| Field | Type | Description |
|-------|------|-------------|
| `license` | `License` |  |
| `subject_id` | `Optional[str]` | Unique identifier for the subject of data acquisition |
| `creation_time` | `datetime (timezone-aware)` | Time that data files were created, used to uniquely identify the data |
| `tags` | `Optional[List[str]]` | Descriptive strings to help categorize and search for data |
| `name` | `Optional[str]` | Name of data, conventionally also the name of the directory containing all data and metadata |
| `institution` | [Organization](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/organizations.py) | An established society, corporation, foundation or other organization that collected this data |
| `funding_source` | List[{[Funding](data_description#Funding)}] | [Funding](data_description#Funding) source. If internal funding, select 'Allen Institute' |
| `data_level` | `DataLevel` | level of processing that data has undergone |
| `group` | `Optional[Group]` | A short name for the group of individuals that collected this data |
| `investigators` | List[{[Person](components/identifiers#Person)}] | Full name(s) of key investigators (e.g. PI, lead scientist, contact person) |
| `project_name` | `str` | A name for a set of coordinated activities intended to achieve one or more objectives. |
| `restrictions` | `Optional[str]` | Detail any restrictions on publishing or sharing these data |
| `modalities` | List[[Modality](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/modalities.py)] | A short name for the specific manner, characteristic, pattern of application, or the employmentof any technology or formal procedure to generate data for a study |
| `data_summary` | `Optional[str]` | Semantic summary of experimental goal |


### `[Funding](data_description#Funding)`

Description of funding sources

| Field | Type | Description |
|-------|------|-------------|
| `funder` | [Organization](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/organizations.py) |  |
| `grant_number` | `Optional[str]` |  |
| `fundee` | Optional[{[Person](components/identifiers#Person)}] | [Person](components/identifiers#Person)(s) funded by this mechanism |
