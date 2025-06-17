"""Example quality control processing"""

from datetime import datetime

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.brain_atlas import CCFv3

from aind_data_schema.core.quality_control import QualityControl, QCMetric, Stage, Status, QCStatus

metrics = [
    # N001 metrics
    QCMetric(
        name="Sample coordinates",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="AP/ML/DV coordinates in sample space",
        value={
            "ML": 28698.816,
            "AP": 10885.395,
            "DV": 11673.58,
        },
        status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        tags=["N001", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="CCF coordinate",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="AP/ML/DV coordinate in CCFv3",
        value={"ML": 5923.0438, "AP": 4270.0208, "DV": 6984.054},
        status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        tags=["N001", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="CCF soma compartment",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="Location of soma in CCF space",
        value=CCFv3.RT,
        status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        tags=["N001", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="Manual estimate soma compartment",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="Unknown",
        value=CCFv3.AV,
        status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        tags=["N001", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="Soma group",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="Unknown",
        value="Thalamus",
        status_history=[QCStatus(evaluator="Shirali Amin", status=Status.PASS, timestamp=datetime(2024, 7, 12))],
        tags=["N001", "Manual reconstruction of neuron"],
    ),
    # N002 metrics
    QCMetric(
        name="Sample coordinates",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="AP/ML/DV coordinates in sample space",
        value={
            "ML": 28531.45,
            "AP": 11628.111,
            "DV": 16348.68,
        },
        status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        tags=["N002", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="CCF coordinate",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="AP/ML/DV coordinate in CCFv3",
        value={
            "ML": 5936.695,
            "AP": 4076.2764,
            "DV": 5190.3741,
        },
        status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        tags=["N002", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="CCF soma compartment",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="Location of soma in CCF space",
        value=CCFv3.PT,
        status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        tags=["N002", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="Manual estimate soma compartment",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="Unknown",
        value=CCFv3.AV,
        status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        tags=["N002", "Manual reconstruction of neuron"],
    ),
    QCMetric(
        name="Soma group",
        modality=Modality.SPIM,
        stage=Stage.ANALYSIS,
        description="Unknown",
        value="Thalamus",
        status_history=[QCStatus(evaluator="Harsh Solanki", status=Status.PASS, timestamp=datetime(2024, 7, 11))],
        tags=["N002", "Manual reconstruction of neuron"],
    ),
]

quality_control = QualityControl(metrics=metrics, default_grouping=["N001", "N002", "Manual reconstruction of neuron"])

serialized = quality_control.model_dump_json()
deserialized = QualityControl.model_validate_json(serialized)
quality_control.write_standard_file(prefix="exaspim")
