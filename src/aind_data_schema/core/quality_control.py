""" Schemas for Quality Metrics """

from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Literal, Optional, Union
import warnings

from aind_data_schema_models.modalities import Modality
from pydantic import Field, SkipValidation, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataCoreModel, DataModel, DiscriminatedList
from aind_data_schema.utils.merge import merge_notes, merge_optional_list, remove_duplicates, merge_str_tuple_lists


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
    description: Optional[str] = Field(
        default=None,
        title="Metric description",
        description="Describes the measured value and the rule that links the value and status.",
    )
    reference: Optional[str] = Field(default=None, title="Metric reference image URL or plot type")
    tags: dict[str, str] = Field(
        default={},
        title="Tags",
        description="Tags group QCMetric objects. Unique keys define groups of tags, for example {'probe': 'probeA'}.",
    )
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

    @model_validator(mode="after")
    def validate_multi_asset(self):
        """Ensure that evaluated_assets is set correctly for multi-asset metrics"""
        if self.stage == Stage.MULTI_ASSET and (not self.evaluated_assets or len(self.evaluated_assets) == 0):
            raise ValueError(f"Metric '{self.name}' is a multi-asset metric and must have evaluated_assets set.")
        elif self.stage != Stage.MULTI_ASSET and self.evaluated_assets:
            raise ValueError(f"Metric '{self.name}' is a single-asset metric and should not have evaluated_assets")
        return self

    @model_validator(mode="before")
    @classmethod
    def fix_tag_lists(cls, self):
        """Convert tags from list to dict if necessary

        This function is for backwards compatibility with v2.2.X where tags were stored as lists of strings.

        Remove this function in aind-data-schema v3.X
        """
        if "tags" not in self:
            return self
        tags = self["tags"]
        if isinstance(tags, list):
            warnings.warn("QCMetric 'tags' field is now a dict. Converting from list to dict", DeprecationWarning)
            self["tags"] = {f"tag_{i+1}": tag for i, tag in enumerate(tags)}
        return self


class CurationHistory(DataModel):
    """Schema to track curator name and timestamp for curation events"""

    curator: str = Field(..., title="Curator")
    timestamp: AwareDatetimeWithDefault = Field(..., title="Timestamp")


class CurationMetric(QCMetric):
    """Description of a curation metric"""

    value: List[Any] = Field(..., title="Curation value")
    type: str = Field(..., title="Curation type")
    curation_history: List[CurationHistory] = Field(default=[], title="Curation history")


