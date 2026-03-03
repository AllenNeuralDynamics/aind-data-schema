# Specimen_procedures

## Model definitions

### HCRSeries

Description of series of HCR staining rounds for mFISH

| Field | Type | Title (Description) |
|-------|------|-------------|
| `codebook_name` | `str` | Codebook name  |
| `number_of_rounds` | `int` | Number of round  |
| `hcr_rounds` | List[[HybridizationChainReaction](#hybridizationchainreaction)] | Hybridization Chain Reaction rounds  |
| `strip_qc_compatible` | `bool` | Strip QC compatible  |
| `cell_id` | `Optional[str]` | Cell ID  |


### HybridizationChainReaction

Description of an HCR staining round

| Field | Type | Title (Description) |
|-------|------|-------------|
| `round_index` | `int` | Round index  |
| `start_time` | `datetime (timezone-aware)` | Round start time  |
| `end_time` | `datetime (timezone-aware)` | Round end time  |
| `stains` | List[[FluorescentStain](reagent.md#fluorescentstain)] | Stains  |
| `probe_concentration` | `float` | Probe concentration (M)  |
| `probe_concentration_unit` | `str` | Probe concentration unit  |


### PlanarSection

Description of a single planar section of brain tissue

| Field | Type | Title (Description) |
|-------|------|-------------|
| `coordinate_system_name` | `str` | Coordinate system name  |
| `start_coordinate` | [Translation](coordinates.md#translation) | Start coordinate  |
| `end_coordinate` | Optional[[Translation](coordinates.md#translation)] | End coordinate  |
| `thickness` | `Optional[float]` | Slice thickness  |
| `thickness_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Slice thickness unit  |
| `partial_slice` | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] | Partial slice (If sectioning does not include the entire slice, indicate which part of the slice is retained.) |
| `output_specimen_id` | `str` | Specimen ID  |
| `targeted_structure` | Optional[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)] | Targeted structure  |
| `includes_surrounding_tissue` | `Optional[bool]` | Includes surrounding tissue (Whether the section includes additional tissue surrounding the targeted structure.) |


### PlanarSectioning

Description of a sectioning procedure performed on the coronal, sagittal, or transverse/axial plane

| Field | Type | Title (Description) |
|-------|------|-------------|
| `coordinate_system` | [CoordinateSystem](coordinates.md#coordinatesystem) or [Atlas](coordinates.md#atlas) or NoneType | Sectioning coordinate system (Only required if different from the Procedures.coordinate_system) |
| `sections` | List[[Section](#section) or [PlanarSection](#planarsection)] | Planar sections (Use PlanarSection for new implementations) |
| `section_orientation` | [SectionOrientation](#sectionorientation) | Sectioning orientation  |


### Section

Description of a single section of brain tissue. Slices should use PlanarSection.

| Field | Type | Title (Description) |
|-------|------|-------------|
| `output_specimen_id` | `str` | Specimen ID  |
| `targeted_structure` | Optional[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)] | Targeted structure  |
| `includes_surrounding_tissue` | `Optional[bool]` | Includes surrounding tissue (Whether the section includes additional tissue surrounding the targeted structure.) |
| <del>`coordinate_system_name`</del> | `Optional[str]` | **[DEPRECATED]** Use PlanarSection instead. Coordinate system name  |
| <del>`start_coordinate`</del> | Optional[[Translation](coordinates.md#translation)] | **[DEPRECATED]** Use PlanarSection instead. Start coordinate  |
| <del>`end_coordinate`</del> | Optional[[Translation](coordinates.md#translation)] | **[DEPRECATED]** Use PlanarSection instead. End coordinate  |
| <del>`thickness`</del> | `Optional[float]` | **[DEPRECATED]** Use PlanarSection instead. Slice thickness  |
| <del>`thickness_unit`</del> | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | **[DEPRECATED]** Use PlanarSection instead. Slice thickness unit  |
| <del>`partial_slice`</del> | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] | **[DEPRECATED]** Use PlanarSection instead. Partial slice (If sectioning does not include the entire slice, indicate which part of the slice is retained.) |


### SectionOrientation

Orientation of sectioning

| Name | Value |
|------|-------|
| `CORONAL` | `Coronal` |
| `SAGITTAL` | `Sagittal` |
| `TRANSVERSE` | `Transverse` |


### Sectioning

Description of a sectioning procedure targeting a specific structure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `sections` | List[[Section](#section)] | Sections  |


### SpecimenProcedure

Description of surgical or other procedure performed on a specimen

| Field | Type | Title (Description) |
|-------|------|-------------|
| `procedure_type` | [SpecimenProcedureType](../aind_data_schema_models/specimen_procedure_types.md#specimenproceduretype) | Procedure type  |
| `procedure_name` | `Optional[str]` | Procedure name  |
| `specimen_id` | `str or List[str]` | Specimen ID(s)  |
| `start_date` | `datetime.date` | Start date  |
| `end_date` | `datetime.date` | End date  |
| `experimenters` | `List[str]` | experimenter(s)  |
| `protocol_id` | `Optional[List[str]]` | Protocol ID (DOI for protocols.io) |
| `protocol_parameters` | `Optional[Dict[str, str]]` | Protocol parameters (Parameters defined in the protocol and their value during this procedure) |
| `procedure_details` | List[[HCRSeries](#hcrseries) or [FluorescentStain](reagent.md#fluorescentstain) or [Sectioning](#sectioning) or [PlanarSectioning](#planarsectioning) or [ProbeReagent](reagent.md#probereagent) or [Reagent](reagent.md#reagent) or [GeneProbeSet](reagent.md#geneprobeset)] | Procedure details (Details of the procedures, including reagents and sectioning information.) |
| `notes` | `Optional[str]` | Notes  |


