# Subject

The `subject.json` file describes the animal from which data is obtained.

The subject file contains information regarding the background of the subject such as sex, species, genotype, any identifiers, where it was sourced from, breeding background, etc.

```{literalinclude} ../../examples/subject.py
:language: python
:linenos:
```

## Model definitions


## `Subject`

Description of a subject of data collection

| Field | Type | Description |
|-------|------|-------------|
| `subject_id` | `str` | Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes. |
| `subject_details` | `typing.Annotated[aind_data_schema.components.subjects.MouseSubject | aind_data_schema.components.subjects.HumanSubject, FieldInfo(annotation=NoneType, required=True, discriminator='object_type')]` |  |
| `notes` | `Optional[str]` |  |
