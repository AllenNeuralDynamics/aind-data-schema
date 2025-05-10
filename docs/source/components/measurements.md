# Measurements

## Model definitions

### Calibration

Generic calibration class

| Field | Type | Description |
|-------|------|-------------|
| `calibration_date` | `datetime (timezone-aware)` |  |
| `description` | `str` | Brief description of what is being calibrated |
| `input` | `List[float | str]` | Calibration input |
| `input_unit` | `SizeUnit | MassUnit | FrequencyUnit | SpeedUnit | VolumeUnit | AngleUnit | TimeUnit | PowerUnit | CurrentUnit | ConcentrationUnit | TemperatureUnit | SoundIntensityUnit | VoltageUnit | MemoryUnit | UnitlessUnit | MagneticFieldUnit | PressureUnit` |  |
| `output` | `List[float | str]` | Calibration output |
| `output_unit` | `SizeUnit | MassUnit | FrequencyUnit | SpeedUnit | VolumeUnit | AngleUnit | TimeUnit | PowerUnit | CurrentUnit | ConcentrationUnit | TemperatureUnit | SoundIntensityUnit | VoltageUnit | MemoryUnit | UnitlessUnit | MagneticFieldUnit | PressureUnit` |  |
| `notes` | `Optional[str]` | Fit equation, etc |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LaserCalibration

Calibration of a laser device

| Field | Type | Description |
|-------|------|-------------|
| `input` | `List[float]` | Power output percentage |
| `input_unit` | `PowerUnit` |  |
| `output` | `List[float]` | Laser strength |
| `output_unit` | `PowerUnit` |  |
| `description` | `typing.Literal['Laser power measured for various percentage output strengths']` |  |
| `calibration_date` | `datetime (timezone-aware)` |  |
| `notes` | `Optional[str]` | Fit equation, etc |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LiquidCalibration

Calibration of a liquid delivery device

| Field | Type | Description |
|-------|------|-------------|
| `input` | `List[float]` | Length of time solenoid is open |
| `input_unit` | `TimeUnit` |  |
| `output` | `List[float]` | Liquid output |
| `output_unit` | `VolumeUnit` |  |
| `description` | `typing.Literal['Liquid volume measured for various solenoid opening times']` |  |
| `calibration_date` | `datetime (timezone-aware)` |  |
| `notes` | `Optional[str]` | Fit equation, etc |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### Maintenance

Generic maintenance class

| Field | Type | Description |
|-------|------|-------------|
| `maintenance_date` | `datetime (timezone-aware)` |  |
| `description` | `str` | Description on maintenance procedure |
| `protocol_id` | `Optional[str]` |  |
| `reagents` | Optional[List[[Reagent](components/reagent.md#reagent)]] |  |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


