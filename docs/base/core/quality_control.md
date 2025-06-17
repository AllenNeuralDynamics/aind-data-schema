# Quality control

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/quality_control.py)

Quality control is a collection of **metrics** evaluated on a data asset.

`QCMetric` objects should be generated during pipelines: from raw data, during processing, and during analysis by researchers.

Every `QCMetric` has a `aind_data_schema.quality_control.State` which takes the value of the metric and compares it to some rule. Metrics can only pass or fail. Metrics that required manual evaluation are set to pending.

## Details

### Metrics

Each `QCMetric` is a single value or set of values that can be computed, or observed, about a set of data as part of an evaluation. These can have any type. See the AIND section for special rules for annotating metrics with options.

Each `QCMetric` is annotated with three pieces of additional metadata: the `Stage` during which it was evaluated, the `Modality` of the evaluated data, and `tags`. `tags` are any string that naturally groups sets of metrics together. Good tags are things like: "Probe A", "Motion correction", and "Pose tracking". The stage and modality are automatically treated as tags, you do not need to include them.

`QCMetric`s have a `Status`. The `Status` should depend directly on the `QCMetric.value`, either by a simple function: "value>5", or by a qualitative rule: "Field of view includes visual areas". The `QCMetric.description` field should be used to describe the rule used to set the status. Metrics can be evaluated multiple times, in which case the new status should be appended the `QCMetric.status_history`.

### QualityControl.evaluate_status()

You can evaluate the state of an combination of metrics filtered by the modality, stage, and tags. You can also filter for the status on a specific date. When evaluating the `Status` of a group of metrics the following rules apply:

First: any metric that is failing and also has a matching tag (or tuple of tags) in the `allow_tag_failures` list is set to pass.

Then given the status of all the metrics in the group:

1. If any metric is still failing, the evaluation fails
2. If any metric is pending and the rest pass the evaluation is pending
3. If all metrics pass the evaluation passes

**Q: What is a metric reference?**

Metrics should include a `QCMetric.reference`. References are intended to be publicly accessible images, figures, multi-panel figures, and videos that support the metric or provide information necessary for manual annotation of a metric's status.

It's good practice to share a single multi-panel figure across multiple references to simplify viewing the QC metadata.

**Q: What are the status options for metrics?**

In our quality control a metric's status is always `PASS`, `PENDING` (waiting for manual annotation), or `FAIL`.

We enforce this minimal set of states to prevent ambiguity and make it easier to build tools that can interpret the status of a data asset.

## Multi-asset QC

During analysis there are many situations where multiple data assets need to be pulled together, often for comparison. For example, FOVs across imaging sessions or recording sessions from a chronic probe might need to get matched up across days. When a `QCEvaluation` is being calculated from multiple assets it should be tagged with `Stage:MULTI_ASSET` and each of its `QCMetric` objects needs to track the assets that were used to generate that metric in the `evaluated_assets` list.

**Q: Where do I store multi-asset QC?**

You should follow the preferred/alternate workflows described above. If your multi-asset analysis pipeline generates a new data asset, put the QC there. If your pipeline does not generate an asset, push a copy of each `QCEvaluation` back to **each** individual data asset.

**Q: I want to be able to store data about each of the evaluated assets in this metric**

Take a look at the `MultiAssetMetric` class in `aind-qcportal-schema`. It allows you to pass a list of values which will be matched up with the `evaluated_assets` names. You can also include options which will appear as dropdowns or checkboxes.

## Example

```{literalinclude} ../../examples/quality_control.py
:language: python
:linenos:
```
