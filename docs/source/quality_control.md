# Quality control

## Overview

Quality control is a collection of **evaluations** based on sets of **metrics** about the data. 

`QCEvaluation`s should be generated during pipelines: before raw data upload, during processing, and during analysis by researchers.

Each `QualityControl`, `QCEvaluation`, and `QCMetric` includes a `aind_data_schema.quality_control.State` which is a timestamped object indicating that the Overall QC/Evaluation/Metric passes, fails, or is in a pending state waiting for manual annotation.

The state of an evaluation is set automatically to the lowest of its metric's states. A single failed metric sets an entire evaluation to fail. While a single pending metric (with all other metrics passing) sets an entire evaluation to pending. An optional setting `QCEvaluation.allow_failed_metrics` allows you to ignore failures, which can be useful in situations where an evaluation is not critical for quality control.

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

Metrics should include a `QCMetric.reference`. References are intended to be publicly accessible images, figures, combined figures with multiple panels, or videos that support the metric or provide information necessary for manual annotation of a metric's status.

**Q: What are the status options for metrics?**

In our quality control a metric's status is always `PASS`, `PENDING` (waiting for manual annotation), or `FAIL`. `PENDING` should be used when a user must manually annotated the metric's state.

We enforce this minimal set of states to prevent ambiguity and make it easier to build tools that can interpret the status of a data asset.

## Details for AIND users

### Uploading QC

#### Preferred workflow 

**Metadata**

If you are building `QCEvaluation` and `QCMetric` objects prior to raw data upload or in a capsule alongside your processing or analysis, your workflow is: 

```
from aind_data_schema.core.quality_control import QualityControl

# Build your QCEvaluations and metrics
evaluations = [QCEvaluation(), ...]

# Build your QualityControl object
qc = QualityControl(evaluations=evaluations)

qc.write_standard_file()
```

The indexer will pick up this file alongside the other metadata files and handle it appropriately.

**References**

Each `QCMetric` you build should have an attached reference. Our preference is that you post these images to [FigURL](https://github.com/flatironinstitute/figurl/blob/main/doc/intro.md) and put the generated URL into the reference.

We recommend that you write PNG files for images and static multi-panel figures, MP4 files for videos, and Altair charts for interactive figures.

#### Alternate workflows

**Metadata**

We'll post documentation on how to append `QCEvaluations` to pre-existing quality_control.json files, via DocDB using the `aind-data-access-api`, in the future. For now, you can refer to the code snippet in the [`aind-qc-capsule-example`](https://github.com/AllenNeuralDynamics/aind-qc-capsule-example/).

**References**

You can also place the references in the data asset itself, to do this include the relative path "qc_images/your_image.png" to that asset inside of the results folder.

### QC Portal

The QC Portal is a browser application that allows users to view and interact with the AIND QC metadata and to annotate ``PENDING`` metrics with qualitative evaluations. The portal is maintained by scientific computing, reach out to us with any questions or concerns.

The portal works by pulling the metadata object from the Document Database (DocDB). When you make changes to metrics or add notes the **submit** button will be enabled, submitting pushes your updates to the DocDB along with a timestamp and your name.

**Q: When does the state get set for the QCEvaluation and QualityControl objects?**

The QC portal automatically calls ``QualityControl.evaluate_status()`` whenever you submit changes to the metrics. This first evaluates the individual `QCEvaluation` objects, and then evaluates the overall status.

**Q: How do reference URLs get pulled into the QC Portal?**

Each metric is associated with a reference figure (PDF preferred), image (png preferred), or video (mp4 preferred). The QC portal can interpret four ways of setting the reference field:

- Provide a relative path to a file in this data asset's S3 bucket, i.e. "figures/my_figure.png". The mount/asset name should not be included.
- Provide a url to a FigURL figure
- Provide the name of one of the interactive plots, e.g. "ecephys-drift-map"

**Q: I saw fancy things like dropdowns in the QC Portal, how do I do that?**

By default the QC portal displays dictionaries as tables where the values can be edited. We also support a few special cases to allow a bit more flexibility or to constrain the actions that manual annotators can take. Install the [`aind-qcportal-schema`](https://github.com/AllenNeuralDynamics/aind-qcportal-schema/blob/dev/src/aind_qcportal_schema/metric_value.py) package and set the `value` field to the corresponding pydantic object to use these. 

### Multi-asset QC

During analysis there are many situations where multiple data assets need to be pulled together, often for comparison. For example, FOVs across imaging sessions or recording sessions from a chronic probe might need to get matched up across days. When a `QCEvaluation` is being calculated from multiple assets it should be tagged with `Stage:MULTI_ASSET` and each of its `QCMetric` objects needs to track the assets that were used to generate that metric in the `evaluated_assets` list.

**Q: Where do I store multi-asset QC?**

You should follow the preferred/alternate workflows described above. If your multi-asset analysis pipeline generates a new data asset, put the QC there. If your pipeline does not generate an asset, push a copy of each `QCEvaluation` back to **each** individual data asset.

**Q: I want to be able to store data about each of the evaluated assets in this metric**

Take a look at the `MultiAssetMetric` class in `aind-qc-portal-schema`. It allows you to pass a list of values which will be matched up with the `evaluated_assets` names. You can also include options which will appear as dropdowns or checkboxes. 