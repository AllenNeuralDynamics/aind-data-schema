"""Example quality control processing"""

from datetime import date

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status

t = date(2022, 11, 22)

eval0 = QCEvaluation(
    evaluation_name="Drift map",
    evaluation_description="Qualitative check that drift map shows minimal movement",
    evaluation_modality=Modality.ECEPHYS,
    evaluation_stage=Stage.PROCESSING,
    evaluator="Fred Flintstone",
    evaluation_date=t,
    qc_metrics=[
        QCMetric(name="Probe A drift", value="High"),
        QCMetric(name="Probe B drift", value="Low"),
        QCMetric(name="Probe C drift", value="Low"),
    ],
    stage_status=Status.FAIL,
    notes="Manually annotated: failed due to high drift on probe A",
)

eval1 = QCEvaluation(
    evaluation_name="Video frame count check",
    evaluation_modality=Modality.BEHAVIOR_VIDEOS,
    evaluation_stage=Stage.RAW,
    evaluator="Fred Flinstone",
    evaluation_date=t,
    qc_metrics=[QCMetric(name="video_1_num_frames", value=662), QCMetric(name="video_2_num_frames", value=662)],
    stage_status=Status.PASS,
    notes="Pass when video_1_num_frames==video_2_num_frames",
)

eval2 = QCEvaluation(
    evaluation_name="Probes present",
    evaluation_modality=Modality.ECEPHYS,
    evaluation_stage=Stage.RAW,
    evaluator="Automated",
    evaluation_date=t,
    qc_metrics=[
        QCMetric(name="ProbeA_success", value=True),
        QCMetric(name="ProbeB_success", value=True),
        QCMetric(name="ProbeC_success", value=True),
    ],
    stage_status=Status.PASS,
)

q = QualityControl(overall_status="Pass", overall_status_date=t, evaluations=[eval0, eval1, eval2])

serialized = q.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
q.write_standard_file()
