# Specimen_procedures

## Model definitions

### HCRSeries

Description of series of HCR staining rounds for mFISH

| Field | Type | Description |
|-------|------|-------------|
| `codebook_name` | `str` |  |
| `number_of_rounds` | `int` |  |
| `hcr_rounds` | List[[HybridizationChainReaction](#hybridizationchainreaction)] |  |
| `strip_qc_compatible` | `bool` |  |
| `cell_id` | `Optional[str]` |  |


### HybridizationChainReaction

Description of an HCR staining round

| Field | Type | Description |
|-------|------|-------------|
| `round_index` | `int` |  |
| `start_time` | `datetime (timezone-aware)` |  |
| `end_time` | `datetime (timezone-aware)` |  |
| `stains` | List[[FluorescentStain](reagent.md#fluorescentstain)] |  |
| `probe_concentration` | `float` |  |
| `probe_concentration_unit` | `str` |  |


### PlanarSectioning

Description of a sectioning procedure performed on the coronal, sagittal, or transverse/axial plane

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Only required if different from the Procedures.coordinate_system |
| `sections` | List[[Section](#section)] |  |
| `section_orientation` | [SectionOrientation](#sectionorientation) |  |


### Section

Description of a slice of brain tissue

| Field | Type | Description |
|-------|------|-------------|
| `output_specimen_id` | `str` |  |
| `targeted_structure` | Optional[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)] |  |
| `coordinate_system_name` | `str` |  |
| `start_coordinate` | [Translation](coordinates.md#translation) |  |
| `end_coordinate` | Optional[[Translation](coordinates.md#translation)] |  |
| `thickness` | `Optional[float]` |  |
| `thickness_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |
| `partial_slice` | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] | If sectioning does not include the entire slice, indicate which part of the slice is retained. |


### SectionOrientation

Orientation of sectioning

| Name | Value |
|------|-------|
| `CORONAL` | `Coronal` |
| `SAGITTAL` | `Sagittal` |
| `TRANSVERSE` | `Transverse` |


### SpecimenProcedure

Description of surgical or other procedure performed on a specimen

| Field | Type | Description |
|-------|------|-------------|
| `procedure_type` | [SpecimenProcedureType](../aind_data_schema_models/specimen_procedure_types.md#specimenproceduretype) |  |
| `procedure_name` | `Optional[str]` |  |
| `specimen_id` | `str` |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `datetime.date` |  |
| `experimenters` | `List[str]` |  |
| `protocol_id` | `Optional[List[str]]` | DOI for protocols.io |
| `protocol_parameters` | `Optional[Dict[str, str]]` | Parameters defined in the protocol and their value during this procedure |
| `procedure_details` | List[[HCRSeries](#hcrseries) or [FluorescentStain](reagent.md#fluorescentstain) or [PlanarSectioning](#planarsectioning) or [ProbeReagent](reagent.md#probereagent) or [Reagent](reagent.md#reagent) or [GeneProbeSet](reagent.md#geneprobeset)] | Details of the procedures, including reagents and sectioning information. |
| `notes` | `Optional[str]` |  |


