# Stimulus

## Model definitions

### FilterType

Types of bandpass filters for auditory stim

| Name | Value |
|------|-------|
| `BUTTERWORTH` | `Butterworth` |
| `OTHER` | `Other` |


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
| `other_parameters` | `dict` |  |
| `notes` | `Optional[str]` |  |


### PulseShape

Types of Opto stim pulse shapes

| Name | Value |
|------|-------|
| `SQUARE` | `Square` |
| `RAMP` | `Ramp` |
| `SINE` | `Sinusoidal` |


