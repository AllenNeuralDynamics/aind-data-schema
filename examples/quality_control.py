"""Example quality control processing"""

from datetime import datetime

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status, QCStatus

t = datetime(2022, 11, 22, 0, 0, 0)

s = QCStatus(evaluator="Bob", status=Status.PASS, timestamp=t)

eval0 = QCEvaluation(
    evaluation_name="Drift map",
    evaluation_description="Qualitative check that drift map shows minimal movement",
    evaluation_modality=Modality.ECEPHYS,
    evaluation_stage=Stage.PROCESSING,
    qc_metrics=[
        QCMetric(name="Probe A drift", value="High", reference="ecephys-drift-map", metric_status_history=[s]),
        QCMetric(name="Probe B drift", value="Low", reference="ecephys-drift-map", metric_status_history=[s]),
        QCMetric(name="Probe C drift", value="Low", reference="ecephys-drift-map", metric_status_history=[s]),
    ],
    notes="Manually annotated: failed due to high drift on probe A",
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
