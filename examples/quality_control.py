"""Example quality control processing"""

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QualityControl, QCMetric, Stage, Status, QCStatus

t = datetime(2022, 11, 22, 0, 0, 0, tzinfo=timezone.utc)

s = QCStatus(evaluator="Automated", status=Status.PASS, timestamp=t)
sp = QCStatus(evaluator="", status=Status.PENDING, timestamp=t)

# Example of how to use a dictionary to provide options for a metric in the QC portal
drift_value_with_options = {
    "value": "",
    "options": ["Low", "Medium", "High"],
    "status": [
        "Pass",
        "Fail",
        "Fail",
    ],  # when set, this field will be used to automatically parse the status, blank forces manual update
    "type": "dropdown",
}

# Example of how to use a dictionary to provide multiple checkable flags, some of which will fail the metric
drift_value_with_flags = {
    "value": "",
    "options": [
        "No Drift",
        "Drift visible in part of acquisition",
        "Drift visible in entire acquisition",
        "Sudden movement event",
    ],
    "status": ["Pass", "Pass", "Fail", "Fail"],
    "type": "checkbox",
}

metrics = [
    QCMetric(
        name="Probe A drift",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        description="Pass when drift map shows minimal movement",
        value=drift_value_with_options,
        reference="ecephys-drift-map",
        status_history=[sp],
        tags={
            "probe": "Probe A",
        },
    ),
    QCMetric(
        name="Probe B drift",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        description="Pass when drift map shows minimal movement",
        value=drift_value_with_flags,
        reference="ecephys-drift-map",
        status_history=[sp],
        tags={
            "probe": "Probe B",
        },
    ),
    QCMetric(
        name="Probe C drift",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        description="Pass when drift map shows minimal movement",
        value="Low",
        reference="ecephys-drift-map",
        status_history=[s],
        tags={
            "probe": "Probe C",
        },
    ),
    QCMetric(
        name="ProbeA",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        description="Pass when probe is present in the recording",
        value=True,
        status_history=[s],
        tags={
            "probe": "Probe A",
        },
    ),
    QCMetric(
        name="ProbeB",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        description="Pass when probe is present in the recording",
        value=True,
        status_history=[s],
        tags={
            "probe": "Probe B",
        },
    ),
    QCMetric(
        name="ProbeC",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        description="Pass when probe is present in the recording",
        value=True,
        status_history=[s],
        tags={
            "probe": "Probe C",
        },
    ),
    QCMetric(
        name="Video 1 frame count",
        modality=Modality.BEHAVIOR_VIDEOS,
        stage=Stage.RAW,
        description="Pass when frame count matches expected",
        value=662,
        status_history=[s],
        tags={
            "video": "Video 1",
        },
    ),
    QCMetric(
        name="Video 2 num frames",
        modality=Modality.BEHAVIOR_VIDEOS,
        stage=Stage.RAW,
        description="Pass when frame count matches expected",
        value=662,
        status_history=[s],
        tags={
            "video": "Video 2",
        },
    ),
]

q = QualityControl(
    metrics=metrics,
    # in visualizations split first by modality, then by probe / video tags
    default_grouping=["modality", ("probe", "video")],
    # allow any metrics with tag video: Video 2 to fail without failing overall QC
    allow_tag_failures=["Video 2"],
)

if __name__ == "__main__":
    serialized = q.model_dump_json()
    deserialized = QualityControl.model_validate_json(serialized)
    q.write_standard_file()
