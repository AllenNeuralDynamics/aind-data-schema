# Measurements

## Model definitions

### Calibration

Generic calibration class

| Field | Type | Title (Description) |
|-------|------|-------------|
| `calibration_date` | `datetime (timezone-aware)` | Date and time of calibration  |
| `description` | `str` | Description (Brief description of what is being calibrated) |
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `measured_at` | `Optional[str]` | Measurement location  |
| `input` | `List[float or str]` | Inputs (Calibration input) |
| `input_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) or [MassUnit](../aind_data_schema_models/units.md#massunit) or [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) or [SpeedUnit](../aind_data_schema_models/units.md#speedunit) or [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) or [AngleUnit](../aind_data_schema_models/units.md#angleunit) or [TimeUnit](../aind_data_schema_models/units.md#timeunit) or [PowerUnit](../aind_data_schema_models/units.md#powerunit) or [CurrentUnit](../aind_data_schema_models/units.md#currentunit) or [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) or [TemperatureUnit](../aind_data_schema_models/units.md#temperatureunit) or [SoundIntensityUnit](../aind_data_schema_models/units.md#soundintensityunit) or [VoltageUnit](../aind_data_schema_models/units.md#voltageunit) or [MemoryUnit](../aind_data_schema_models/units.md#memoryunit) or [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) or [MagneticFieldUnit](../aind_data_schema_models/units.md#magneticfieldunit) or [PressureUnit](../aind_data_schema_models/units.md#pressureunit) or {TorqueUnit} | Input unit  |
| `repeats` | `Optional[int]` | Number of repeats (If each input was repeated multiple times, provide the number of repeats) |
| `output` | `List[float or str]` | Outputs (Calibration output (provide the average if repeated)) |
| `output_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) or [MassUnit](../aind_data_schema_models/units.md#massunit) or [FrequencyUnit](../aind_data_schema_models/units.md#frequencyunit) or [SpeedUnit](../aind_data_schema_models/units.md#speedunit) or [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) or [AngleUnit](../aind_data_schema_models/units.md#angleunit) or [TimeUnit](../aind_data_schema_models/units.md#timeunit) or [PowerUnit](../aind_data_schema_models/units.md#powerunit) or [CurrentUnit](../aind_data_schema_models/units.md#currentunit) or [ConcentrationUnit](../aind_data_schema_models/units.md#concentrationunit) or [TemperatureUnit](../aind_data_schema_models/units.md#temperatureunit) or [SoundIntensityUnit](../aind_data_schema_models/units.md#soundintensityunit) or [VoltageUnit](../aind_data_schema_models/units.md#voltageunit) or [MemoryUnit](../aind_data_schema_models/units.md#memoryunit) or [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) or [MagneticFieldUnit](../aind_data_schema_models/units.md#magneticfieldunit) or [PressureUnit](../aind_data_schema_models/units.md#pressureunit) or {TorqueUnit} | Output unit  |
| `fit` | Optional[[CalibrationFit](#calibrationfit)] | Fit (Fit equation for the calibration data used during data acquisition) |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### CalibrationFit

Fit equation for calibration data

| Field | Type | Title (Description) |
|-------|------|-------------|
| `fit_type` | [FitType](#fittype) | Fit type  |
| `fit_parameters` | `Optional[dict]` | Fit parameters (Parameters of the fit equation, e.g. slope and intercept for linear fit) |


### FitType

Type of fit for calibration data

| Name | Value |
|------|-------|
| `LINEAR_INTERPOLATION` | `linear_interpolation` |
| `LINEAR` | `linear` |
| `OTHER` | `other` |


### Maintenance

Generic maintenance class

| Field | Type | Title (Description) |
|-------|------|-------------|
| `maintenance_date` | `datetime (timezone-aware)` | Date and time of maintenance  |
| `description` | `str` | Description (Description on maintenance procedure) |
| `protocol_id` | `Optional[str]` | Protocol ID  |
| `reagents` | Optional[List[[Reagent](reagent.md#reagent)]] | Reagents  |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### PowerCalibration

Calibration of a device that outputs power based on input strength

| Field | Type | Title (Description) |
|-------|------|-------------|
| `input` | `List[float]` | Input (Power, voltage, or percentage input strength) |
| `input_unit` | `aind_data_schema_models.units.PowerUnit or aind_data_schema_models.units.VoltageUnit` | Input unit  |
| `output` | `List[float]` | Output (Power output (provide the average if repeated)) |
| `output_unit` | [PowerUnit](../aind_data_schema_models/units.md#powerunit) | Output unit  |
| `description` | `"Power measured for various power or percentage input strengths"` |   |
| `calibration_date` | `datetime (timezone-aware)` | Date and time of calibration  |
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `measured_at` | `Optional[str]` | Measurement location  |
| `repeats` | `Optional[int]` | Number of repeats (If each input was repeated multiple times, provide the number of repeats) |
| `fit` | Optional[[CalibrationFit](#calibrationfit)] | Fit (Fit equation for the calibration data used during data acquisition) |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


### VolumeCalibration

Calibration of a liquid delivery device based on solenoid/valve opening times

| Field | Type | Title (Description) |
|-------|------|-------------|
| `input` | `List[float]` | Input times (Length of time solenoid/valve is open) |
| `input_unit` | [TimeUnit](../aind_data_schema_models/units.md#timeunit) | Input unit  |
| `repeats` | `Optional[int]` | Number of repeats (If each input was repeated multiple times, provide the number of repeats) |
| `output` | `List[float]` | Output (Volume output (provide the average if repeated)) |
| `output_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) | Output unit  |
| `description` | `"Volume measured for various solenoid opening times"` |   |
| `calibration_date` | `datetime (timezone-aware)` | Date and time of calibration  |
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `measured_at` | `Optional[str]` | Measurement location  |
| `fit` | Optional[[CalibrationFit](#calibrationfit)] | Fit (Fit equation for the calibration data used during data acquisition) |
| `notes` | `Optional[str]` | Notes  |
| `device_name` | `str` | Device name (Must match a device defined in the instrument.json) |


