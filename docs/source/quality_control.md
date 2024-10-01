# Quality control

## Overview

Quality control is a collection of **evaluations** based on sets of **metrics** about the data. When a raw data asset is first indexed an empty `QualityControl` is created. As a user, you then construct `QCEvaluation` objects which contain one or more `QCMetric`s and append these to the `QualityControl`. Adding your `QCEvaluation`s is done through the `aind-data-access-api`.

Each `QualityControl`, `QCEvaluation`, and `QCMetric` includes a `aind_data_schema.quality_control.State` which is a timestamped object indicating that the Overall QC/Evaluation/Metric passes, fails, or is in a pending state waiting for manual annotation.

The state of an evaluation is set automatically to the lowest of its metric's states. A single failed metric sets an entire evaluation to fail. While a single pending metric (with all other metrics passing) sets an entire evaluation to pending. An optional setting `QCEvaluation.allow_failed_metrics` allows you to ignore failures, which can be useful in situations where an evaluation is not critical for quality control (for example: a camera feed that often has failures but does not affect the rest of the experiment).

## Details

**Q: What is an evaluation?**

Each `QCEvaluation` should be thought of as a single aspect of the data asset that can be evaluated for quality, at a specific stage in data acquisition and processing. For example, the brain moves a small amount during both electrophysiology and optical recordings. This drift can be measured by various automated quantiative metrics, as well as qualititative metrics evaluated by a human observer. The state of an evaluation depends on the state of its metrics according to these rules:

- If all metrics pass the evaluation passes
- If any metric fails the evaluation fails (except when the `allow_failed_metrics` flag is set)
- If any metric is pending (and the rest pass) the evaluation is pending

Make sure to annotate `QCEvaluation`s with the `Stage` and `Modality` they are related to.

**Q: What is a metric?**

A metric is any single value or set of values that can be computed, or observed, about a set of data as part of an evaluation. These can have any type, but the QC apps that scientific computing supports expect you to use metrics that are numerical, string, bool, arrays of these values. See the AIND section for special rules for annotating metrics with options.

Metrics have a status which is set by a rule, usually some function of the metric value. The rule should be encoded in the metric description. Metrics can be evaluated multiple times, in which case the new status will be appended the `QCMetric.metric_status_history`. The latest status can be retrived by using `QCMetric.metric_status`.

Each metric should also include a `QCMetric.reference`. References are intended to be publicly accessible images, figures, combined figures with multiple panels, or videos that support the metric or provide information necessary for manual annotation of a metric's status.

**Q: What are the status options for metrics?**

In our quality control a metric's status is always PASS, PENDING (waiting for manual annotation), or FAIL. PENDING is used when the QC evaluation is not yet complete.

We enforce this minimal set of states to prevent ambiguity and make it easier to build tools that can interpret the status of a data asset.

## Details for AIND users

### Uploading QC

**Preferred workflow**

If you are building `QCEvaluations` in a capsule alongside your processing or analysis, your workflow is: 

```
from aind_data_schema.core.quality_control import QualityControl

# Build your QCEvaluations and metrics
evaluations = [QCEvaluation(), ...]

# Build your QualityControl object
qc = QualityControl(evaluations=evaluations)

qc.write_standard_file()
```

**Alternate workflow**

If need to build evaluations for a _different_ data asset, for example making evaluations for a primary data asset that you are derived from, but need to be attached to that original asset, then you need to set the `asset_id` field of each QCEvaluation. There is an `aind-data-access-api` function that can help you pull all the relevant `QCEvaluation` objects for a specific `_id`. Note that you can point the `asset_id` field at _any_ asset, so your capsule does not need to be directly linked to a particular primary data asset to generate evaluations for it.

### QC Portal

The QC Portal is a web application that allows users to view and interact with the AIND QC metadata and to annotate ``PENDING`` metrics with qualitative evaluations. The portal is maintained by scientific computing, reach out to us with any questions or concerns.

The portal works by pulling the metadata object from the Document Database (DocDB). When you make changes to metrics or add notes the **submit** button will be enabled, submitting pushes your updates to the DocDB along with a timestamp and your name.

**Q: When does the state get set for the QualityControl and QCEvaluation objects?**

The QC portal automatically calls ``QualityControl.evaluate_status()`` whenever you submit changes to the metrics. Note that while it's possible to evaluate the status of ``QCEvaluation`` objects directly, this could lead to inconsistencies in the overall status of the ``QualityControl`` object.

**Q: How do reference URLs get pulled into the QC Portal?**

Each metric is associated with a reference figure, image, or video. The QC portal can interpret four ways of setting the reference field:

- Provide a relative path to a file in this data asset's S3 bucket
- Provide a full path to a file in a different S3 bucket (starting with "s3://")
- Provide a url to a file (starting with "http://" or "https://")
- Provide the name of one of the interactive plots, e.g. "ecephys-drift-map"

There are many situations where it's helpful to be able to "swipe" between two images. If you have two identical images separated by a ';' the portal will allow users to swipe between them. For example, you might show snippets of the raw electrophysiology raster with detected spikes overlaid on the swipe.

**Q: I saw fancy things like dropdowns in the QC Portal, how do I do that?**

By default the QC portal displays dictionaries as tables where the values can be edited. We also support a few special cases to allow a bit more flexibility or to constrain the actions that manual annotators can take. Install the `aind-qcportal-schema` package and set the `value` field to the corresponding pydantic object to use these. 