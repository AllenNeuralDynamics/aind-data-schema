# Reagent

## Model definitions

### Antibody

Description of an antibody used in immunolableing

| Field | Type | Description |
|-------|------|-------------|
| `immunolabel_class` | [ImmunolabelClass](#immunolabelclass) |  |
| `fluorophore` | Optional[[Fluorophore](#fluorophore)] |  |
| `mass` | `float` |  |
| `mass_unit` | [MassUnit](aind_data_schema_models/units.md#massunit) |  |
| `notes` | `Optional[str]` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### Fluorophore

Fluorophores used in HCR and Immunolabeling

| Name | Value |
|------|-------|
| `ALEXA_405` | `Alexa Fluor 405` |
| `ALEXA_488` | `Alexa Fluor 488` |
| `ALEXA_546` | `Alexa Fluor 546` |
| `ALEXA_568` | `Alexa Fluor 568` |
| `ALEXA_594` | `Alexa Fluor 594` |
| `ALEXA_633` | `Alexa Fluor 633` |
| `ALEXA_647` | `Alexa Fluor 647` |
| `ATTO_488` | `ATTO 488` |
| `ATTO_565` | `ATTO 565` |
| `ATTO_643` | `ATTO 643` |
| `CY3` | `Cyanine Cy 3` |


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
| `fluorophore` | [Fluorophore](#fluorophore) |  |
| `excitation_wavelength` | `int` |  |
| `excitation_wavelength_unit` | [SizeUnit](aind_data_schema_models/units.md#sizeunit) |  |
| `stain_type` | [StainType](#staintype) |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### ImmunolabelClass

Type of antibodies

| Name | Value |
|------|-------|
| `PRIMARY` | `Primary` |
| `SECONDARY` | `Secondary` |
| `CONJUGATE` | `Conjugate` |


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
| `fluorophore` | [Fluorophore](#fluorophore) |  |
| `excitation_wavelength` | `int` |  |
| `excitation_wavelength_unit` | [SizeUnit](aind_data_schema_models/units.md#sizeunit) |  |
| `stain_type` | [StainType](#staintype) |  |
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
| `stain_type` | [StainType](#staintype) |  |
| `concentration` | `float` |  |
| `concentration_unit` | [ConcentrationUnit](aind_data_schema_models/units.md#concentrationunit) |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### StainType

Stain types for probes describing what is being labeled

| Name | Value |
|------|-------|
| `RNA` | `RNA` |
| `NUCLEAR` | `Nuclear` |
| `FILL` | `Fill` |


