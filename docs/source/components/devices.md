# Devices

## Model definitions

### AdditionalImagingDevice

Description of additional devices

| Field | Type | Title (Description) |
|-------|------|-------------|
| `imaging_device_type` | [ImagingDeviceType](../aind_data_schema_models/devices.md#imagingdevicetype) | Device type  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### AirPuffDevice

Description of an air puff device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `diameter` | `float` | Spout diameter  |
| `diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Arena

Description of a rectangular arena

| Field | Type | Title (Description) |
|-------|------|-------------|
| `size` | [Scale](coordinates.md#scale) | 3D Size  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `objects_in_arena` | List[[Device](#device)] | Objects in arena  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Camera

Camera Detector

| Field | Type | Title (Description) |
|-------|------|-------------|
| `detector_type` | [DetectorType](../aind_data_schema_models/devices.md#detectortype) |   |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) | Data interface  |
| `cooling` | [Cooling](../aind_data_schema_models/devices.md#cooling) | Cooling  |
| `frame_rate` | `Optional[decimal.Decimal]` | Frame rate (Hz) (Frame rate being used) |
| `frame_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] | Frame rate unit  |
| `immersion` | Optional[[ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium)] | Immersion  |
| `chroma` | Optional[[CameraChroma](../aind_data_schema_models/devices.md#camerachroma)] | Camera chroma  |
| `sensor_width` | `Optional[int]` | Width of the sensor (pixels)  |
| `sensor_height` | `Optional[int]` | Height of the sensor (pixels)  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `sensor_format` | `Optional[str]` | Sensor format  |
| `sensor_format_unit` | `Optional[str]` | Sensor format unit  |
| `bit_depth` | `Optional[int]` | Bit depth  |
| `bin_mode` | [BinMode](../aind_data_schema_models/devices.md#binmode) | Detector binning mode  |
| `bin_width` | `Optional[int]` | Bin width  |
| `bin_height` | `Optional[int]` | Bin height  |
| `bin_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Bin size unit  |
| `gain` | `Optional[decimal.Decimal]` | Gain  |
| `crop_offset_x` | `Optional[int]` | Crop offset x  |
| `crop_offset_y` | `Optional[int]` | Crop offset y  |
| `crop_width` | `Optional[int]` | Crop width  |
| `crop_height` | `Optional[int]` | Crop width  |
| `crop_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Crop size unit  |
| `recording_software` | Optional[[Software](identifiers.md#software)] | Recording software  |
| `driver` | Optional[[DeviceDriver](../aind_data_schema_models/devices.md#devicedriver)] | Driver  |
| `driver_version` | `Optional[str]` | Driver version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### CameraAssembly

Named assembly of a camera and lens (and optionally a filter)

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Camera assembly name  |
| `target` | [CameraTarget](../aind_data_schema_models/devices.md#cameratarget) | Camera target  |
| `camera` | [Camera](#camera) | Camera  |
| `lens` | [Lens](#lens) | Lens  |
| `filter` | Optional[[Filter](#filter)] | Filter  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to instrument transform (Position and orientation of the device in the instrument coordinate system) |


### Catheter

Description of a catheter device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `catheter_material` | [CatheterMaterial](#cathetermaterial) | Catheter material  |
| `catheter_design` | [CatheterDesign](#catheterdesign) | Catheter design  |
| `catheter_port` | [CatheterPort](#catheterport) | Catheter port  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### CatheterDesign

Type of catheter design

| Name | Value |
|------|-------|
| `MAGNETIC` | `Magnetic` |
| `NONMAGNETIC` | `Non-magnetic` |
| `NA` | `N/A` |


### CatheterMaterial

Type of catheter material

| Name | Value |
|------|-------|
| `NAKED` | `Naked` |
| `SILICONE` | `VAB silicone` |
| `MESH` | `VAB mesh` |


### CatheterPort

Type of catheter port

| Name | Value |
|------|-------|
| `SINGLE` | `Single` |
| `DOUBLE` | `Double` |


### Computer

Description of a computer

| Field | Type | Title (Description) |
|-------|------|-------------|
| `operating_system` | `Optional[str]` | Operating system  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### DAQChannel

Named input or output channel on a DAQ device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_name` | `str` | DAQ channel name  |
| `channel_type` | [DaqChannelType](../aind_data_schema_models/devices.md#daqchanneltype) | DAQ channel type  |
| `port` | `Optional[int]` | DAQ port  |
| <del>`channel_index`</del> | `Optional[int]` | **[DEPRECATED]** Use DAQChannel.port instead. DAQ channel index  |
| `sample_rate` | `Optional[decimal.Decimal]` | DAQ channel sample rate (Hz)  |
| `sample_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] | Sample rate unit  |
| `event_based_sampling` | `Optional[bool]` | Set to true if DAQ channel is sampled at irregular intervals  |


### DAQDevice

Data acquisition device containing multiple I/O channels

| Field | Type | Title (Description) |
|-------|------|-------------|
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) | Type of connection to PC  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `channels` | List[[DAQChannel](#daqchannel)] | DAQ channels  |
| `firmware_version` | `Optional[str]` | Firmware version  |
| `hardware_version` | `Optional[str]` | Hardware version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Detector

Description of a generic detector

| Field | Type | Title (Description) |
|-------|------|-------------|
| `detector_type` | [DetectorType](../aind_data_schema_models/devices.md#detectortype) | Detector Type  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) | Data interface  |
| `cooling` | [Cooling](../aind_data_schema_models/devices.md#cooling) | Cooling  |
| `frame_rate` | `Optional[decimal.Decimal]` | Frame rate (Hz) (Frame rate being used) |
| `frame_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] | Frame rate unit  |
| `immersion` | Optional[[ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium)] | Immersion  |
| `chroma` | Optional[[CameraChroma](../aind_data_schema_models/devices.md#camerachroma)] | Camera chroma  |
| `sensor_width` | `Optional[int]` | Width of the sensor (pixels)  |
| `sensor_height` | `Optional[int]` | Height of the sensor (pixels)  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `sensor_format` | `Optional[str]` | Sensor format  |
| `sensor_format_unit` | `Optional[str]` | Sensor format unit  |
| `bit_depth` | `Optional[int]` | Bit depth  |
| `bin_mode` | [BinMode](../aind_data_schema_models/devices.md#binmode) | Detector binning mode  |
| `bin_width` | `Optional[int]` | Bin width  |
| `bin_height` | `Optional[int]` | Bin height  |
| `bin_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Bin size unit  |
| `gain` | `Optional[decimal.Decimal]` | Gain  |
| `crop_offset_x` | `Optional[int]` | Crop offset x  |
| `crop_offset_y` | `Optional[int]` | Crop offset y  |
| `crop_width` | `Optional[int]` | Crop width  |
| `crop_height` | `Optional[int]` | Crop width  |
| `crop_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Crop size unit  |
| `recording_software` | Optional[[Software](identifiers.md#software)] | Recording software  |
| `driver` | Optional[[DeviceDriver](../aind_data_schema_models/devices.md#devicedriver)] | Driver  |
| `driver_version` | `Optional[str]` | Driver version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Device

Generic device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### DevicePosition

Position class for devices

| Field | Type | Title (Description) |
|-------|------|-------------|
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to instrument transform (Position and orientation of the device in the instrument coordinate system) |


### DigitalMicromirrorDevice

Description of a Digital Micromirror Device (DMD)

| Field | Type | Title (Description) |
|-------|------|-------------|
| `max_dmd_patterns` | `int` | Max DMD patterns  |
| `double_bounce_design` | `bool` | Double bounce design  |
| `invert_pixel_values` | `bool` | Invert pixel values  |
| `motion_padding_x` | `int` | Motion padding X (pixels)  |
| `motion_padding_y` | `int` | Motion padding Y (pixels)  |
| `padding_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Padding unit  |
| `pixel_size` | `decimal.Decimal` | DMD Pixel size  |
| `pixel_size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Pixel size unit  |
| `start_phase` | `decimal.Decimal` | DMD Start phase (fraction of cycle)  |
| `dmd_flip` | `bool` | DMD Flip  |
| `dmd_curtain` | `List[decimal.Decimal]` | DMD Curtain  |
| `dmd_curtain_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | dmd_curtain_unit  |
| `line_shear` | `List[int]` | Line shear (pixels)  |
| `line_shear_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Line shear unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Disc

Description of a running disc (i.e. MindScope Disc)

| Field | Type | Title (Description) |
|-------|------|-------------|
| `radius` | `decimal.Decimal` | Radius (cm)  |
| `radius_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | radius unit  |
| `output` | Optional[[DaqChannelType](../aind_data_schema_models/devices.md#daqchanneltype)] |  (analog or digital electronics) |
| `encoder` | `Optional[str]` | Encoder (Encoder hardware type) |
| `decoder` | `Optional[str]` | Decoder (Decoder chip type) |
| `encoder_firmware` | Optional[[Software](identifiers.md#software)] | Encoder firmware (Firmware to read from decoder chip counts) |
| `surface_material` | `Optional[str]` | Surface material  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Enclosure

Description of an enclosure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `size` | [Scale](coordinates.md#scale) | Size  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `internal_material` | `Optional[str]` | Internal material  |
| `external_material` | `str` | External material  |
| `grounded` | `bool` | Grounded  |
| `laser_interlock` | `bool` | Laser interlock  |
| `air_filtration` | `bool` | Air filtration  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### EphysAssembly

Named assembly for combining a manipulator and extracellular ephys probes

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Ephys assembly name  |
| `manipulator` | [Manipulator](#manipulator) | Manipulator  |
| `probes` | List[[EphysProbe](#ephysprobe)] | Probes that are held by this module  |


### EphysProbe

Probe used in an extracellular ephys experiment

| Field | Type | Title (Description) |
|-------|------|-------------|
| `probe_model` | [ProbeModel](../aind_data_schema_models/devices.md#probemodel) | Probe model  |
| `headstage` | Optional[[Device](#device)] | Headstage for this probe  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### FiberAssembly

Module for inserted fiber photometry recording

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Fiber assembly name  |
| `manipulator` | [Manipulator](#manipulator) | Manipulator  |
| `fibers` | List[[FiberProbe](#fiberprobe)] | Probes that are held by this module  |


### FiberPatchCord

Description of a patch cord

| Field | Type | Title (Description) |
|-------|------|-------------|
| `core_diameter` | `decimal.Decimal` | Core diameter (um)  |
| `numerical_aperture` | `decimal.Decimal` | Numerical aperture  |
| `photobleaching_date` | `Optional[datetime.date]` | Photobleaching date  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### FiberProbe

Description of a fiber optic probe

| Field | Type | Title (Description) |
|-------|------|-------------|
| `core_diameter` | `decimal.Decimal` | Core diameter (um)  |
| `core_diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Core diameter unit  |
| `numerical_aperture` | `decimal.Decimal` | Numerical aperture  |
| `ferrule_material` | Optional[[FerruleMaterial](../aind_data_schema_models/devices.md#ferrulematerial)] | Ferrule material  |
| `active_length` | `Optional[decimal.Decimal]` | Active length (mm) (Length of taper) |
| `total_length` | `decimal.Decimal` | Total length (mm)  |
| `length_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Length unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Filter

Filter used in a light path

| Field | Type | Title (Description) |
|-------|------|-------------|
| `filter_type` | [FilterType](../aind_data_schema_models/devices.md#filtertype) | Type of filter  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `cut_off_wavelength` | `Optional[int]` | Cut-off wavelength (nm)  |
| `cut_on_wavelength` | `Optional[int]` | Cut-on wavelength (nm)  |
| `center_wavelength` | `int or List[int] or NoneType` | Center wavelength (nm) (Single wavelength or list of wavelengths for MULTIBAND or MULTI_NOTCH filters) |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Wavelength unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### HarpDevice

DAQ that uses the Harp protocol for synchronization and data transmission

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `harp_device_type` | [HarpDeviceType](../aind_data_schema_models/harp_types.md#harpdevicetype) | Type of Harp device  |
| `core_version` | `Optional[str]` | Core version  |
| `tag_version` | `Optional[str]` | Tag version  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) | Data interface  |
| `is_clock_generator` | `bool` | Is Clock Generator  |
| `channels` | List[[DAQChannel](#daqchannel)] | DAQ channels  |
| `firmware_version` | `Optional[str]` | Firmware version  |
| `hardware_version` | `Optional[str]` | Hardware version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Lamp

Description of a Lamp lightsource

| Field | Type | Title (Description) |
|-------|------|-------------|
| `wavelength_min` | `Optional[int]` | Wavelength minimum (nm)  |
| `wavelength_max` | `Optional[int]` | Wavelength maximum (nm)  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Wavelength unit  |
| `temperature` | `Optional[int]` | Temperature (K)  |
| `temperature_unit` | Optional[[TemperatureUnit](../aind_data_schema_models/units.md#temperatureunit)] | Temperature unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Laser

Laser module with a specific wavelength (may be a sub-component of a larger assembly)

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `wavelength` | `int` | Wavelength (nm)  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Wavelength unit  |
| `coupling` | Optional[[Coupling](../aind_data_schema_models/devices.md#coupling)] | Coupling  |
| `coupling_efficiency` | `Optional[decimal.Decimal]` | Coupling efficiency (percent)  |
| `coupling_efficiency_unit` | `"percent"` | Coupling efficiency unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### LaserAssembly

Named assembly combining a manipulator, lasers, collimator, and fibers

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Laser assembly name  |
| `manipulator` | [Manipulator](#manipulator) | Manipulator  |
| `lasers` | List[[Laser](#laser)] | Lasers connected to this module  |
| `collimator` | [Device](#device) | Collimator  |
| `fiber` | [FiberPatchCord](#fiberpatchcord) | Fiber patch  |


### Lens

Lens

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### LickSpout

Description of a lick spout

| Field | Type | Title (Description) |
|-------|------|-------------|
| `spout_diameter` | `decimal.Decimal` | Spout diameter (mm)  |
| `spout_diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Spout diameter unit  |
| `solenoid_valve` | [Device](#device) | Solenoid valve  |
| `lick_sensor` | [Device](#device) or [HarpDevice](#harpdevice) | Lick sensor  |
| `lick_sensor_type` | Optional[[LickSensorType](../aind_data_schema_models/devices.md#licksensortype)] | Lick sensor type  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### LickSpoutAssembly

Description of multiple lick spouts, possibly mounted on a stage

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Lick spout assembly name  |
| `lick_spouts` | List[[LickSpout](#lickspout)] | Water spouts  |
| `motorized_stage` | Optional[[MotorizedStage](#motorizedstage)] | Motorized stage  |


### LightAssembly

Named assembly of a light source and lens

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Light assembly name  |
| `light` | [Laser](#laser) or [LightEmittingDiode](#lightemittingdiode) or [Lamp](#lamp) |   |
| `lens` | [Lens](#lens) | Lens  |
| `filter` | Optional[[Filter](#filter)] | Filter  |


### LightEmittingDiode

Description of a Light Emitting Diode (LED) device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `wavelength` | `int` | Wavelength (nm)  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Wavelength unit  |
| `bandwidth` | `Optional[int]` | Bandwidth (FWHM)  |
| `bandwidth_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] | Bandwidth unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Manipulator

Manipulator used on a dome module

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Microscope

Description of a microscope

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Monitor

Description of visual display for visual stimuli

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `refresh_rate` | `int` | Refresh rate (Hz)  |
| `width` | `int` | Width (pixels)  |
| `height` | `int` | Height (pixels)  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `viewing_distance` | `decimal.Decimal` | Viewing distance (cm)  |
| `viewing_distance_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Viewing distance unit  |
| `contrast` | `Optional[int]` | Contrast (Monitor's contrast setting) |
| `contrast_unit` | Optional[[UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit)] | Contrast unit  |
| `brightness` | `Optional[int]` | Brightness (Monitor's brightness setting) |
| `brightness_unit` | Optional[[UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit)] | Brightness unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to instrument transform (Position and orientation of the device in the instrument coordinate system) |


### MotorizedStage

Description of motorized stage

| Field | Type | Title (Description) |
|-------|------|-------------|
| `travel` | `decimal.Decimal` | Travel of device (mm)  |
| `travel_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Travel unit  |
| `firmware` | Optional[[Software](identifiers.md#software)] | Firmware  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### MyomatrixArray

Description of a Myomatrix array

| Field | Type | Title (Description) |
|-------|------|-------------|
| `array_type` | [MyomatrixArrayType](../aind_data_schema_models/devices.md#myomatrixarraytype) | Array type  |
| `threads` | List[[MyomatrixThread](#myomatrixthread)] | Array threads  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### MyomatrixContact

Description of a contact on a myomatrix thread

| Field | Type | Title (Description) |
|-------|------|-------------|
| `body_part` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Body part of contact insertion (Use MouseBodyParts) |
| `relative_position` | [AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative) | Relative position (Position relative to procedures coordinate system) |
| `muscle` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Muscle of contact insertion (Use MouseEmgMuscles) |
| `in_muscle` | `bool` | In muscle  |


### MyomatrixThread

Description of a thread of a myomatrix array

| Field | Type | Title (Description) |
|-------|------|-------------|
| `ground_electrode_location` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Location of ground electrode (Use GroundWireLocations) |
| `contacts` | List[[MyomatrixContact](#myomatrixcontact)] | Contacts  |


### NeuropixelsBasestation

PXI-based Neuropixels DAQ

| Field | Type | Title (Description) |
|-------|------|-------------|
| `basestation_firmware_version` | `str` | Basestation firmware version  |
| `bsc_firmware_version` | `str` | Basestation connect board firmware  |
| `slot` | `int` | Slot number for this basestation  |
| `ports` | List[[ProbePort](#probeport)] | Basestation ports  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |   |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `channels` | List[[DAQChannel](#daqchannel)] | DAQ channels  |
| `firmware_version` | `Optional[str]` | Firmware version  |
| `hardware_version` | `Optional[str]` | Hardware version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Objective

Description of an objective device

| Field | Type | Title (Description) |
|-------|------|-------------|
| `numerical_aperture` | `decimal.Decimal` | Numerical aperture (in air)  |
| `magnification` | `decimal.Decimal` | Magnification  |
| `immersion` | [ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium) | Immersion  |
| `objective_type` | Optional[[ObjectiveType](../aind_data_schema_models/devices.md#objectivetype)] | Objective type  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Olfactometer

Description of an olfactometer for odor stimuli

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `harp_device_type` | [HarpDeviceType](../aind_data_schema_models/harp_types.md#harpdevicetype) | Type of Harp device  |
| `channels` | List[[OlfactometerChannel](#olfactometerchannel)] |   |
| `core_version` | `Optional[str]` | Core version  |
| `tag_version` | `Optional[str]` | Tag version  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) | Data interface  |
| `is_clock_generator` | `bool` | Is Clock Generator  |
| `firmware_version` | `Optional[str]` | Firmware version  |
| `hardware_version` | `Optional[str]` | Hardware version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### OlfactometerChannel

description of a Olfactometer channel

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_index` | `int` | Channel index  |
| `channel_type` | [OlfactometerChannelType](#olfactometerchanneltype) | Channel type  |
| `flow_capacity` | `100 or 1000` | Flow capacity  |
| `flow_unit` | `str` | Flow unit  |


### OlfactometerChannelType

Olfactometer channel types

| Name | Value |
|------|-------|
| `ODOR` | `Odor` |
| `CARRIER` | `Carrier` |


### OpenEphysAcquisitionBoard

Multichannel electrophysiology DAQ

| Field | Type | Title (Description) |
|-------|------|-------------|
| `ports` | List[[ProbePort](#probeport)] | Acquisition board ports  |
| `data_interface` | `"USB"` |   |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `channels` | List[[DAQChannel](#daqchannel)] | DAQ channels  |
| `firmware_version` | `Optional[str]` | Firmware version  |
| `hardware_version` | `Optional[str]` | Hardware version  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### PatchClampEphysAssembly

Assembly combining a manipulator and headstage used for Patch clamp ephys

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Patch clamp Assembly Name  |
| `manipulator` | [Manipulator](#manipulator) | Manipulator  |
| `headstage` | [Device](#device) | Headstage  |


### PockelsCell

Description of a Pockels Cell

| Field | Type | Title (Description) |
|-------|------|-------------|
| `polygonal_scanner` | `Optional[str]` | Polygonal scanner (Must match name of Polygonal scanner) |
| `on_time` | `Optional[decimal.Decimal]` | On time (fraction of cycle)  |
| `off_time` | `Optional[decimal.Decimal]` | Off time (fraction of cycle)  |
| `time_setting_unit` | [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) | Time setting unit  |
| `beam_modulation` | `Optional[decimal.Decimal]` | Beam modulation (V)  |
| `beam_modulation_unit` | Optional[[VoltageUnit](../aind_data_schema_models/units.md#voltageunit)] | Beam modulation unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### PolygonalScanner

Description of a Polygonal scanner

| Field | Type | Title (Description) |
|-------|------|-------------|
| `speed` | `int` | Speed (rpm)  |
| `speed_unit` | [SpeedUnit](../aind_data_schema_models/units.md#speedunit) | Speed unit  |
| `number_faces` | `int` | Number of faces  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### ProbePort

Port for a probe connection

| Field | Type | Title (Description) |
|-------|------|-------------|
| `index` | `int` | One-based port index  |
| `probes` | `List[str]` | Names of probes connected to this port  |


### Scanner

Description of a MRI Scanner

| Field | Type | Title (Description) |
|-------|------|-------------|
| `magnetic_strength` | `float` | Magnetic strength (T)  |
| `magnetic_strength_unit` | [MagneticFieldUnit](../aind_data_schema_models/units.md#magneticfieldunit) | Magnetic strength unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### ScanningStage

Description of a scanning motorized stages

| Field | Type | Title (Description) |
|-------|------|-------------|
| `stage_axis_direction` | [StageAxisDirection](../aind_data_schema_models/devices.md#stageaxisdirection) | Direction of stage axis  |
| `stage_axis_name` | [AxisName](../aind_data_schema_models/coordinates.md#axisname) | Name of stage axis  |
| `travel` | `decimal.Decimal` | Travel of device (mm)  |
| `travel_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Travel unit  |
| `firmware` | Optional[[Software](identifiers.md#software)] | Firmware  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Speaker

Description of a speaker for auditory stimuli

| Field | Type | Title (Description) |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |   |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] | Relative position  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Device coordinate system  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Device to instrument transform (Position and orientation of the device in the instrument coordinate system) |


### Treadmill

Description of treadmill platform

| Field | Type | Title (Description) |
|-------|------|-------------|
| `treadmill_width` | `decimal.Decimal` | Width of treadmill (mm)  |
| `width_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Width unit  |
| `encoder` | Optional[[Device](#device)] | Encoder  |
| `pulse_per_revolution` | `Optional[int]` | Pulse per revolution  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Tube

Description of a tube platform

| Field | Type | Title (Description) |
|-------|------|-------------|
| `diameter` | `decimal.Decimal` | Diameter  |
| `diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Diameter unit  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


### Wheel

Description of a running wheel

| Field | Type | Title (Description) |
|-------|------|-------------|
| `radius` | `decimal.Decimal` | Radius (mm)  |
| `width` | `decimal.Decimal` | Width (mm)  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `encoder` | [Device](#device) | Encoder  |
| `pulse_per_revolution` | `int` | Pulse per revolution  |
| `magnetic_brake` | [Device](#device) | Magnetic brake  |
| `torque_sensor` | [Device](#device) | Torque sensor  |
| `name` | `str` | Device name  |
| `serial_number` | `Optional[str]` | Serial number  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] | Manufacturer  |
| `model` | `Optional[str]` | Model  |
| `additional_settings` | `Optional[dict]` | Additional parameters  |
| `notes` | `Optional[str]` | Notes  |


