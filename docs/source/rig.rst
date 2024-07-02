Rig/Instrument
==============

**Q: What is a rig? What is an instrument?**

The rig or instrument is the collection of devices that are used to collect data. Rig is used for physiology (ephys/
ophys) and behavior data, while instrument is used for light sheet or confocal imaging. The naming difference is largely 
due to how these different subfields describe things.

**Q: What are devices?**

Devices are pieces of hardware that are used for experiments - the components of the rig/instrument. 

**Q: What’s the difference between rig and session? They both have a lot of device information – what lives where?**

The intention is to use the rig schema to describe the static state of the rig to reduce the amount of redundant 
information that must be created for each session. The rig/instrument schema describe the devices that are used to
collect data. Specifically, these schemas escribe the devices their part numbers and key specifications. There might be 
settings that are static settings (e.g. on visual monitors, the brightness and contrast are hardware settings that are 
set on the monitor and not controlled programmatically). In the session schema, we specify which devices for the rig 
are active, and any parameters or settings for those devices that are variable (e.g. the laser power of the laser). 
For most users, the rig file should be relatively stable, being updated when a device is replaced or changed. However, 
for others the rigs are in greater state of flux and the files are updated more frequently.

**Q: How do I create a rig or instrument file?**

Currently, these are created manually. This can either be done using the `metadata entry web application <https://metadata-entry.allenneuraldynamics.org/>`_
or by writing python code that imports `aind-data-schema <https://github.com/allenNeuralDynamics/aind-data-schema>`_.

**Q: Do I need to create a new rig/instrument file for each data asset?**

Ideally no. The rig/instrument file should be relatively stable and hopefully won’t change much from one day to the
next, so you can reuse the same file for multiple data assets. However, when the devices in a rig do change, the rig/
instrument file must be updated. For instance, replacing a broken Neuropixels probe requires an updated file, as does 
adding or moving a camera to a rig. The `rig_id` and the `date_of_modification` should make it clear when the file was 
last updated.

**Q: How is the `rig_id` defined?**

The `rig_id` consists of the room number_the rig description_the date it was modified. So an ephys rig in room 123 that 
was updated on February 13, 2024 would have the id of "123_EPHYS1_20240213". The rig description can contain a short 
description as desired by the team, e.g. EPHYS1_VIS or EPHYS_OPTO.

**Q: Can I use the same json interchangeably for different behavior boxes?**

No. Different boxes have different instances of devices (e.g. different serial numbers) and need separate metadata that 
reflects that.

**Q: Do I really need to name my device? If so, what should I name it?**

Yes! The device name is required and is the key point for linking specific devices to calibration information, DAQ 
device channels, and session settings. Please add a name to each device. Please do not use the serial number of the 
device. Simple descriptive names are fine: “Red_laser” or “Laser_1” are fine examples. “LAS-442552OI93” is not ideal. 
Please don’t squeeze metadata into device names. If there is information that we need to know about the device that 
isn’t in the schema, create an issue so we can add it. You can also use the `notes` field to track additional details 
that might not warrant a schema update.

**Q: Do I need to provide serial numbers for all my devices?**

Serial number is not a required field. It is valuable to provide it, though, so please try to provide this 
information when possible. But if you cannot obtain the serial number of a device you can proceed without it.

**Q: What is an assembly?**

An assembly is a collection of devices that function together and share a single position. E.g. a camera and the 
lens attached to it, or an ephys probe with its manipulator.

**Q: There are devices in my rig that don’t have specific classes in the schema. How do I add them?**

This depends on if you need to track more information than name/manufacturer/part number/serial number? 
    **No:** This doesn't need a specific class and you can add it under `additional_devices` using the `Device` 
    class. Feel free to use the notes field to add a description of the device and how you are using it if needed. 
    **Yes:** if this is a device that you need to specify more information about, we will need to add a specific
    class for it. Open an issue on GitHub specifying what kind of information is needed to be tracked and we’ll be in 
    touch about adding it shortly.

**Q: The Manufacturer for my device isn't in the list? What do I do?**

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

**Q: How do I specify the position of the devices in my rig? What is the coordinate system?**

The `RelativePosition` class enables you to specify the position of a device in the rig. This class includes both 
position and rotation information of the device. For this to communicate anything, you must also specify the reference 
point and axes of the device as well as the `origin` and `rig_axes` of the Rig. You get to define these how it works 
best for you, but I recommend discussing it with your team and SIPE. Some devices really should have position 
information in order for the data to be interpretable  (e.g. cameras or visual monitors). Other devices are positioned 
wherever they fit and their position doesn’t impact what they do or how the data is interpreted. These devices do not 
require position information. 
