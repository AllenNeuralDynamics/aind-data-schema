# Devices

## Model definitions

### AdditionalImagingDevice

Description of additional devices

| Field | Type | Description |
|-------|------|-------------|
| `imaging_device_type` | {ImagingDeviceType} |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### AnatomicalRelative

Relative positions in 3D space

| Name | Value |
|------|-------|
| `SUPERIOR` | `Superior` |
| `INFERIOR` | `Inferior` |
| `ANTERIOR` | `Anterior` |
| `POSTERIOR` | `Posterior` |
| `LEFT` | `Left` |
| `RIGHT` | `Right` |
| `MEDIAL` | `Medial` |
| `LATERAL` | `Lateral` |
| `ORIGIN` | `Origin` |


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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### AxisName

Axis name

| Name | Value |
|------|-------|
| `X` | `X` |
| `Y` | `Y` |
| `Z` | `Z` |
| `AP` | `AP` |
| `ML` | `ML` |
| `SI` | `SI` |
| `DEPTH` | `Depth` |


### BinMode

Detector binning mode

| Name | Value |
|------|-------|
| `ADDITIVE` | `Additive` |
| `AVERAGE` | `Average` |
| `NONE` | `None` |


### Camera

Camera Detector

| Field | Type | Description |
|-------|------|-------------|
| `detector_type` | {DetectorType} |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `data_interface` | {DataInterface} |  |
| `cooling` | {Cooling} |  |
| `frame_rate` | `Optional[decimal.Decimal]` | Frame rate being used |
| `frame_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] |  |
| `immersion` | Optional[{ImmersionMedium}] |  |
| `chroma` | Optional[{CameraChroma}] |  |
| `sensor_width` | `Optional[int]` |  |
| `sensor_height` | `Optional[int]` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `sensor_format` | `Optional[str]` |  |
| `sensor_format_unit` | `Optional[str]` |  |
| `bit_depth` | `Optional[int]` |  |
| `bin_mode` | {BinMode} |  |
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
| `driver` | Optional[{DeviceDriver}] |  |
| `driver_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### CameraAssembly

