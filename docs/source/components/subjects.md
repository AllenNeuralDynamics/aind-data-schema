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


### Housing

Description of subject housing

| Field | Type | Description |
|-------|------|-------------|
| `cage_id` | `Optional[str]` |  |
| `room_id` | `Optional[str]` |  |
| `light_cycle` | Optional[{LightCycle}] |  |
| `home_cage_enrichment` | `List[HomeCageEnrichment]` |  |
| `cohoused_subjects` | `List[str]` | List of IDs of other subjects housed in same cage |


### HumanSubject

Description of a human subject

| Field | Type | Description |
|-------|------|-------------|
| `sex` | `Sex` |  |
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
| `sex` | `Sex` |  |
| `date_of_birth` | `datetime.date` |  |
| `strain` | `typing.Annotated[typing.Union[aind_data_schema_models.species._C57Bl_6J, aind_data_schema_models.species._Balb_C], FieldInfo(annotation=NoneType, required=True, discriminator='name')]` |  |
| `species` | `typing.Annotated[typing.Union[aind_data_schema_models.species._Callithrix_Jacchus, aind_data_schema_models.species._Homo_Sapiens, aind_data_schema_models.species._Macaca_Mulatta, aind_data_schema_models.species._Mus_Musculus, aind_data_schema_models.species._Rattus_Norvegicus], FieldInfo(annotation=NoneType, required=True, discriminator='name')]` |  |
| `alleles` | `List[aind_data_schema_models.pid_names.PIDName]` | Allele names and persistent IDs |
| `genotype` | `str` | Genotype of the animal providing both alleles |
| `breeding_info` | Optional[{BreedingInfo}] |  |
| `wellness_reports` | List[{WellnessReport}] |  |
| `housing` | Optional[{Housing}] |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Where the subject was acquired from. If bred in-house, use Allen Institute. |
| `restrictions` | `Optional[str]` | Any restrictions on use or publishing based on subject source |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` | RRID of mouse if acquired from supplier |


### WellnessReport

Wellness report on animal health

| Field | Type | Description |
|-------|------|-------------|
| `date` | `datetime.date` |  |
| `report` | `str` |  |


