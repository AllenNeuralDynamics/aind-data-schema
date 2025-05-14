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
**No:** This doesn't need a specific class and you can add it under `additional_devices` using the `Device` 
class. Feel free to use the notes field to add a description of the device and how you are using it if needed. 
**Yes:** if this is a device that you need to specify more information about, we will need to add a specific
class for it. Open an issue on GitHub specifying what kind of information is needed to be tracked and we’ll be in 
touch about adding it shortly.

### Missing organizations

Check the `organizations.py` file in the `aind-data-schema-models` which contains the master list of organizations. This 
list gets sublisted to specific manufacturers for specific device types to make it easier for you to find relevant 
options. If your manufacturer is in the master list but isn't an option for the device you are trying to use it for, open 
a GitHub issue for the `aind-data-schema-models` repo asking that your manufacturer be added to the options for your 
device type. If your manufacturer is not in the master list, open a GitHub issue for the `aind-data-schema-models` repo 
asking that your manufacturer be added to the list. Also specify what device type(s) it is relevant to. Please try to 
provide (1) the full name of the Manufacturer, (2) any common acronym or abbreviation they might use, and (3) if 
possible identify the RORID for the company at ror.org. Not every company is in that registry, so you might not find it 
(in which case let us know that you tried). You are more likely than we are to be able to disambiguate between 
similarly named companies if there are other companies with similar names in the registry.

### Position

The `RelativePosition` class enables you to specify the position of a device in the rig. This class includes both 
position and rotation information of the device. For this to communicate anything, you must also specify the reference 
point and axes of the device as well as the `origin` and `rig_axes` of the Rig. You get to define these how it works 
best for you, but I recommend discussing it with your team and SIPE. Some devices really should have position 
information in order for the data to be interpretable  (e.g. cameras or visual monitors). Other devices are positioned 
wherever they fit and their position doesn’t impact what they do or how the data is interpreted. These devices do not 
require position information.

## Examples

- [Ephys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ephys_instrument.py)
- [AIBS Smartspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aibs_smartspim.py)
- [AIND Smartspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aind_smartspim_instrument.py)
- [Exaspim instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/exaspim_instrument.py)
- [FIP / Ophys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/fip_ophys_instrument.py)
- [Multi-plane ophys instrument](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/multiplane_ophys_instrument.py)

## Model definitions