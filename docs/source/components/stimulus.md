# Stimulus

## Model definitions

### AuditoryStimulation

Description of an auditory stimulus

| Field | Type | Description |
|-------|------|-------------|
| `stimulus_name` | `str` |  |
| `sample_frequency` | `decimal.Decimal` |  |
| `amplitude_modulation_frequency` | `Optional[int]` |  |
| `frequency_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) |  |
| `bandpass_low_frequency` | `Optional[decimal.Decimal]` |  |
| `bandpass_high_frequency` | `Optional[decimal.Decimal]` |  |
| `bandpass_filter_type` | Optional[[FilterType](../aind_data_schema_models/devices.md#filtertype)] |  |
| `bandpass_order` | `Optional[int]` |  |
| `notes` | `Optional[str]` |  |


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


### OlfactoryStimulation

Description of a olfactory stimulus

| Field | Type | Description |
|-------|------|-------------|
| `stimulus_name` | `str` |  |
| `channels` | List[[OlfactometerChannelConfig](#olfactometerchannelconfig)] |  |
| `notes` | `Optional[str]` |  |


### OptoStimulation

Description of opto stimulation parameters

| Field | Type | Description |
|-------|------|-------------|
| `stimulus_name` | `str` |  |
| `pulse_shape` | [PulseShape](#pulseshape) |  |
| `pulse_frequency` | `List[decimal.Decimal]` |  |
| `pulse_frequency_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) |  |
| `number_pulse_trains` | `List[int]` |  |
| `pulse_width` | `List[int]` |  |
| `pulse_width_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `pulse_train_duration` | `List[decimal.Decimal]` |  |
| `pulse_train_duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `fixed_pulse_train_interval` | `bool` |  |
| `pulse_train_interval` | `Optional[decimal.Decimal]` | Time between pulse trains |
| `pulse_train_interval_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `baseline_duration` | `decimal.Decimal` | Duration of baseline recording prior to first pulse train |
| `baseline_duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `other_parameters` | `dict` |  |
| `notes` | `Optional[str]` |  |


### PhotoStimulation

Description of a photostimulation acquisition

| Field | Type | Description |
|-------|------|-------------|
| `stimulus_name` | `str` |  |
| `number_groups` | `int` |  |
| `groups` | List[[PhotoStimulationGroup](#photostimulationgroup)] |  |
| `inter_trial_interval` | `decimal.Decimal` |  |
| `inter_trial_interval_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `other_parameters` | `dict` |  |
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


### VisualStimulation

Description of visual stimulus parameters. Provides a high level description of stimulus.

| Field | Type | Description |
|-------|------|-------------|
| `stimulus_name` | `str` |  |
| `stimulus_parameters` | `dict` | Define and list the parameter values used (e.g. all TF or orientation values) |
| `stimulus_template_name` | `List[str]` | Name of image set or movie displayed |
| `notes` | `Optional[str]` |  |


