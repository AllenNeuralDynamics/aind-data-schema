""" Schemas for Quality Metrics """

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Any

from aind_data_schema_models.modalities import Modality
from pydantic import Field, BaseModel, field_validator

from aind_data_schema.base import AindCoreModel, AindModel, AwareDatetimeWithDefault


class Status(str, Enum):
    """QC Status"""

    FAIL = "Fail"
    PASS = "Pass"
    PENDING = "Pending"


class Stage(str, Enum):
    """QCEvaluation Stage

    When during data processing the QC metrics were derived.
    """

    RAW = "Raw data"
    PROCESSING = "Processing"
    ANALYSIS = "Analysis"


class QCStatus(BaseModel):
    """Description of a QC status, set by an evaluator"""

    evaluator: str = Field(..., title="Status evaluator full name")
    status: Status = Field(..., title="Status")
    timestamp: AwareDatetimeWithDefault = Field(..., title="Status date")


class QCMetric(BaseModel):
    """Description of a single quality control metric"""

    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")
    description: Optional[str] = Field(default=None, title="Metric description")
    reference: Optional[str] = Field(default=None, title="Metric reference image URL or plot type")
    metric_status_history: List[QCStatus] = Field(default=[], title="Metric status history")

    @property
    def metric_status(self) -> QCStatus:
        """Get the latest status object for this metric

        Returns
        -------
        QCStatus
            Most recent status object
        """
        return self.metric_status_history[-1]

    @field_validator("metric_status_history")
    def validate_metric_status_history(cls, v):
        if len(v) == 0:
            raise ValueError("At least one QCStatus object must be provided")
        return v


class QCEvaluation(AindModel):
    """Description of one evaluation stage, with one or more metrics"""

    evaluation_modality: Modality.ONE_OF = Field(..., title="Modality")
    evaluation_stage: Stage = Field(..., title="Evaluation stage")
    evaluation_name: str = Field(..., title="Evaluation name")
    evaluation_description: Optional[str] = Field(default=None, title="Evaluation description")
    qc_metrics: List[QCMetric] = Field(..., title="QC metrics")
    notes: Optional[str] = Field(default=None, title="Notes")
    evaluation_status_history: List[QCStatus] = Field(default=[], title="Evaluation status history")
    allow_failed_metrics: bool = Field(default=False, title="Allow metrics to fail")

    @property
    def evaluation_status(self) -> QCStatus:
        """Get the latest status object for this evaluation

        Returns
        -------
        QCStatus
            Most recent status object
        """
        if len(self.evaluation_status_history) == 0:
            self.evaluate_status()

        return self.evaluation_status_history[-1]

    @property
    def failed_metrics(self) -> list[QCMetric]:
        """Return any metrics that are failing

        Returns none if allow_failed_metrics is False

        Returns
        -------
        list[QCMetric]
            Metrics that fail
        """
        if not self.allow_failed_metrics:
            return None
        else:
            failing_metrics = []
            for metric in self.qc_metrics:
                if metric.metric_status.status == Status.FAIL:
                    failing_metrics.append(metric)

            return failing_metrics

    def evaluate_status(self, timestamp=datetime.now()):
        """Loop through all metrics and evaluate the status of the evaluation
        Any fail -> FAIL
        If no fails, then any pending -> PENDING
        All PASS -> PASS
        """
        new_status = QCStatus(evaluator="Automated", status=Status.PASS, timestamp=timestamp)

        latest_metric_statuses = [metric.metric_status.status for metric in self.qc_metrics]

        if (not self.allow_failed_metrics) and any(status == Status.FAIL for status in latest_metric_statuses):
            new_status.status = Status.FAIL
        elif any(status == Status.PENDING for status in latest_metric_statuses):
            new_status.status = Status.PENDING

        self.evaluation_status_history.append(new_status)


class QualityControl(AindCoreModel):
    """Description of quality metrics for a data asset"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_control.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.0"] = Field("1.0.0")
    evaluations: List[QCEvaluation] = Field(..., title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
    overall_status_history: List[QCStatus] = Field(default=[], title="Overall status history")

    @property
    def overall_status(self) -> QCStatus:
        """Get the latest status object for the overall QC

        Returns
        -------
        QCStatus
            Most recent status object
        """
        if len(self.overall_status_history) == 0:
            self.evaluate_status()

        return self.overall_status_history[-1]

    def evaluate_status(self, timestamp=datetime.now()):
        """Evaluate the status of all evaluations, then evaluate the status of the overall QC
        Any FAIL -> FAIL
        If no fails, then any PENDING -> PENDING
        All PASS -> PASS
        """
        for evaluation in self.evaluations:
            evaluation.evaluate_status(timestamp=timestamp)

        new_status = QCStatus(evaluator="Automated", status=Status.PASS, timestamp=timestamp)

        latest_eval_statuses = [evaluation.evaluation_status.status for evaluation in self.evaluations]

        if any(status == Status.FAIL for status in latest_eval_statuses):
            new_status.status = Status.FAIL
        elif any(status == Status.PENDING for status in latest_eval_statuses):
            new_status.status = Status.PENDING

        self.overall_status_history.append(new_status)
