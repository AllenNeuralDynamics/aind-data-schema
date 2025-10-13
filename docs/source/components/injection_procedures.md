# Injection_procedures

## Model definitions

### Injection

Description of an injection procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `injection_materials` | List[[ViralMaterial](#viralmaterial) or [NonViralMaterial](#nonviralmaterial)] | Injection material  |
| `targeted_structure` | Optional[[MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel)] | Injection target (Use InjectionTargets) |
| `relative_position` | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] | Relative position  |
| `dynamics` | List[[InjectionDynamics](#injectiondynamics)] | Injection dynamics (List of injection events, one per location/depth) |
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |


### InjectionDynamics

Description of the volume and rate of an injection

| Field | Type | Title (Description) |
|-------|------|-------------|
| `profile` | [InjectionProfile](#injectionprofile) | Injection profile  |
| `volume` | `Optional[float]` | Injection volume  |
| `volume_unit` | Optional[[VolumeUnit](../aind_data_schema_models/units.md#volumeunit)] | Injection volume unit  |
| `duration` | `Optional[float]` | Injection duration  |
| `duration_unit` | Optional[[TimeUnit](../aind_data_schema_models/units.md#timeunit)] | Injection duration unit  |
| `injection_current` | `Optional[float]` | Injection current (uA)  |
| `injection_current_unit` | Optional[[CurrentUnit](../aind_data_schema_models/units.md#currentunit)] | Injection current unit  |
| `alternating_current` | `Optional[str]` | Alternating current  |


### InjectionProfile

Injection profile

| Name | Value |
|------|-------|
| `BOLUS` | `Bolus` |
| `CONTINUOUS` | `Continuous` |
| `PULSED` | `Pulsed` |


### NonViralMaterial

Description of a non-viral injection material

| Field | Type | Title (Description) |
|-------|------|-------------|
| `concentration` | `Optional[float]` | Concentration (Must provide concentration unit) |
| `concentration_unit` | `Optional[str]` | Concentration unit (For example, mg/mL) |
| `name` | `str` | Name  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) | Source  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Research Resource ID  |
| `lot_number` | `Optional[str]` | Lot number  |
| `expiration_date` | `Optional[datetime.date]` | Lot expiration date  |


### TarsVirusIdentifiers

TARS data for a viral prep

| Field | Type | Title (Description) |
|-------|------|-------------|
| `virus_tars_id` | `Optional[str]` | Virus ID, usually begins 'AiV'  |
| `plasmid_tars_alias` | `Optional[List[str]]` | List of plasmid aliases (Alias used to reference the plasmid, usually begins 'AiP') |
| `prep_lot_number` | `str` | Preparation lot number  |
| `prep_date` | `Optional[datetime.date]` | Preparation lot date (Date this prep lot was titered) |
| `prep_type` | Optional[[VirusPrepType](#viruspreptype)] | Viral prep type  |
| `prep_protocol` | `Optional[str]` | Prep protocol  |


### ViralMaterial

Description of viral material for injections

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Full genome name (Full genome for virus construct) |
| `tars_identifiers` | Optional[[TarsVirusIdentifiers](#tarsvirusidentifiers)] | TARS IDs (TARS database identifiers) |
| `addgene_id` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Addgene id (Registry must be Addgene) |
| `titer` | `Optional[int]` | Effective titer (Final titer of viral material, accounting for mixture/diliution) |
| `titer_unit` | `Optional[str]` | Titer unit (For example, gc/mL) |


### VirusPrepType

Type of virus preparation

| Name | Value |
|------|-------|
| `CRUDE` | `Crude` |
| `PURIFIED` | `Purified` |


