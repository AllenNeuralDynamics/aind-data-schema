Frequently Asked Questions
==========================

<b>Rig/Instrument</b>

Q: What is a rig? What is an instrument?
A: The rig or instrument is the collection of devices that are used to collect data. Rig is used for physiology (ephys/
    ophys) and behavior data, while instrument is used for light sheet or confocal imaging. The naming difference is
    largely due to how these different subfields describe things.

Q: What’s the difference between rig and session? They both have a lot of device information – what lives where?
A: The intention is to use the rig schema to describe the static state of the rig to reduce the amount of redundant
    information that must be created for each session. The rig/instrument schema describe the devices that are used to
    collect data. Specifically, these schemas escribe the devices their part numbers and key specifications. There
    might be settings that are static settings (e.g. on visual monitors, the brightness and contrast are hardware
    settings that are set on the monitor and not controlled programmatically). In the session schema, we specify which
    devices for the rig are active, and any parameters or settings for those devices that are variable (e.g. the laser
    power of the laser). For most users, the rig file should be relatively stable, being updated when a device is
    replaced or changed. However, for others the rigs are in greater state of flux and the files are updated more
    frequently.

Q: How do I create a rig or instrument file?
A: Currently, these are created manually. This can either be done using the GUI 
    (https://metadata-entry.allenneuraldynamics.org/) or by writing python code that imports aind-data-schema.

Q: Do I need to create a new rig/instrument file for each data asset?
A: Ideally no. The rig/instrument file should be relatively stable and hopefully won’t change much from one day to the
    next. However, when the devices in a rig do change, the rig/instrument file must be updated. For instance,
    replacing a broken Neuropixels probe requires an updated file, as does adding or moving a camera to a rig. The
    `rig_id` and the `date_of_modification` should make it clear when the file was last updated.

Q: How is the `rig_id` defined?
A: The `rig_id` consists of the room number, the rig description, and the date it was modified. So an ephys rig in room
    123 that was updated on February 13, 2024 would have the id of "123_EPHYS1_20240213". The rig description can
    contain a short description as desired by the team, e.g. EPHYS1_VIS or EPHYS_OPTO.

Q: Can I use the same json interchangeably for different behavior boxes?
A: No. Different boxes have different instances of devices (e.g. different serial numbers) and need separate metadata
    that reflects that.

Q: Do I really need to name my device? If so, what should I name it?
A: Yes! The device name is required and is the key point for linking specific devices to calibration information, DAQ
    device channels, and session settings. Please add a name to each device. Please do not use the serial number of the
    device. Simple descriptive names are fine: “Red_laser” or “Laser_1” are fine examples. “LAS-442552OI93” is not
    ideal. Please don’t squeeze metadata into device names. If there is information that we need to know about the
    device that isn’t in the schema, create an issue so we can add it. You can also use the `Notes` field to track 
    additional details that might not warrant a schema update.

Q: Do I need to provide serial numbers for all my devices?
A: Serial number is not a required field. It is valuable to provide it, though, so please try to provide this
    information when possible. But if you cannot obtain the serial number of a device you can proceed without it.

