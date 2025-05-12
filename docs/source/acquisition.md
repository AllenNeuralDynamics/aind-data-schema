# Acquisition

An acquisition is single episode of data collection that creates one data asset. The acquisition metadata describes what devices were active and their configurations, as well as what stimulus was presented to the subject. An acquisition consists of parallel `Data Streams` and `Stimulus Epochs`, described below.

**Q: What are Streams?**

A stream is the data that is being acquired at one time. A stream can contain multiple modalities, for instance: ecephys, 
behavior videos, and behavior. They are part of one stream if they are being acquired simultaneously and their start and 
end times are roughly the same. A single session may consist of a single stream, or there can be multiple streams in a 
session (e.g. if Neuropixels probes are repositioned part way through the session).

**Q: What are Stimulus Epochs?**

The Stimulus Epoch describes any stimulus/behavior information. This can include behavioral tasks, sensory stimuli, 
optogenetic stimulation, etc. A session can have a single or multiple stimulus epochs. And, importantly, the timing of 
the streams and the stimulus epochs may or may not be aligned.

**Q: Hunh? I’m confused.**

Perhaps these diagrams can help?

![image](_static/session_image_1.png)

Example session with single stream and epoch

![image](_static/session_image_2.png)

Example where the animal is engaged with a single behavior, and there are two distinct data streams. E.g. repositioned 
probes to target different structures. 

![image](_static/session_image_3.png)

Example where there is one data stream during the session, but multiple stimulus epochs. E.g. active behavior, passive 
behavior replay, and optotagging.

Example where there is one data stream during the session, but multiple stimulus epochs. E.g. active behavior, passive 
behavior replay, and optotagging.

**Q: Why do both Stream and Stimulus Epoch have a field for `light_source_configs`?**

The Stream describes the data being collected. A light source involved in data acquisition (e.g. the laser used for 
2-photon imaging) should be described in the Stream. The Stimulus Epoch describes any stimulus/behavior that occurs 
during the session. A light source involved in a stimulus (e.g. the laser used for optotagging or photostim) should be 
in the Stimulus Epoch.

**Q: How do I create a stimulus table?**

A stimulus table is not part of the metadata but is part of the data itself. We track high level stimulus parameters in 
the Stimulus Class, but the trial-by-trial stimulus information belongs in the NWB file itself.

**Q: Can you explain the `stimulus_parameters` field? How do I use this?**

Great question! We began defining specific classes for different stimulus and behavior modalities, but quickly found 
that this won't be scalable. You can currently use these classes if they work for you. However, in the long run we 
would like this to move into the `script` field. This field uses the Software class, which has a field for 
`parameters`. Users should use this to document the parameters used to control the stimulus or behavior. parameters
should have unambiguous names (e.g. "trial_duration" rather than "duration") and units must be provided as a separate
field (e.g. "trial_duration_unit"). We recommend that you use software to define these and be consistent within your 
projects. Please reach out with questions and we can help you with this.

**Q: What should I put for the `session_type`?**

Ideally a short phrase that describes the session that you use consistently within the project. This field serves to
identify related sessions.

**Q: How do I create the session file?**

We are working with scientific teams to create metadata mappers to ingest this metadata using both acquisition software 
and SLIMS. Until this is fully functional, these files must be created manually.

**Q: How do I know if my mouse platform is "active"?**

There are experiments in which the mouse platform is actively controlled by the stimulus/behavior software - i.e. the 
resistance of the wheel is adjusted based on the subject's activity. This is an "active" mouse platform. Most platforms 
we use are currently not active in this way.

**Q: How do I use the Calibration field?**

This is to track any device calibrations that are performed, such as gamma correction for monitors, reward valve 
delivery calibration, laser power calibration, etc. For calibrations that are done less frequently (e.g. gamma 
correction) this can be documented in the Rig schema. For calibrations that are done frequently, they can do documented 
in the Session schema. Both places use the same class. This class identifies which device is calibrated (using the 
device's name), a description of the calibration (e.g. "Laser power calibration"), and then an input dictionary and an 
output dictionary. You can use this as makes most sense for your needs, but we envision the input dictionary having 
input values (say laser power percentage settings) and the output dictionary having output values (say the measured 
wattage out of the laser). You define the key and provide a list of the values. We recommed that you use the same 
dictionary structures when you do the same calibrations (when possible).

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
