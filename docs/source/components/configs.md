# Configs

## Model definitions

### AirPuffConfig

Air puff device configuration

| Field | Type | Description |
|-------|------|-------------|
| `valence` | `Valence` |  |
| `relative_position` | `List[AnatomicalRelative]` |  |
| `coordinate_system` | Optional[{CoordinateSystem}] |  |
| `transform` | Optional[List[{Translation} or {Rotation} or {Scale} or {Affine}]] |  |
| `pressure` | `Optional[float]` |  |
| `pressure_unit` | `Optional[PressureUnit]` |  |
| `duration` | `Optional[float]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Channel

Configuration of a channel

| Field | Type | Description |
|-------|------|-------------|
| `channel_name` | `str` |  |
| `intended_measurement` | `Optional[str]` | What signal is this channel measuring |
| `detector` | {DetectorConfig} |  |
| `additional_device_names` | Optional[List[{DeviceConfig}]] | Mirrors, dichroics, etc |
| `light_sources` | List[{LaserConfig} or {LightEmittingDiodeConfig}] |  |
| `variable_power` | `Optional[bool]` | Set to true when the power varies across Planes -- put the power in the Plane.power field |
| `excitation_filters` | Optional[List[{DeviceConfig}]] |  |
| `emission_filters` | Optional[List[{DeviceConfig}]] |  |
| `emission_wavelength` | `Optional[int]` |  |
| `emission_wavelength_unit` | `Optional[SizeUnit]` |  |


### CoupledPlane

Configuration of a pair of coupled imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `plane_index` | `int` |  |
| `coupled_plane_index` | `int` | Plane index of the coupled plane |
| `power_ratio` | `float` |  |
| `depth` | `float` |  |
| `depth_unit` | `SizeUnit` |  |
| `power` | `float` |  |
| `power_unit` | `PowerUnit` |  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfstructure) |  |


### DetectorConfig

Configuration of detector settings

| Field | Type | Description |
|-------|------|-------------|
| `exposure_time` | `float` |  |
| `exposure_time_unit` | `TimeUnit` |  |
| `trigger_type` | `TriggerType` |  |
| `compression` | Optional[{Code}] | Compression algorithm used during acquisition |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### DeviceConfig

Parent class for all configurations

| Field | Type | Description |
|-------|------|-------------|
| `device_name` | `str` | Must match a device defined in the instrument.json |


### EphysAssemblyConfig

Group of configurations for an ephys assembly

| Field | Type | Description |
|-------|------|-------------|
| `manipulator` | {ManipulatorConfig} |  |
| `probes` | List[{ProbeConfig}] |  |
| `modules` | Optional[List[{MISModuleConfig}]] | Configurations for conveniently tracking manipulator modules, e.g. on the New Scale dome. |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### FiberAssemblyConfig

Inserted fiber photometry probe recorded in a stream

| Field | Type | Description |
|-------|------|-------------|
| `manipulator` | {ManipulatorConfig} |  |
| `probes` | List[{ProbeConfig}] |  |
| `patch_cords` | List[{PatchCordConfig}] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Image

Description of an N-D image

| Field | Type | Description |
|-------|------|-------------|
| `channel_name` | `str` |  |
| `dimensions_unit` | `SizeUnit` |  |
| `image_to_acquisition_transform` | List[{Translation} or {Rotation} or {Scale} or {Affine}] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[{Scale}] |  |


### ImageSPIM

Description of an N-D image acquired with SPIM

| Field | Type | Description |
|-------|------|-------------|
| `file_name` | `aind_data_schema.components.wrappers.AssetPath` |  |
| `imaging_angle` | `int` | Angle of the detector relative to the image plane relative to perpendicular |
| `imaging_angle_unit` | `AngleUnit` |  |
| `image_start_time` | `Optional[datetime (timezone-aware)]` |  |
| `image_end_time` | `Optional[datetime (timezone-aware)]` |  |
| `channel_name` | `str` |  |
| `dimensions_unit` | `SizeUnit` |  |
| `image_to_acquisition_transform` | List[{Translation} or {Rotation} or {Scale} or {Affine}] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[{Scale}] |  |


### ImagingConfig

Configuration of an imaging instrument

| Field | Type | Description |
|-------|------|-------------|
| `channels` | `List[typing.Annotated[typing.Union[aind_data_schema.components.configs.Channel, aind_data_schema.components.configs.SlapChannel], FieldInfo(annotation=NoneType, required=True, discriminator='object_type')]]` |  |
| `coordinate_system` | Optional[{CoordinateSystem}] | Required for ImageSPIM objects and when the imaging coordinate system differs from the Acquisition.coordinate_system |
| `images` | `List[typing.Annotated[typing.Union[aind_data_schema.components.configs.PlanarImage, aind_data_schema.components.configs.PlanarImageStack, aind_data_schema.components.configs.ImageSPIM], FieldInfo(annotation=NoneType, required=True, discriminator='object_type')]]` |  |
| `sampling_strategy` | Optional[{SamplingStrategy}] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Immersion

Configuration of immersion medium

| Field | Type | Description |
|-------|------|-------------|
| `medium` | `ImmersionMedium` |  |
| `refractive_index` | `float` |  |


### InterleavedStrategy

Description of an interleaved image sampling strategy

| Field | Type | Description |
|-------|------|-------------|
| `image_index_sequence` | `List[int]` |  |
| `frame_rate` | `float` |  |
| `frame_rate_unit` | `FrequencyUnit` |  |


### LaserConfig

Configuration of laser settings in an acquisition

| Field | Type | Description |
|-------|------|-------------|
| `wavelength` | `int` |  |
| `wavelength_unit` | `SizeUnit` |  |
| `power` | `Optional[float]` |  |
| `power_unit` | `Optional[PowerUnit]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LickSpoutConfig

