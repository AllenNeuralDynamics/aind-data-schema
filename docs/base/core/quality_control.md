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

If you find yourself computing a value for something smaller than an entire modality of data in an asset you are performing *curation*, i.e. you are determining the status of a subset of a modality in the data asset. We provide the [CurationMetric](#curationmetric) and [ElementCurationMetric](#elementcurationmetric) models for this purpose. You should put a dictionary in the `CurationMetric.value` field that contains a mapping between the subsets (usually neurons, ROIs, channels, etc) and their values.

The difference between the two options is that:

- [CurationMetric](#curationmetric) expects a single dictionary to describe the curation and any update to the curation requires writing a new copy of the entire dictionary. This makes `CurationMetric` best suited to curations that act on multiple elements of the data asset at once, for example: splitting and combining clusters after spike sorting.
- [ElementCurationMetric](#elementcurationmetric) should be used when each element of a data asset has its own curation and these can change over time. Instead of accepting just one dictionary, the `ElementCurationMetric.value` wraps each element's curation data in an outer dictionary that is split by elements. This makes updating a single element's curation more efficient.

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
