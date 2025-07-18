# Configs

## Model definitions

### AirPuffConfig

Air puff device configuration

| Field | Type | Description |
|-------|------|-------------|
| `valence` | [Valence](#valence) |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] |  |
| `pressure` | `Optional[float]` |  |
| `pressure_unit` | Optional[[PressureUnit](../aind_data_schema_models/units.md#pressureunit)] |  |
| `duration` | `Optional[float]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### CatheterConfig

Configuration of a catheter

| Field | Type | Description |
|-------|------|-------------|
| `targeted_structure` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Use options from MouseBloodVessels |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Channel

Configuration of a channel

| Field | Type | Description |
|-------|------|-------------|
| `channel_name` | `str` |  |
| `intended_measurement` | `Optional[str]` | What signal is this channel measuring |
| `detector` | [DetectorConfig](#detectorconfig) |  |
| `additional_device_names` | Optional[List[[DeviceConfig](#deviceconfig)]] | Mirrors, dichroics, etc |
| `light_sources` | List[[LaserConfig](#laserconfig) or [LightEmittingDiodeConfig](#lightemittingdiodeconfig)] |  |
| `variable_power` | `Optional[bool]` | Set to true when the power varies across Planes -- put the power in the Plane.power field |
| `excitation_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] |  |
| `emission_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] |  |
| `emission_wavelength` | `Optional[int]` |  |
| `emission_wavelength_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |


### CoupledPlane

Configuration of a pair of coupled imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `plane_index` | `int` |  |
| `coupled_plane_index` | `int` | Plane index of the coupled plane |
| `power_ratio` | `float` |  |
| `depth` | `float` |  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `power` | `float` |  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) |  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) |  |


### DetectorConfig

Configuration of detector settings

| Field | Type | Description |
|-------|------|-------------|
| `exposure_time` | `float` |  |
| `exposure_time_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `trigger_type` | [TriggerType](#triggertype) |  |
| `compression` | Optional[[Code](identifiers.md#code)] | Compression algorithm used during acquisition |
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
| `manipulator` | [ManipulatorConfig](#manipulatorconfig) |  |
| `probes` | List[[ProbeConfig](#probeconfig)] |  |
| `modules` | Optional[List[[MISModuleConfig](#mismoduleconfig)]] | Configurations for conveniently tracking manipulator modules, e.g. on the New Scale dome. |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### FiberAssemblyConfig

Inserted fiber photometry probe recorded in a stream

| Field | Type | Description |
|-------|------|-------------|
| `manipulator` | [ManipulatorConfig](#manipulatorconfig) |  |
| `probes` | List[[ProbeConfig](#probeconfig)] |  |
| `patch_cords` | List[[PatchCordConfig](#patchcordconfig)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Image

Description of an N-D image

| Field | Type | Description |
|-------|------|-------------|
| `channel_name` | `str` |  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] |  |


### ImageSPIM

Description of an N-D image acquired with SPIM

| Field | Type | Description |
|-------|------|-------------|
| `file_name` | `AssetPath` |  |
| `imaging_angle` | `int` | Angle of the detector relative to the image plane relative to perpendicular |
| `imaging_angle_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) |  |
| `image_start_time` | `Optional[datetime (timezone-aware)]` |  |
| `image_end_time` | `Optional[datetime (timezone-aware)]` |  |
| `channel_name` | `str` |  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] |  |


### ImagingConfig

Configuration of an imaging instrument

