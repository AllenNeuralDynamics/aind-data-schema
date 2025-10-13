# Metadata

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/metadata.py)

The `metadata.json` gathers together the other metadata files and adds information about where the data asset is stored.

## Core file

### Metadata

The records in the Data Asset Collection needs to contain certain fields
to easily query and index the data.

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Data Asset Name (Name of the data asset.) |
| `location` | `str` | Location (Current location of the data asset.) |
| `other_identifiers` | Optional[Dict[[Database](components/identifiers.md#database), List[str]]] | Other identifiers (Links to the data asset on secondary platforms.) |
| `subject` | Optional[[Subject](subject.md#subject)] | Subject (Subject of data collection.) |
| `data_description` | Optional[[DataDescription](data_description.md#datadescription)] | Data Description (A logical collection of data files.) |
| `procedures` | Optional[[Procedures](procedures.md#procedures)] | Procedures (All procedures performed on a subject.) |
| `instrument` | Optional[[Instrument](instrument.md#instrument)] | Instrument (Devices used to acquire data.) |
| `processing` | Optional[[Processing](processing.md#processing)] | Processing (All processes run on data.) |
| `acquisition` | Optional[[Acquisition](acquisition.md#acquisition)] | Acquisition (Data acquisition) |
| `quality_control` | Optional[[QualityControl](quality_control.md#qualitycontrol)] | Quality Control (Description of quality metrics for a data asset) |
| `model` | Optional[[Model](model.md#model)] | Model (Description of a machine learning model trained on data.) |
