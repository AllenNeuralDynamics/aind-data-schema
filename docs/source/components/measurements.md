# Measurements

## Model definitions

### Calibration

Generic calibration class

| Field | Type | Description |
|-------|------|-------------|
| `calibration_date` | `datetime (timezone-aware)` |  |
| `description` | `str` | Brief description of what is being calibrated |
| `input` | `List[float or str]` | Calibration input |
| `input_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) or [MassUnit](../aind_data_schema_models/units.md#massunit) or [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) or [SpeedUnit](../aind_data_schema_models/units.md#speedunit) or [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) or [AngleUnit](../aind_data_schema_models/units.md#angleunit) or [TimeUnit](../aind_data_schema_models/units.md#timeunit) or [PowerUnit](../aind_data_schema_models/units.md#powerunit) or [CurrentUnit](../aind_data_schema_models/units.md#currentunit) or [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) or [TemperatureUnit](../aind_data_schema_models/units.md#temperatureunit) or [SoundIntensityUnit](../aind_data_schema_models/units.md#soundintensityunit) or [VoltageUnit](../aind_data_schema_models/units.md#voltageunit) or [MemoryUnit](../aind_data_schema_models/units.md#memoryunit) or [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) or [MagneticFieldUnit](../aind_data_schema_models/units.md#magneticfieldunit) or [PressureUnit](../aind_data_schema_models/units.md#pressureunit) |  |
| `repeats` | `Optional[int]` | If each input was repeated multiple times, provide the number of repeats |
| `output` | `List[float or str]` | Calibration output (provide the average if repeated) |
| `output_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) or [MassUnit](../aind_data_schema_models/units.md#massunit) or [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) or [SpeedUnit](../aind_data_schema_models/units.md#speedunit) or [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) or [AngleUnit](../aind_data_schema_models/units.md#angleunit) or [TimeUnit](../aind_data_schema_models/units.md#timeunit) or [PowerUnit](../aind_data_schema_models/units.md#powerunit) or [CurrentUnit](../aind_data_schema_models/units.md#currentunit) or [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) or [TemperatureUnit](../aind_data_schema_models/units.md#temperatureunit) or [SoundIntensityUnit](../aind_data_schema_models/units.md#soundintensityunit) or [VoltageUnit](../aind_data_schema_models/units.md#voltageunit) or [MemoryUnit](../aind_data_schema_models/units.md#memoryunit) or [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) or [MagneticFieldUnit](../aind_data_schema_models/units.md#magneticfieldunit) or [PressureUnit](../aind_data_schema_models/units.md#pressureunit) |  |
| `fit` | Optional[[CalibrationFit](#calibrationfit)] | Fit equation for the calibration data used during data acquisition |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### CalibrationFit

Fit equation for calibration data

| Field | Type | Description |
|-------|------|-------------|
| `fit_type` | [FitType](#fittype) |  |
| `fit_parameters` | `Optional[dict]` | Parameters of the fit equation, e.g. slope and intercept for linear fit |


### FitType

Type of fit for calibration data

| Name | Value |
|------|-------|
| `LINEAR_INTERPOLATION` | `linear_interpolation` |
| `LINEAR` | `linear` |
| `OTHER` | `other` |


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


### PowerCalibration

Calibration of a device that outputs power based on input strength

| Field | Type | Description |
|-------|------|-------------|
| `input` | `List[float]` | Power, voltage, or percentage input strength |
| `input_unit` | `aind_data_schema_models.units.PowerUnit or aind_data_schema_models.units.VoltageUnit` |  |
| `output` | `List[float]` | Power output (provide the average if repeated) |
| `output_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) |  |
| `description` | `"Power measured for various power or percentage input strengths"` |  |
| `calibration_date` | `datetime (timezone-aware)` |  |
| `repeats` | `Optional[int]` | If each input was repeated multiple times, provide the number of repeats |
| `fit` | Optional[[CalibrationFit](#calibrationfit)] | Fit equation for the calibration data used during data acquisition |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


### VolumeCalibration

Calibration of a liquid delivery device based on solenoid/valve opening times

| Field | Type | Description |
|-------|------|-------------|
| `input` | `List[float]` | Length of time solenoid/valve is open |
| `input_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) |  |
| `repeats` | `Optional[int]` | If each input was repeated multiple times, provide the number of repeats |
| `output` | `List[float]` | Volume output (provide the average if repeated) |
| `output_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) |  |
| `description` | `"Volume measured for various solenoid opening times"` |  |
| `calibration_date` | `datetime (timezone-aware)` |  |
| `fit` | Optional[[CalibrationFit](#calibrationfit)] | Fit equation for the calibration data used during data acquisition |
| `notes` | `Optional[str]` |  |
| `device_name` | `str` | Must match a device defined in the instrument.json |


