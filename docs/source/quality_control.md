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

`tags` are groups of descriptors that define how metrics are organized hierarchically, making it easier to visualize metrics. Good tag keys (groups) are things like "probe" and good tag values are things like "Probe A" or just "A".

```{python}
# For an electrophysiology metric
tags = {
    "probe": "A",
    "shank": "0",
}

# For a behavioral video metric
tags = {
    "video": "left body",
}
```

Use the `QualityControl.default_grouping` list to define how users should organize a visualization by default. In almost all cases *modality should be the top-level grouping*. For example, building on the example above you might group by: `["modality", ("probe", "video"), "shank"]` to get a tree split by modality first (which naturally splits ephys and behavior-videos tags into two groups), then by which probe or video a metric belongs to, and finally only for probes the individual shanks are split into groups.

### QualityControl.evaluate_status()

You can evaluate the state of a set of metrics filtered by any combination of modalities, stages, and tags on a specific date (by default, today). When evaluating the [Status](#status) of a group of metrics the following rules apply:

First, any metric that has a tag *value* in the `QualityControl.allow_tag_failures` list is ignored. This allows you to specify that certain metrics are not critical to a data asset.

Then, given the status of all the remaining metrics in the group:

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

| Field | Type | Title (Description) |
|-------|------|-------------|
| `metrics` | List[[QCMetric](quality_control.md#qcmetric) or [CurationMetric](quality_control.md#curationmetric)] | Evaluations  |
| `key_experimenters` | `Optional[List[str]]` | Key experimenters (Experimenters who are responsible for quality control of this data asset) |
| `notes` | `Optional[str]` | Notes  |
| `default_grouping` | `List[str or tuple[str, ...]]` | Default grouping (Tag *keys* that should be used to group metrics hierarchically for visualization) |
| `allow_tag_failures` | `List[str]` | Allow tag failures (List of tag *values* that are allowed to fail without failing the overall QC) |
| `status` | `Optional[dict]` | Status mapping (Mapping of tags, modalities, and stages to their evaluated status, automatically computed) |


## Model definitions

### CurationHistory

Schema to track curator name and timestamp for curation events

| Field | Type | Title (Description) |
|-------|------|-------------|
| `curator` | `str` | Curator  |
| `timestamp` | `datetime (timezone-aware)` | Timestamp  |


### CurationMetric

Description of a curation metric

| Field | Type | Title (Description) |
|-------|------|-------------|
| `value` | `List[typing.Any]` | Curation value  |
| `type` | `str` | Curation type  |
| `curation_history` | List[[CurationHistory](quality_control.md#curationhistory)] | Curation history  |
| `name` | `str` | Metric name  |
| `modality` | [Modality](aind_data_schema_models/modalities.md#modality) | Modality  |
| `stage` | [Stage](quality_control.md#stage) | Evaluation stage  |
| `status_history` | List[[QCStatus](quality_control.md#qcstatus)] | Metric status history  |
| `description` | `Optional[str]` | Metric description  |
| `reference` | `Optional[str]` | Metric reference image URL or plot type  |
| `tags` | `Dict[str, str]` | Tags (Tags group QCMetric objects. Unique keys define groups of tags, for example {'probe': 'probeA'}.) |
| `evaluated_assets` | `Optional[List[str]]` | List of asset names that this metric depends on (Set to None except when a metric's calculation required data coming from a different data asset.) |


### QCMetric

Description of a single quality control metric

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Metric name  |
| `modality` | [Modality](aind_data_schema_models/modalities.md#modality) | Modality  |
| `stage` | [Stage](quality_control.md#stage) | Evaluation stage  |
| `value` | `typing.Any` | Metric value  |
| `status_history` | List[[QCStatus](quality_control.md#qcstatus)] | Metric status history  |
| `description` | `Optional[str]` | Metric description  |
| `reference` | `Optional[str]` | Metric reference image URL or plot type  |
| `tags` | `Dict[str, str]` | Tags (Tags group QCMetric objects. Unique keys define groups of tags, for example {'probe': 'probeA'}.) |
| `evaluated_assets` | `Optional[List[str]]` | List of asset names that this metric depends on (Set to None except when a metric's calculation required data coming from a different data asset.) |


### QCStatus

Description of a QC status, set by an evaluator

| Field | Type | Title (Description) |
|-------|------|-------------|
| `evaluator` | `str` | Status evaluator full name  |
| `status` | [Status](quality_control.md#status) | Status  |
| `timestamp` | `datetime (timezone-aware)` | Status date  |


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
