# Reagent

## Model definitions

### FluorescentStain

Description of a fluorescent stain

| Field | Type | Description |
|-------|------|-------------|
| `probe` | [GeneProbe](#geneprobe) or [ProteinProbe](#proteinprobe) or [SmallMoleculeProbe](#smallmoleculeprobe) |  |
| `stain_type` | [StainType](../aind_data_schema_models/reagent.md#staintype) |  |
| `fluorophore` | [Fluorophore](#fluorophore) |  |
| `initiator_name` | `Optional[str]` |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] |  |
| `lot_number` | `Optional[str]` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### Fluorophore

Flurophore used in HCR, Immunolabeling, etc

| Field | Type | Description |
|-------|------|-------------|
| `fluorophore_type` | [FluorophoreType](../aind_data_schema_models/reagent.md#fluorophoretype) |  |
| `excitation_wavelength` | `int` |  |
| `excitation_wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |


### GeneProbe

Description of a set of oligonucleotide probes targeting a specific gene

| Field | Type | Description |
|-------|------|-------------|
| `gene` | [PIDName](../aind_data_schema_models/pid_names.md#pidname) |  |
| `probes` | Optional[List[[OligoProbe](#oligoprobe)]] |  |


### GeneProbeSet

set of probes used in BarSEQ

| Field | Type | Description |
|-------|------|-------------|
| `gene_probes` | List[[GeneProbe](#geneprobe)] |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] |  |
| `lot_number` | `Optional[str]` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### OligoProbe

Description of an oligonucleotide probe

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `sequence` | `str` |  |


### ProbeReagent

Description of a probe used as a reagent

| Field | Type | Description |
|-------|------|-------------|
| `target` | [GeneProbe](#geneprobe) or [ProteinProbe](#proteinprobe) or [SmallMoleculeProbe](#smallmoleculeprobe) |  |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] |  |
| `lot_number` | `Optional[str]` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### ProteinProbe

Description of a protein probe including antibodies

| Field | Type | Description |
|-------|------|-------------|
| `protein` | [PIDName](../aind_data_schema_models/pid_names.md#pidname) |  |
| `species` | Optional[[Species](../aind_data_schema_models/species.md#species)] |  |
| `mass` | `float` |  |
| `mass_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) |  |
| `sequence` | `Optional[str]` |  |


### Reagent

Description of reagent used in procedure

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] |  |
| `lot_number` | `Optional[str]` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### SmallMoleculeProbe

Description of a small molecule probe

| Field | Type | Description |
|-------|------|-------------|
| `molecule` | [PIDName](../aind_data_schema_models/pid_names.md#pidname) |  |
| `mass` | `float` |  |
| `mass_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) |  |