Named assembly of a camera and lens (and optionally a filter)

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `target` | {CameraTarget} |  |
| `camera` | [Camera](#camera) |  |
| `lens` | [Lens](#lens) |  |
| `filter` | Optional[[Filter](#filter)] |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Position and orientation of the device in the instrument coordinate system |


### CameraChroma

Color vs. black & white

| Name | Value |
|------|-------|
| `COLOR` | `Color` |
| `BW` | `Monochrome` |


### CameraTarget

Target of camera

| Name | Value |
|------|-------|
| `BODY` | `Body` |
| `BRAIN` | `Brain` |
| `EYE` | `Eye` |
| `FACE` | `Face` |
| `TONGUE` | `Tongue` |
| `OTHER` | `Other` |


### Computer

Description of a computer

| Field | Type | Description |
|-------|------|-------------|
| `operating_system` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Cooling

Cooling medium name

| Name | Value |
|------|-------|
| `AIR` | `Air` |
| `WATER` | `Water` |
| `NONE` | `None` |


### Coupling

Laser coupling type

| Name | Value |
|------|-------|
| `FREE_SPACE` | `Free-space` |
| `MMF` | `Multi-mode fiber` |
| `SMF` | `Single-mode fiber` |
| `OTHER` | `Other` |


### DAQChannel

Named input or output channel on a DAQ device

| Field | Type | Description |
|-------|------|-------------|
| `channel_name` | `str` |  |
| `channel_type` | {DaqChannelType} |  |
| `port` | `Optional[int]` |  |
| `channel_index` | `Optional[int]` |  |
| `sample_rate` | `Optional[decimal.Decimal]` |  |
| `sample_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] |  |
| `event_based_sampling` | `Optional[bool]` |  |


### DAQDevice

Data acquisition device containing multiple I/O channels

| Field | Type | Description |
|-------|------|-------------|
| `data_interface` | {DataInterface} |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### DaqChannelType

DAQ Channel type

| Name | Value |
|------|-------|
| `AI` | `Analog Input` |
| `AO` | `Analog Output` |
| `DI` | `Digital Input` |
| `DO` | `Digital Output` |


### DataInterface

Connection between a device and a PC

| Name | Value |
|------|-------|
| `CAMERALINK` | `CameraLink` |
| `COAX` | `Coax` |
| `ETH` | `Ethernet` |
| `PCIE` | `PCIe` |
| `PXI` | `PXI` |
| `USB` | `USB` |
| `OTHER` | `Other` |


### Detector

Description of a generic detector

| Field | Type | Description |
|-------|------|-------------|
| `detector_type` | {DetectorType} |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `data_interface` | {DataInterface} |  |
| `cooling` | {Cooling} |  |
| `frame_rate` | `Optional[decimal.Decimal]` | Frame rate being used |
| `frame_rate_unit` | Optional[[FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit)] |  |
| `immersion` | Optional[{ImmersionMedium}] |  |
| `chroma` | Optional[{CameraChroma}] |  |
| `sensor_width` | `Optional[int]` |  |
| `sensor_height` | `Optional[int]` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `sensor_format` | `Optional[str]` |  |
| `sensor_format_unit` | `Optional[str]` |  |
| `bit_depth` | `Optional[int]` |  |
| `bin_mode` | {BinMode} |  |
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
| `driver` | Optional[{DeviceDriver}] |  |
| `driver_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### DetectorType

Detector type name

| Name | Value |
|------|-------|
| `CAMERA` | `Camera` |
| `PMT` | `Photomultiplier Tube` |
| `OTHER` | `Other` |


### Device

Generic device

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### DeviceDriver

DeviceDriver name

| Name | Value |
|------|-------|
| `OPENGL` | `OpenGL` |
| `VIMBA` | `Vimba` |
| `NVIDIA` | `Nvidia Graphics` |


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
| `line_shear_units` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Disc

Description of a running disc (i.e. MindScope Disc)

| Field | Type | Description |
|-------|------|-------------|
| `radius` | `decimal.Decimal` |  |
| `radius_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `output` | Optional[{DaqChannelType}] | analog or digital electronics |
| `encoder` | `Optional[str]` | Encoder hardware type |
| `decoder` | `Optional[str]` | Decoder chip type |
| `encoder_firmware` | Optional[[Software](identifiers.md#software)] | Firmware to read from decoder chip counts |
| `surface_material` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Enum

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.

| Name | Value |
|------|-------|



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
| `probe_model` | {ProbeModel} |  |
| `headstage` | Optional[[Device](#device)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### FerruleMaterial

Fiber probe ferrule material type name

| Name | Value |
|------|-------|
| `CERAMIC` | `Ceramic` |
| `STAINLESS_STEEL` | `Stainless steel` |


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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### FiberProbe

Description of a fiber optic probe

| Field | Type | Description |
|-------|------|-------------|
| `core_diameter` | `decimal.Decimal` |  |
| `core_diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `numerical_aperture` | `decimal.Decimal` |  |
| `ferrule_material` | Optional[{FerruleMaterial}] |  |
| `active_length` | `Optional[decimal.Decimal]` | Length of taper |
| `total_length` | `decimal.Decimal` |  |
| `length_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Filter

Filter used in a light path

| Field | Type | Description |
|-------|------|-------------|
| `filter_type` | [FilterType](stimulus.md#filtertype) |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `cut_off_wavelength` | `Optional[int]` |  |
| `cut_on_wavelength` | `Optional[int]` |  |
| `center_wavelength` | `Optional[int]` |  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### FilterType

Filter type

| Name | Value |
|------|-------|
| `BANDPASS` | `Band pass` |
| `DICHROIC` | `Dichroic` |
| `LONGPASS` | `Long pass` |
| `MULTIBAND` | `Multiband` |
| `ND` | `Neutral density` |
| `NOTCH` | `Notch` |
| `SHORTPASS` | `Short pass` |


### FrequencyUnit

Enumeration of Frequency Measurements

| Name | Value |
|------|-------|
| `KHZ` | `kilohertz` |
| `HZ` | `hertz` |
| `mHZ` | `millihertz` |


### HarpDevice

DAQ that uses the Harp protocol for synchronization and data transmission

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `harp_device_type` | [HarpDeviceType](../aind_data_schema_models/harp_types.md#harpdevicetype) |  |
| `core_version` | `Optional[str]` |  |
| `tag_version` | `Optional[str]` |  |
| `data_interface` | {DataInterface} |  |
| `is_clock_generator` | `bool` |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### ImagingDeviceType

Imaginge device type name

| Name | Value |
|------|-------|
| `BEAM_EXPANDER` | `Beam expander` |
| `SAMPLE_CHAMBER` | `Sample Chamber` |
| `DIFFUSER` | `Diffuser` |
| `GALVO` | `Galvo` |
| `LASER_COMBINER` | `Laser combiner` |
| `LASER_COUPLER` | `Laser coupler` |
| `PRISM` | `Prism` |
| `OBJECTIVE` | `Objective` |
| `ROTATION_MOUNT` | `Rotation mount` |
| `SLIT` | `Slit` |
| `TUNABLE_LENS` | `Tunable lens` |
| `OTHER` | `Other` |


### ImmersionMedium

Immersion medium name

| Name | Value |
|------|-------|
| `AIR` | `air` |
| `MULTI` | `multi` |
| `OIL` | `oil` |
| `PBS` | `PBS` |
| `WATER` | `water` |
| `OTHER` | `other` |
| `EASYINDEX` | `easy index` |
| `ECI` | `ethyl cinnimate` |
| `ACB` | `aqueous clearing buffer` |


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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Laser

Laser module with a specific wavelength (may be a sub-component of a larger assembly)

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `wavelength` | `int` |  |
| `wavelength_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) |  |
| `coupling` | Optional[{Coupling}] |  |
| `coupling_efficiency` | `Optional[decimal.Decimal]` |  |
| `coupling_efficiency_unit` | `"percent"` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### LickSensorType

Type of lick sensor

| Name | Value |
|------|-------|
| `CAPACITIVE` | `Capacitive` |
| `CONDUCTIVE` | `Conductive` |
| `PIEZOELECTIC` | `Piezoelectric` |


### LickSpout

Description of a lick spout

| Field | Type | Description |
|-------|------|-------------|
| `spout_diameter` | `decimal.Decimal` |  |
| `spout_diameter_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `solenoid_valve` | [Device](#device) |  |
| `lick_sensor` | [Device](#device) |  |
| `lick_sensor_type` | Optional[{LickSensorType}] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### MagneticFieldUnit

Magnetic field units

| Name | Value |
|------|-------|
| `T` | `tesla` |
| `MT` | `millitesla` |
| `UT` | `microtesla` |


### Manipulator

Manipulator used on a dome module

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Microscope

Description of a microscope

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### MyomatrixArray

Description of a Myomatrix array

| Field | Type | Description |
|-------|------|-------------|
| `array_type` | {MyomatrixArrayType} |  |
| `threads` | List[[MyomatrixThread](#myomatrixthread)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### MyomatrixArrayType

Type of Myomatrix array

| Name | Value |
|------|-------|
| `INJECTED` | `Injected` |
| `SUTURED` | `Sutured` |


### MyomatrixContact

Description of a contact on a myomatrix thread

| Field | Type | Description |
|-------|------|-------------|
| `body_part` | `aind_data_schema_models.mouse_anatomy.MouseAnatomyModel` | Use MouseBodyParts |
| `relative_position` | [AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative) | Position relative to procedures coordinate system |
| `muscle` | `aind_data_schema_models.mouse_anatomy.MouseAnatomyModel` | Use MouseEmgMuscles |
| `in_muscle` | `bool` |  |


### MyomatrixThread

Description of a thread of a myomatrix array

| Field | Type | Description |
|-------|------|-------------|
| `ground_electrode_location` | `aind_data_schema_models.mouse_anatomy.MouseAnatomyModel` | Use GroundWireLocations |
| `contacts` | List[[MyomatrixContact](#myomatrixcontact)] |  |


### NeuropixelsBasestation

PXI-based Neuropixels DAQ

| Field | Type | Description |
|-------|------|-------------|
| `basestation_firmware_version` | `str` |  |
| `bsc_firmware_version` | `str` |  |
| `slot` | `int` |  |
| `ports` | List[[ProbePort](#probeport)] |  |
| `data_interface` | {DataInterface} |  |
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `channels` | List[[DAQChannel](#daqchannel)] |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### Objective

Description of an objective device

| Field | Type | Description |
|-------|------|-------------|
| `numerical_aperture` | `decimal.Decimal` |  |
| `magnification` | `decimal.Decimal` |  |
| `immersion` | {ImmersionMedium} |  |
| `objective_type` | Optional[{ObjectiveType}] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### ObjectiveType

Objective type for Slap2

| Name | Value |
|------|-------|
| `REMOTE` | `Remote` |
| `PRIMARY` | `Primary` |


### Olfactometer

Description of an olfactometer for odor stimuli

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `harp_device_type` | [HarpDeviceType](../aind_data_schema_models/harp_types.md#harpdevicetype) |  |
| `channels` | List[[OlfactometerChannel](#olfactometerchannel)] |  |
| `core_version` | `Optional[str]` |  |
| `tag_version` | `Optional[str]` |  |
| `data_interface` | {DataInterface} |  |
| `is_clock_generator` | `bool` |  |
| `firmware_version` | `Optional[str]` |  |
| `hardware_version` | `Optional[str]` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### PolygonalScanner

Description of a Polygonal scanner

| Field | Type | Description |
|-------|------|-------------|
| `speed` | `int` |  |
| `speed_unit` | {SpeedUnit} |  |
| `number_faces` | `int` |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### PowerUnit

Unit for power, set or measured

| Name | Value |
|------|-------|
| `UW` | `microwatt` |
| `MW` | `milliwatt` |
| `PERCENT` | `percent` |


### ProbeModel

Probe model name

| Name | Value |
|------|-------|
| `MI_ULED_PROBE` | `Michigan uLED Probe (Version 1)` |
| `MP_PHOTONIC_V1` | `MPI Photonic Probe (Version 1)` |
| `NP_OPTO_DEMONSTRATOR` | `Neuropixels Opto (Demonstrator)` |
| `NP_UHD_FIXED` | `Neuropixels UHD (Fixed)` |
| `NP_UHD_SWITCHABLE` | `Neuropixels UHD (Switchable)` |
| `NP1` | `Neuropixels 1.0` |
| `NP2_SINGLE_SHANK` | `Neuropixels 2.0 (Single Shank)` |
| `NP2_MULTI_SHANK` | `Neuropixels 2.0 (Multi Shank)` |
| `NP2_QUAD_BASE` | `Neuropixels 2.0 (Quad Base)` |


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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### ScanningStage

Description of a scanning motorized stages

| Field | Type | Description |
|-------|------|-------------|
| `stage_axis_direction` | {StageAxisDirection} |  |
| `stage_axis_name` | [AxisName](../aind_data_schema_models/coordinates.md#axisname) |  |
| `travel` | `decimal.Decimal` |  |
| `travel_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `firmware` | Optional[[Software](identifiers.md#software)] |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `manufacturer` | Optional[[Organization](../aind_data_schema_models/organizations.md#organization)] |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### SizeUnit

Enumeration of Length Measurements

| Name | Value |
|------|-------|
| `M` | `meter` |
| `CM` | `centimeter` |
| `MM` | `millimeter` |
| `UM` | `micrometer` |
| `NM` | `nanometer` |
| `IN` | `inch` |
| `PX` | `pixel` |


### Speaker

Description of a speaker for auditory stimuli

| Field | Type | Description |
|-------|------|-------------|
| `manufacturer` | [Organization](../aind_data_schema_models/organizations.md#organization) |  |
| `name` | `str` |  |
| `serial_number` | `Optional[str]` |  |
| `model` | `Optional[str]` |  |
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |
| `relative_position` | List[[AnatomicalRelative](../aind_data_schema_models/coordinates.md#anatomicalrelative)] |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] |  |
| `transform` | Optional[List[[Translation](coordinates.md#translation) or [Rotation](coordinates.md#rotation) or [Scale](coordinates.md#scale) or [Affine](coordinates.md#affine)]] | Position and orientation of the device in the instrument coordinate system |


### SpeedUnit

Enumeration of Speed Measurements

| Name | Value |
|------|-------|
| `RPM` | `rotations per minute` |


### StageAxisDirection

Direction of motion for motorized stage

| Name | Value |
|------|-------|
| `DETECTION_AXIS` | `Detection axis` |
| `ILLUMINATION_AXIS` | `Illumination axis` |
| `PERPENDICULAR_AXIS` | `Perpendicular axis` |


### TemperatureUnit

Temperature units

| Name | Value |
|------|-------|
| `C` | `Celsius` |
| `K` | `Kelvin` |


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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


### UnitlessUnit

Unitless options

| Name | Value |
|------|-------|
| `PERCENT` | `percent` |
| `FC` | `fraction of cycle` |


### VoltageUnit

Voltage units

| Name | Value |
|------|-------|
| `V` | `Volts` |


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
| `additional_settings` | `Optional[aind_data_schema.base.GenericModel]` |  |
| `notes` | `Optional[str]` |  |


