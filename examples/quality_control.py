"""Example quality control processing"""

from datetime import date

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric

t = date(2022, 11, 22)

q = QualityControl(
    overall_status="Pass",
    overall_status_date=t,
    evaluations=[
        QCEvaluation(
            evaluation_modality=Modality.BEHAVIOR_VIDEOS,
            evaluation_stage="Data acquisition: video frame count check",
            evaluator_full_name="Fred Flinstone",
            evaluation_date=t,
            qc_metrics=[
                QCMetric(
                    name="video_1_num_frames",
                    value=662
                ),
                QCMetric(
                    name="video_2_num_frames",
                    value=662
                )
            ],
            stage_status="Pass",
            notes="Pass when video_1_num_frames==video_2_num_frames"
        ),
        QCEvaluation(
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage="Data acquisition: probes present",
            evaluator_full_name="Automated",
            evaluation_date=t,
            qc_metrics=[
                QCMetric(
                    name="ProbeA_success",
                    value=True
                ),
                QCMetric(
                    name="ProbeB_success",
                    value=True
                ),
                QCMetric(
                    name="ProbeC_success",
                    value=True
                )
            ],
            stage_status="Pass",
        ),
    ],
)

serialized = q.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
q.write_standard_file()
