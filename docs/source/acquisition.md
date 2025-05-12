# Acquisition

An acquisition is single episode of data collection that creates one data asset.

The acquisition metadata is split into two parallel pieces:

- `DataStream`: What devices were active and their configurations.
- `StimulusEpoch`: What stimulus was presented to the subject.

Both streams and epochs have independent start and stop times and can contain multiple modalities. Your acquisition probably falls into one of the three common types:

- Single data stream and one stimulus epoch (or no stimulus): these acquisitions are common for imaging experiments with specimens where there's no stimulus.
- Single data stream with multiple stimulus epochs: common during animal physiology when you might do both an experimental stimulus and then follow that with one or more epochs of quite wakefulness, receptive field mapping, etc.
- Single stimulus epoch with multiple data streams: less common, but can occur if you switch modalities during an experiment or change the position of an acute recording device.

**Q: Diagrams **

![image](_static/session_image_1.png)

Example session with single stream and epoch

![image](_static/session_image_2.png)

Example where the animal is engaged with a single behavior, and there are two distinct data streams. E.g. repositioned 
probes to target different structures. 

![image](_static/session_image_3.png)

Example where there is one data stream during the session, but multiple stimulus epochs. E.g. active behavior, passive behavior replay, and optotagging.

## Examples

- [Ephys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ephys_acquisition.py)
- [ExaSPIM acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/exaspim_acquisition.py)
- [Bergamo ophys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/bergamo_ophys_acquisition.py)
- [Multi-plane ophys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/multiplane_ophys_acquisition.py)
- [Ophys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ophys_acquisition.py)

## Model definitions

### Acquisition

Description of an imaging acquisition

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | `str` |  |
| `specimen_id` | `Optional[str]` | Specimen ID is required for in vitro imaging modalities |
| `acquisition_start_time` | `datetime (timezone-aware)` |  |
| `acquisition_end_time` | `datetime (timezone-aware)` |  |
| `experimenters` | List[[Person](components/identifiers.md#person)] |  |
| `protocol_id` | `Optional[List[str]]` | DOI for protocols.io |
| `ethics_review_id` | `Optional[List[str]]` |  |
| `instrument_id` | `str` |  |
| `acquisition_type` | `str` |  |
| `notes` | `Optional[str]` |  |
| `coordinate_system` | Optional[[CoordinateSystem](components/coordinates.md#coordinatesystem)] | Required when coordinates are provided within the Acquisition |
| `calibrations` | List[[Calibration](components/measurements.md#calibration) or [LiquidCalibration](components/measurements.md#liquidcalibration) or [LaserCalibration](components/measurements.md#lasercalibration)] | List of calibration measurements taken prior to acquisition. |
| `maintenance` | List[[Maintenance](components/measurements.md#maintenance)] | List of maintenance on instrument prior to acquisition. |
| `data_streams` | List[[DataStream](#datastream)] | A data stream is a collection of devices that are recorded simultaneously. Each acquisition can include multiple streams (e.g., if the manipulators are moved to a new location) |
| `stimulus_epochs` | List[[StimulusEpoch](#stimulusepoch)] |  |
| `subject_details` | Optional[[AcquisitionSubjectDetails](#acquisitionsubjectdetails)] |  |


### AcquisitionSubjectDetails

Details about the subject during an acquisition

| Field | Type | Description |
|-------|------|-------------|
| `animal_weight_prior` | `Optional[decimal.Decimal]` | Animal weight before procedure |
| `animal_weight_post` | `Optional[decimal.Decimal]` | Animal weight after procedure |
| `weight_unit` | [MassUnit](aind_data_schema_models/units.md#massunit) |  |
| `anaesthesia` | Optional[[Anaesthetic](procedures.md#anaesthetic)] |  |
| `mouse_platform_name` | `str` |  |
| `reward_consumed_total` | `Optional[decimal.Decimal]` |  |
| `reward_consumed_unit` | Optional[[VolumeUnit](aind_data_schema_models/units.md#volumeunit)] |  |


### DataStream

Data streams with a start and stop time

| Field | Type | Description |
|-------|------|-------------|
| `stream_start_time` | `datetime (timezone-aware)` |  |
| `stream_end_time` | `datetime (timezone-aware)` |  |
| `modalities` | List[[Modality](aind_data_schema_models/modalities.md#modality)] | Modalities that are acquired in this stream |
| `code` | Optional[List[[Code](components/identifiers.md#code)]] |  |
| `notes` | `Optional[str]` |  |
| `active_devices` | `List[str]` | Device names must match devices in the Instrument |
| `configurations` | List[[LightEmittingDiodeConfig](components/configs.md#lightemittingdiodeconfig) or [LaserConfig](components/configs.md#laserconfig) or [ManipulatorConfig](components/configs.md#manipulatorconfig) or [DetectorConfig](components/configs.md#detectorconfig) or [PatchCordConfig](components/configs.md#patchcordconfig) or [FiberAssemblyConfig](components/configs.md#fiberassemblyconfig) or [MRIScan](components/configs.md#mriscan) or [LickSpoutConfig](components/configs.md#lickspoutconfig) or [AirPuffConfig](components/configs.md#airpuffconfig) or [ImagingConfig](components/configs.md#imagingconfig) or [SlapPlane](components/configs.md#slapplane) or [SampleChamberConfig](components/configs.md#samplechamberconfig) or [ProbeConfig](components/configs.md#probeconfig) or [EphysAssemblyConfig](components/configs.md#ephysassemblyconfig)] |  |
| `connections` | List[[Connection](instrument.md#connection)] | Connections that are specific to this acquisition, and are not present in the Instrument |


### PerformanceMetrics

Summary of a StimulusEpoch

| Field | Type | Description |
|-------|------|-------------|
| `output_parameters` | `aind_data_schema.base.GenericModel` |  |
| `reward_consumed_during_epoch` | `Optional[decimal.Decimal]` |  |
| `reward_consumed_unit` | Optional[[VolumeUnit](aind_data_schema_models/units.md#volumeunit)] |  |
| `trials_total` | `Optional[int]` |  |
| `trials_finished` | `Optional[int]` |  |
| `trials_rewarded` | `Optional[int]` |  |


### StimulusEpoch

Description of stimulus used during data acquisition

| Field | Type | Description |
|-------|------|-------------|
| `stimulus_start_time` | `datetime (timezone-aware)` | When a specific stimulus begins. This might be the same as the acquisition start time. |
| `stimulus_end_time` | `datetime (timezone-aware)` | When a specific stimulus ends. This might be the same as the acquisition end time. |
| `stimulus_name` | `str` |  |
| `code` | Optional[[Code](components/identifiers.md#code)] | Custom code/script used to control the behavior/stimulus and parameters |
| `stimulus_modalities` | List[[StimulusModality](aind_data_schema_models/stimulus_modality.md#stimulusmodality)] |  |
| `performance_metrics` | Optional[[PerformanceMetrics](#performancemetrics)] |  |
| `notes` | `Optional[str]` |  |
| `active_devices` | `List[str]` | Device names must match devices in the Instrument |
| `configurations` | List[[SpeakerConfig](components/configs.md#speakerconfig) or [LightEmittingDiodeConfig](components/configs.md#lightemittingdiodeconfig) or [LaserConfig](components/configs.md#laserconfig) or [MousePlatformConfig](components/configs.md#mouseplatformconfig)] |  |
