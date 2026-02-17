# Configs

## Model definitions

### AirPuffConfig

Air puff device configuration

| Field | Type | Title (Description) |
|-------|------|-------------|
| `valence` | [Valence](#valence) | Valence  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Initial relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to acquisition transform  |
| `pressure` | `Optional[float]` | Pressure  |
| `pressure_unit` | Optional[[PressureUnit](../aind_data_schema_models/units.md#pressureunit)] | Pressure unit  |
| `duration` | `Optional[float]` | Duration  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### CatheterConfig

Configuration of a catheter

| Field | Type | Title (Description) |
|-------|------|-------------|
| `targeted_structure` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Targeted blood vessel (Use options from MouseBloodVessels) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### Channel

Configuration of a channel

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_name` | `str` | Channel  |
| `intended_measurement` | `Optional[str]` | Intended measurement (What signal is this channel measuring) |
| `detector` | [DetectorConfig](#detectorconfig) | Detector configuration  |
| `additional_device_names` | Optional[List[[DeviceConfig](#deviceconfig)]] | Additional device names (Mirrors, dichroics, etc) |
| `light_sources` | List[[LaserConfig](#laserconfig) or [LightEmittingDiodeConfig](#lightemittingdiodeconfig)] | Light source configurations  |
| `variable_power` | `Optional[bool]` | Variable power (Set to true when the power varies across Planes -- put the power in the Plane.power field) |
| `excitation_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] | Excitation filters  |
| `emission_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] | Emission filters  |
| `emission_wavelength` | `Optional[int]` | Emission wavelength  |
| `emission_wavelength_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Emission wavelength unit  |


### CoupledPlane

Configuration of a pair of coupled imaging plane

| Field | Type | Title (Description) |
|-------|------|-------------|
| `plane_index` | `int` | Plane index  |
| `coupled_plane_index` | `int` | Coupled plane index (Plane index of the coupled plane) |
| `power_ratio` | `float` | Power ratio  |
| `depth` | `float` | Depth  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Depth unit  |
| `power` | `float` | Power  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) | Power unit  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) | Targeted structure  |


### DetectorConfig

Configuration of detector settings

