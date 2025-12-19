# Surgery_procedures

## Model definitions

### Anaesthetic

Description of an anaesthetic

| Field | Type | Title (Description) |
|-------|------|-------------|
| `anaesthetic_type` | `str` | Type  |
| `duration` | `float` | Duration  |
| `duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Duration unit  |
| `level` | `Optional[float]` | Level (percent)  |


### BrainInjection

Description of an injection procedure into a brain

| Field | Type | Title (Description) |
|-------|------|-------------|
| `coordinate_system_name` | `str` | Coordinate system name  |
| `coordinates` | List[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Injection coordinate, depth, and rotation  |
| `targeted_structure` | Optional[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)] | Injection targeted brain structure  |
| `injection_materials` | List[[ViralMaterial](injection_procedures.md#viralmaterial) or [NonViralMaterial](injection_procedures.md#nonviralmaterial)] | Injection material  |
| `relative_position` | Optional[List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)]] | Relative position  |
| `dynamics` | List[[InjectionDynamics](injection_procedures.md#injectiondynamics)] | Injection dynamics (List of injection events, one per location/depth) |
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |


### CatheterImplant

Description of a catheter implant procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `where_performed` | [Organization](../aind_data_schema_models/organizations.md#organization) | Where performed  |
| `implanted_device` | [Catheter](devices.md#catheter) | Implanted device  |
| `device_config` | [CatheterConfig](configs.md#catheterconfig) | Device configuration  |


### Craniotomy

Description of craniotomy procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `craniotomy_type` | [CraniotomyType](#craniotomytype) | Craniotomy type  |
| `coordinate_system_name` | `Optional[str]` | Coordinate system name  |
| `position` | [Translation](coordinates.md#translation) or List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] or NoneType | Craniotomy position  |
| `size` | `Optional[float]` | Craniotomy size (Diameter or side length) |
| `size_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Craniotomy size unit  |
| `protective_material` | Optional[[ProtectiveMaterial](#protectivematerial)] | Protective material  |
| `implant_part_number` | `Optional[str]` | Implant part number  |
| `dura_removed` | `Optional[bool]` | Dura removed  |


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

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `description` | `str` | Description  |
| `notes` | `Optional[str]` | Notes  |


### GroundWireImplant

Ground wire implant procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `ground_electrode_location` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Location of ground electrode  |
| `ground_wire_hole` | `Optional[int]` | Ground wire hole (For SHIELD implants, the hole number for the ground wire) |
| `ground_wire_material` | Optional[[GroundWireMaterial](#groundwirematerial)] | Ground wire material  |
| `ground_wire_diameter` | `Optional[float]` | Ground wire diameter  |
| `ground_wire_diameter_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Ground wire diameter unit  |


### GroundWireMaterial

Ground wire material name

| Name | Value |
|------|-------|
| `SILVER` | `Silver` |
| `PLATINUM_IRIDIUM` | `Platinum iridium` |


### Headframe

Description of headframe procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `headframe_type` | `str` | Headframe type  |
| `headframe_part_number` | `Optional[str]` | Headframe part number  |
| `headframe_material` | Optional[[HeadframeMaterial](#headframematerial)] | Headframe material  |
| `well_part_number` | `Optional[str]` | Well part number  |
| `well_type` | `Optional[str]` | Well type  |


### HeadframeMaterial

Headframe material name

| Name | Value |
|------|-------|
| `STEEL` | `Steel` |
| `TITANIUM` | `Titanium` |
| `WHITE_ZIRCONIA` | `White Zirconia` |


### MyomatrixInsertion

Description of a Myomatrix array insertion for EMG

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `ground_electrode` | [GroundWireImplant](#groundwireimplant) | Ground electrode  |
| `implanted_device` | [MyomatrixArray](devices.md#myomatrixarray) | Implanted device  |


### Perfusion

Description of a perfusion procedure that creates a specimen

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `output_specimen_ids` | `List[str]` | Specimen ID (IDs of specimens resulting from this procedure.) |


### ProbeImplant

Description of a probe (fiber, ephys) implant procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `implanted_device` | [EphysProbe](devices.md#ephysprobe) or [FiberProbe](devices.md#fiberprobe) | Implanted device  |
| `device_config` | [ProbeConfig](configs.md#probeconfig) | Device configuration  |


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

| Field | Type | Title (Description) |
|-------|------|-------------|
| `sample_type` | [SampleType](#sampletype) | Sample type  |
| `time` | `datetime (timezone-aware)` | Collection time  |
| `collection_volume` | `float` | Collection volume  |
| `collection_volume_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) | Collection volume unit  |
| `collection_method` | `Optional[str]` | Collection method for terminal collection  |


### SampleType

Sample type

| Name | Value |
|------|-------|
| `BLOOD` | `Blood` |
| `OTHER` | `Other` |