class QualityControl(DataCoreModel):
    """Collection of quality control metrics evaluated on a data asset to determine pass/fail status"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_control.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.4.1"]] = Field(default="2.4.1")
    metrics: DiscriminatedList[QCMetric | CurationMetric] = Field(..., title="Evaluations")
    key_experimenters: Optional[List[str]] = Field(
        default=None,
        title="Key experimenters",
        description="Experimenters who are responsible for quality control of this data asset",
    )
    notes: Optional[str] = Field(default=None, title="Notes")

    default_grouping: List[str | tuple[str, ...]] = Field(
        ...,
        title="Default grouping",
        description="Tag *keys* that should be used to group metrics hierarchically for visualization",
    )
    allow_tag_failures: List[str] = Field(
        default=[],
        title="Allow tag failures",
        description="List of tag *values* that are allowed to fail without failing the overall QC",
    )
    status: Optional[dict] = Field(
        default=None,
        title="Status mapping",
        description="Mapping of tags, modalities, and stages to their evaluated status, automatically computed",
    )

    @property
    def tags(self) -> List[str]:
        """Get all unique tag values from all metrics

        Returns
        -------
        List[str]
            List of all unique tag values across all metrics
        """
        all_tags = []
        for metric in self.metrics:
            all_tags.extend(metric.tags.values())
        return list(set(all_tags))

    @property
    def tag_pairs(self) -> List[str]:
        """Get all unique tag key:value pairs from all metrics

        Returns
        -------
        List[str]
            List of all unique tag key:value pairs across all metrics in 'key:value' format
        """
        all_tag_pairs = []
        for metric in self.metrics:
            for key, value in metric.tags.items():
                all_tag_pairs.append(f"{key}:{value}")
        return list(set(all_tag_pairs))

    @property
    def modalities(self) -> List[Modality.ONE_OF]:
        """Get all unique modalities from all metrics

        Returns
        -------
        List[Modality.ONE_OF]
            List of all unique modalities across all metrics
        """
        all_modalities = []
        for metric in self.metrics:
            all_modalities.append(metric.modality)
        return list(set(all_modalities))

    @property
    def stages(self) -> List[Stage]:
        """Get all unique stages from all metrics

        Returns
        -------
        List[Stage]
            List of all unique stages across all metrics
        """
        all_stages = []
        for metric in self.metrics:
            all_stages.append(metric.stage)
        return list(set(all_stages))

    @model_validator(mode="after")
    def compute_status(self):
        """Automatically compute status for each tag, modality, and stage"""
        if self.metrics:
            computed_status = {}

            # Compute tag statuses (using key:value format)
            for tag_pair in self.tag_pairs:
                computed_status[tag_pair] = self.evaluate_status(tag=tag_pair)

            # Compute modality statuses
            for modality in self.modalities:
                computed_status[modality.abbreviation] = self.evaluate_status(modality=modality)

            # Compute stage statuses
            for stage in self.stages:
                computed_status[stage] = self.evaluate_status(stage=stage)

            self.status = computed_status
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
            modality_filter=modality,
            stage_filter=stage,
            tag_filter=tag,
            allow_tag_failures=self.allow_tag_failures,
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
        # Merge each inner tuple in the two default_grouping lists
        combined_default_grouping = merge_str_tuple_lists(self.default_grouping, other.default_grouping)
        combined_allow_tag_failures = list(set(self.allow_tag_failures + other.allow_tag_failures))

        # Remove duplicates
        if combined_experimenters:
            combined_experimenters = remove_duplicates(combined_experimenters)

        return QualityControl(
            metrics=combined_metrics,
            notes=combined_notes,
            key_experimenters=combined_experimenters,
            default_grouping=combined_default_grouping,
            allow_tag_failures=combined_allow_tag_failures,
        )

    @model_validator(mode="before")
    def fix_default_grouping_list(cls, value: dict) -> dict:
        """Convert default grouping from list of strings to list of list of strings if necessary
        This function is for backwards compatibility with v2.2.X where default_grouping was stored as a list of strings.
        Remove this function in aind-data-schema v3.X
        """
        if "default_grouping" not in value:
            return value

        if all(isinstance(item, str) for item in value["default_grouping"]):
            first_metric = value["metrics"][0]
            if isinstance(first_metric, dict) and "tags" in first_metric:
                if isinstance(first_metric["tags"], list):
                    value["default_grouping"] = [["modality"], ["tag_1"]]

        return value


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
    modality_filter: Optional[List[Modality.ONE_OF]] = None,
    stage_filter: Optional[List[Stage]] = None,
    tag_filter: Optional[List[str]] = None,
    allow_tag_failures: List[str] = [],
):
    """Get the status of metrics filtered by modality, stage, tag, and date.

    tag_filter can contain either 'key:value' pairs or just tag values for backward compatibility.
    allow_tag_failures can contain either 'key:value' pairs or just tag values.
    """
    filtered_statuses = []
    for metric in metrics:
        # Apply filters
        if modality_filter and metric.modality not in modality_filter:
            continue
        if stage_filter and metric.stage not in stage_filter:
            continue
        if tag_filter:
            # Check if any of the filter tags match this metric's tags
            # Support both 'key:value' format and just values for backward compatibility
            metric_tag_pairs = [f"{k}:{v}" for k, v in metric.tags.items()]
            metric_tag_values = list(metric.tags.values())
            if not any(t in metric_tag_pairs or t in metric_tag_values for t in tag_filter):
                continue

        # Get status at the specified date using the helper function
        status = _get_status_by_date(metric, date)
        # Check if any of our tag key:value pairs or values are in the allow_tag_failures list
        if status == Status.FAIL and metric.tags:
            metric_tag_pairs = [f"{k}:{v}" for k, v in metric.tags.items()]
            metric_tag_values = list(metric.tags.values())
            if any(
                tag_pair in allow_tag_failures or tag_value in allow_tag_failures
                for tag_pair, tag_value in zip(metric_tag_pairs, metric_tag_values)
            ):
                status = Status.PASS
        filtered_statuses.append(status)

    return filtered_statuses
