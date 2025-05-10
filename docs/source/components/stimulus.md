# Stimulus

## Model definitions

### OlfactometerChannelConfig

Description of olfactometer channel configurations

| Field | Type | Description |
|-------|------|-------------|
| `channel_index` | `int` |  |
| `odorant` | `str` |  |
| `odorant_dilution` | `decimal.Decimal` |  |
| `odorant_dilution_unit` | `ConcentrationUnit` |  |
| `notes` | `Optional[str]` |  |


### PhotoStimulationGroup

Description of a photostimulation group

| Field | Type | Description |
|-------|------|-------------|
| `group_index` | `int` |  |
| `number_of_neurons` | `int` |  |
| `stimulation_laser_power` | `decimal.Decimal` |  |
| `stimulation_laser_power_unit` | `PowerUnit` |  |
| `number_trials` | `int` |  |
| `number_spirals` | `int` |  |
| `spiral_duration` | `decimal.Decimal` |  |
| `spiral_duration_unit` | `TimeUnit` |  |
| `inter_spiral_interval` | `decimal.Decimal` |  |
| `inter_spiral_interval_unit` | `TimeUnit` |  |
| `other_parameters` | `aind_data_schema.base.GenericModel` |  |
| `notes` | `Optional[str]` |  |


