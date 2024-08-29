""" Schemas for Quality Metrics """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Literal, Optional, Any

from aind_data_schema_models.modalities import Modality
from pydantic import Field, BaseModel

from aind_data_schema.base import AindCoreModel, AindModel


class Status(str, Enum):
    """QC Status"""

    FAIL = "Fail"
    PASS = "Pass"


class Stage(str, Enum):
    """QCEvaluation Stage

    When during data processing the QC metrics were derived.
    """

    RAW = "Raw data"
    PREPROCESSING = "Preprocessing"
    ANALYSIS = "Analysis"


class QCMetric(BaseModel):
    """Description of a single quality control metric"""
    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")
    description: Optional[str] = Field(default=None, title="Metric description")
    references: Optional[List[str]] = Field(default=None, title="Metric reference URLs")


class QCEvaluation(AindModel):
    """Description of one evaluation stage, with one or more metrics"""

    evaluation_modality: Modality.ONE_OF = Field(..., title="Modality")
    evaluation_stage: Stage = Field(..., title="Evaluation stage")
    evaluation_name: str = Field(..., title="Evaluation name")
    evaluation_desc: Optional[str] = Field(default=None, title="Evaluation description")
    evaluator: str = Field(..., title="Evaluator full name")
    evaluation_date: date = Field(..., title="Evaluation date")
    qc_metrics: List[QCMetric] = Field(title="QC metrics")
    stage_status: Status = Field(..., title="Stage status")
    notes: Optional[str] = Field(default=None, title="Notes")


class QualityControl(AindCoreModel):
    """Description of quality metrics for a data asset"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_control.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.0"] = Field("1.0.0")
    overall_status: Status = Field(..., title="Overall status")
    overall_status_date: date = Field(..., title="Date of status")
    evaluations: List[QCEvaluation] = Field(..., title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
