# Stimulus

## Model definitions

### ConcentrationUnit

Concentraion units

| Name | Value |
|------|-------|
| `M` | `molar` |
| `UM` | `micromolar` |
| `NM` | `nanomolar` |
| `MASS_PERCENT` | `% m/m` |
| `VOLUME_PERCENT` | `% v/v` |


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



### FilterType

Types of bandpass filters for auditory stim

| Name | Value |
|------|-------|
| `BUTTERWORTH` | `Butterworth` |
| `OTHER` | `Other` |


### FrequencyUnit

Enumeration of Frequency Measurements

| Name | Value |
|------|-------|
| `KHZ` | `kilohertz` |
| `HZ` | `hertz` |
| `mHZ` | `millihertz` |


### OlfactometerChannelConfig

Description of olfactometer channel configurations

| Field | Type | Description |
|-------|------|-------------|
| `channel_index` | `int` |  |
| `odorant` | `str` |  |
| `odorant_dilution` | `decimal.Decimal` |  |
| `odorant_dilution_unit` | [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) |  |
| `notes` | `Optional[str]` |  |


### PhotoStimulationGroup

Description of a photostimulation group

| Field | Type | Description |
|-------|------|-------------|
| `group_index` | `int` |  |
| `number_of_neurons` | `int` |  |
| `stimulation_laser_power` | `decimal.Decimal` |  |
| `stimulation_laser_power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) |  |
| `number_trials` | `int` |  |
| `number_spirals` | `int` |  |
| `spiral_duration` | `decimal.Decimal` |  |
| `spiral_duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `inter_spiral_interval` | `decimal.Decimal` |  |
| `inter_spiral_interval_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `other_parameters` | `aind_data_schema.base.GenericModel` |  |
| `notes` | `Optional[str]` |  |


### PowerUnit

Unit for power, set or measured

| Name | Value |
|------|-------|
| `UW` | `microwatt` |
| `MW` | `milliwatt` |
| `PERCENT` | `percent` |


### PulseShape

Types of Opto stim pulse shapes

| Name | Value |
|------|-------|
| `SQUARE` | `Square` |
| `RAMP` | `Ramp` |
| `SINE` | `Sinusoidal` |


### TimeUnit

Enumeration of Time Measurements

| Name | Value |
|------|-------|
| `HR` | `hour` |
| `M` | `minute` |
| `S` | `second` |
| `MS` | `millisecond` |
| `US` | `microsecond` |
| `NS` | `nanosecond` |


