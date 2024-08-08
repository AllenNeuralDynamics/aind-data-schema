from datetime import date

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QualityControl, QCEvaluation

t = date(2022, 11, 22)

q = QualityControl(
    overall_status="Pass",
    overall_status_date=t,
    evaluations=[
        QCEvaluation(
            evaluation_modality=Modality.BEHAVIOR_VIDEOS,
            evaluation_stage="Data acquisition",
            evaluator_full_name="Fred Flinstone",
            evaluation_date=t,
            qc_metrics={
                "Video_1_num_frames": 662,
                "Video_2_num_frames": 662,
                "Frame_match": True,
            },
            stage_status="Pass",
        ),
        QCEvaluation(
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage="Data acqusition",
            evaluator_full_name="Fred Flinstone",
            evaluation_date=t,
            qc_metrics={
                "ProbeA_success": True,
                "ProbeB_success": True,
                "ProbeC_success": False,
            },
            stage_status="Pass",
        )
    ]
)

serialized = q.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
q.write_standard_file()