| Field | Type | Title (Description) |
|-------|------|-------------|
| `exposure_time` | `float` | Exposure time  |
| `exposure_time_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Exposure time unit  |
| `trigger_type` | [TriggerType](#triggertype) | Trigger type  |
| `compression` | Optional[[Code](identifiers.md#code)] | Compression (Compression algorithm used during acquisition) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### DeviceConfig

Parent class for all configurations

| Field | Type | Title (Description) |
|-------|------|-------------|
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### EphysAssemblyConfig

Group of configurations for an ephys assembly

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manipulator` | [ManipulatorConfig](#manipulatorconfig) | Manipulator configuration  |
| `probes` | List[[ProbeConfig](#probeconfig)] | Probe configurations  |
| `modules` | Optional[List[[MISModuleConfig](#mismoduleconfig)]] | Modules (Configurations for conveniently tracking manipulator modules, e.g. on the New Scale dome.) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### FiberAssemblyConfig

Inserted fiber photometry probe recorded in a stream

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manipulator` | [ManipulatorConfig](#manipulatorconfig) | Manipulator configuration  |
| `probes` | List[[ProbeConfig](#probeconfig)] | Probe configurations  |
| `patch_cords` | List[[PatchCordConfig](#patchcordconfig)] | Fiber photometry devices  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### Image

Description of an N-D image

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_name` | `str` | Channel name  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Dimensions unit  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Image to acquisition transform (Position, rotation, and scale of the image. Note that depth should be in the planes.) |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] | Dimensions  |


### ImageSPIM

Description of an N-D image acquired with SPIM

| Field | Type | Title (Description) |
|-------|------|-------------|
| `file_name` | `AssetPath` | File name  |
| `imaging_angle` | `int` | Imaging angle (Angle of the detector relative to the image plane relative to perpendicular) |
| `imaging_angle_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) | Imaging angle unit  |
| `image_start_time` | `Optional[datetime (timezone-aware)]` | Image acquisition start time  |
| `image_end_time` | `Optional[datetime (timezone-aware)]` | Image acquisition end time  |
| `channel_name` | `str` | Channel name  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Dimensions unit  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Image to acquisition transform (Position, rotation, and scale of the image. Note that depth should be in the planes.) |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] | Dimensions  |


### ImagingConfig

Configuration of an imaging instrument

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channels` | List[[Channel](#channel) or [SlapChannel](#slapchannel)] |   |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Coordinate system (Required for ImageSPIM objects and when the imaging coordinate system differs from the Acquisition.coordinate_system) |
| `images` | List[[PlanarImage](#planarimage) or [PlanarImageStack](#planarimagestack) or [ImageSPIM](#imagespim)] | Images  |
| `sampling_strategy` | Optional[[SamplingStrategy](#samplingstrategy)] | Sampling strategy  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### Immersion

Configuration of immersion medium

| Field | Type | Title (Description) |
|-------|------|-------------|
| `medium` | [ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium) | Immersion medium  |
| `refractive_index` | `float` | Index of refraction  |


### InterleavedStrategy

Description of an interleaved image sampling strategy

| Field | Type | Title (Description) |
|-------|------|-------------|
| `image_index_sequence` | `List[int]` | Interleaving sequence  |
| `frame_rate` | `float` | Frame rate  |
| `frame_rate_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) | Frame rate unit  |


### LaserConfig

Configuration of laser settings in an acquisition

| Field | Type | Title (Description) |
|-------|------|-------------|
| `wavelength` | `int` | Wavelength (nm)  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Wavelength unit  |
| `power` | `Optional[float]` | Excitation power  |
| `power_unit` | Optional[[PowerUnit](../aind_data_schema_models/units.md#powerunit)] | Excitation power unit  |
| `power_measured_at` | `Optional[str]` | Power measurement location (For example: objective, patch cable, etc) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### LickSpoutConfig

Lick spout acquisition information

| Field | Type | Title (Description) |
|-------|------|-------------|
| `solution` | [Liquid](#liquid) | Solution  |
| `solution_valence` | [Valence](#valence) | Valence  |
| `volume` | `float` | Volume  |
| `volume_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) | Volume unit  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Initial relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to acquisition transform (Entry coordinate, depth, and rotation in the Acquisition.coordinate_system) |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### LightEmittingDiodeConfig

Configuration of LED settings

| Field | Type | Title (Description) |
|-------|------|-------------|
| `power` | `Optional[float]` | Excitation power  |
| `power_unit` | Optional[[PowerUnit](../aind_data_schema_models/units.md#powerunit)] | Excitation power unit  |
| `power_measured_at` | `Optional[str]` | Power measurement location (For example: objective, patch cable, etc) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### Liquid

Solution names

| Name | Value |
|------|-------|
| `WATER` | `Water` |
| `SUCROSE` | `Sucrose` |
| `QUININE` | `Quinine` |
| `CITRIC_ACID` | `Citric acid` |
| `OTHER` | `Other` |


### MISCameraConfig

Configuration for a camera used in a New Scale modular insertion system

| Field | Type | Title (Description) |
|-------|------|-------------|
| `detector_config` | [DetectorConfig](#detectorconfig) | Detector configuration  |
| `module` | [MISModuleConfig](#mismoduleconfig) | Module  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to instrument transform (Position and orientation of the device in the instrument coordinate system) |


### MISModuleConfig

Modular insertion system module configuration

| Field | Type | Title (Description) |
|-------|------|-------------|
| `arc_angle` | `float` | Arc Angle (deg)  |
| `module_angle` | `float` | Module Angle (deg)  |
| `rotation_angle` | `Optional[float]` | Rotation Angle (deg)  |
| `angle_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) | Angle unit  |
| `notes` | `Optional[str]` | Notes  |


### MRAcquisitionType

MRI acquisition type

| Name | Value |
|------|-------|
| `SCAN_2D` | `2D` |
| `SCAN_3D` | `3D` |


### MRIScan

Configuration of a 3D scan

| Field | Type | Title (Description) |
|-------|------|-------------|
| `index` | `int` | Index (Index of the scan in the session, starting at 1) |
| `setup` | `bool` | Setup (Positioning, shim, and other pre-scan adjustments) |
| `pulse_sequence_type` | [PulseSequenceType](#pulsesequencetype) | Scan sequence (BIDS PulseSequenceType) |
| `mr_acquisition_type` | [MRAcquisitionType](#mracquisitiontype) | MR acquisition type (BIDS MRAcquisitionType / DICOM Tag 0018,0023) |
| `resolution` | Optional[[Scale](coordinates.md#scale)] | Voxel resolution  |
| `resolution_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Voxel resolution unit  |
| `additional_scan_parameters` | `Optional[dict]` | Parameters  |
| `rare_factor` | `Optional[int]` | RARE factor  |
| `echo_time` | `decimal.Decimal` | Echo time (s) (BIDS EchoTime / DICOM Tag 0018,0081) |
| `echo_time_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Echo time unit  |
| `effective_echo_time` | `Optional[decimal.Decimal]` | Effective echo time  |
| `repetition_time` | `decimal.Decimal` | Repetition time (s) (BIDS RepetitionTime / DICOM Tag 0018,0080) |
| `repetition_time_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Repetition time unit  |
| `scanner_coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Scanner coordinate system  |
| `affine_transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | MRI Scan affine transform (NIFTI sform/qform, Bruker vc_transform, etc) |
| `subject_position` | [SubjectPosition](#subjectposition) | Subject position  |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### ManipulatorConfig

Configuration of a manipulator

| Field | Type | Title (Description) |
|-------|------|-------------|
| `coordinate_system` | [CoordinateSystem](coordinates.md#coordinatesystem) | Device coordinate system  |
| `local_axis_positions` | [Translation](coordinates.md#translation) | Local axis positions  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### MousePlatformConfig

Configuration for mouse platforms

| Field | Type | Title (Description) |
|-------|------|-------------|
| `objects_in_arena` | `Optional[List[str]]` | Objects in area  |
| `active_control` | `bool` | Active control (True when movement of the mouse platform is dynamically controlled by the experimenter) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### OlfactometerChannelInfo

Configuration of a channel in an olfactometer

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_index` | `int` | Channel index  |
| `odorant` | `str` | Odorant  |
| `dilution` | `decimal.Decimal` | Odorant dilution  |
| `dilution_unit` | [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) | Dilution unit  |


### OlfactometerConfig

Configuration of olfactometer

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_configs` | List[[OlfactometerChannelInfo](#olfactometerchannelinfo)] | Channel configurations (List of channels with their odorant and concentration) |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### PatchCordConfig

Configuration of a patch cord and its output power to another device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channels` | List[[Channel](#channel)] | Channels  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### PlanarImage

Description of an N-D image acquired in a specific imaging plane

| Field | Type | Title (Description) |
|-------|------|-------------|
| `planes` | List[[Plane](#plane) or [CoupledPlane](#coupledplane) or [SlapPlane](#slapplane)] | Imaging planes  |
| `channel_name` | `str` | Channel name  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Dimensions unit  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Image to acquisition transform (Position, rotation, and scale of the image. Note that depth should be in the planes.) |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] | Dimensions  |


### PlanarImageStack

Description of a stack of images acquired in a specific imaging plane

| Field | Type | Title (Description) |
|-------|------|-------------|
| `power_function` | [PowerFunction](#powerfunction) | Power function  |
| `depth_start` | `float` | Starting depth  |
| `depth_end` | `float` | Ending depth  |
| `depth_step` | `float` | Step size  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Depth unit  |
| `planes` | List[[Plane](#plane) or [CoupledPlane](#coupledplane) or [SlapPlane](#slapplane)] | Imaging planes  |
| `channel_name` | `str` | Channel name  |
| `dimensions_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Dimensions unit  |
| `image_to_acquisition_transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Image to acquisition transform (Position, rotation, and scale of the image. Note that depth should be in the planes.) |
| `dimensions` | Optional[[Scale](coordinates.md#scale)] | Dimensions  |


### Plane

Configuration of an imaging plane

| Field | Type | Title (Description) |
|-------|------|-------------|
| `depth` | `float` | Depth  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Depth unit  |
| `power` | `float` | Power  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) | Power unit  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) | Targeted structure  |


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

| Field | Type | Title (Description) |
|-------|------|-------------|
| `primary_targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) | Targeted structure  |
| `other_targeted_structure` | Optional[List[[BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3)]] | Other targeted structure  |
| `atlas_coordinate` | Optional[[AtlasCoordinate](coordinates.md#atlascoordinate)] | Target coordinate in Acquisition.atlas  |
| `coordinate_system` | [CoordinateSystem](coordinates.md#coordinatesystem) | Device coordinate system (Device coordinate system, defines un-rotated probe's orientation relative to the Acquisition.coordinate_system) |
| `transform` | List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)] | Device to acquisition transform (Entry coordinate, depth, and rotation in the Acquisition.coordinate_system) |
| `dye` | `Optional[str]` | Dye  |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### PulseSequenceType

MRI pulse sequence type

| Name | Value |
|------|-------|
| `RARE` | `RARE` |
| `FLASH` | `FLASH` |
| `MSME` | `MSME` |
| `OTHER` | `Other` |


### SampleChamberConfig

Configuration of a sample chamber

| Field | Type | Title (Description) |
|-------|------|-------------|
| `chamber_immersion` | [Immersion](#immersion) | Acquisition chamber immersion data  |
| `sample_immersion` | Optional[[Immersion](#immersion)] | Acquisition sample immersion data  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### SamplingStrategy

Description of an image sampling strategy

| Field | Type | Title (Description) |
|-------|------|-------------|
| `frame_rate` | `float` | Frame rate  |
| `frame_rate_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) | Frame rate unit  |


### SlapAcquisitionType

Type of slap acquisition

| Name | Value |
|------|-------|
| `PARENT` | `Parent` |
| `BRANCH` | `Branch` |


### SlapChannel

Configuration of a channel for Slap

| Field | Type | Title (Description) |
|-------|------|-------------|
| `dilation` | `int` | Dilation  |
| `dilation_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Dilation unit  |
| `description` | `Optional[str]` | Description  |
| `channel_name` | `str` | Channel  |
| `intended_measurement` | `Optional[str]` | Intended measurement (What signal is this channel measuring) |
| `detector` | [DetectorConfig](#detectorconfig) | Detector configuration  |
| `additional_device_names` | Optional[List[[DeviceConfig](#deviceconfig)]] | Additional device names (Mirrors, dichroics, etc) |
| `light_sources` | List[[LaserConfig](#laserconfig) or [LightEmittingDiodeConfig](#lightemittingdiodeconfig)] | Light source configurations  |
| `variable_power` | `Optional[bool]` | Variable power (Set to true when the power varies across Planes -- put the power in the Plane.power field) |
| `excitation_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] | Excitation filters  |
| `emission_filters` | Optional[List[[DeviceConfig](#deviceconfig)]] | Emission filters  |
| `emission_wavelength` | `Optional[int]` | Emission wavelength  |
| `emission_wavelength_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Emission wavelength unit  |


### SlapPlane

Configuration of an imagine plane on a Slap microscope

| Field | Type | Title (Description) |
|-------|------|-------------|
| `dmd_dilation_x` | `int` | DMD Dilation X (pixels)  |
| `dmd_dilation_y` | `int` | DMD Dilation Y (pixels)  |
| `dilation_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Dilation unit  |
| `slap_acquisition_type` | [SlapAcquisitionType](#slapacquisitiontype) | Slap experiment type  |
| `target_neuron` | `Optional[str]` | Target neuron  |
| `target_branch` | `Optional[str]` | Target branch  |
| `path_to_array_of_frame_rates` | `AssetPath` | Array of frame rates (Relative path from metadata json to file) |
| `depth` | `float` | Depth  |
| `depth_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Depth unit  |
| `power` | `float` | Power  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) | Power unit  |
| `targeted_structure` | [BrainAtlas](../aind_data_schema_models/brain_atlas.md#ccfv3) | Targeted structure  |


### SpeakerConfig

Configuration of auditory speaker configuration

| Field | Type | Title (Description) |
|-------|------|-------------|
| `volume` | `Optional[float]` | Volume (dB)  |
| `volume_unit` | Optional[[SoundIntensityUnit](../aind_data_schema_models/units.md#soundintensityunit)] | Volume unit  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### StackStrategy

Description of a stack image sampling strategy

| Field | Type | Title (Description) |
|-------|------|-------------|
| `image_repeats` | `int` | Number of image repeats  |
| `stack_repeats` | `int` | Number of stack repeats  |
| `frame_rate` | `float` | Frame rate  |
| `frame_rate_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) | Frame rate unit  |


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


