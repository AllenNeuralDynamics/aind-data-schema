""" Schemas for Quality Metrics """

from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Literal, Optional, Union

from aind_data_schema_models.modalities import Modality
from pydantic import BaseModel, Field, SkipValidation, field_validator, model_validator

from aind_data_schema.base import DataCoreModel, DataModel, AwareDatetimeWithDefault


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


class QCEvaluation(DataModel):
    """Description of one evaluation stage, with one or more metrics"""

    modality: Modality.ONE_OF = Field(..., title="Modality")
    stage: Stage = Field(..., title="Evaluation stage")
    name: str = Field(..., title="Evaluation name")
    description: Optional[str] = Field(default=None, title="Evaluation description")
    metrics: List[QCMetric] = Field(..., title="QC metrics")
    tags: Optional[List[str]] = Field(
        default=None, title="Tags", description="Tags can be used to group QCEvaluation objects into groups"
    )
    notes: Optional[str] = Field(default=None, title="Notes")
    allow_failed_metrics: bool = Field(
        default=False,
        title="Allow metrics to fail",
        description=(
            "Set to true for evaluations that are not critical to the overall state of QC for a data asset, this"
            " will allow individual metrics to fail while still passing the evaluation."
        ),
    )
    latest_status: Optional[Status] = Field(default=None, title="Evaluation status")
    created: AwareDatetimeWithDefault = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc), title="Evaluation creation date"
    )

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
    def compute_latest_status(self):
        """Compute the status of the evaluation based on the status of its metrics"""
        self.latest_status = self.evaluate_status()
        return self

    def evaluate_status(self, date: Optional[datetime] = None) -> Status:
        """Loop through all metrics and return the evaluation's status

        Any fail -> FAIL
        If no fails, then any pending -> PENDING
        All PASS -> PASS

        Returns
        -------
        Status
            Current status of the evaluation
        """
        if not date:
            date = datetime.now(tz=timezone.utc)

        latest_metric_statuses = []

        for metric in self.metrics:
            # loop backwards through metric statuses until you find one that is before the provided date
            for status in reversed(metric.status_history):
                if status.timestamp <= date:
                    latest_metric_statuses.append(status.status)
                    break

        if not latest_metric_statuses:
            raise ValueError(f"No status existed prior to the provided date {date.isoformat()}")

        if (not self.allow_failed_metrics) and any(status == Status.FAIL for status in latest_metric_statuses):
            return Status.FAIL
        elif any(status == Status.PENDING for status in latest_metric_statuses):
            return Status.PENDING

        return Status.PASS

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


class QualityControl(DataCoreModel):
    """Description of quality metrics for a data asset"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_control.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.2"]] = Field(default="2.0.2")
    evaluations: List[QCEvaluation] = Field(..., title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")

    def status(
        self,
        modality: Union[Modality.ONE_OF, List[Modality.ONE_OF], None] = None,
        stage: Union[Stage, List[Stage], None] = None,
        tag: Union[str, List[str], None] = None,
        date: Optional[datetime] = None,
    ) -> Status:
        """Loop through all evaluations and return the overall status

        Any FAIL -> FAIL
        If no fails, then any PENDING -> PENDING
        All PASS -> PASS
        """
        if not date:
            date = datetime.now(tz=timezone.utc)

        if not modality and not stage and not tag:
            eval_statuses = [evaluation.evaluate_status(date=date) for evaluation in self.evaluations]
        else:
            if modality and not isinstance(modality, list):
                modality = [modality]
            if stage and not isinstance(stage, list):
                stage = [stage]
            if tag and not isinstance(tag, list):
                tag = [tag]

            eval_statuses = [
                evaluation.evaluate_status(date=date)
                for evaluation in self.evaluations
                if (not modality or any(evaluation.modality == mod for mod in modality))
                and (not stage or any(evaluation.stage == sta for sta in stage))
                and (not tag or (evaluation.tags and any(t in evaluation.tags for t in tag)))
            ]

        if any(status == Status.FAIL for status in eval_statuses):
            return Status.FAIL
        elif any(status == Status.PENDING for status in eval_statuses):
            return Status.PENDING

        return Status.PASS

    def __add__(self, other: "QualityControl") -> "QualityControl":
        """Combine two QualityControl objects"""

        # Check for schema version incompability
        if self.schema_version != other.schema_version:
            raise ValueError(
                f"Cannot combine QualityControl objects with different schema versions: {self.schema_version} and {other.schema_version}"
            )

        # Combine
        evaluations = self.evaluations + other.evaluations
        if self.notes and other.notes:
            notes = self.notes + "\n" + other.notes
        elif self.notes:
            notes = self.notes
        elif other.notes:
            notes = other.notes
        else:
            notes = None

        return QualityControl(evaluations=evaluations, notes=notes)
