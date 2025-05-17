# Procedures

The `procedures.json` file contains anything done to the subject or specimen prior to data collection. This can include surgeries, injections, tissue processing, sectioning, immunolabeling, etc. The procedures metadata also contains implanted devices and their configurations, for example for chronic insertions.

## Subject vs. specimen

**Subject** procedures are performed on a live subject (e.g. injections, surgeries, implants, perfusions, etc.) whereas **specimen** procedures are performed on tissue extracted after perfusion (e.g. tissue processing, immunolabeling, sectioning, etc.).

Sectioned specimens must have unique IDs appended as a suffix to the subject ID: `subject_id-specimen_number`.

## Perfusions

**Perfusions** are subject procedures that produce specimens and sectioning is a specimen procedure that produces new specimens.

## Ethics review ID vs. protocol ID

All experimental work with animals and humans must be approved by an IACUC (Institute Animal Care Use Committee) or IRB (Institutional Review Board), the corresponding ID number should be stored in the `ethics_review_id` fields.

Protocol ID refers to the DOI for a published protocol describing a procedure, for example those stored in the [AIND protocols.io workspace](https://www.protocols.io/workspaces/allen-institute-for-neural-dynamics).

## Examples

- [Generic procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/procedures.py)
- [SmartSPIM procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/aibs_smartspim_procedures.py)
- [Ophys procedures](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/examples/ophys_procedures.py)

## Model definitions