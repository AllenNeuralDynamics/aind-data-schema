# Data description

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/data_description.py)

The `data_description.json` file tracks administrative information about a data asset, including affiliated researchers/organizations, projects, data modalities, dates of collection, and more.

## Uniqueness

Every data asset is uniquely identified by its `DataDescription.name` field, which combines the `subject_id` and acquisition `session_end_time`. You can group data assets together using the `DataDescription.tags: List[str]`. Tags should be shared across assets within experiments. **Do not repeat information in the tags that already exists elsewhere in the metadata**, for example modalities should never be included in tags.

## Example

```{literalinclude} ../../examples/data_description.py
:language: python
:linenos:
```
