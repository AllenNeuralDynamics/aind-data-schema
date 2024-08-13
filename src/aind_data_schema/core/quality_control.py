""" Schemas for Quality Metrics """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Literal, Optional

from aind_data_schema_models.modalities import Modality
from pydantic import Field

from aind_data_schema.base import AindCoreModel, AindGeneric, AindGenericType, AindModel


class Status(str, Enum):
    """QC Status"""

    FAIL = "Fail"
    PASS = "Pass"


class QCEvaluation(AindModel):
    """Description of one evaluation stage"""

    evaluation_modality: Modality.ONE_OF = Field(..., title="Modality")
    evaluation_stage: str = Field(..., title="Evaluation stage")
    evaluator_full_name: str = Field(..., title="Evaluator full name")
    evaluation_date: date = Field(..., title="Evaluation date")
    qc_metrics: AindGenericType = Field(AindGeneric(), title="QC metrics")
    stage_status: Status = Field(..., title="Stage status")
    notes: Optional[str] = Field(None, title="Notes")


class QualityControl(AindCoreModel):
    """Description of quality metrics for a data asset"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/quality_metrics.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.0.1"] = Field("0.0.1")
    overall_status: Status = Field(..., title="Overall status")
    overall_status_date: date = Field(..., title="Date of status")
    evaluations: List[QCEvaluation] = Field(..., title="Evaluations")
    notes: Optional[str] = Field(None, title="Notes")
