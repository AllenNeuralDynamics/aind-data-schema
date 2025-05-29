# Procedures

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/procedures.py)

The `procedures.json` file contains anything done to the subject or specimen prior to data collection. This can include surgeries, injections, tissue processing, sectioning, immunolabeling, etc. The procedures metadata also contains implanted devices and their configurations, for example for chronic insertions.

## Subject vs. specimen

**Subject** procedures are performed on a live subject (e.g. injections, surgeries, implants, perfusions, etc.) whereas **specimen** procedures are performed on tissue extracted after perfusion (e.g. tissue processing, immunolabeling, sectioning, etc.).

Sectioned specimens must have unique IDs appended as a suffix to the subject ID: `subject_id-specimen_number`.

## Perfusions

**Perfusions** are subject procedures that produce specimens and sectioning is a specimen procedure that produces new specimens.

## Ethics review ID vs. protocol ID

All experimental work with animals and humans must be approved by an IACUC (Institute Animal Care Use Committee) or IRB (Institutional Review Board), the corresponding ID number should be stored in the `ethics_review_id` fields.

Protocol ID refers to the DOI for a published protocol describing a procedure, for example those stored in the [AIND protocols.io workspace](https://www.protocols.io/workspaces/allen-institute-for-neural-dynamics).

## Examples

- [Generic procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/procedures.py)
- [SmartSPIM procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aibs_smartspim_procedures.py)
- [Ophys procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ophys_procedures.py)

## Core file

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


## Model definitions

### Anaesthetic

Description of an anaesthetic

| Field | Type | Description |
|-------|------|-------------|
| `anaesthetic_type` | `str` |  |
| `duration` | `decimal.Decimal` |  |
| `duration_unit` | [TimeUnit](aind_data_schema_models/units.md#timeunit) |  |
| `level` | `Optional[decimal.Decimal]` |  |


### BrainInjection

Description of an injection procedure into a brain

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system_name` | `str` |  |
| `coordinates` | List[List[[Translation](components/coordinates.md#translation) or [Rotation](components/coordinates.md#rotation) or [Scale](components/coordinates.md#scale) or [Affine](components/coordinates.md#affine)]] |  |
| `targeted_structure` | Optional[[BrainAtlas](aind_data_schema_models/brain_atlas.md#ccfstructure)] |  |
| `injection_materials` | List[[ViralMaterial](#viralmaterial) or [NonViralMaterial](#nonviralmaterial)] |  |
| `relative_position` | Optional[List[[AnatomicalRelative](aind_data_schema_models/coordinates.md#anatomicalrelative)]] |  |
| `dynamics` | List[[InjectionDynamics](#injectiondynamics)] | List of injection events, one per location/depth |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |


### CatheterDesign

Type of catheter design

| Name | Value |
|------|-------|
| `MAGNETIC` | `Magnetic` |
| `NONMAGNETIC` | `Non-magnetic` |
| `NA` | `N/A` |


### CatheterImplant

Description of a catheter implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `where_performed` | [Organization](aind_data_schema_models/organizations.md#organization) |  |
| `catheter_material` | [CatheterMaterial](#cathetermaterial) |  |
| `catheter_design` | [CatheterDesign](#catheterdesign) |  |
| `catheter_port` | [CatheterPort](#catheterport) |  |
| `targeted_structure` | [MouseAnatomyModel](aind_data_schema_models/external.md#mouseanatomymodel) | Use options from MouseBloodVessels |


### CatheterMaterial

Type of catheter material

| Name | Value |
|------|-------|
| `NAKED` | `Naked` |
| `SILICONE` | `VAB silicone` |
| `MESH` | `VAB mesh` |


### CatheterPort

Type of catheter port

| Name | Value |
|------|-------|
| `SINGLE` | `Single` |
| `DOUBLE` | `Double` |


### Craniotomy

Description of craniotomy procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `craniotomy_type` | [CraniotomyType](#craniotomytype) |  |
| `coordinate_system_name` | `Optional[str]` |  |
| `position` | [Translation](components/coordinates.md#translation) or List[[AnatomicalRelative](aind_data_schema_models/coordinates.md#anatomicalrelative)] or NoneType |  |
| `size` | `Optional[float]` | Diameter or side length |
| `size_unit` | Optional[[SizeUnit](aind_data_schema_models/units.md#sizeunit)] |  |
| `protective_material` | Optional[[ProtectiveMaterial](#protectivematerial)] |  |
| `implant_part_number` | `Optional[str]` |  |
| `dura_removed` | `Optional[bool]` |  |


### CraniotomyType

Name of craniotomy Type

| Name | Value |
|------|-------|
| `DHC` | `Dual hemisphere craniotomy` |
| `WHC` | `Whole hemisphere craniotomy` |
| `CIRCLE` | `Circle` |
| `SQUARE` | `Square` |
| `OTHER` | `Other` |


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
| `ground_electrode_location` | [MouseAnatomyModel](aind_data_schema_models/external.md#mouseanatomymodel) |  |
| `ground_wire_hole` | `Optional[int]` | For SHIELD implants, the hole number for the ground wire |
| `ground_wire_material` | Optional[[GroundWireMaterial](#groundwirematerial)] |  |
| `ground_wire_diameter` | `Optional[decimal.Decimal]` |  |
| `ground_wire_diameter_unit` | Optional[[SizeUnit](aind_data_schema_models/units.md#sizeunit)] |  |


### GroundWireMaterial

Ground wire material name

| Name | Value |
|------|-------|
| `SILVER` | `Silver` |
| `PLATINUM_IRIDIUM` | `Platinum iridium` |


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
| `headframe_material` | Optional[[HeadframeMaterial](#headframematerial)] |  |
| `well_part_number` | `Optional[str]` |  |
| `well_type` | `Optional[str]` |  |


### HeadframeMaterial

Headframe material name

| Name | Value |
|------|-------|
| `STEEL` | `Steel` |
| `TITANIUM` | `Titanium` |
| `WHITE_ZIRCONIA` | `White Zirconia` |


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
| `targeted_structure` | Optional[[MouseAnatomyModel](aind_data_schema_models/external.md#mouseanatomymodel)] | Use InjectionTargets |
| `relative_position` | Optional[List[[AnatomicalRelative](aind_data_schema_models/coordinates.md#anatomicalrelative)]] |  |
| `dynamics` | List[[InjectionDynamics](#injectiondynamics)] | List of injection events, one per location/depth |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |


### InjectionDynamics

Description of the volume and rate of an injection

| Field | Type | Description |
|-------|------|-------------|
| `profile` | [InjectionProfile](#injectionprofile) |  |
| `volume` | `Optional[decimal.Decimal]` |  |
| `volume_unit` | Optional[[VolumeUnit](aind_data_schema_models/units.md#volumeunit)] |  |
| `rate` | `Optional[decimal.Decimal]` |  |
| `rate_unit` | Optional[[VolumeUnit](aind_data_schema_models/units.md#volumeunit)] |  |
| `duration` | `Optional[decimal.Decimal]` |  |
| `duration_unit` | Optional[[TimeUnit](aind_data_schema_models/units.md#timeunit)] |  |
| `injection_current` | `Optional[decimal.Decimal]` |  |
| `injection_current_unit` | Optional[[CurrentUnit](aind_data_schema_models/units.md#currentunit)] |  |
| `alternating_current` | `Optional[str]` |  |


### InjectionProfile

Injection profile

| Name | Value |
|------|-------|
| `BOLUS` | `Bolus` |
| `CONTINUOUS` | `Continuous` |
| `PULSED` | `Pulsed` |


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
| `material_type` | `"Reagent"` |  |
| `concentration` | `Optional[float]` | Must provide concentration unit |
| `concentration_unit` | `Optional[str]` | For example, mg/mL |
| `name` | `str` |  |
| `source` | [Organization](aind_data_schema_models/organizations.md#organization) |  |
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
| `section_orientation` | [SectionOrientation](#sectionorientation) |  |


### ProbeImplant

Description of a probe (fiber, ephys) implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `implanted_device_names` | `List[str]` | Devices must exist in Procedures.implanted_devices |


### ProtectiveMaterial

Name of material applied to craniotomy

| Name | Value |
|------|-------|
| `AGAROSE` | `Agarose` |
| `DURAGEL` | `Duragel` |
| `KWIK_CAST` | `Kwik-Cast` |
| `SORTA_CLEAR` | `SORTA-clear` |
| `OTHER` | `Other - see notes` |


### SampleCollection

Description of a single sample collection

| Field | Type | Description |
|-------|------|-------------|
| `sample_type` | [SampleType](#sampletype) |  |
| `time` | `datetime (timezone-aware)` |  |
| `collection_volume` | `decimal.Decimal` |  |
| `collection_volume_unit` | [VolumeUnit](aind_data_schema_models/units.md#volumeunit) |  |
| `collection_method` | `Optional[str]` |  |


### SampleType

Sample type

| Name | Value |
|------|-------|
| `BLOOD` | `Blood` |
| `OTHER` | `Other` |


### Section

Description of a slice of brain tissue

| Field | Type | Description |
|-------|------|-------------|
| `output_specimen_id` | `str` |  |
| `targeted_structure` | Optional[[BrainAtlas](aind_data_schema_models/brain_atlas.md#ccfstructure)] |  |
| `coordinate_system_name` | `str` |  |
| `start_coordinate` | [Translation](components/coordinates.md#translation) |  |
| `end_coordinate` | Optional[[Translation](components/coordinates.md#translation)] |  |
| `thickness` | `Optional[float]` |  |
| `thickness_unit` | Optional[[SizeUnit](aind_data_schema_models/units.md#sizeunit)] |  |
| `partial_slice` | Optional[List[[AnatomicalRelative](aind_data_schema_models/coordinates.md#anatomicalrelative)]] | If sectioning does not include the entire slice, indicate which part of the slice is retained. |


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
| `procedure_type` | [SpecimenProcedureType](aind_data_schema_models/specimen_procedure_types.md#specimenproceduretype) |  |
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
| `weight_unit` | [MassUnit](aind_data_schema_models/units.md#massunit) |  |
| `anaesthesia` | Optional[[Anaesthetic](#anaesthetic)] |  |
| `workstation_id` | `Optional[str]` |  |
| `coordinate_system` | Optional[[CoordinateSystem](components/coordinates.md#coordinatesystem)] | Only required when the Surgery.coordinate_system is different from the Procedures.coordinate_system |
| `measured_coordinates` | Optional[Dict[[Origin](aind_data_schema_models/coordinates.md#origin), [Translation](components/coordinates.md#translation)]] | Coordinates measured during the procedure, for example Bregma and Lambda |
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
| `prep_type` | Optional[[VirusPrepType](#viruspreptype)] |  |
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
| `material_type` | `"Virus"` |  |
| `name` | `str` | Full genome for virus construct |
| `tars_identifiers` | Optional[[TarsVirusIdentifiers](#tarsvirusidentifiers)] | TARS database identifiers |
| `addgene_id` | `Optional[aind_data_schema_models.pid_names.PIDName]` | Registry must be Addgene |
| `titer` | `Optional[int]` | Final titer of viral material, accounting for mixture/diliution |
| `titer_unit` | `Optional[str]` | For example, gc/mL |


### VirusPrepType

Type of virus preparation

| Name | Value |
|------|-------|
| `CRUDE` | `Crude` |
| `PURIFIED` | `Purified` |


### WaterRestriction

Description of a water restriction procedure

| Field | Type | Description |
|-------|------|-------------|
| `ethics_review_id` | `str` |  |
| `target_fraction_weight` | `int` |  |
| `target_fraction_weight_unit` | [UnitlessUnit](aind_data_schema_models/units.md#unitlessunit) |  |
| `minimum_water_per_day` | `decimal.Decimal` |  |
| `minimum_water_per_day_unit` | [VolumeUnit](aind_data_schema_models/units.md#volumeunit) |  |
| `baseline_weight` | `decimal.Decimal` | Weight at start of water restriction |
| `weight_unit` | [MassUnit](aind_data_schema_models/units.md#massunit) |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `Optional[datetime.date]` |  |
