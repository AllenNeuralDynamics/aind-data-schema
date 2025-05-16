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
| `parameters` | `Optional[aind_data_schema.base.GenericModel]` | Parameters used in the code or script |
| `core_dependency` | Optional[[Software](#software)] | For code with a core software package dependency, e.g. Bonsai |


### CombinedData

Description of a group of data assets

| Field | Type | Description |
|-------|------|-------------|
| `assets` | List[[DataAsset](#dataasset)] |  |
| `name` | `Optional[str]` |  |
| `external_links` | Dict[[ExternalPlatforms](#externalplatforms), List[str]] | Links to the Combined Data asset, if materialized. |
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



### ExternalPlatforms

External Platforms of Data Assets.

| Name | Value |
|------|-------|
| `CODEOCEAN` | `Code Ocean` |


### Person

Person identifier

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | First and last name OR anonymous ID |
| `registry` | `aind_data_schema_models.registries._Orcid` |  |
| `registry_identifier` | `Optional[str]` |  |


### Software

Software package identifier

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name of the software package |
| `version` | `Optional[str]` | Version of the software package |


