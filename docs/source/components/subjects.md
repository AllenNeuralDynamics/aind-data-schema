# Subjects

## Model definitions

### BreedingInfo

Description of breeding info for subject

| Field | Type | Description |
|-------|------|-------------|
| `breeding_group` | `str` |  |
| `maternal_id` | `str` |  |
| `maternal_genotype` | `str` |  |
| `paternal_id` | `str` |  |
| `paternal_genotype` | `str` |  |


### CalibrationObject

Description of a calibration object

| Field | Type | Description |
|-------|------|-------------|
| `empty` | `bool` | Set to true if the calibration was performed with no object. |
| `description` | `str` |  |
| `objects` | Optional[List[[Device](devices.md#device)]] | For calibration objects that are built up from one or more devices. |


### HomeCageEnrichment

Materials provided in animal home cage

| Name | Value |
|------|-------|
| `NO_ENRICHMENT` | `No enrichment` |
| `PLASTIC_SHELTER` | `Plastic shelter` |
| `PLASTIC_TUBE` | `Plastic tube` |
| `RUNNING_WHEEL` | `Running wheel` |
| `OTHER` | `Other` |


### Housing

Description of subject housing

| Field | Type | Description |
|-------|------|-------------|
| `cage_id` | `Optional[str]` |  |
| `room_id` | `Optional[str]` |  |
| `light_cycle` | Optional[[LightCycle](#lightcycle)] |  |
| `home_cage_enrichment` | List[[HomeCageEnrichment](#homecageenrichment)] |  |
| `cohoused_subjects` | `List[str]` | List of IDs of other subjects housed in same cage |


### HumanSubject

Description of a human subject

| Field | Type | Description |
|-------|------|-------------|
| `sex` | [Sex](#sex) |  |
| `year_of_birth` | `int` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Where the subject was acquired from. |


### LightCycle

Description of vivarium light cycle times

| Field | Type | Description |
|-------|------|-------------|
| `lights_on_time` | `datetime.time` | Time in UTC that lights were turned on |
| `lights_off_time` | `datetime.time` | Time in UTC that lights were turned off |


### MouseSubject

Description of a mouse subject

| Field | Type | Description |
|-------|------|-------------|
| `sex` | [Sex](#sex) |  |
| `date_of_birth` | `datetime.date` |  |
| `strain` | [Strain](../aind_data_schema_models/species.md#strain) |  |
| `species` | [Species](../aind_data_schema_models/species.md#species) |  |
| `alleles` | List[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Allele names and persistent IDs |
| `genotype` | `str` | Genotype of the animal providing both alleles |
| `breeding_info` | Optional[[BreedingInfo](#breedinginfo)] |  |
| `wellness_reports` | List[[WellnessReport](#wellnessreport)] |  |
| `housing` | Optional[[Housing](#housing)] |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Where the subject was acquired from. If bred in-house, use Allen Institute. |
| `restrictions` | `Optional[str]` | Any restrictions on use or publishing based on subject source |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | RRID of mouse if acquired from supplier |


### Sex

Subject sex name

| Name | Value |
|------|-------|
| `FEMALE` | `Female` |
| `MALE` | `Male` |


### WellnessReport

Wellness report on animal health

| Field | Type | Description |
|-------|------|-------------|
| `date` | `datetime.date` |  |
| `report` | `str` |  |


