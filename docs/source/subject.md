# Subject

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/subject.py)

The `subject.json` file describes the subject from which data was obtained.

## Example

```{literalinclude} ../../examples/subject.py
:language: python
:linenos:
```


## Core file

### Subject

Description of a subject of data collection

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | `str` | Unique identifier for the subject of data acquisition |
| `subject_details` | [MouseSubject](components/subjects.md#mousesubject) or [HumanSubject](components/subjects.md#humansubject) or [CalibrationObject](components/subjects.md#calibrationobject) |  |
| `notes` | `Optional[str]` |  |
