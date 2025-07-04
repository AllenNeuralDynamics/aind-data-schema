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
