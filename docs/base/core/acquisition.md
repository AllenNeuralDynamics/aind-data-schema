# Acquisition

An acquisition is single episode of data collection that creates one data asset.

The acquisition metadata is split into two parallel pieces:

- `DataStream`: What devices were active and their configurations.
- `StimulusEpoch`: What stimulus was presented to the subject.

Both streams and epochs have independent start and stop times and can contain multiple modalities. Your acquisition probably falls into one of the three common types:

- Single data stream and one stimulus epoch (or no stimulus): these acquisitions are common for imaging experiments with specimens where there's no stimulus.
- Single data stream with multiple stimulus epochs: common during animal physiology when you might do both an experimental stimulus and then follow that with one or more epochs of quite wakefulness, receptive field mapping, etc.
- Single stimulus epoch with multiple data streams: less common, but can occur if you switch modalities during an experiment or change the position of an acute recording device.

## Diagrams

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