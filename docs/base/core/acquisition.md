# Acquisition

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/acquisition.py)

An acquisition is single episode of data collection that creates one data asset.

The acquisition metadata is split into two parallel pieces the `DataStream` and the `StimulusEpoch`. At any given moment in time the active `DataStream`(s) represents all modalities of data being acquired, while the `StimulusEpoch` represents all stimuli being presented.

- `DataStream`: A set of devices that are acquiring data and their configurations.
- `StimulusEpoch`: All stimuli being presented to the subject. Not all acquisitions have StimulusEpochs.

A single DataStream should capture all the modalities of data acquired as a group, even when their start/stop times differ by a small amount.

Because the start and stop times are independent for data streams and stimulus epochs almost all acquisitions will fall into one of these three common types:

1. Single data stream and one stimulus epoch (including no stimulus): these acquisitions are common for imaging experiments with specimens where there might be no stimulus presented.
2. Single data stream with multiple stimulus epochs: common during animal physiology when you might do both an experimental stimulus and then follow that with one or more epochs of quite wakefulness, receptive field mapping, etc.
3. Single stimulus epoch with multiple data streams: less common, but can occur if you switch modalities during an experiment or change the configuration of an acute recording device.

## Uniqueness

You can uniquely identify acquisition sessions (and therefore a specific data asset) by their acquisition datetime (`Acquisition.acquisition_end_time`). In addition, the `Acquisition.acquisition_type` is an open `str` field where you can put conceptual information that groups similar acquisitions together. This should not be completely redundant with project names, modalities, stimulus names, or any other fields in the metadata.

For example, in the `"Brain Computer Interface"` project name, good acquisition types would be strings like: `"BCI: Single neuron stim"` and `"BCI: Group neuron stim"`. These phrases clearly identify what part of a project these acquisitions belong to, without being overly redundant with controlled fields in the metadata.

## Stimulus parameters

You should use the `Code.parameters` field to store your stimulus properties for each [StimulusEpoch](#stimulusepoch). We have pre-existing parameter schemas for a subset of stimuli defined [here](components/stimulus.md) or you can define your own schema.

## FAQs

### When should a DataStream be split in two

The `DataStream` should be split if there is a change in data modalities or a change in the configuration of devices. Or if a modality is only acquired during a subset of the time the stream is active. For example, if you acquire behavior videos for a full hour of an acquisition and only collect ecephys for twenty minutes you should separate these into two streams. If the start and ends times are within a few minutes of each other you should combine the modalities into a single stream.

### When should a StimulusEpoch be split in two

The `StimulusEpoch` should be split if the purpose of the presented stimuli changes. For example: receptive field mapping and optogenetic manipulation are two different stimulus epochs. Individual trials of optogenetic manipulation are part of a single stimulus epoch.

Most experimenters will be familiar with the idea of breaking down an experiment into blocks and then further into trials: blocks and trials are part of one stimulus epoch. Information about blocks and trials are *parameters* that describe a stimulus epoch and can be stored in the `StimulusEpoch.code.parameters`.

## Diagrams

![image](_static/session_image_1.png)

Example acquisition demonstrating situation **1**: one data stream, one stimulus epoch.

![image](_static/session_image_3.png)

Example acquisition demonstrating situation **2**: one data stream, multiple stimulus epochs.

![image](_static/session_image_2.png)

Example acquisition demonstrating **3**: one stimulus epoch, multiple data streams.

## Examples

- [Ephys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ephys_acquisition.py)
- [ExaSPIM acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/exaspim_acquisition.py)
- [Bergamo ophys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/bergamo_ophys_acquisition.py)
- [Multi-plane ophys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/multiplane_ophys_acquisition.py)
- [Ophys acquisition](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ophys_acquisition.py)
