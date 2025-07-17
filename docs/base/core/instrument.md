# Instrument

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/instrument.py)

The `instrument.json` collects the components, mostly hardware devices, used to collect data. In general, the instrument schema describes the static state of the data acquisition hardware across sessions. The [Acquisition](acquisition.md) is used to describe the configuration of components for a specific session.

Instrument files are created manually, either through the [metadata-entry app](https://metadata-entry.allenneuraldynamics.org) or by writing python code that uses [aind-data-schema](https://github.com/allenNeuralDynamics/aind-data-schema). In general, your `instrument.json` file should be re-used across every session without changes until a device is added, removed, or moved, or maintenance is performed. The last change to an instrument should be timestamped in the `Instrument.modification_date` field.

## Uniqueness

It is critical to be able to identify data assets acquired on the same hardware. The schema is designed such that the combination of the `instrument_id` and `modification_date` uniquely specify the state of an instrument.

## Devices

Each `Device` has a `name` field which is used as a "foreign key" in the metadata schema. The `name` allows us to link together device definitions in the instrument with their configurations in the acquisition, as well as to link devices with connections. Use simple descriptive names like "Red laser".

### Assemblies

An assembly is a collection of devices that function together and share a single position. E.g. a camera and the lens attached to it, or an ephys probe with its manipulator.

### Devices that aren't in the schema

If you only need to track the `name`, `manufacturer`, `model`, and `serial_number` you can create custom devices using the `Device` class. The `Device.notes` field should be used to provide a description of the device and how it is used.

If you need to specify additional information about a device we will need to add a specific class for it. Open an [issue](https://github.com/AllenNeuralDynamics/aind-data-schema/issues) specifying what kind of information is needed to be tracked and developers will follow up with you.

### Missing organizations

You can find the full list of [Organizations](aind_data_schema_models/organizations.md) in the `aind-data-schema-models` repository. Some device types are restricted to a subset of this full list to simplify the `metadata-entry` app. Please open an [issue](https://github.com/AllenNeuralDynamics/aind-data-schema/issues) if you need a manufacturer that isn't available in either the main list or one of the subsets.

## Position

### RelativePosition

For all devices where a position is expected you are *required* to provide the relative position. This is a `List[AnatomicalRelative]`, for example you can specify that a computer monitor is `[Anterior]`. Relative positions should be used for devices that might have small position adjustments made from day-to-day and where the exact position is not important.

### Exact position

For devices where you know the exact position you need to describe the `CoordinateSystem` and and `transform` of the device. The transform describes the `device_to_instrument` transformation, i.e. given a point in the device's coordinate system (0,0,0) how do you need to translate (and rotate/scale) that point to place it in the instrument's coordinate system. Please refer to the [coordinate systems](coordinate_systems.md) page for additional details.

## Examples

- [Ephys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ephys_instrument.py)
- [AIBS Smartspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aibs_smartspim.py)
- [AIND Smartspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aind_smartspim_instrument.py)
- [Exaspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/exaspim_instrument.py)
- [FIP / Ophys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/fip_ophys_instrument.py)
- [Multi-plane ophys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/multiplane_ophys_instrument.py)
