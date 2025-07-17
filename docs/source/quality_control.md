# Quality control

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/quality_control.py)

Quality control is a collection of **metrics** evaluated on a data asset.

[QCMetric](#qcmetric) objects should be generated during pipelines: from raw data, during processing, and during analysis by researchers.

Every [QCMetric](#qcmetric) has a `aind_data_schema.quality_control.State` which takes the value of the metric and compares it to some rule. Metrics can only pass or fail. Metrics that require manual evaluation are set to pending.

## Details

### Metrics

Each [QCMetric](#qcmetric) is a single value or array of values that can be computed, or observed, about one modality in a data asset. These can have any type. Metrics should be significant: i.e. whether they pass or fail should matter for the modality. Metrics need to be human understandable. If you find yourself generating more than fifty metrics for a modality you should group them together (i.e. make the value a dictionary combining similar metrics and the rule an evaluation of multiple fields in the dictionary).

Each [QCMetric](#qcmetric) has a [Status](#status). The [Status](#status) should depend directly on the `QCMetric.value`, either by a simple function: "value>5", or by a qualitative rule: "Field of view includes visual areas". The `QCMetric.description` field should describe the rule used to set the status. Metrics can be evaluated multiple times, in which case the new status should be appended the `QCMetric.status_history`.

Each [QCMetric](#qcmetric) is annotated with three pieces of additional metadata: the [Stage](#stage) during which it was evaluated, the [Modality](aind_data_schema_models/modalities.md#modality) of the evaluated data, and [tags](#tags).

### Curations

If you find yourself computing a value for something smaller than an entire modality of data in an asset you are performing *curation*, i.e. you are determining the status of a subset of a modality in the data asset. We provide the [CurationMetric](#curationmetric) for this purpose. You should put a dictionary in the `CurationMetric.value` field that contains a mapping between the subsets (usually neurons, ROIs, channels, etc) and their values.

### Tags

`tags` are any string that naturally groups sets of metrics together. Good tags are things like: "Probe A", "Motion correction", and "Pose tracking". The stage and modality are automatically treated as tags, you do not need to include them in the tags list.

### QualityControl.evaluate_status()

You can evaluate the state of a set of metrics filtered by any combination of modalities, stages, and tags on a specific date (by default, today). When evaluating the [Status](#status) of a group of metrics the following rules apply:

First, any metric that is failing and also has a matching tag (or tuple of tags) in the `QualityControl.allow_tag_failures` list is set to pass. This allows you to specify that certain metrics are not critical to a data asset.

Then, given the status of all the metrics in the group:

1. If any metric is still failing, the evaluation fails
2. If any metric is pending and the rest pass the evaluation is pending
3. If all metrics pass the evaluation passes

**Q: What is a metric reference?**

Each [QCMetric](#qcmetric) should include a `QCMetric.reference`. References should be publicly accessible images, figures, multi-panel figures, and videos that support the metric value/status or provide the information necessary for manual annotation.

It's good practice to share a single multi-panel figure across multiple references to simplify viewing the quality control.

**Q: What are the status options for metrics?**

In our quality control a metric's status is always `PASS`, `PENDING` (waiting for manual annotation), or `FAIL`.

We enforce this minimal set of states to prevent ambiguity and make it easier to build tools that can interpret the status of a data asset.

## Multi-asset QC

During analysis there are many situations where multiple data assets need to be pulled together, often for comparison. For example, FOVs across imaging sessions or recording sessions from a chronic probe might need to get matched up across days. When a [QCMetric](#qcmetric) is being calculated from multiple assets it should be tagged with `Stage:MULTI_ASSET` and each of its metrics needs to track the assets that were used to generate that metric in the `evaluated_assets` list.

## Example

```{literalinclude} ../../examples/quality_control.py
:language: python
:linenos:
```

## Core file

### QualityControl

Collection of quality control metrics evaluated on a data asset to determine pass/fail status

| Field | Type | Description |
|-------|------|-------------|
| `metrics` | List[[QCMetric](quality_control.md#qcmetric) or [CurationMetric](quality_control.md#curationmetric)] |  |
| `key_experimenters` | `Optional[List[str]]` | Experimenters who are responsible for quality control of this data asset |
| `notes` | `Optional[str]` |  |
| `default_grouping` | `List[str]` | Default tag grouping for this QualityControl object, used in visualizations |
| `allow_tag_failures` | `List[str or tuple]` | List of tags that are allowed to fail without failing the overall QC |
| `status` | `Optional[dict]` | Mapping of tags, modalities, and stages to their evaluated status, automatically computed |


## Model definitions

### CurationHistory

Schema to track curator name and timestamp for curation events

| Field | Type | Description |
|-------|------|-------------|
| `curator` | `str` |  |
| `timestamp` | `datetime (timezone-aware)` |  |


### CurationMetric

Description of a curation metric

| Field | Type | Description |
|-------|------|-------------|
| `value` | `List[typing.Any]` |  |
| `type` | `str` |  |
| `curation_history` | List[[CurationHistory](quality_control.md#curationhistory)] |  |
| `name` | `str` |  |
| `modality` | [Modality](aind_data_schema_models/modalities.md#modality) |  |
| `stage` | [Stage](quality_control.md#stage) |  |
| `status_history` | List[[QCStatus](quality_control.md#qcstatus)] |  |
| `description` | `Optional[str]` |  |
| `reference` | `Optional[str]` |  |
| `tags` | `List[str]` | Tags group QCMetric objects to allow for grouping and filtering |
| `evaluated_assets` | `Optional[List[str]]` | Set to None except when a metric's calculation required data coming from a different data asset. |


### QCMetric

Description of a single quality control metric

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `modality` | [Modality](aind_data_schema_models/modalities.md#modality) |  |
| `stage` | [Stage](quality_control.md#stage) |  |
| `value` | `typing.Any` |  |
| `status_history` | List[[QCStatus](quality_control.md#qcstatus)] |  |
| `description` | `Optional[str]` |  |
| `reference` | `Optional[str]` |  |
| `tags` | `List[str]` | Tags group QCMetric objects to allow for grouping and filtering |
| `evaluated_assets` | `Optional[List[str]]` | Set to None except when a metric's calculation required data coming from a different data asset. |


### QCStatus

Description of a QC status, set by an evaluator

| Field | Type | Description |
|-------|------|-------------|
| `evaluator` | `str` |  |
| `status` | [Status](quality_control.md#status) |  |
| `timestamp` | `datetime (timezone-aware)` |  |


### Stage

Quality control stage

When during data processing the QC metrics were derived.

| Name | Value |
|------|-------|
| `RAW` | `Raw data` |
| `PROCESSING` | `Processing` |
| `ANALYSIS` | `Analysis` |
| `MULTI_ASSET` | `Multi-asset` |


### Status

QC Status

| Name | Value |
|------|-------|
| `FAIL` | `Fail` |
| `PASS` | `Pass` |
| `PENDING` | `Pending` |
