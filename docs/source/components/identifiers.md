# Identifiers

## Model definitions

### Code

Code or script identifier

| Field | Type | Title (Description) |
|-------|------|-------------|
| `url` | `str` | Code URL (URL to code repository) |
| `name` | `Optional[str]` | Name  |
| `version` | `Optional[str]` | Code version  |
| `container` | Optional[[Container](#container)] | Container  |
| `run_script` | `Optional[pathlib._local.Path]` | Run script (Path to run script) |
| `language` | `Optional[str]` | Programming language (Programming language used) |
| `language_version` | `Optional[str]` | Programming language version  |
| `input_data` | Optional[List[[DataAsset](#dataasset) or [CombinedData](#combineddata)]] | Input data (Input data used in the code or script) |
| `parameters` | `Optional[dict]` | Parameters (Parameters used in the code or script) |
| `core_dependency` | Optional[[Software](#software)] | Core dependency (For code with a core software package dependency, e.g. Bonsai) |


### CombinedData

Description of a group of data assets

| Field | Type | Title (Description) |
|-------|------|-------------|
| `assets` | List[[DataAsset](#dataasset)] | Data assets  |
| `name` | `Optional[str]` | Name  |
| `database_identifier` | Optional[Dict[[Database](#database), List[str]]] | Database identifier (ID or link to the Combined Data asset, if materialized.) |
| `description` | `Optional[str]` | Description (Intention or approach used to select group of assets) |


### Container

Code container identifier, e.g. Docker

| Field | Type | Title (Description) |
|-------|------|-------------|
| `container_type` | `str` | Type (Type of container, e.g. Docker, Singularity) |
| `tag` | `str` | Tag (Tag of the container, e.g. version number) |
| `uri` | `str` | URI (URI of the container, e.g. Docker Hub URL) |


### DataAsset

Description of a single data asset

| Field | Type | Title (Description) |
|-------|------|-------------|
| `url` | `str` | Asset location (URL pointing to the data asset) |


### Database

Database platforms that can host data assets

| Name | Value |
|------|-------|
| `CODEOCEAN` | `Code Ocean` |
| `DANDI` | `DANDI` |


### Person

Person identifier

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Person's name (First and last name OR anonymous ID) |
| `registry` | [Registry](../aind_data_schema_models/registries.md#registry) | Registry  |
| `registry_identifier` | `Optional[str]` | ORCID ID  |


### Software

Software package identifier

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Software name (Name of the software package) |
| `version` | `Optional[str]` | Software version (Version of the software package) |


