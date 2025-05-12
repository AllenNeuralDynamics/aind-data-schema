# Measurements

## Model definitions

### Calibration

Generic calibration class

| Field | Type | Description |
|-------|------|-------------|
| `calibration_date` | `datetime (timezone-aware)` |  |
| `description` | `str` | Brief description of what is being calibrated |
| `input` | `List[float or str]` | Calibration input |
| `input_unit` | [SizeUnit](aind_data_schema_models/units.md#sizeunit) or [MassUnit](aind_data_schema_models/units.md#massunit) or [FrequencyUnit](aind_data_schema_models/units.md#frequencyunit) or {SpeedUnit} or [VolumeUnit](aind_data_schema_models/units.md#volumeunit) or [AngleUnit](aind_data_schema_models/units.md#angleunit) or [TimeUnit](aind_data_schema_models/units.md#timeunit) or [PowerUnit](aind_data_schema_models/units.md#powerunit) or [CurrentUnit](aind_data_schema_models/units.md#currentunit) or [ConcentrationUnit](aind_data_schema_models/units.md#concentrationunit) or [TemperatureUnit](aind_data_schema_models/units.md#temperatureunit) or [SoundIntensityUnit](aind_data_schema_models/units.md#soundintensityunit) or [VoltageUnit](aind_data_schema_models/units.md#voltageunit) or [MemoryUnit](aind_data_schema_models/units.md#memoryunit) or [UnitlessUnit](aind_data_schema_models/units.md#unitlessunit) or [MagneticFieldUnit](aind_data_schema_models/units.md#magneticfieldunit) or [PressureUnit](aind_data_schema_models/units.md#pressureunit) |  |
| `output` | `List[float or str]` | Calibration output |
| `output_unit` | [SizeUnit](aind_data_schema_models/units.md#sizeunit) or [MassUnit](aind_data_schema_models/units.md#massunit) or [FrequencyUnit](aind_data_schema_models/units.md#frequencyunit) or {SpeedUnit} or [VolumeUnit](aind_data_schema_models/units.md#volumeunit) or [AngleUnit](aind_data_schema_models/units.md#angleunit) or [TimeUnit](aind_data_schema_models/units.md#timeunit) or [PowerUnit](aind_data_schema_models/units.md#powerunit) or [CurrentUnit](aind_data_schema_models/units.md#currentunit) or [ConcentrationUnit](aind_data_schema_models/units.md#concentrationunit) or [TemperatureUnit](aind_data_schema_models/units.md#temperatureunit) or [SoundIntensityUnit](aind_data_schema_models/units.md#soundintensityunit) or [VoltageUnit](aind_data_schema_models/units.md#voltageunit) or [MemoryUnit](aind_data_schema_models/units.md#memoryunit) or [UnitlessUnit](aind_data_schema_models/units.md#unitlessunit) or [MagneticFieldUnit](aind_data_schema_models/units.md#magneticfieldunit) or [PressureUnit](aind_data_schema_models/units.md#pressureunit) |  |
| `notes` | `Optional[str]` | Fit equation, etc |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LaserCalibration

Calibration of a laser device

| Field | Type | Description |
|-------|------|-------------|
| `input` | `List[float]` | Power output percentage |
| `input_unit` | [PowerUnit](aind_data_schema_models/units.md#powerunit) |  |
| `output` | `List[float]` | Laser strength |
| `output_unit` | [PowerUnit](aind_data_schema_models/units.md#powerunit) |  |
| `description` | `"Laser power measured for various percentage output strengths"` |  |
| `calibration_date` | `datetime (timezone-aware)` |  |
| `notes` | `Optional[str]` | Fit equation, etc |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### LiquidCalibration

Calibration of a liquid delivery device

| Field | Type | Description |
|-------|------|-------------|
| `input` | `List[float]` | Length of time solenoid is open |
| `input_unit` | [TimeUnit](aind_data_schema_models/units.md#timeunit) |  |
| `output` | `List[float]` | Liquid output |
| `output_unit` | [VolumeUnit](aind_data_schema_models/units.md#volumeunit) |  |
| `description` | `"Liquid volume measured for various solenoid opening times"` |  |
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
| `reagents` | Optional[List[[Reagent](reagent.md#reagent)]] |  |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


