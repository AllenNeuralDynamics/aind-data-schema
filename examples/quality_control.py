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
    "options": ["No Drift", "Drift visible in part of session", "Drift visible in entire session", "Sudden movement event"],
    "status": ["Pass", "Pass", "Fail", "Fail"],
    "type": "checkbox",
}

eval0 = QCEvaluation(
    name="Drift map",
    description="Check that all probes show minimal drift",
    modality=Modality.ECEPHYS,
    stage=Stage.RAW,
    metrics=[
        QCMetric(
            name="Probe A drift",
            description="Qualitative check that drift map shows minimal movement",
            value=drift_value_with_options,
            reference="ecephys-drift-map",
            status_history=[sp],
        ),
        QCMetric(
            name="Probe B drift",
            description="Qualitative check that drift map shows minimal movement",
            value=drift_value_with_flags,
            reference="ecephys-drift-map",
            status_history=[sp],
        ),
        QCMetric(name="Probe C drift", value="Low", reference="ecephys-drift-map", status_history=[s]),
    ],
    notes="",
)

eval1 = QCEvaluation(
    name="Video frame count check",
    modality=Modality.BEHAVIOR_VIDEOS,
    stage=Stage.RAW,
    metrics=[
        QCMetric(
            name="Expected frame count",
            description="Expected frame count from experiment length, always pass",
            value=662,
            status_history=[s]
        ),
        QCMetric(
            name="Video 1 frame count",
            description="Pass when frame count matches expected",
            value=662,
            status_history=[s]
        ),
        QCMetric(
            name="Video 2 num frames",
            description="Pass when frame count matches expected",
            value=662, 
            status_history=[s]),
    ],
)

eval2 = QCEvaluation(
    name="Probes present",
    description="Pass when data from a probe is present",
    modality=Modality.ECEPHYS,
    stage=Stage.RAW,
    metrics=[
        QCMetric(name="ProbeA", value=True, status_history=[s]),
        QCMetric(name="ProbeB", value=True, status_history=[s]),
        QCMetric(name="ProbeC", value=True, status_history=[s]),
    ],
)

q = QualityControl(evaluations=[eval0, eval1, eval2])

# This is a special call that needs to be made to populate the .overall_status and .evaluation_status properties
# Note that the timestamp is set here because of how examples testing works, in general you should not set the
# timestamp manually

serialized = q.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
q.write_standard_file()
