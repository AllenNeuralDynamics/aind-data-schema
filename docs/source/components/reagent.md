# Reagent

## Model definitions

### Antibody

Description of an antibody used in immunolableing

| Field | Type | Description |
|-------|------|-------------|
| `immunolabel_class` | `ImmunolabelClass` |  |
| `fluorophore` | `Optional[Fluorophore]` |  |
| `mass` | `float` |  |
| `mass_unit` | `MassUnit` |  |
| `notes` | `Optional[str]` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### GeneProbes

Description of a set of oligonucleotide probes targeting a specific gene

| Field | Type | Description |
|-------|------|-------------|
| `gene` | `aind_data_schema_models.pid_names.PIDName` |  |
| `probes` | List[[OligoProbe](#oligoprobe)] |  |


### GeneticStain

Description of an oligonucleotide probe(s) targeting a gene and readout

| Field | Type | Description |
|-------|------|-------------|
| `gene_probe` | [GeneProbes](#geneprobes) |  |
| `readout` | [Readout](#readout) or [HCRReadout](#hcrreadout) |  |
| `species` | `typing.Annotated[typing.Union[aind_data_schema_models.species._Callithrix_Jacchus, aind_data_schema_models.species._Homo_Sapiens, aind_data_schema_models.species._Macaca_Mulatta, aind_data_schema_models.species._Mus_Musculus, aind_data_schema_models.species._Rattus_Norvegicus], FieldInfo(annotation=NoneType, required=True, discriminator='name')]` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### HCRReadout

Description of a readout for HCR

| Field | Type | Description |
|-------|------|-------------|
| `initiator_name` | `str` |  |
| `fluorophore` | `Fluorophore` |  |
| `excitation_wavelength` | `int` |  |
| `excitation_wavelength_unit` | `SizeUnit` |  |
| `stain_type` | `StainType` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### OligoProbe

Description of an oligonucleotide probe

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `sequence` | `str` |  |


### OligoProbeSet

set of probes used in BarSEQ

| Field | Type | Description |
|-------|------|-------------|
| `gene_probes` | List[[GeneProbes](#geneprobes)] |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### Readout

Description of a readout

| Field | Type | Description |
|-------|------|-------------|
| `fluorophore` | `Fluorophore` |  |
| `excitation_wavelength` | `int` |  |
| `excitation_wavelength_unit` | `SizeUnit` |  |
| `stain_type` | `StainType` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### Reagent

Description of reagent used in procedure

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### Stain

Description of a non-oligo probe stain

| Field | Type | Description |
|-------|------|-------------|
| `stain_type` | `StainType` |  |
| `concentration` | `float` |  |
| `concentration_unit` | `ConcentrationUnit` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


