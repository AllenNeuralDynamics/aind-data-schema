# Acquisition

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/acquisition.py)

An acquisition is single episode of data collection that creates one data asset.

The acquisition metadata is split into two parallel pieces the `DataStream` and the `StimulusEpoch`. At any given moment in time the active `DataStream` represents all modalities of data being acquired, while the `StimulusEpoch` represents all stimuli being presented.

- `DataStream`: All devices that are acquiring data and their configurations.
- `StimulusEpoch`: All stimuli being presented to the subject.

In situations where data or stimulus modalities change, or where the configuration of devices or presented stimuli change significantly, you should start a new `DataStream` or `StimulusEpoch`. Note that because the start and stop times are independent almost all acquisitions will fall into one of these three common types:

1. Single data stream and one stimulus epoch (including no stimulus): these acquisitions are common for imaging experiments with specimens where there might be no stimulus presented.
2. Single data stream with multiple stimulus epochs: common during animal physiology when you might do both an experimental stimulus and then follow that with one or more epochs of quite wakefulness, receptive field mapping, etc.
3. Single stimulus epoch with multiple data streams: less common, but can occur if you switch modalities during an experiment or change the configuration of an acute recording device.

## Uniqueness

You can uniquely identify acquisition sessions (and therefore a specific data asset) by their acquisition datetime (`Acquisition.session_start_time`). In addition, the `Acquisition.acquisition_type` is an open `str` field where you can put information that groups similar acquisitions together. Examples of good acquisition types are strings like: `"Training"`, `"Stage 1"`, `"Behavior with fiber photometry"` and other phrases that clearly identify what part of an experiment this acquisition belongs to.

## FAQs

### When should a DataStream be split in two

The `DataStream` should be split if there is a change in data modalities or a change in the configuration of devices.

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
