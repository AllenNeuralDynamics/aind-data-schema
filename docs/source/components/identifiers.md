# Identifiers

## Model definitions

### Code

Code or script identifier

| Field | Type | Description |
|-------|------|-------------|
| `url` | `str` | URL to code repository |
| `name` | `Optional[str]` |  |
| `version` | `Optional[str]` |  |
| `container` | Optional[[Container](#container)] |  |
| `run_script` | `Optional[pathlib.Path]` | Path to run script |
| `language` | `Optional[str]` | Programming language used |
| `language_version` | `Optional[str]` |  |
| `input_data` | Optional[List[[DataAsset](#dataasset) or [CombinedData](#combineddata)]] | Input data used in the code or script |
| `parameters` | `Optional[dict]` | Parameters used in the code or script |
| `core_dependency` | Optional[[Software](#software)] | For code with a core software package dependency, e.g. Bonsai |


### CombinedData

Description of a group of data assets

| Field | Type | Description |
|-------|------|-------------|
| `assets` | List[[DataAsset](#dataasset)] |  |
| `name` | `Optional[str]` |  |
| `database_identifier` | Optional[Dict[[Database](#database), List[str]]] | ID or link to the Combined Data asset, if materialized. |
| `description` | `Optional[str]` | Intention or approach used to select group of assets |


### Container

Code container identifier, e.g. Docker

| Field | Type | Description |
|-------|------|-------------|
| `container_type` | `str` | Type of container, e.g. Docker, Singularity |
| `tag` | `str` | Tag of the container, e.g. version number |
| `uri` | `str` | URI of the container, e.g. Docker Hub URL |


### DataAsset

Description of a single data asset

| Field | Type | Description |
|-------|------|-------------|
| `url` | `str` | URL pointing to the data asset |


### Database

Database platforms that can host data assets

| Name | Value |
|------|-------|
| `CODEOCEAN` | `Code Ocean` |
| `DANDI` | `DANDI` |


### Person

Person identifier

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | First and last name OR anonymous ID |
| `registry` | [Registry](../aind_data_schema_models/registries.md#registry) |  |
| `registry_identifier` | `Optional[str]` |  |


### Software

Software package identifier

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name of the software package |
| `version` | `Optional[str]` | Version of the software package |


