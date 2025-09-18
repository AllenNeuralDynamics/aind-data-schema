# Devices

## Model definitions

### AdditionalImagingDevice

Description of additional devices

| Field | Type | Description |
|-------|------|-------------|
| `imaging_device_type` | [ImagingDeviceType](../aind_data_schema_models/devices.md#imagingdevicetype) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### AirPuffDevice

Description of an air puff device

| Field | Type | Description |
|-------|------|-------------|
| `diameter` | `float` |  |
| `diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Arena

Description of a rectangular arena

| Field | Type | Description |
|-------|------|-------------|
| `size` | [Scale](coordinates.md#scale) |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `objects_in_arena` | List[[Device](#device)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Camera

Camera Detector

| Field | Type | Description |
|-------|------|-------------|
| `detector_type` | [DetectorType](../aind_data_schema_models/devices.md#detectortype) |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |  |
| `cooling` | [Cooling](../aind_data_schema_models/devices.md#cooling) |  |
| `frame_rate` | `Optional[decimal.Decimal]` | Frame rate being used |
| `frame_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] |  |
| `immersion` | Optional[[ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium)] |  |
| `chroma` | Optional[[CameraChroma](../aind_data_schema_models/devices.md#camerachroma)] |  |
| `sensor_width` | `Optional[int]` |  |
| `sensor_height` | `Optional[int]` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `sensor_format` | `Optional[str]` |  |
| `sensor_format_unit` | `Optional[str]` |  |
| `bit_depth` | `Optional[int]` |  |
| `bin_mode` | [BinMode](../aind_data_schema_models/devices.md#binmode) |  |
| `bin_width` | `Optional[int]` |  |
| `bin_height` | `Optional[int]` |  |
| `bin_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `gain` | `Optional[decimal.Decimal]` |  |
| `crop_offset_x` | `Optional[int]` |  |
| `crop_offset_y` | `Optional[int]` |  |
| `crop_width` | `Optional[int]` |  |
| `crop_height` | `Optional[int]` |  |
| `crop_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `recording_software` | Optional[[Software](identifiers.md#software)] |  |
| `driver` | Optional[[DeviceDriver](../aind_data_schema_models/devices.md#devicedriver)] |  |
| `driver_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### CameraAssembly

Named assembly of a camera and lens (and optionally a filter)

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `target` | [CameraTarget](../aind_data_schema_models/devices.md#cameratarget) |  |
| `camera` | [Camera](#camera) |  |
| `lens` | [Lens](#lens) |  |
| `filter` | Optional[[Filter](#filter)] |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Position and orientation of the device in the instrument coordinate system |


### Catheter

Description of a catheter device

| Field | Type | Description |
|-------|------|-------------|
| `catheter_material` | [CatheterMaterial](#cathetermaterial) |  |
| `catheter_design` | [CatheterDesign](#catheterdesign) |  |
| `catheter_port` | [CatheterPort](#catheterport) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


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

| Field | Type | Description |
|-------|------|-------------|
| `operating_system` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### DAQChannel

Named input or output channel on a DAQ device

| Field | Type | Description |
|-------|------|-------------|
| `channel_name` | `str` |  |
| `channel_type` | [DaqChannelType](../aind_data_schema_models/devices.md#daqchanneltype) |  |
| `port` | `Optional[int]` |  |
| <del>`channel_index`</del> | `Optional[int]` | **[DEPRECATED]** Use DAQChannel.port instead. |
| `sample_rate` | `Optional[decimal.Decimal]` |  |
| `sample_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] |  |
| `event_based_sampling` | `Optional[bool]` |  |


### DAQDevice

Data acquisition device containing multiple I/O channels

| Field | Type | Description |
|-------|------|-------------|
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Detector

Description of a generic detector

| Field | Type | Description |
|-------|------|-------------|
| `detector_type` | [DetectorType](../aind_data_schema_models/devices.md#detectortype) |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |  |
| `cooling` | [Cooling](../aind_data_schema_models/devices.md#cooling) |  |
| `frame_rate` | `Optional[decimal.Decimal]` | Frame rate being used |
| `frame_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] |  |
| `immersion` | Optional[[ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium)] |  |
| `chroma` | Optional[[CameraChroma](../aind_data_schema_models/devices.md#camerachroma)] |  |
| `sensor_width` | `Optional[int]` |  |
| `sensor_height` | `Optional[int]` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `sensor_format` | `Optional[str]` |  |
| `sensor_format_unit` | `Optional[str]` |  |
| `bit_depth` | `Optional[int]` |  |
| `bin_mode` | [BinMode](../aind_data_schema_models/devices.md#binmode) |  |
| `bin_width` | `Optional[int]` |  |
| `bin_height` | `Optional[int]` |  |
| `bin_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `gain` | `Optional[decimal.Decimal]` |  |
| `crop_offset_x` | `Optional[int]` |  |
| `crop_offset_y` | `Optional[int]` |  |
| `crop_width` | `Optional[int]` |  |
| `crop_height` | `Optional[int]` |  |
| `crop_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `recording_software` | Optional[[Software](identifiers.md#software)] |  |
| `driver` | Optional[[DeviceDriver](../aind_data_schema_models/devices.md#devicedriver)] |  |
| `driver_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Device

Generic device

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### DevicePosition

Position class for devices

| Field | Type | Description |
|-------|------|-------------|
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Position and orientation of the device in the instrument coordinate system |


### DigitalMicromirrorDevice

Description of a Digital Micromirror Device (DMD)

| Field | Type | Description |
|-------|------|-------------|
| `max_dmd_patterns` | `int` |  |
| `double_bounce_design` | `bool` |  |
| `invert_pixel_values` | `bool` |  |
| `motion_padding_x` | `int` |  |
| `motion_padding_y` | `int` |  |
| `padding_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `pixel_size` | `decimal.Decimal` |  |
| `pixel_size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `start_phase` | `decimal.Decimal` |  |
| `dmd_flip` | `bool` |  |
| `dmd_curtain` | `List[decimal.Decimal]` |  |
| `dmd_curtain_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `line_shear` | `List[int]` |  |
| `line_shear_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Disc

Description of a running disc (i.e. MindScope Disc)

| Field | Type | Description |
|-------|------|-------------|
| `radius` | `decimal.Decimal` |  |
| `radius_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `output` | Optional[[DaqChannelType](../aind_data_schema_models/devices.md#daqchanneltype)] | analog or digital electronics |
| `encoder` | `Optional[str]` | Encoder hardware type |
| `decoder` | `Optional[str]` | Decoder chip type |
| `encoder_firmware` | Optional[[Software](identifiers.md#software)] | Firmware to read from decoder chip counts |
| `surface_material` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Enclosure

Description of an enclosure

| Field | Type | Description |
|-------|------|-------------|
| `size` | [Scale](coordinates.md#scale) |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `internal_material` | `Optional[str]` |  |
| `external_material` | `str` |  |
| `grounded` | `bool` |  |
| `laser_interlock` | `bool` |  |
| `air_filtration` | `bool` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### EphysAssembly

Named assembly for combining a manipulator and ephys probes

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `manipulator` | [Manipulator](#manipulator) |  |
| `probes` | List[[EphysProbe](#ephysprobe)] |  |


### EphysProbe

Probe used in an ephys experiment

| Field | Type | Description |
|-------|------|-------------|
| `probe_model` | [ProbeModel](../aind_data_schema_models/devices.md#probemodel) |  |
| `headstage` | Optional[[Device](#device)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### FiberAssembly

Module for inserted fiber photometry recording

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `manipulator` | [Manipulator](#manipulator) |  |
| `fibers` | List[[FiberProbe](#fiberprobe)] |  |


### FiberPatchCord

Description of a patch cord

| Field | Type | Description |
|-------|------|-------------|
| `core_diameter` | `decimal.Decimal` |  |
| `numerical_aperture` | `decimal.Decimal` |  |
| `photobleaching_date` | `Optional[datetime.date]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### FiberProbe

Description of a fiber optic probe

| Field | Type | Description |
|-------|------|-------------|
| `core_diameter` | `decimal.Decimal` |  |
| `core_diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `numerical_aperture` | `decimal.Decimal` |  |
| `ferrule_material` | Optional[[FerruleMaterial](../aind_data_schema_models/devices.md#ferrulematerial)] |  |
| `active_length` | `Optional[decimal.Decimal]` | Length of taper |
| `total_length` | `decimal.Decimal` |  |
| `length_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Filter

Filter used in a light path

| Field | Type | Description |
|-------|------|-------------|
| `filter_type` | [FilterType](../aind_data_schema_models/devices.md#filtertype) |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `cut_off_wavelength` | `Optional[int]` |  |
| `cut_on_wavelength` | `Optional[int]` |  |
| `center_wavelength` | `int or List[int] or NoneType` | Single wavelength or list of wavelengths for MULTIBAND or MULTI_NOTCH filters |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### HarpDevice

DAQ that uses the Harp protocol for synchronization and data transmission

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `harp_device_type` | [HarpDeviceType](../aind_data_schema_models/harp_types.md#harpdevicetype) |  |
| `core_version` | `Optional[str]` |  |
| `tag_version` | `Optional[str]` |  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |  |
| `is_clock_generator` | `bool` |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Lamp

Description of a Lamp lightsource

| Field | Type | Description |
|-------|------|-------------|
| `wavelength_min` | `Optional[int]` |  |
| `wavelength_max` | `Optional[int]` |  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `temperature` | `Optional[int]` |  |
| `temperature_unit` | Optional[[TemperatureUnit](../aind_data_schema_models/units.md#temperatureunit)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Laser

Laser module with a specific wavelength (may be a sub-component of a larger assembly)

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `wavelength` | `int` |  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `coupling` | Optional[[Coupling](../aind_data_schema_models/devices.md#coupling)] |  |
| `coupling_efficiency` | `Optional[decimal.Decimal]` |  |
| `coupling_efficiency_unit` | `"percent"` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### LaserAssembly

Named assembly combining a manipulator, lasers, collimator, and fibers

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `manipulator` | [Manipulator](#manipulator) |  |
| `lasers` | List[[Laser](#laser)] |  |
| `collimator` | [Device](#device) |  |
| `fiber` | [FiberPatchCord](#fiberpatchcord) |  |


### Lens

Lens

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### LickSpout

Description of a lick spout

| Field | Type | Description |
|-------|------|-------------|
| `spout_diameter` | `decimal.Decimal` |  |
| `spout_diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `solenoid_valve` | [Device](#device) |  |
| `lick_sensor` | [Device](#device) |  |
| `lick_sensor_type` | Optional[[LickSensorType](../aind_data_schema_models/devices.md#licksensortype)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### LickSpoutAssembly

Description of multiple lick spouts, possibly mounted on a stage

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `lick_spouts` | List[[LickSpout](#lickspout)] |  |
| `motorized_stage` | Optional[[MotorizedStage](#motorizedstage)] |  |


### LightAssembly

Named assembly of a light source and lens

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `light` | [Laser](#laser) or [LightEmittingDiode](#lightemittingdiode) or [Lamp](#lamp) |  |
| `lens` | [Lens](#lens) |  |
| `filter` | Optional[[Filter](#filter)] |  |


### LightEmittingDiode

Description of a Light Emitting Diode (LED) device

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `wavelength` | `int` |  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `bandwidth` | `Optional[int]` |  |
| `bandwidth_unit` | Optional[[SizeUnit](../aind_data_schema_models/units.md#sizeunit)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Manipulator

Manipulator used on a dome module

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Microscope

Description of a microscope

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Monitor

Description of visual display for visual stimuli

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `refresh_rate` | `int` |  |
| `width` | `int` |  |
| `height` | `int` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `viewing_distance` | `decimal.Decimal` |  |
| `viewing_distance_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `contrast` | `Optional[int]` | Monitor's contrast setting |
| `brightness` | `Optional[int]` | Monitor's brightness setting |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Position and orientation of the device in the instrument coordinate system |


### MotorizedStage

Description of motorized stage

| Field | Type | Description |
|-------|------|-------------|
| `travel` | `decimal.Decimal` |  |
| `travel_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `firmware` | Optional[[Software](identifiers.md#software)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### MyomatrixArray

Description of a Myomatrix array

| Field | Type | Description |
|-------|------|-------------|
| `array_type` | [MyomatrixArrayType](../aind_data_schema_models/devices.md#myomatrixarraytype) |  |
| `threads` | List[[MyomatrixThread](#myomatrixthread)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### MyomatrixContact

Description of a contact on a myomatrix thread

| Field | Type | Description |
|-------|------|-------------|
| `body_part` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Use MouseBodyParts |
| `relative_position` | [AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative) | Position relative to procedures coordinate system |
| `muscle` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Use MouseEmgMuscles |
| `in_muscle` | `bool` |  |


### MyomatrixThread

Description of a thread of a myomatrix array

| Field | Type | Description |
|-------|------|-------------|
| `ground_electrode_location` | [MouseAnatomyModel](../aind_data_schema_models/external.md#mouseanatomymodel) | Use GroundWireLocations |
| `contacts` | List[[MyomatrixContact](#myomatrixcontact)] |  |


### NeuropixelsBasestation

PXI-based Neuropixels DAQ

| Field | Type | Description |
|-------|------|-------------|
| `basestation_firmware_version` | `str` |  |
| `bsc_firmware_version` | `str` |  |
| `slot` | `int` |  |
| `ports` | List[[ProbePort](#probeport)] |  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Objective

Description of an objective device

| Field | Type | Description |
|-------|------|-------------|
| `numerical_aperture` | `decimal.Decimal` |  |
| `magnification` | `decimal.Decimal` |  |
| `immersion` | [ImmersionMedium](../aind_data_schema_models/devices.md#immersionmedium) |  |
| `objective_type` | Optional[[ObjectiveType](../aind_data_schema_models/devices.md#objectivetype)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Olfactometer

Description of an olfactometer for odor stimuli

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `harp_device_type` | [HarpDeviceType](../aind_data_schema_models/harp_types.md#harpdevicetype) |  |
| `channels` | List[[OlfactometerChannel](#olfactometerchannel)] |  |
| `core_version` | `Optional[str]` |  |
| `tag_version` | `Optional[str]` |  |
| `data_interface` | [DataInterface](../aind_data_schema_models/devices.md#datainterface) |  |
| `is_clock_generator` | `bool` |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### OlfactometerChannel

description of a Olfactometer channel

| Field | Type | Description |
|-------|------|-------------|
| `channel_index` | `int` |  |
| `channel_type` | [OlfactometerChannelType](#olfactometerchanneltype) |  |
| `flow_capacity` | `100 or 1000` |  |
| `flow_unit` | `str` |  |


### OlfactometerChannelType

Olfactometer channel types

| Name | Value |
|------|-------|
| `ODOR` | `Odor` |
| `CARRIER` | `Carrier` |


### OpenEphysAcquisitionBoard

Multichannel electrophysiology DAQ

| Field | Type | Description |
|-------|------|-------------|
| `ports` | List[[ProbePort](#probeport)] |  |
| `data_interface` | `"DataInterface.USB"` |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### PockelsCell

Description of a Pockels Cell

| Field | Type | Description |
|-------|------|-------------|
| `polygonal_scanner` | `Optional[str]` | Must match name of Polygonal scanner |
| `on_time` | `Optional[decimal.Decimal]` |  |
| `off_time` | `Optional[decimal.Decimal]` |  |
| `time_setting_unit` | [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) |  |
| `beam_modulation` | `Optional[decimal.Decimal]` |  |
| `beam_modulation_unit` | Optional[[VoltageUnit](../aind_data_schema_models/units.md#voltageunit)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### PolygonalScanner

Description of a Polygonal scanner

| Field | Type | Description |
|-------|------|-------------|
| `speed` | `int` |  |
| `speed_unit` | [SpeedUnit](../aind_data_schema_models/units.md#speedunit) |  |
| `number_faces` | `int` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### ProbePort

Port for a probe connection

| Field | Type | Description |
|-------|------|-------------|
| `index` | `int` |  |
| `probes` | `List[str]` |  |


### Scanner

Description of a MRI Scanner

| Field | Type | Description |
|-------|------|-------------|
| `magnetic_strength` | `float` |  |
| `magnetic_strength_unit` | [MagneticFieldUnit](../aind_data_schema_models/units.md#magneticfieldunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### ScanningStage

Description of a scanning motorized stages

| Field | Type | Description |
|-------|------|-------------|
| `stage_axis_direction` | [StageAxisDirection](../aind_data_schema_models/devices.md#stageaxisdirection) |  |
| `stage_axis_name` | [AxisName](../aind_data_schema_models/coordinates.md#axisname) |  |
| `travel` | `decimal.Decimal` |  |
| `travel_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `firmware` | Optional[[Software](identifiers.md#software)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Speaker

Description of a speaker for auditory stimuli

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Position and orientation of the device in the instrument coordinate system |


### Treadmill

Description of treadmill platform

| Field | Type | Description |
|-------|------|-------------|
| `treadmill_width` | `decimal.Decimal` |  |
| `width_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `encoder` | Optional[[Device](#device)] |  |
| `pulse_per_revolution` | `Optional[int]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Tube

Description of a tube platform

| Field | Type | Description |
|-------|------|-------------|
| `diameter` | `decimal.Decimal` |  |
| `diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


### Wheel

Description of a running wheel

| Field | Type | Description |
|-------|------|-------------|
| `radius` | `decimal.Decimal` |  |
| `width` | `decimal.Decimal` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `encoder` | [Device](#device) |  |
| `pulse_per_revolution` | `int` |  |
| `magnetic_brake` | [Device](#device) |  |
| `torque_sensor` | [Device](#device) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[dict]` |  |
| `notes` | `Optional[str]` |  |


