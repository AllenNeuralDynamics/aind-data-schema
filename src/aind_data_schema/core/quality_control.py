""" Schemas for Quality Metrics """

from enum import Enum
from typing import Any, List, Literal, Optional

from aind_data_schema_models.modalities import Modality
from pydantic import BaseModel, Field, field_validator, model_validator

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
    MULTI_ASSET = "Multi-asset"


class QCStatus(BaseModel):
    """Description of a QC status, set by an evaluator"""

    evaluator: str = Field(..., title="Status evaluator full name")
    status: Status = Field(..., title="Status")
    timestamp: AwareDatetimeWithDefault = Field(..., title="Status date")


class QCMetric(BaseModel):
    """Description of a single quality control metric"""

    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")
    status_history: List[QCStatus] = Field(default=[], title="Metric status history")
    description: Optional[str] = Field(default=None, title="Metric description")
    reference: Optional[str] = Field(default=None, title="Metric reference image URL or plot type")
    evaluated_assets: Optional[List[str]] = Field(
        default=None,
        title="List of asset names that this metric depends on",
        description="Set to None except when a metric's calculation required data coming from a different data asset.",
    )

    @property
    def status(self) -> QCStatus:
        """Get the latest status object for this metric

        Returns
        -------
        QCStatus
            Most recent status object
        """
        return self.status_history[-1]

    @field_validator("status_history")
    def validate_status_history(cls, v):
        """Ensure that at least one QCStatus object is provided"""
        if len(v) == 0:
            raise ValueError("At least one QCStatus object must be provided")
        return v


class QCEvaluation(AindModel):
    """Description of one evaluation stage, with one or more metrics"""

    modality: Modality.ONE_OF = Field(..., title="Modality")
    stage: Stage = Field(..., title="Evaluation stage")
    name: str = Field(..., title="Evaluation name")
    description: Optional[str] = Field(default=None, title="Evaluation description")
    metrics: List[QCMetric] = Field(..., title="QC metrics")
    notes: Optional[str] = Field(default=None, title="Notes")
    allow_failed_metrics: bool = Field(
        default=False,
        title="Allow metrics to fail",
        description=(
            "Set to true for evaluations that are not critical to the overall state of QC for a data asset, this"
            " will allow individual metrics to fail while still passing the evaluation."
        ),
    )

    @property
    def status(self) -> Status:
        """Loop through all metrics and return the evaluation's status

        Any fail -> FAIL
        If no fails, then any pending -> PENDING
        All PASS -> PASS

        Returns
        -------
        Status
            Current status of the evaluation
        """
        latest_metric_statuses = [metric.status.status for metric in self.metrics]

        if (not self.allow_failed_metrics) and any(status == Status.FAIL for status in latest_metric_statuses):
            return Status.FAIL
        elif any(status == Status.PENDING for status in latest_metric_statuses):
            return Status.PENDING

        return Status.PASS

    @property
    def failed_metrics(self) -> Optional[List[QCMetric]]:
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
            for metric in self.metrics:
                if metric.status.status == Status.FAIL:
                    failing_metrics.append(metric)

            return failing_metrics

    @model_validator(mode="after")
    def validate_multi_asset(cls, v):
        """Ensure that the evaluated_assets field in any attached metrics is set correctly"""
        stage = v.stage
        metrics = v.metrics

        if stage == Stage.MULTI_ASSET:
            for metric in metrics:
                if not metric.evaluated_assets or len(metric.evaluated_assets) == 0:
                    raise ValueError(
                        f"Metric '{metric.name}' is in a multi-asset QCEvaluation and must have evaluated_assets set."
                    )
        else:
            # make sure all evaluated assets are None
            for metric in metrics:
                if metric.evaluated_assets:
                    raise ValueError(
                        (
                            f"Metric '{metric.name}' is in a single-asset QCEvaluation"
                            " and should not have evaluated_assets"
                        )
                    )
        return v


class QualityControl(AindCoreModel):
    """Description of quality metrics for a data asset"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_control.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.1.1"] = Field(default="1.1.1")
    evaluations: List[QCEvaluation] = Field(..., title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")

    def status(self, modality: str = None, stage: Stage = None) -> Status:
        """Loop through all evaluations and return the overall status

        Any FAIL -> FAIL
        If no fails, then any PENDING -> PENDING
        All PASS -> PASS

        Parameters
        ----------
        modality : str, optional
            Modality.ONE_OF to filter by, by default None
        stage : Stage, optional
            Stage to filter by, by default None

        Returns
        -------
        Status
        """
        eval_statuses = [
            evaluation.status
            for evaluation in self.evaluations
            if (not modality or evaluation.modality == modality) and (not stage or evaluation.stage == stage)
        ]

        if any(status == Status.FAIL for status in eval_statuses):
            return Status.FAIL
        elif any(status == Status.PENDING for status in eval_statuses):
            return Status.PENDING

        return Status.PASS
