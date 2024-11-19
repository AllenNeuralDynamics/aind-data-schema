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

**Q: What is a metric reference?**

Metrics should include a `QCMetric.reference`. References are intended to be publicly accessible images, figures, combined figures with multiple panels, or videos that support the metric or provide information necessary for manual annotation of a metric's status.

See the AIND section for specifics about how references are rendered in the QC Portal.

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

#### Alternate workflow

In the event that you aren't generating a data asset, for example when running a QC capsule for an existing raw data asset, you will need to push your QCEValuation objects to DocDB directly and push your figures to kachery-cloud (aka FigURL).

**Metadata**

For now, you can refer to the code snippet in the [`aind-qc-capsule-example`](https://github.com/AllenNeuralDynamics/aind-qc-capsule-example/). You'll need your DocDB asset ID. To get this you can run this snippet of code using the name of your data asset:

```{python}
from aind_data_access_api.document_db import MetadataDbClient

API_GATEWAY_HOST = "api.allenneuraldynamics.org"
DATABASE = "metadata_index"
COLLECTION = "data_assets"

docdb_api_client = MetadataDbClient(
  host=API_GATEWAY_HOST,
  database=DATABASE,
  collection=COLLECTION,
)

ASSET_NAME = "behavior_711042_2024-08-07_12-20-41"

filter_query = {"name": ASSET_NAME}
projection = {"_id": 1}
response = docdb_api_client.retrieve_docdb_records(
  filter_query=filter_query,
  projection=projection,
)

id = response[0]["_id"]
```

We'll post documentation on how to append `QCEvaluations` to pre-existing quality_control.json files, via DocDB using the `aind-data-access-api`, in the future.

**References**

In the alternate workflow you won't generate a data asset. This means you need to upload your figures to an external server. We use `kachery-cloud` for this purpose. `pip install kachery-cloud`

When running in a Code Ocean capsule you will need kachery credentials. You can temporarily attach personal credentials by running `kachery-cloud-init` in a terminal and logging into Github or using a personal access token. For pipeline runs you need to ask Dan to attach the AIND credentials to your capsule. Once you have credentials:

```{python}
import kachery_cloud as kcl
from pathlib import Path

filename = '/path/to/filename.dat'
uri = kcl.store_file(filename)

QCMetric.reference = uri + Path(filename).suffix
```

### QC Portal

The QC Portal is a browser application that allows users to view and interact with the AIND QC metadata and to annotate ``PENDING`` metrics with qualitative evaluations. The portal is maintained by scientific computing, reach out to us with any questions or concerns.

The portal works by pulling the metadata object from the Document Database (DocDB). When you make changes to metrics or add notes the **submit** button will be enabled, submitting pushes your updates to the DocDB along with a timestamp and your name.

**Q: When does the state get set for the QCEvaluation and QualityControl objects?**

The QC portal automatically calls ``QualityControl.evaluate_status()`` whenever you submit changes to the metrics. This first evaluates the individual `QCEvaluation` objects, and then evaluates the overall status.

**Q: How do reference URLs get pulled into the QC Portal?**

Each metric is associated with a reference figure. We support:

- Vector files (svg, pdf)
- Images (png, jpg, etc)
- Videos (mp4)
- Neuroglancer links (url)
- Rerun files (rrd)

Figures, images, and videos can be any size, but they will fit best on the screen if they are landscape and shaped roughly like a computer screen (for example, 1280×800 or 1900×1200 px).

You can link to your references in one of four ways:

- Provide a relative path to a file in the data asset's S3 bucket, i.e. "figures/my_figure.png". The mount/asset name should not be included.
- Provide a url to a publicly accessible file, i.e. "https://mywebsite.com/myfile.png"
- Provide a path to any public S3 bucket, i.e. "s3://bucket/myfile.png"
- Provide a FigURL/kachery-cloud hash, i.e. "sha1://uuid.ext", note that only for FigURL hashes you **must append the filetype**. The hash only doesn't tell us what type of file will be returned.

**Q: I saw fancy things like dropdowns in the QC Portal, how do I do that?**

By default the QC portal displays dictionaries as tables where the values can be edited. We also support a few special cases to allow a bit more flexibility or to constrain the actions that manual annotators can take. Install the [`aind-qcportal-schema`](https://github.com/AllenNeuralDynamics/aind-qcportal-schema/blob/dev/src/aind_qcportal_schema/metric_value.py) package and set the `value` field to the corresponding pydantic object to use these. Current options include:

- Dropdowns (optionally the options can auto-set the value)
- Checkboxes (again options can auto-set the value)
- Rule-based metrics (the rule is automatically run to set the value)
- Multi-asset metrics where each asset is assigned it's own value

There are also some custom rules for the value field. If you provide:

- Two strings separated by a semicolon `;` they will be displayed in a "Swipe" pane that lets you swipe back and forth between the two things. Mostly useful for overlay images.
- A dictionary where every value is a list of equal length, it will be displayed as a table where the keys are column headers and the values are rows. If a key "index" is included the values will be used to name the rows.

### Multi-asset QC

During analysis there are many situations where multiple data assets need to be pulled together, often for comparison. For example, FOVs across imaging sessions or recording sessions from a chronic probe might need to get matched up across days. When a `QCEvaluation` is being calculated from multiple assets it should be tagged with `Stage:MULTI_ASSET` and each of its `QCMetric` objects needs to track the assets that were used to generate that metric in the `evaluated_assets` list.

**Q: Where do I store multi-asset QC?**

You should follow the preferred/alternate workflows described above. If your multi-asset analysis pipeline generates a new data asset, put the QC there. If your pipeline does not generate an asset, push a copy of each `QCEvaluation` back to **each** individual data asset.

**Q: I want to be able to store data about each of the evaluated assets in this metric**

Take a look at the `MultiAssetMetric` class in `aind-qc-portal-schema`. It allows you to pass a list of values which will be matched up with the `evaluated_assets` names. You can also include options which will appear as dropdowns or checkboxes.
