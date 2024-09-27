# Quality control

## Overview

Quality control is a collection of **evaluations** based on sets of **metrics** about the data. As a user, you build a `QualityControl` object and append `QCEvaluation`s to it, each of which contains one or more `QCMetric`s

Each `QualityControl`, `QCEvaluation`, and `QCMetric` includes a `aind_data_schema.quality_control.State` which is a timestamped object indicating that the QC/Evaluation/Metric passes, fails, or is in a pending state waiting for manual annotation.

The state of an evaluation is set automatically to the lowest of its metric's states. A single failed metric sets an entire evaluation to fail. While a single pending metric (with all other metrics passing) sets an entire evaluation to pending. An optional setting `QCEvaluation.allow_failed_metrics` allows you to ignore failures, which can be useful in situations where an evaluation is not critical for quality control (for example: a camera feed that often has failures but which don't affect the rest of the experiment).

## Details

**Q: What is an evaluation?**

Each `QCEvaluation` should be thought of as a single aspect of the data asset that can be evaluated. For example, the brain might moves a small amount during both electrophysiology and optical recordings. This drift can be measured by various automated quantiative metrics, as well as qualititative metrics evaluated by a human observer. The state of an evaluation depends on the state of its metrics according to these rules:

- If all metrics pass the evaluation passes
- If any metric fails the evaluation fails (unless the `allow_failed_metrics` flag is set)
- If any metric is pending (and the rest pass) the evaluation is pending

Make sure to annotate `QCEvaluation`s with the `Stage` and `Modality` they are related to. In the quality control apps we separate metrics by these attributes.

**Q: What is a metric?**

A metric is any single value or set of values that can be computed, or observed, about a set of data as part of an evaluation. These can have any type, but the QC apps that scientific computing supports expect you to use metrics that are numerical, string, bool, or arrays/dictionaries of these values.

Metrics also have a status which is set by a rule, usually some function of the metric value. The rule should be encoded in the metric description. The metric status should also include both the evaluator (``"automated"`` or the evaluator's full name) and be timestamped. Metrics can be evaluated multiple times or have their status overridden by ressearchers, in which case the new status will be appended the `QCMetric.metric_status_history`. The latest status can be retrived by using `QCMetric.metric_status`.

Each metric should also include a `QCMetric.reference`. References are intended to be images, figures, or videos that support the metric or provide information necessary for manual annotation of a metric's status. There are four ways to set the reference field:

- Provide a relative path to a file in an S3 bucket
- Provide a full path to a file in an S3 bucket (starting with "s3://")
- Provide a url to a file (starting with "http://" or "https://")
- Provide the name of one of the interactive plots, e.g. "ecephys-drift-map"

**Q: What are the status options for metrics?**

In our quality control a metric's status is always PASS, PENDING (waiting for manual annotation), or FAIL. When passing or failing assets the *rule* used to make that determination should be included in the `QCMetric` description. PENDING is used when the QC evaluation is not yet complete.

We enforce this minimal set of states to prevent ambiguity and make it easier to build tools that can interpret the status of a data asset.

## Details for AIND users

### QC Portal

The QC Portal is a web application that allows users to view and interact with the QC metadata and to annotate ``PENDING`` metrics with qualitative evaluations. The portal is in testing, please get in touch with Dan to work on getting your data into the appropriate format.

The portal works by pulling the metadata object from the Document Database (DocDB). Updates to the metadata are pushed up to DocDB when users submit their changes.

**Q: How do reference URLs get pulled into the QC Portal?**

Each metric can be associated with a single reference URL, pointing to an image file (ideally SVG or PNG) or to the name of an interactive plot.

For URLs you can provide the path in three ways:

- You can provide the relative path in the results folder and we can have the qc app look up the file path from the rest of the metadata
- The full path to the S3 bucket with the image S3://...etc...
- The path to an external image http://...etc...

For interactive plots you simply provide the plot name, e.g. "ecephys-drift-map". Please see the repository for the full list of interactive plots (src/aind-qc-portal/interactive-plots/)

**Q: When does the state get set for the QualityControl and QCEvaluation objects?**

The QC portal automatically calls ``QualityControl.evaluate_status()`` whenever you submit changes to the metrics. Note that while it's possible to evaluate the status of ``QCEvaluation`` objects directly, this could lead to inconsistencies in the overall status of the ``QualityControl`` object.
