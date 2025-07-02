# Surgery_procedures

## Model definitions

### Anaesthetic

Description of an anaesthetic

| Field | Type | Description |
|-------|------|-------------|
| `anaesthetic_type` | `str` |  |
| `duration` | `float` |  |
| `duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `level` | `Optional[float]` |  |


### BrainInjection

Description of an injection procedure into a brain

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system_name` | `str` |  |
| `coordinates` | List[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] |  |
| `targeted_structure` | Optional[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)] |  |
| `injection_materials` | List[[ViralMaterial](injection_procedures.md#viralmaterial) or [NonViralMaterial](injection_procedures.md#nonviralmaterial)] |  |
| `relative_position` | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] |  |
| `dynamics` | List[[InjectionDynamics](injection_procedures.md#injectiondynamics)] | List of injection events, one per location/depth |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |


### CatheterImplant

Description of a catheter implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `where_performed` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `implanted_device` | [Catheter](devices.md#catheter) |  |
| `device_config` | [CatheterConfig](configs.md#catheterconfig) |  |


### Craniotomy

Description of craniotomy procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `craniotomy_type` | [CraniotomyType](#craniotomytype) |  |
| `coordinate_system_name` | `Optional[str]` |  |
| `position` | [Translation](coordinates.md#translation) or List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] or NoneType |  |
| `size` | `Optional[float]` | Diameter or side length |
| `size_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |
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
| `ground_electrode_location` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) |  |
| `ground_wire_hole` | `Optional[int]` | For SHIELD implants, the hole number for the ground wire |
| `ground_wire_material` | Optional[[GroundWireMaterial](#groundwirematerial)] |  |
| `ground_wire_diameter` | `Optional[float]` |  |
| `ground_wire_diameter_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |


### GroundWireMaterial

Ground wire material name

| Name | Value |
|------|-------|
| `SILVER` | `Silver` |
| `PLATINUM_IRIDIUM` | `Platinum iridium` |


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


### MyomatrixInsertion

Description of a Myomatrix array insertion for EMG

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `ground_electrode` | [GroundWireImplant](#groundwireimplant) |  |
| `implanted_device` | [MyomatrixArray](devices.md#myomatrixarray) |  |


### Perfusion

Description of a perfusion procedure that creates a specimen

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `output_specimen_ids` | `List[str]` | IDs of specimens resulting from this procedure. |


### ProbeImplant

Description of a probe (fiber, ephys) implant procedure

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `implanted_device` | [EphysProbe](devices.md#ephysprobe) or [FiberProbe](devices.md#fiberprobe) |  |
| `device_config` | [ProbeConfig](configs.md#probeconfig) |  |


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
| `collection_volume` | `float` |  |
| `collection_volume_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) |  |
| `collection_method` | `Optional[str]` |  |


### SampleType

Sample type

| Name | Value |
|------|-------|
| `BLOOD` | `Blood` |
| `OTHER` | `Other` |