Lick spout acquisition information

| Field | Type | Description |
|-------|------|-------------|
| `solution` | `Liquid` |  |
| `solution_valence` | `Valence` |  |
| `volume` | `float` |  |
| `volume_unit` | `VolumeUnit` |  |
| `relative_position` | `List[AnatomicalRelative]` |  |
| `coordinate_system` | Optional[{CoordinateSystem}] |  |
| `transform` | Optional[List[{Translation} or {Rotation} or {Scale} or {Affine}]] | Entry coordinate, depth, and rotation in the Acquisition.coordinate_system |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LightEmittingDiodeConfig

Configuration of LED settings

| Field | Type | Description |
|-------|------|-------------|
| `power` | `Optional[float]` |  |
| `power_unit` | `Optional[PowerUnit]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### MISModuleConfig

Modular insertion system module configuration

| Field | Type | Description |
|-------|------|-------------|
| `arc_angle` | `float` |  |
| `module_angle` | `float` |  |
| `rotation_angle` | `Optional[float]` |  |
| `angle_unit` | `AngleUnit` |  |
| `notes` | `Optional[str]` |  |


### MRIScan

Configuration of a 3D scan

| Field | Type | Description |
|-------|------|-------------|
| `scan_index` | `int` |  |
| `scan_type` | `ScanType` |  |
| `primary_scan` | `bool` | Indicates the primary scan used for downstream analysis |
| `scan_sequence_type` | `MriScanSequence` |  |
| `rare_factor` | `Optional[int]` |  |
| `echo_time` | `decimal.Decimal` |  |
| `echo_time_unit` | `TimeUnit` |  |
| `effective_echo_time` | `Optional[decimal.Decimal]` |  |
| `repetition_time` | `decimal.Decimal` |  |
| `repetition_time_unit` | `TimeUnit` |  |
| `scan_coordinate_system` | Optional[{CoordinateSystem}] |  |
| `scan_affine_transform` | Optional[List[{Translation} or {Rotation} or {Scale} or {Affine}]] | NIFTI sform/qform, Bruker vc_transform, etc |
| `subject_position` | `SubjectPosition` |  |
| `resolution` | Optional[{Scale}] |  |
| `resolution_unit` | `Optional[SizeUnit]` |  |
| `additional_scan_parameters` | `aind_data_schema.base.GenericModel` |  |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### ManipulatorConfig

Configuration of a manipulator

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system` | {CoordinateSystem} |  |
| `local_axis_positions` | {Translation} |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### MousePlatformConfig

Configuration for mouse platforms

| Field | Type | Description |
|-------|------|-------------|
| `objects_in_arena` | `Optional[List[str]]` |  |
| `active_control` | `bool` | True when movement of the mouse platform is dynamically controlled by the experimenter |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### PatchCordConfig

Configuration of a patch cord and its output power to another device

| Field | Type | Description |
|-------|------|-------------|
| `channels` | List[{Channel}] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### PlanarImage

Description of an N-D image acquired in a specific imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `planes` | `List[typing.Annotated[typing.Union[aind_data_schema.components.configs.Plane, aind_data_schema.components.configs.CoupledPlane, aind_data_schema.components.configs.SlapPlane], FieldInfo(annotation=NoneType, required=True, discriminator='object_type')]]` |  |
| `channel_name` | `str` |  |
| `dimensions_unit` | `SizeUnit` |  |
| `image_to_acquisition_transform` | List[{Translation} or {Rotation} or {Scale} or {Affine}] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[{Scale}] |  |


