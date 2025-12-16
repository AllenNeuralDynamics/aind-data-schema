# Subjects

## Model definitions

### BreedingInfo

Description of breeding info for subject

| Field | Type | Title (Description) |
|-------|------|-------------|
| <del>`breeding_group`</del> | `Optional[str]` | **[DEPRECATED]** Field will be removed in future releases. Breeding Group  |
| `maternal_id` | `str` | Maternal specimen ID  |
| `maternal_genotype` | `str` | Maternal genotype  |
| `paternal_id` | `str` | Paternal specimen ID  |
| `paternal_genotype` | `str` | Paternal genotype  |


### CalibrationObject

Description of a calibration object

| Field | Type | Title (Description) |
|-------|------|-------------|
| `empty` | `bool` | Empty (Set to true if the calibration was performed with no object.) |
| `description` | `str` | Description  |
| `objects` | Optional[List[[Device](devices.md#device)]] | Objects (For calibration objects that are built up from one or more devices.) |


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

| Field | Type | Title (Description) |
|-------|------|-------------|
| `cage_id` | `Optional[str]` | Cage ID  |
| `room_id` | `Optional[str]` | Room ID  |
| `light_cycle` | Optional[[LightCycle](#lightcycle)] | Light cycle  |
| `home_cage_enrichment` | List[[HomeCageEnrichment](#homecageenrichment)] | Home cage enrichment  |
| `cohoused_subjects` | `List[str]` | Co-housed subjects (List of IDs of other subjects housed in same cage) |


### HumanSubject

Description of a human subject

| Field | Type | Title (Description) |
|-------|------|-------------|
| `sex` | [Sex](#sex) | Sex  |
| `year_of_birth` | `int` | Year of birth  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source (Where the subject was acquired from.) |


### LightCycle

Description of vivarium light cycle times

| Field | Type | Title (Description) |
|-------|------|-------------|
| `lights_on_time` | `datetime.time` | Lights on time (Time in UTC that lights were turned on) |
| `lights_off_time` | `datetime.time` | Lights off time (Time in UTC that lights were turned off) |


### MouseSubject

Description of a mouse subject

| Field | Type | Title (Description) |
|-------|------|-------------|
| `sex` | [Sex](#sex) | Sex  |
| `date_of_birth` | `datetime.date` | Date of birth  |
| `strain` | [Strain](../aind_data_schema_models/species.md#strain) | Strain  |
| `species` | [Species](../aind_data_schema_models/species.md#species) | Species  |
| `alleles` | List[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Alleles (Allele names and persistent IDs) |
| `genotype` | `str` | Genotype (Genotype of the animal providing both alleles) |
| `breeding_info` | Optional[[BreedingInfo](#breedinginfo)] | Breeding Info  |
| `wellness_reports` | List[[WellnessReport](#wellnessreport)] | Wellness Report  |
| `housing` | Optional[[Housing](#housing)] | Housing  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source (Where the subject was acquired from. If bred in-house, use Allen Institute.) |
| `restrictions` | `Optional[str]` | Restrictions (Any restrictions on use or publishing based on subject source) |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | RRID (RRID of mouse if acquired from supplier) |


### Sex

Subject sex name

| Name | Value |
|------|-------|
| `FEMALE` | `Female` |
| `MALE` | `Male` |


### WellnessReport

Wellness report on animal health

| Field | Type | Title (Description) |
|-------|------|-------------|
| `date` | `datetime.date` | Date  |
| `report` | `str` | Report  |


