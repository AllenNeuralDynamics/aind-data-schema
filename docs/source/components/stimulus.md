# Stimulus

## Model definitions

### AuditoryStimulation

Description of an auditory stimulus

| Field | Type | Title (Description) |
|-------|------|-------------|
| `stimulus_name` | `str` | Stimulus name  |
| `sample_frequency` | `decimal.Decimal` | Sample frequency  |
| `amplitude_modulation_frequency` | `Optional[int]` | Amplitude modulation frequency  |
| `frequency_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) | Tone frequency unit  |
| `bandpass_low_frequency` | `Optional[decimal.Decimal]` | Bandpass low frequency  |
| `bandpass_high_frequency` | `Optional[decimal.Decimal]` | Bandpass high frequency  |
| `bandpass_filter_type` | Optional[[FilterType](../aind_data_schema_models/devices.md#filtertype)] | Bandpass filter type  |
| `bandpass_order` | `Optional[int]` | Bandpass order  |
| `notes` | `Optional[str]` | Notes  |


### FilterType

Types of bandpass filters for auditory stim

| Name | Value |
|------|-------|
| `BUTTERWORTH` | `Butterworth` |
| `OTHER` | `Other` |


### OlfactometerChannelConfig

**DEPRECATED**: Use OlfactometerConfig in aind_data_schema.components.configs

Description of olfactometer channel configurations

| Field | Type | Title (Description) |
|-------|------|-------------|
| `channel_index` | `int` | Channel index  |
| `odorant` | `str` | Odorant  |
| `odorant_dilution` | `decimal.Decimal` | Odorant dilution  |
| `odorant_dilution_unit` | [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) | Dilution unit  |
| `notes` | `Optional[str]` | Notes  |


### OlfactoryStimulation

**DEPRECATED**: Use StimulusEpoch.stimulus_name and OlfactometerConfig in aind_data_schema.components.configs

Description of a olfactory stimulus

| Field | Type | Title (Description) |
|-------|------|-------------|
| `stimulus_name` | `str` | Stimulus name  |
| <del>`channels`</del> | Optional[List[[OlfactometerChannelConfig](#olfactometerchannelconfig)]] | **[DEPRECATED]** Use OlfactometerConfig instead. Channels  |
| <del>`notes`</del> | `Optional[str]` | **[DEPRECATED]** Use OlfactometerConfig instead. Notes  |


### OptoStimulation

Description of opto stimulation parameters

| Field | Type | Title (Description) |
|-------|------|-------------|
| `stimulus_name` | `str` | Stimulus name  |
| `pulse_shape` | [PulseShape](#pulseshape) | Pulse shape  |
| `pulse_frequency` | `List[decimal.Decimal]` | Pulse frequency (Hz)  |
| `pulse_frequency_unit` | [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) | Pulse frequency unit  |
| `number_pulse_trains` | `List[int]` | Number of pulse trains  |
| `pulse_width` | `List[int]` | Pulse width (ms)  |
| `pulse_width_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Pulse width unit  |
| `pulse_train_duration` | `List[decimal.Decimal]` | Pulse train duration (s)  |
| `pulse_train_duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Pulse train duration unit  |
| `fixed_pulse_train_interval` | `bool` | Fixed pulse train interval  |
| `pulse_train_interval` | `Optional[decimal.Decimal]` | Pulse train interval (s) (Time between pulse trains) |
| `pulse_train_interval_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Pulse train interval unit  |
| `baseline_duration` | `decimal.Decimal` | Baseline duration (s) (Duration of baseline recording prior to first pulse train) |
| `baseline_duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Baseline duration unit  |
| `other_parameters` | `Optional[dict]` | Other parameters  |
| `notes` | `Optional[str]` | Notes  |


### PhotoStimulation

Description of a photostimulation acquisition

| Field | Type | Title (Description) |
|-------|------|-------------|
| `stimulus_name` | `str` | Stimulus name  |
| `number_groups` | `int` | Number of groups  |
| `groups` | List[[PhotoStimulationGroup](#photostimulationgroup)] | Groups  |
| `inter_trial_interval` | `decimal.Decimal` | Inter trial interval (s)  |
| `inter_trial_interval_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Inter trial interval unit  |
| `other_parameters` | `Optional[dict]` | Other parameters  |
| `notes` | `Optional[str]` | Notes  |


### PhotoStimulationGroup

Description of a photostimulation group

| Field | Type | Title (Description) |
|-------|------|-------------|
| `group_index` | `int` | Group index  |
| `number_of_neurons` | `int` | Number of neurons  |
| `stimulation_laser_power` | `decimal.Decimal` | Stimulation laser power (mW)  |
| `stimulation_laser_power_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) | Stimulation laser power unit  |
| `number_trials` | `int` | Number of trials  |
| `number_spirals` | `int` | Number of spirals  |
| `spiral_duration` | `decimal.Decimal` | Spiral duration (s)  |
| `spiral_duration_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Spiral duration unit  |
| `inter_spiral_interval` | `decimal.Decimal` | Inter trial interval (s)  |
| `inter_spiral_interval_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Inter trial interval unit  |
| `other_parameters` | `Optional[dict]` | Other parameters  |
| `notes` | `Optional[str]` | Notes  |


### PulseShape

Types of Opto stim pulse shapes

| Name | Value |
|------|-------|
| `SQUARE` | `Square` |
| `RAMP` | `Ramp` |
| `SINE` | `Sinusoidal` |


### VisualStimulation

Description of visual stimulus parameters. Provides a high level description of stimulus.

| Field | Type | Title (Description) |
|-------|------|-------------|
| `stimulus_name` | `str` | Stimulus name  |
| `stimulus_parameters` | `Optional[dict]` | Stimulus parameters (Define and list the parameter values used (e.g. all TF or orientation values)) |
| `stimulus_template_name` | `List[str]` | Stimulus template name (Name of image set or movie displayed) |
| `notes` | `Optional[str]` | Notes  |


