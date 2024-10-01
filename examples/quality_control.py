"""Example quality control processing"""

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status, QCStatus

t = datetime(2022, 11, 22, 0, 0, 0, tzinfo=timezone.utc)

s = QCStatus(evaluator="Automated", status=Status.PASS, timestamp=t)
sp = QCStatus(evaluator="", status=Status.PENDING, timestamp=t)

# Example of how to use a dictionary to provide options a metric
drift_value_with_options = {
    "value": "",
    "options": ["Low", "Medium", "High"],
    "status": [
        "Pass",
        "Fail",
        "Fail",
    ],  # when set, this field will be used to automatically parse the status, blank forces manual update
    "type": "dropdown",  # other type options: "checkbox"
}

# Example of how to use a dictionary to provide multiple checkable flags, some of which will fail the metric
drift_value_with_flags = {
    "value": "",
    "options": ["Drift visible in entire session", "Drift visible in part of session", "Sudden movement event"],
    "status": ["Fail", "Pass", "Fail"],
    "type": "checkbox",
}

eval0 = QCEvaluation(
    evaluation_name="Drift map",
    evaluation_description="Qualitative check that drift map shows minimal movement",
    evaluation_modality=Modality.ECEPHYS,
    evaluation_stage=Stage.RAW,
    qc_metrics=[
        QCMetric(
            name="Probe A drift",
            value=drift_value_with_options,
            reference="ecephys-drift-map",
            metric_status_history=[sp],
        ),
        QCMetric(
            name="Probe B drift",
            value=drift_value_with_flags,
            reference="ecephys-drift-map",
            metric_status_history=[sp],
        ),
        QCMetric(name="Probe C drift", value="Low", reference="ecephys-drift-map", metric_status_history=[s]),
    ],
    notes="",
)

eval1 = QCEvaluation(
    evaluation_name="Video frame count check",
    evaluation_modality=Modality.BEHAVIOR_VIDEOS,
    evaluation_stage=Stage.RAW,
    qc_metrics=[
        QCMetric(name="video_1_num_frames", value=662, metric_status_history=[s]),
        QCMetric(name="video_2_num_frames", value=662, metric_status_history=[s]),
    ],
    notes="Pass when video_1_num_frames==video_2_num_frames",
)

eval2 = QCEvaluation(
    evaluation_name="Probes present",
    evaluation_modality=Modality.ECEPHYS,
    evaluation_stage=Stage.RAW,
    qc_metrics=[
        QCMetric(name="ProbeA_success", value=True, metric_status_history=[s]),
        QCMetric(name="ProbeB_success", value=True, metric_status_history=[s]),
        QCMetric(name="ProbeC_success", value=True, metric_status_history=[s]),
    ],
)

q = QualityControl(evaluations=[eval0, eval1, eval2])

# This is a special call that needs to be made to populate the .overall_status and .evaluation_status properties
# Note that the timestamp is set here because of how examples testing works, in general you should not set the
# timestamp manually
q.evaluate_status(timestamp=t)

serialized = q.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
q.write_standard_file()
