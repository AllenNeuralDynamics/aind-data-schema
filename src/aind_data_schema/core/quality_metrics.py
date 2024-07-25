""" Schemas for Quality Metrics """

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import Field

from aind_data_schema_models.modalities import Modality
from aind_data_schema.base import AindCoreModel, AindGeneric, AindGenericType, AindModel


class Status(Enum):
    """QC Status"""

    FAIL = "Fail"
    PASS = "Pass"
    UNKNOWN = "Unknown"


class QCEvaluation(AindModel):
    """Description of one evaluation stage"""

    evaluation_modality: Modality = Field(..., title="Modality")
    evaluation_stage: str = Field(..., title="Evaluation stage")
    evaluator_full_name: str = Field(..., title="Evaluator full name")
    evaluation_date: date = Field(..., title="Evaluation date")
    qc_metrics: AindGenericType = Field(AindGeneric(), title="QC metrics")
    stage_status: Status = Field(..., title="Stage status")
    notes: Optional[str] = Field(None, title="Notes")


class QualityMetrics(AindCoreModel):
    """Description of quality metrics for a data asset"""

    schema_version: str = Field(
        "0.0.1",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    overall_status: Status = Field(..., title="Overall status")
    overall_status_date: date = Field(..., title="Date of status")
    evaluations: List[QCEvaluation] = Field(..., title="Evaluations")
    notes: Optional[str] = Field(None, title="Notes")
