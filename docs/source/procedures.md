# Procedures

The `procedures.json` file contains Procedures, anything done to the subject or specimen prior to data collection. This can include surgeries, injections, tissue processing, sectioning, immunolabeleing, etc.

**Subject** procedures are performed on a live subject (e.g. injections, surgeries, implants, perfusions, etc.) 
whereas **specimen** procedures are performed on tissue extracted after perfusion (e.g. tissue processing, 
immunolabeleing, sectioning, etc.). Sectioned specimens will have unique IDs (`subject_id-specimen_number`)

**Perfusions** are subject procedures that produce specimens and sectioning is a specimen procedure that produces new specimens.

**IACUC Protocol vs Protocol ID**

`iacuc_protocol` all experimental work with animals must follow an IACUC (Institute Animal Care Use Committee) protocol. The protocol ID refers to the DOI for a published protocol, for example those stored in the 
`AIND protocols.io workspace <https://www.protocols.io/workspaces/allen-institute-for-neural-dynamics>`_.


### Anaesthetic

Description of an anaesthetic

| Field | Type | Description |
|-------|------|-------------|
| `anaesthetic_type` | `str` |  |
| `duration` | `decimal.Decimal` |  |
| `duration_unit` | `TimeUnit` |  |
| `level` | `Optional[decimal.Decimal]` |  |


### BrainInjection

