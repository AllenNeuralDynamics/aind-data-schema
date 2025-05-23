# Processing

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/processing.py)

The `processing.json` file captures the data processing and analysis steps that have been carried out – mostly for derived data assets. This tracks what code was used for each step, when it was run, what the input and outputs where, what parameters were set. This includes things like spike sorting, image alignment, cell segmentation. It also includes manual annotation, quality control, and data analysis.

The processing file should be appended to with each subsequent stage of processing or analysis.

## Example

```{literalinclude} ../../examples/processing.py
:language: python
:linenos:
```
