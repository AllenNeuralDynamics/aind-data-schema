# Instrument

The `instrument.json` collects the components, mostly hardware devices, used to collect data. In general, the instrument schema describes the static state of the data acquisition hardware across sessions. The [Acquisition](acquisition.md) is used to describe the configuration of components for a specific session.

Instrument files are created manually, either through the [metadata-entry app](https://metadata-entry.allenneuraldynamics.org) or by writing python code that uses [aind-data-schema](https://github.com/allenNeuralDynamics/aind-data-schema). In general, your `instrument.json` file should be re-used across every session without changes until a maintenance event is performed that requires an update. Changes to the instrument should be timestamped using the `Instrument.date_of_modification` field.

## FAQs

### instrument_id

Best practice for tracking instruments is to store (1) the location, (2) the common name, and (3) the last modification date in the `Instrument.instrument_id` field using the pattern `<location>_<name>_<date>`. This makes it very easy to query the metadata to find all acquisitions performed with identical hardware conditions.

### Device.name

The `Device.name` field is a "foreign key" in the metadata schema that allows us to link together the device definitions in the instrument with their configurations in the acquisition, as well as to link devices with connections. You should use simple descriptive names like "Red laser" or "Laser 1". Do 

### Assemblies

An assembly is a collection of devices that function together and share a single position. E.g. a camera and the 
lens attached to it, or an ephys probe with its manipulator.

### Devices that aren't in the schema

This depends on if you need to track more information than name/manufacturer/part number/serial number?

- **No:** This doesn't need a specific class and you can add it to the components list using the `Device` class. Feel free to use the notes field to add a description of the device and how you are using it if needed.
- **Yes:** if this is a device that you need to specify more information about, we will need to add a specific class for it. Open an issue on GitHub specifying what kind of information is needed to be tracked and we’ll be in touch about adding it shortly.

### Missing organizations

You can find the full list of [Organizations](aind_data_schema_models/organizations.md) in the `aind-data-schema-models` repository. Some device types are restricted to a subset of this full list to simplify the `metadata-entry` app. Please open an issue if you need a manufacturer that isn't available in either the main list or one of the subsets.

### Position

#### RelativePosition

For all devices where a position is expected you are *required* to provide the relative position. This is a `List[AnatomicalRelative]`, for example you can specify that a computer monitor is `[Anterior]`. Relative positions should be used for devices that might have small position adjustments made from day-to-day and where the exact position is not important.

For devices where you know the exact position you need to describe the `CoordinateSystem` and and `transform` of the device. The transform describes the `device_to_instrument` transformation, i.e. given a point in the device's coordinate system (0,0,0) how do you need to translate (and rotate/scale) that point to place it in the instrument's coordinate system. Please refer to the [Coordinate Systems](coordinate_systems.md) page for additional details.

## Examples

- [Ephys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ephys_instrument.py)
- [AIBS Smartspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aibs_smartspim.py)
- [AIND Smartspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aind_smartspim_instrument.py)
- [Exaspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/exaspim_instrument.py)
- [FIP / Ophys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/fip_ophys_instrument.py)
- [Multi-plane ophys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/multiplane_ophys_instrument.py)

## Model definitions