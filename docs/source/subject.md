# Subject

The `subject.json` file describes the subject from which data was obtained.

## Example

```{literalinclude} ../../examples/subject.py
:language: python
:linenos:
```

## Model definitions


### Subject

Description of a subject of data collection

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | `str` | Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes. |
| `subject_details` | [MouseSubject](components/subjects.md#mousesubject) or [HumanSubject](components/subjects.md#humansubject) |  |
| `notes` | `Optional[str]` |  |