### PlanarImageStack

Description of a stack of images acquired in a specific imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `power_function` | `PowerFunction` |  |
| `depth_start` | `float` |  |
| `depth_end` | `float` |  |
| `depth_step` | `float` |  |
| `depth_unit` | `SizeUnit` |  |
| `planes` | `List[typing.Annotated[typing.Union[aind_data_schema.components.configs.Plane, aind_data_schema.components.configs.CoupledPlane, aind_data_schema.components.configs.SlapPlane], FieldInfo(annotation=NoneType, required=True, discriminator='object_type')]]` |  |
| `channel_name` | `str` |  |
| `dimensions_unit` | `SizeUnit` |  |
| `image_to_acquisition_transform` | List[{Translation} or {Rotation} or {Scale} or {Affine}] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[{Scale}] |  |


### Plane

Configuration of an imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `depth` | `float` |  |
| `depth_unit` | `SizeUnit` |  |
| `power` | `float` |  |
| `power_unit` | `PowerUnit` |  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfstructure) |  |


### ProbeConfig

Configuration for a device inserted into a brain

| Field | Type | Description |
|-------|------|-------------|
| `primary_targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfstructure) |  |
| `other_targeted_structure` | Optional[List[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfstructure)]] |  |
| `atlas_coordinate` | Optional[{AtlasCoordinate}] |  |
| `coordinate_system` | {CoordinateSystem} |  |
| `transform` | List[{Translation} or {Rotation} or {Scale} or {Affine}] | Entry coordinate, depth, and rotation in the Acquisition.coordinate_system |
| `dye` | `Optional[str]` |  |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### SampleChamberConfig

Configuration of a sample chamber

| Field | Type | Description |
|-------|------|-------------|
| `chamber_immersion` | {Immersion} |  |
| `sample_immersion` | Optional[{Immersion}] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### SamplingStrategy

Description of an image sampling strategy

| Field | Type | Description |
|-------|------|-------------|
| `frame_rate` | `float` |  |
| `frame_rate_unit` | `FrequencyUnit` |  |


### SlapChannel

Configuration of a channel for Slap

| Field | Type | Description |
|-------|------|-------------|
| `dilation` | `int` |  |
| `dilation_unit` | `SizeUnit` |  |
| `description` | `Optional[str]` |  |
| `channel_name` | `str` |  |
| `intended_measurement` | `Optional[str]` | What signal is this channel measuring |
| `detector` | {DetectorConfig} |  |
| `additional_device_names` | Optional[List[{DeviceConfig}]] | Mirrors, dichroics, etc |
| `light_sources` | List[{LaserConfig} or {LightEmittingDiodeConfig}] |  |
| `variable_power` | `Optional[bool]` | Set to true when the power varies across Planes -- put the power in the Plane.power field |
| `excitation_filters` | Optional[List[{DeviceConfig}]] |  |
| `emission_filters` | Optional[List[{DeviceConfig}]] |  |
| `emission_wavelength` | `Optional[int]` |  |
| `emission_wavelength_unit` | `Optional[SizeUnit]` |  |


### SlapPlane

Configuration of an imagine plane on a Slap microscope

| Field | Type | Description |
|-------|------|-------------|
| `dmd_dilation_x` | `int` |  |
| `dmd_dilation_y` | `int` |  |
| `dilation_unit` | `SizeUnit` |  |
| `slap_acquisition_type` | `SlapAcquisitionType` |  |
| `target_neuron` | `Optional[str]` |  |
| `target_branch` | `Optional[str]` |  |
| `path_to_array_of_frame_rates` | `aind_data_schema.components.wrappers.AssetPath` | Relative path from metadata json to file |
| `depth` | `float` |  |
| `depth_unit` | `SizeUnit` |  |
| `power` | `float` |  |
| `power_unit` | `PowerUnit` |  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfstructure) |  |


### SpeakerConfig

Configuration of auditory speaker configuration

| Field | Type | Description |
|-------|------|-------------|
| `volume` | `Optional[float]` |  |
| `volume_unit` | `Optional[SoundIntensityUnit]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### StackStrategy

Description of a stack image sampling strategy

| Field | Type | Description |
|-------|------|-------------|
| `image_repeats` | `int` |  |
| `stack_repeats` | `int` |  |
| `frame_rate` | `float` |  |
| `frame_rate_unit` | `FrequencyUnit` |  |


