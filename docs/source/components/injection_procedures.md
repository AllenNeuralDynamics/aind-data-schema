# Injection_procedures

## Model definitions

### Injection

Description of an injection procedure

| Field | Type | Description |
|-------|------|-------------|
| `injection_materials` | List[[ViralMaterial](#viralmaterial) or [NonViralMaterial](#nonviralmaterial)] |  |
| `targeted_structure` | Optional[[MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel)] | Use InjectionTargets |
| `relative_position` | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] |  |
| `dynamics` | List[[InjectionDynamics](#injectiondynamics)] | List of injection events, one per location/depth |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |


### InjectionDynamics

Description of the volume and rate of an injection

| Field | Type | Description |
|-------|------|-------------|
| `profile` | [InjectionProfile](#injectionprofile) |  |
| `volume` | `Optional[float]` |  |
| `volume_unit` | Optional[[VolumeUnit](../aind_data_schema_models/units.md#volumeunit)] |  |
| `duration` | `Optional[float]` |  |
| `duration_unit` | Optional[[TimeUnit](../aind_data_schema_models/units.md#timeunit)] |  |
| `injection_current` | `Optional[float]` |  |
| `injection_current_unit` | Optional[[CurrentUnit](../aind_data_schema_models/units.md#currentunit)] |  |
| `alternating_current` | `Optional[str]` |  |


### InjectionProfile

Injection profile

| Name | Value |
|------|-------|
| `BOLUS` | `Bolus` |
| `CONTINUOUS` | `Continuous` |
| `PULSED` | `Pulsed` |


### NonViralMaterial

Description of a non-viral injection material

| Field | Type | Description |
|-------|------|-------------|
| `concentration` | `Optional[float]` | Must provide concentration unit |
| `concentration_unit` | `Optional[str]` | For example, mg/mL |
| `name` | `str` |  |
| `source` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `rrid` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] |  |
| `lot_number` | `Optional[str]` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### TarsVirusIdentifiers

TARS data for a viral prep

| Field | Type | Description |
|-------|------|-------------|
| `virus_tars_id` | `Optional[str]` |  |
| `plasmid_tars_alias` | `Optional[List[str]]` | Alias used to reference the plasmid, usually begins 'AiP' |
| `prep_lot_number` | `str` |  |
| `prep_date` | `Optional[datetime.date]` | Date this prep lot was titered |
| `prep_type` | Optional[[VirusPrepType](#viruspreptype)] |  |
| `prep_protocol` | `Optional[str]` |  |


### ViralMaterial

Description of viral material for injections

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Full genome for virus construct |
| `tars_identifiers` | Optional[[TarsVirusIdentifiers](#tarsvirusidentifiers)] | TARS database identifiers |
| `addgene_id` | Optional[[PIDName](../aind_data_schema_models/pid_names.md#pidname)] | Registry must be Addgene |
| `titer` | `Optional[int]` | Final titer of viral material, accounting for mixture/diliution |
| `titer_unit` | `Optional[str]` | For example, gc/mL |


### VirusPrepType

Type of virus preparation

| Name | Value |
|------|-------|
| `CRUDE` | `Crude` |
| `PURIFIED` | `Purified` |


