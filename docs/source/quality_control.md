# Quality control

## Overview

Quality control is a collection of **evaluations** based on sets of **metrics** about the data. 

`QCEvaluation`s should be generated during pipelines: before raw data upload, during processing, and during analysis by researchers.

The overall `QualityControl`, each `QCEvaluation`, and each `QCMetric` can be evaluated to get a `aind_data_schema.quality_control.State` which indicates whether the Overall QC/Evaluation/Metric passes, fails, or is in a pending state waiting for manual annotation.

The state of an evaluation is set automatically to the lowest of its metric's states. A single failed metric sets an entire evaluation to fail. A single pending metric (with all other metrics passing) sets an entire evaluation to pending. An optional setting `QCEvaluation.allow_failed_metrics` allows you to ignore failures, which can be useful in situations where an evaluation is not critical for quality control.

## Details

**Q: What is an evaluation?**

Each `QCEvaluation` should be thought of as a single aspect of the data asset, from one `Modality`, that is evaluated for quality at a specific `Stage` in data acquisition or analysis. For example, the brain moves a small amount during electrophysiology. This evaluation would be marked with `Stage:RAW` and `Modality:ECEPHYS`. Evaluations will often consist of multiple metrics, some of which can be measured and evaluated automatically, as well as qualititative metrics that need to be evaluated by a human observer.

The state of an evaluation depends on the state of its metrics according to these rules:

- If any metric fails the evaluation fails (except when `allow_failed_metrics=True`, see below)
- If any metric is pending and the rest pass the evaluation is pending
- If all metrics pass the evaluation passes

There are many situations where quality control is evaluated on an aspect of the data that isn't critical to the overall experimental goals. For example, you may have a `QCEvaluation` that checks whether the temperature and humidity sensors on the rig were functional, but the overall analysis can proceed with or without the these data. In these situations set `QCEvaluation.allow_failed_metrics=True` to allow the evaluation to pass even if these sensors actually failed. This ensures that the overall `QualityControl` for the data asset can also pass, without regard to these optional elements of the data. 

**Q: What is a metric?**

Each `QCMetric` is a single value or set of values that can be computed, or observed, about a set of data as part of an evaluation. These can have any type. See the AIND section for special rules for annotating metrics with options.

`QCMetric`s have a `Status`. The `Status` should depend directly on the `QCMetric.value`, either by a simple function: "value>5", or by a qualitative rule: "Field of view includes visual areas". The `QCMetric.description` field should be used to describe the rule used to set the status. Metrics can be evaluated multiple times, in which case the new status should be appended the `QCMetric.status_history`.

**Q: What is a metric reference?**

Metrics should include a `QCMetric.reference`. References are intended to be publicly accessible images, figures, combined figures with multiple panels, or videos that support the metric or provide information necessary for manual annotation of a metric's status.

See the AIND section for specifics about how references are rendered in the QC Portal.

**Q: What are the status options for metrics?**

In our quality control a metric's status is always `PASS`, `PENDING` (waiting for manual annotation), or `FAIL`.

We enforce this minimal set of states to prevent ambiguity and make it easier to build tools that can interpret the status of a data asset.

## Details for AIND users

Instructions for uploading QC for viewing in the QC portal can be found [here](https://github.com/AllenNeuralDynamics/aind-qc-portal).

### Multi-asset QC

During analysis there are many situations where multiple data assets need to be pulled together, often for comparison. For example, FOVs across imaging sessions or recording sessions from a chronic probe might need to get matched up across days. When a `QCEvaluation` is being calculated from multiple assets it should be tagged with `Stage:MULTI_ASSET` and each of its `QCMetric` objects needs to track the assets that were used to generate that metric in the `evaluated_assets` list.

**Q: Where do I store multi-asset QC?**

You should follow the preferred/alternate workflows described above. If your multi-asset analysis pipeline generates a new data asset, put the QC there. If your pipeline does not generate an asset, push a copy of each `QCEvaluation` back to **each** individual data asset.

**Q: I want to be able to store data about each of the evaluated assets in this metric**

Take a look at the `MultiAssetMetric` class in `aind-qc-portal-schema`. It allows you to pass a list of values which will be matched up with the `evaluated_assets` names. You can also include options which will appear as dropdowns or checkboxes.