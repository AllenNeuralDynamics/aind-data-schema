# Reagent

## Model definitions

### FluorescentStain

Description of a fluorescent stain

| Field | Type | Title (Description) |
|-------|------|-------------|
| `probe` | [GeneProbe](#geneprobe) or [ProteinProbe](#proteinprobe) or [SmallMoleculeProbe](#smallmoleculeprobe) | Target of the stain  |
| `stain_type` | [StainType](../aind_data_schema_models/reagent.md#staintype) | Stain type  |
| `fluorophore` | [Fluorophore](#fluorophore) | Fluorophore used in the stain  |
| `initiator_name` | `Optional[str]` | Initiator for HCR probes  |
| `name` | `str` | Name  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Research Resource ID  |
| `lot_number` | `Optional[str]` | Lot number  |
| `expiration_date` | `Optional[datetime.date]` | Lot expiration date  |


### Fluorophore

Flurophore used in HCR, Immunolabeling, etc

| Field | Type | Title (Description) |
|-------|------|-------------|
| `fluorophore_type` | [FluorophoreType](../aind_data_schema_models/reagent.md#fluorophoretype) | Fluorophore type  |
| `excitation_wavelength` | `int` | Excitation wavelength (nm)  |
| `excitation_wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Excitation wavelength unit  |


### GeneProbe

Description of a set of oligonucleotide probes targeting a specific gene

| Field | Type | Title (Description) |
|-------|------|-------------|
| `gene` | [PIDName](../aind_data_schema_models/pid_names.md#pidname) | Gene name  |
| `probes` | Optional[List[[OligoProbe](#oligoprobe)]] | Probes  |


### GeneProbeSet

set of probes used in BarSEQ

| Field | Type | Title (Description) |
|-------|------|-------------|
| `gene_probes` | List[[GeneProbe](#geneprobe)] | Gene probes  |
| `name` | `str` | Name  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Research Resource ID  |
| `lot_number` | `Optional[str]` | Lot number  |
| `expiration_date` | `Optional[datetime.date]` | Lot expiration date  |


### OligoProbe

Description of an oligonucleotide probe

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Name  |
| `sequence` | `str` | Sequence  |


### ProbeReagent

Description of a probe used as a reagent

| Field | Type | Title (Description) |
|-------|------|-------------|
| `target` | [GeneProbe](#geneprobe) or [ProteinProbe](#proteinprobe) or [SmallMoleculeProbe](#smallmoleculeprobe) | Target  |
| `name` | `str` | Name  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Research Resource ID  |
| `lot_number` | `Optional[str]` | Lot number  |
| `expiration_date` | `Optional[datetime.date]` | Lot expiration date  |


### ProteinProbe

Description of a protein probe including antibodies

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protein` | [PIDName](../aind_data_schema_models/pid_names.md#pidname) | Target protein name  |
| `species` | Optional[[Species](../aind_data_schema_models/species.md#species)] | Species of the probe  |
| `mass` | `float` | Mass of protein probe (ug)  |
| `mass_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) | Mass unit  |
| `sequence` | `Optional[str]` | Amino acid sequence of the probe  |


### Reagent

Description of reagent used in procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Name  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Research Resource ID  |
| `lot_number` | `Optional[str]` | Lot number  |
| `expiration_date` | `Optional[datetime.date]` | Lot expiration date  |


### SmallMoleculeProbe

Description of a small molecule probe

| Field | Type | Title (Description) |
|-------|------|-------------|
| `molecule` | [PIDName](../aind_data_schema_models/pid_names.md#pidname) | Target small molecule name  |
| `mass` | `float` | Mass of small molecule probe (ug)  |
| `mass_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) | Mass unit  |


