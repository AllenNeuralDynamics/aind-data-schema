"""Example quality control processing"""

from datetime import datetime

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.brain_atlas import CCFStructure

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status, QCStatus

eval0 = QCEvaluation(
    name="N001",
    description="Manual reconstruction of neuron",
    modality=Modality.SPIM,
    stage=Stage.ANALYSIS,
    metrics=[
        QCMetric(
            name="Horta coordinates",
            description="AP/ML/DV coordinates in Horta space",
            value={
                "ML": 28698.816,
                "AP": 10885.395,
                "DV": 11673.58,
            },
            status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        ),
        QCMetric(
            name="CCF coordinate",
            description="AP/ML/DV coordinate in CCFv3",
            value={
                "ML": 5923.0438,
                "AP": 4270.0208,
                "DV": 6984.054
            },
            status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        ),
        QCMetric(
            name="CCF soma compartment",
            description="Location of soma in CCF space",
            value=CCFStructure.RT,
            status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        ),
        QCMetric(
            name="Manual estimate soma compartment",
            description="Unknown",
            value=CCFStructure.AV,
            status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        ),
        QCMetric(
            name="Soma group",
            description="Unknown",
            value="Thalamus",
            status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        ),
    ],
    created=datetime(2024, 7, 12),
)

eval1 = QCEvaluation(
    name="N002",
    description="Manual reconstruction of neuron",
    modality=Modality.SPIM,
    stage=Stage.ANALYSIS,
    metrics=[
        QCMetric(
            name="Horta coordinates",
            description="AP/ML/DV coordinates in Horta space",
            value={
                "ML": 28531.45,
                "AP": 11628.111,
                "DV": 16348.68,
            },
            status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        ),
        QCMetric(
            name="CCF coordinate",
            description="AP/ML/DV coordinate in CCFv3",
            value={
                "ML": 5936.695,
                "AP": 4076.2764,
                "DV": 5190.3741,
            },
            status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        ),
        QCMetric(
            name="CCF soma compartment",
            description="Location of soma in CCF space",
            value=CCFStructure.PT,
            status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        ),
        QCMetric(
            name="Manual estimate soma compartment",
            description="Unknown",
            value=CCFStructure.AV,
            status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        ),
        QCMetric(
            name="Soma group",
            description="Unknown",
            value="Thalamus",
            status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        )
    ],
    created=datetime(2024, 7, 11),
)

q = QualityControl(evaluations=[eval0, eval1])

# This is a special call that needs to be made to populate the .overall_status and .evaluation_status properties
# Note that the timestamp is set here because of how examples testing works, in general you should not set the
# timestamp manually

serialized = q.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
q.write_standard_file(prefix="exaspim")
