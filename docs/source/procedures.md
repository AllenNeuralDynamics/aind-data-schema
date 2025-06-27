# Procedures

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/procedures.py)

The `procedures.json` file contains anything done to the subject or specimen prior to data collection. This can include surgeries, injections, tissue processing, sectioning, immunolabeling, etc. The procedures metadata also contains implanted devices and their configurations, for example for chronic insertions.

## Subject procedure vs. specimen procedure

**Subject** procedures are performed on a live subject (e.g. injections, surgeries, implants, perfusions, etc.) whereas **specimen** procedures are performed on tissue extracted after perfusion (e.g. tissue processing, immunolabeling, sectioning, etc.).

Sectioned specimens must have a unique number appended as a suffix to the subject ID: `<subject_id>_<###>`.

## Examples

- [Generic procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/procedures.py)
- [SmartSPIM procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aibs_smartspim_procedures.py)
- [Ophys procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ophys_procedures.py)

## Core file

### Procedures

Description of all procedures performed on a subject, including surgeries, injections, and tissue processing

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | `str` | Unique identifier for the subject of data acquisition |
| `subject_procedures` | List[[Surgery](components/subject_procedures.md#surgery) or [Injection](components/injection_procedures.md#injection) or [TrainingProtocol](components/subject_procedures.md#trainingprotocol) or [WaterRestriction](components/subject_procedures.md#waterrestriction) or [GenericSubjectProcedure](components/subject_procedures.md#genericsubjectprocedure)] | Procedures performed on a live subject |
| `specimen_procedures` | List[[SpecimenProcedure](components/specimen_procedures.md#specimenprocedure)] | Procedures performed on tissue extracted after perfusion |
| `coordinate_system` | Optional[[CoordinateSystem](components/coordinates.md#coordinatesystem)] | Origin and axis definitions for determining the configured position of devices implanted during procedures. Required when coordinates are provided within the Procedures |
| `notes` | `Optional[str]` |  |