| Field | Type | Description |
|-------|------|-------------|
| `channels` | List[[Channel](#channel) or [SlapChannel](#slapchannel)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Required for ImageSPIM objects and when the imaging coordinate system differs from the Acquisition.coordinate_system |
| `images` | List[[PlanarImage](#planarimage) or [PlanarImageStack](#planarimagestack) or [ImageSPIM](#imagespim)] |  |
| `sampling_strategy` | Optional[[SamplingStrategy](#samplingstrategy)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Immersion

Configuration of immersion medium

| Field | Type | Description |
|-------|------|-------------|
| `medium` | [ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium) |  |
| `refractive_index` | `float` |  |


### InterleavedStrategy

Description of an interleaved image sampling strategy

| Field | Type | Description |
|-------|------|-------------|
| `image_index_sequence` | `List[int]` |  |
| `frame_rate` | `float` |  |
| `frame_rate_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) |  |


### LaserConfig

Configuration of laser settings in an acquisition

| Field | Type | Description |
|-------|------|-------------|
| `wavelength` | `int` |  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `power` | `Optional[float]` |  |
| `power_unit` | Optional[[PowerUnit](../aind_data_schema_models/units.md#powerunit)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LickSpoutConfig

Lick spout acquisition information

| Field | Type | Description |
|-------|------|-------------|
| `solution` | [Liquid](#liquid) |  |
| `solution_valence` | [Valence](#valence) |  |
| `volume` | `float` |  |
| `volume_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Entry coordinate, depth, and rotation in the Acquisition.coordinate_system |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LightEmittingDiodeConfig

Configuration of LED settings

| Field | Type | Description |
|-------|------|-------------|
| `power` | `Optional[float]` |  |
| `power_unit` | Optional[[PowerUnit](../aind_data_schema_models/units.md#powerunit)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Liquid

Solution names

| Name | Value |
|------|-------|
| `WATER` | `Water` |
| `SUCROSE` | `Sucrose` |
| `QUININE` | `Quinine` |
| `CITRIC_ACID` | `Citric acid` |
| `OTHER` | `Other` |


### MISModuleConfig

Modular insertion system module configuration

| Field | Type | Description |
|-------|------|-------------|
| `arc_angle` | `float` |  |
| `module_angle` | `float` |  |
| `rotation_angle` | `Optional[float]` |  |
| `angle_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) |  |
| `notes` | `Optional[str]` |  |


### MRIScan

Configuration of a 3D scan

| Field | Type | Description |
|-------|------|-------------|
| `scan_index` | `int` |  |
| `scan_type` | [ScanType](#scantype) |  |
| `primary_scan` | `bool` | Indicates the primary scan used for downstream analysis |
| `scan_sequence_type` | [MriScanSequence](#mriscansequence) |  |
| `rare_factor` | `Optional[int]` |  |
| `echo_time` | `decimal.Decimal` |  |
| `echo_time_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `effective_echo_time` | `Optional[decimal.Decimal]` |  |
| `repetition_time` | `decimal.Decimal` |  |
| `repetition_time_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `scan_coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `scan_affine_transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | NIFTI sform/qform, Bruker vc_transform, etc |
| `subject_position` | [SubjectPosition](#subjectposition) |  |
| `resolution` | Optional[[Scale](coordinates.md#scale)] |  |
| `resolution_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |
| `additional_scan_parameters` | `dict` |  |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### ManipulatorConfig

Configuration of a manipulator

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system` | [CoordinateSystem](coordinates.md#coordinatesystem) |  |
| `local_axis_positions` | [Translation](coordinates.md#translation) |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### MousePlatformConfig

Configuration for mouse platforms

| Field | Type | Description |
|-------|------|-------------|
| `objects_in_arena` | `Optional[List[str]]` |  |
| `active_control` | `bool` | True when movement of the mouse platform is dynamically controlled by the experimenter |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### MriScanSequence

MRI scan sequence

| Name | Value |
|------|-------|
| `RARE` | `RARE` |
| `OTHER` | `Other` |


### PatchCordConfig

Configuration of a patch cord and its output power to another device

| Field | Type | Description |
|-------|------|-------------|
| `channels` | List[[Channel](#channel)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### PlanarImage

Description of an N-D image acquired in a specific imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `planes` | List[[Plane](#plane) or [CoupledPlane](#coupledplane) or [SlapPlane](#slapplane)] |  |
| `channel_name` | `str` |  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] |  |


### PlanarImageStack

Description of a stack of images acquired in a specific imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `power_function` | [PowerFunction](#powerfunction) |  |
| `depth_start` | `float` |  |
| `depth_end` | `float` |  |
| `depth_step` | `float` |  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `planes` | List[[Plane](#plane) or [CoupledPlane](#coupledplane) or [SlapPlane](#slapplane)] |  |
| `channel_name` | `str` |  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Position, rotation, and scale of the image. Note that depth should be in the planes. |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] |  |


### Plane

Configuration of an imaging plane

| Field | Type | Description |
|-------|------|-------------|
| `depth` | `float` |  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `power` | `float` |  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) |  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) |  |


### PowerFunction

Power functions

| Name | Value |
|------|-------|
| `CONSTANT` | `Constant` |
| `LINEAR` | `Linear` |
| `EXPONENTIAL` | `Exponential` |
| `OTHER` | `Other` |


### ProbeConfig

Configuration for a device inserted into a brain

| Field | Type | Description |
|-------|------|-------------|
| `primary_targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) |  |
| `other_targeted_structure` | Optional[List[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)]] |  |
| `atlas_coordinate` | Optional[[AtlasCoordinate](coordinates.md#atlascoordinate)] |  |
| `coordinate_system` | [CoordinateSystem](coordinates.md#coordinatesystem) | Device coordinate system, defines un-rotated probe's orientation relative to the Acquisition.coordinate_system |
| `transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Entry coordinate, depth, and rotation in the Acquisition.coordinate_system |
| `dye` | `Optional[str]` |  |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### SampleChamberConfig

Configuration of a sample chamber

| Field | Type | Description |
|-------|------|-------------|
| `chamber_immersion` | [Immersion](#immersion) |  |
| `sample_immersion` | Optional[[Immersion](#immersion)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### SamplingStrategy

Description of an image sampling strategy

| Field | Type | Description |
|-------|------|-------------|
| `frame_rate` | `float` |  |
| `frame_rate_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) |  |


### ScanType

Type of scan

| Name | Value |
|------|-------|
| `SETUP` | `Set Up` |
| `SCAN_3D` | `3D Scan` |


### SlapAcquisitionType

Type of slap acquisition

| Name | Value |
|------|-------|
| `PARENT` | `Parent` |
| `BRANCH` | `Branch` |


### SlapChannel

Configuration of a channel for Slap

| Field | Type | Description |
|-------|------|-------------|
| `dilation` | `int` |  |
| `dilation_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `description` | `Optional[str]` |  |
| `channel_name` | `str` |  |
| `intended_measurement` | `Optional[str]` | What signal is this channel measuring |
| `detector` | [DetectorConfig](#detectorconfig) |  |
| `additional_device_names` | Optional[List[[DeviceConfig](#deviceconfig)]] | Mirrors, dichroics, etc |
| `light_sources` | List[[LaserConfig](#laserconfig) or [LightEmittingDiodeConfig](#lightemittingdiodeconfig)] |  |
| `variable_power` | `Optional[bool]` | Set to true when the power varies across Planes -- put the power in the Plane.power field |
| `excitation_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] |  |
| `emission_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] |  |
| `emission_wavelength` | `Optional[int]` |  |
| `emission_wavelength_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |


### SlapPlane

Configuration of an imagine plane on a Slap microscope

| Field | Type | Description |
|-------|------|-------------|
| `dmd_dilation_x` | `int` |  |
| `dmd_dilation_y` | `int` |  |
| `dilation_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `slap_acquisition_type` | [SlapAcquisitionType](#slapacquisitiontype) |  |
| `target_neuron` | `Optional[str]` |  |
| `target_branch` | `Optional[str]` |  |
| `path_to_array_of_frame_rates` | `AssetPath` | Relative path from metadata json to file |
| `depth` | `float` |  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `power` | `float` |  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) |  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) |  |


### SpeakerConfig

Configuration of auditory speaker configuration

| Field | Type | Description |
|-------|------|-------------|
| `volume` | `Optional[float]` |  |
| `volume_unit` | Optional[[SoundIntensityUnit](../aind_data_schema_models/units.md#soundintensityunit)] |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### StackStrategy

Description of a stack image sampling strategy

| Field | Type | Description |
|-------|------|-------------|
| `image_repeats` | `int` |  |
| `stack_repeats` | `int` |  |
| `frame_rate` | `float` |  |
| `frame_rate_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) |  |


### SubjectPosition

Subject position

| Name | Value |
|------|-------|
| `PRONE` | `Prone` |
| `SUPINE` | `Supine` |


### TriggerType

Types of detector triggers

| Name | Value |
|------|-------|
| `INTERNAL` | `Internal` |
| `EXTERNAL` | `External` |


### Valence

Valence of a stimulus

| Name | Value |
|------|-------|
| `POSITIVE` | `Positive` |
| `NEGATIVE` | `Negative` |
| `NEUTRAL` | `Neutral` |
| `UNKNOWN` | `Unknown` |