Description of an injection procedure into a brain

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system_name` | `str` |  |
| `coordinates` | List[List[[Translation](components/coordinates.md#translation) or [Rotation](components/coordinates.md#rotation) or [Scale](components/coordinates.md#scale) or [Affine](components/coordinates.md#affine)]] |  |
| `targeted_structure` | Optional[[BrainAtlas](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/brain_atlas.py)] |  |
| `injection_materials` | List[[ViralMaterial](#viralmaterial) or [NonViralMaterial](#nonviralmaterial)] |  |
| `relative_position` | `Optional[List[AnatomicalRelative]]` |  |
| `dynamics` | List[[InjectionDynamics](#injectiondynamics)] | List of injection events, one per location/depth |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |


### CatheterImplant

Description of a catheter implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `where_performed` | [Organization](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/organizations.py) |  |
| `catheter_material` | `CatheterMaterial` |  |
| `catheter_design` | `CatheterDesign` |  |
| `catheter_port` | `CatheterPort` |  |
| `targeted_structure` | `aind_data_schema_models.mouse_anatomy.MouseAnatomyModel` | Use options from MouseBloodVessels |


### Craniotomy

Description of craniotomy procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `craniotomy_type` | `CraniotomyType` |  |
| `coordinate_system_name` | `Optional[str]` |  |
| `position` | [Translation](components/coordinates.md#translation) or List[AnatomicalRelative] or NoneType |  |
| `size` | `Optional[float]` | Diameter or side length |
| `size_unit` | `Optional[SizeUnit]` |  |
| `protective_material` | `Optional[ProtectiveMaterial]` |  |
| `implant_part_number` | `Optional[str]` |  |
| `dura_removed` | `Optional[bool]` |  |


### GenericSubjectProcedure

Description of a non-surgical procedure performed on a subject

| Field | Type | Description |
|-------|------|-------------|
| `start_date` | `datetime.date` |  |
| `experimenters` | Optional[List[[Person](components/identifiers.md#person)]] |  |
| `ethics_review_id` | `str` |  |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `description` | `str` |  |
| `notes` | `Optional[str]` |  |


### GenericSurgeryProcedure

Description of a surgery procedure performed on a subject

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `description` | `str` |  |
| `notes` | `Optional[str]` |  |


### GroundWireImplant

Ground wire implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `ground_electrode_location` | `aind_data_schema_models.mouse_anatomy.MouseAnatomyModel` |  |
| `ground_wire_hole` | `Optional[int]` | For SHIELD implants, the hole number for the ground wire |
| `ground_wire_material` | `Optional[GroundWireMaterial]` |  |
| `ground_wire_diameter` | `Optional[decimal.Decimal]` |  |
| `ground_wire_diameter_unit` | `Optional[SizeUnit]` |  |


### HCRSeries

Description of series of HCR staining rounds for mFISH

| Field | Type | Description |
|-------|------|-------------|
| `codebook_name` | `str` |  |
| `number_of_rounds` | `int` |  |
| `hcr_rounds` | List[[HybridizationChainReaction](#hybridizationchainreaction)] |  |
| `strip_qc_compatible` | `bool` |  |
| `cell_id` | `Optional[str]` |  |


### Headframe

Description of headframe procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `headframe_type` | `str` |  |
| `headframe_part_number` | `str` |  |
| `headframe_material` | `Optional[HeadframeMaterial]` |  |
| `well_part_number` | `Optional[str]` |  |
| `well_type` | `Optional[str]` |  |


### HybridizationChainReaction

Description of an HCR staining round

| Field | Type | Description |
|-------|------|-------------|
| `round_index` | `int` |  |
| `start_time` | `datetime (timezone-aware)` |  |
| `end_time` | `datetime (timezone-aware)` |  |
| `genetic_stains` | List[[GeneticStain](components/reagent.md#geneticstain)] |  |
| `probe_concentration` | `decimal.Decimal` |  |
| `probe_concentration_unit` | `str` |  |
| `other_stains` | List[[Stain](components/reagent.md#stain)] |  |


### Injection

Description of an injection procedure

| Field | Type | Description |
|-------|------|-------------|
| `injection_materials` | List[[ViralMaterial](#viralmaterial) or [NonViralMaterial](#nonviralmaterial)] |  |
| `targeted_structure` | `Optional[aind_data_schema_models.mouse_anatomy.MouseAnatomyModel]` | Use InjectionTargets |
| `relative_position` | `Optional[List[AnatomicalRelative]]` |  |
| `dynamics` | List[[InjectionDynamics](#injectiondynamics)] | List of injection events, one per location/depth |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |


### InjectionDynamics

Description of the volume and rate of an injection

| Field | Type | Description |
|-------|------|-------------|
| `profile` | `InjectionProfile` |  |
| `volume` | `Optional[decimal.Decimal]` |  |
| `volume_unit` | `Optional[VolumeUnit]` |  |
| `rate` | `Optional[decimal.Decimal]` |  |
| `rate_unit` | `Optional[VolumeUnit]` |  |
| `duration` | `Optional[decimal.Decimal]` |  |
| `duration_unit` | `Optional[TimeUnit]` |  |
| `injection_current` | `Optional[decimal.Decimal]` |  |
| `injection_current_unit` | `Optional[CurrentUnit]` |  |
| `alternating_current` | `Optional[str]` |  |


### MyomatrixInsertion

Description of a Myomatrix array insertion for EMG

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `ground_electrode` | [GroundWireImplant](#groundwireimplant) |  |
| `implanted_device_name` | `str` | Must match a MyomatrixArray in Procedures.implanted_devices |


### NonViralMaterial

Description of a non-viral injection material

| Field | Type | Description |
|-------|------|-------------|
| `material_type` | `typing.Literal['Reagent']` |  |
| `concentration` | `Optional[float]` | Must provide concentration unit |
| `concentration_unit` | `Optional[str]` | For example, mg/mL |
| `name` | `str` |  |
| `source` | [Organization](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/organizations.py) |  |
| `rrid` | `Optional[aind_data_schema_models.pid_names.PIDName]` |  |
| `lot_number` | `str` |  |
| `expiration_date` | `Optional[datetime.date]` |  |


### Perfusion

Description of a perfusion procedure that creates a specimen

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `output_specimen_ids` | `List[str]` | IDs of specimens resulting from this procedure. |


### PlanarSectioning

Description of a sectioning procedure performed on the coronal, sagittal, or transverse/axial plane

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system` | Optional[[CoordinateSystem](components/coordinates.md#coordinatesystem)] | Only required if different from the Procedures.coordinate_system |
| `sections` | List[[Section](#section)] |  |
| `section_orientation` | `SectionOrientation` |  |


### ProbeImplant

Description of a probe (fiber, ephys) implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `implanted_device_names` | `List[str]` | Devices must exist in Procedures.implanted_devices |


### Procedures

Description of all procedures performed on a subject

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | `str` | Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes. |
| `subject_procedures` | List[[Surgery](#surgery) or [TrainingProtocol](#trainingprotocol) or [WaterRestriction](#waterrestriction) or [GenericSubjectProcedure](#genericsubjectprocedure)] |  |
| `specimen_procedures` | List[[SpecimenProcedure](#specimenprocedure)] |  |
| `implanted_devices` | List[[EphysProbe](components/devices.md#ephysprobe) or [FiberProbe](components/devices.md#fiberprobe) or [MyomatrixArray](components/devices.md#myomatrixarray)] |  |
| `configurations` | List[[ProbeConfig](components/configs.md#probeconfig) or [DeviceConfig](components/configs.md#deviceconfig)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](components/coordinates.md#coordinatesystem)] | Required when coordinates are provided in the procedures |
| `notes` | `Optional[str]` |  |


### SampleCollection

Description of a single sample collection

| Field | Type | Description |
|-------|------|-------------|
| `sample_type` | `SampleType` |  |
| `time` | `datetime (timezone-aware)` |  |
| `collection_volume` | `decimal.Decimal` |  |
| `collection_volume_unit` | `VolumeUnit` |  |
| `collection_method` | `Optional[str]` |  |


### Section

Description of a slice of brain tissue

| Field | Type | Description |
|-------|------|-------------|
| `output_specimen_id` | `str` |  |
| `targeted_structure` | Optional[[BrainAtlas](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/brain_atlas.py)] |  |
| `coordinate_system_name` | `str` |  |
| `start_coordinate` | [Translation](components/coordinates.md#translation) |  |
| `end_coordinate` | Optional[[Translation](components/coordinates.md#translation)] |  |
| `thickness` | `Optional[float]` |  |
| `thickness_unit` | `Optional[SizeUnit]` |  |
| `partial_slice` | `Optional[List[AnatomicalRelative]]` | If sectioning does not include the entire slice, indicate which part of the slice is retained. |


### SpecimenProcedure

Description of surgical or other procedure performed on a specimen

| Field | Type | Description |
|-------|------|-------------|
| `procedure_type` | `SpecimenProcedureType` |  |
| `procedure_name` | `Optional[str]` |  |
| `specimen_id` | `str` |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `datetime.date` |  |
| `experimenters` | List[[Person](components/identifiers.md#person)] |  |
| `protocol_id` | `Optional[List[str]]` | DOI for protocols.io |
| `procedure_details` | List[[HCRSeries](#hcrseries) or [Antibody](components/reagent.md#antibody) or [PlanarSectioning](#planarsectioning) or [Reagent](components/reagent.md#reagent) or [OligoProbeSet](components/reagent.md#oligoprobeset)] |  |
| `notes` | `Optional[str]` |  |


### Surgery

Description of subject procedures performed at one time

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `start_date` | `datetime.date` |  |
| `experimenters` | Optional[List[[Person](components/identifiers.md#person)]] |  |
| `ethics_review_id` | `Optional[str]` |  |
| `animal_weight_prior` | `Optional[decimal.Decimal]` | Animal weight before procedure |
| `animal_weight_post` | `Optional[decimal.Decimal]` | Animal weight after procedure |
| `weight_unit` | `MassUnit` |  |
| `anaesthesia` | Optional[[Anaesthetic](#anaesthetic)] |  |
| `workstation_id` | `Optional[str]` |  |
| `coordinate_system` | Optional[[CoordinateSystem](components/coordinates.md#coordinatesystem)] | Only required when the Surgery.coordinate_system is different from the Procedures.coordinate_system |
| `measured_coordinates` | Optional[Dict[Origin, [Translation](components/coordinates.md#translation)]] | Coordinates measured during the procedure, for example Bregma and Lambda |
| `procedures` | List[[CatheterImplant](#catheterimplant) or [Craniotomy](#craniotomy) or [ProbeImplant](#probeimplant) or [Headframe](#headframe) or [BrainInjection](#braininjection) or [Injection](#injection) or [MyomatrixInsertion](#myomatrixinsertion) or [GenericSurgeryProcedure](#genericsurgeryprocedure) or [Perfusion](#perfusion) or [SampleCollection](#samplecollection)] |  |
| `notes` | `Optional[str]` |  |


### TarsVirusIdentifiers

TARS data for a viral prep

| Field | Type | Description |
|-------|------|-------------|
| `virus_tars_id` | `Optional[str]` |  |
| `plasmid_tars_alias` | `Optional[List[str]]` | Alias used to reference the plasmid, usually begins 'AiP' |
| `prep_lot_number` | `str` |  |
| `prep_date` | `Optional[datetime.date]` | Date this prep lot was titered |
| `prep_type` | `Optional[VirusPrepType]` |  |
| `prep_protocol` | `Optional[str]` |  |


### TrainingProtocol

Description of an animal training protocol

| Field | Type | Description |
|-------|------|-------------|
| `training_name` | `str` |  |
| `protocol_id` | `Optional[str]` |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `Optional[datetime.date]` |  |
| `notes` | `Optional[str]` |  |


### ViralMaterial

Description of viral material for injections

| Field | Type | Description |
|-------|------|-------------|
| `material_type` | `typing.Literal['Virus']` |  |
| `name` | `str` | Full genome for virus construct |
| `tars_identifiers` | Optional[[TarsVirusIdentifiers](#tarsvirusidentifiers)] | TARS database identifiers |
| `addgene_id` | `Optional[aind_data_schema_models.pid_names.PIDName]` | Registry must be Addgene |
| `titer` | `Optional[int]` | Final titer of viral material, accounting for mixture/diliution |
| `titer_unit` | `Optional[str]` | For example, gc/mL |


### WaterRestriction

Description of a water restriction procedure

| Field | Type | Description |
|-------|------|-------------|
| `ethics_review_id` | `str` |  |
| `target_fraction_weight` | `int` |  |
| `target_fraction_weight_unit` | `UnitlessUnit` |  |
| `minimum_water_per_day` | `decimal.Decimal` |  |
| `minimum_water_per_day_unit` | `VolumeUnit` |  |
| `baseline_weight` | `decimal.Decimal` | Weight at start of water restriction |
| `weight_unit` | `MassUnit` |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `Optional[datetime.date]` |  |
