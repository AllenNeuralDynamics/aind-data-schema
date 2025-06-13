""" Schemas for Quality Metrics """

from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Literal, Optional, Union

from aind_data_schema_models.modalities import Modality
from pydantic import Field, SkipValidation, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel, DiscriminatedList
from aind_data_schema.components.identifiers import Person
from aind_data_schema.utils.merge import merge_notes, merge_optional_list


class Status(str, Enum):
    """QC Status"""

    FAIL = "Fail"
    PASS = "Pass"
    PENDING = "Pending"


class Stage(str, Enum):
    """Quality control stage

    When during data processing the QC metrics were derived.
    """

    RAW = "Raw data"
    PROCESSING = "Processing"
    ANALYSIS = "Analysis"
    MULTI_ASSET = "Multi-asset"


class QCStatus(DataModel):
    """Description of a QC status, set by an evaluator"""

    evaluator: str = Field(..., title="Status evaluator full name")
    status: Status = Field(..., title="Status")
    timestamp: AwareDatetimeWithDefault = Field(..., title="Status date")


class QCMetric(DataModel):
    """Description of a single quality control metric"""

    name: str = Field(..., title="Metric name")
    modality: Modality.ONE_OF = Field(..., title="Modality")
    stage: Stage = Field(..., title="Evaluation stage")
    value: Any = Field(..., title="Metric value")
    status_history: List[QCStatus] = Field(default=[], title="Metric status history", min_length=1)
    description: Optional[str] = Field(default=None, title="Metric description")
    reference: Optional[str] = Field(default=None, title="Metric reference image URL or plot type")
    tags: List[str] = Field(
        default=[], title="Tags", description="Tags can be used to group QCMetric objects into groups"
    )
    evaluated_assets: Optional[List[str]] = Field(
        default=None,
        title="List of asset names that this metric depends on",
        description=(
            "Set to None except when a metric's calculation required data " "coming from a different data asset."
        ),
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

    @model_validator(mode="after")
    def validate_multi_asset(cls, v):
        """Ensure that evaluated_assets is set correctly for multi-asset metrics"""
        if v.stage == Stage.MULTI_ASSET and (not v.evaluated_assets or len(v.evaluated_assets) == 0):
            raise ValueError(f"Metric '{v.name}' is a multi-asset metric and must have evaluated_assets set.")
        elif v.stage != Stage.MULTI_ASSET and v.evaluated_assets:
            raise ValueError(f"Metric '{v.name}' is a single-asset metric and should not have evaluated_assets")
        return v


class CurationHistory(DataModel):
    """Schema to track curator name and timestamp for curation events"""

    curator: Person = Field(..., title="Curator")
    timestamp: AwareDatetimeWithDefault = Field(..., title="Timestamp")


class CurationMetric(QCMetric):
    """Description of a curation metric"""

    value: List[Any] = Field(..., title="Curation value")
    type: str = Field(..., title="Curation type")
    curation_history: List[CurationHistory] = Field(default=[], title="Curation history")


class QualityControl(DataCoreModel):
    """Description of quality metrics for a data asset"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_control.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.4"]] = Field(default="2.0.4")
    metrics: DiscriminatedList[QCMetric | CurationMetric] = Field(..., title="Evaluations")
    key_experimenters: Optional[List[Person]] = Field(
        default=None,
        title="Key experimenters",
        description="Experimenters who are responsible for quality control of this data asset",
    )
    notes: Optional[str] = Field(default=None, title="Notes")

    default_grouping: List[str] = Field(
        ...,
        title="Default grouping",
        description="Default tag grouping for this QualityControl object, used in visualizations",
    )
    allow_tag_failures: List[str] = Field(
        default=[],
        title="Allow tag failures",
        description="List of tags that are allowed to fail without failing the overall QC",
    )
    status: Optional[dict] = Field(
        default=None,
        title="Tag status mapping",
        description="Mapping of tags to their evaluated status, automatically computed",
    )

    @property
    def tags(self) -> List[str]:
        """Get all unique tags from all metrics

        Returns
        -------
        List[str]
            List of all unique tags across all metrics
        """
        all_tags = []
        for metric in self.metrics:
            all_tags.extend(metric.tags)
        return list(set(all_tags))

    @model_validator(mode="after")
    def compute_tag_status(self):
        """Automatically compute status for each tag"""
        if self.metrics:
            tag_status = {}
            for tag in self.tags:
                tag_status[tag] = self.evaluate_status(tag=tag)
            self.status = tag_status
        return self

    def evaluate_status(
        self,
        modality: Union[Modality.ONE_OF, List[Modality.ONE_OF], None] = None,
        stage: Union[Stage, List[Stage], None] = None,
        tag: Union[str, List[str], None] = None,
        date: Optional[datetime] = None,
    ) -> Status:
        """Loop through all metrics and return the overall status

        Any FAIL -> FAIL (unless tag is in allow_tag_failures)
        If no fails, then any PENDING -> PENDING
        All PASS -> PASS
        """
        if not date:
            date = datetime.now(tz=timezone.utc)

        # Convert to lists for consistent handling
        if modality and not isinstance(modality, list):
            modality = [modality]
        if stage and not isinstance(stage, list):
            stage = [stage]
        if tag and not isinstance(tag, list):
            tag = [tag]

        filtered_statuses = _get_filtered_statuses(
            metrics=self.metrics,
            date=date,
            modality=modality,
            stage=stage,
            tag=tag,
            allow_tag_failures=self.allow_tag_failures
        )

        if any(status == Status.FAIL for status in filtered_statuses):
            return Status.FAIL
        elif any(status == Status.PENDING for status in filtered_statuses):
            return Status.PENDING

        return Status.PASS

    def __add__(self, other: "QualityControl") -> "QualityControl":
        """Combine two QualityControl objects"""

        # Check for schema version incompability
        if self.schema_version != other.schema_version:
            raise ValueError(
                "Cannot combine QualityControl objects with different schema "
                + f"versions: {self.schema_version} and {other.schema_version}"
            )

        combined_metrics = self.metrics + other.metrics
        combined_experimenters = merge_optional_list(self.key_experimenters, other.key_experimenters)
        combined_notes = merge_notes(self.notes, other.notes)
        combined_default_grouping = list(set(self.default_grouping + other.default_grouping))
        combined_allow_tag_failures = list(set(self.allow_tag_failures + other.allow_tag_failures))

        return QualityControl(
            metrics=combined_metrics,
            notes=combined_notes,
            key_experimenters=combined_experimenters,
            default_grouping=combined_default_grouping,
            allow_tag_failures=combined_allow_tag_failures,
        )


def _get_status_by_date(metric: QCMetric | CurationMetric, date: datetime) -> Status:
    """Get the status of a metric at a specific date by looking through status_history.

    Returns the status that was active at the given date by finding the most recent
    status entry that occurred on or before the specified date.

    Parameters
    ----------
    metric : QCMetric | CurationMetric
        The metric to get the status for
    date : datetime
        The date to check the status at

    Returns
    -------
    Status
        The status that was active at the given date
    """
    # Find the most recent status that occurred on or before the given date
    valid_statuses = []
    for status_entry in metric.status_history:
        if status_entry.timestamp <= date:
            valid_statuses.append(status_entry)

    if not valid_statuses:
        # If no status entries exist on or before the date, return the earliest status
        # This handles the case where we're asking for a date before any status was recorded
        return metric.status_history[0].status

    # Return the most recent valid status (status_history should be chronologically ordered)
    return max(valid_statuses, key=lambda s: s.timestamp).status


def _get_filtered_statuses(
    metrics: list[QCMetric | CurationMetric],
    date: datetime,
    modality: Optional[List[Modality.ONE_OF]] = None,
    stage: Optional[List[Stage]] = None,
    tag: Optional[List[str]] = None,
    allow_tag_failures: List[str] = []
):
    """Get the status of metrics filtered by modality, stage, tag, and date."""
    filtered_statuses = []
    for metric in metrics:
        # Apply filters
        if modality and metric.modality not in modality:
            continue
        if stage and metric.stage not in stage:
            continue
        if tag and not (metric.tags and any(t in metric.tags for t in tag)):
            continue

        # Get status at the specified date using the helper function
        status = _get_status_by_date(metric, date)
        # Convert FAIL to PASS for metrics with allowed failure tags
        if status == Status.FAIL and metric.tags and any(t in allow_tag_failures for t in metric.tags):
            status = Status.PASS
        filtered_statuses.append(status)

    return filtered_statuses
