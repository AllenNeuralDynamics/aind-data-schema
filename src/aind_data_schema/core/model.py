""" schema describing an analysis model """

from decimal import Decimal
from enum import Enum
from typing import Any, Optional, List, Literal

from pydantic import Field

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.system_architecture import ModelBackbone

from aind_data_schema.base import AindCoreModel, AindGenericType, AindModel, AwareDatetimeWithDefault
from aind_data_schema.components.devices import Software


class ModelArchitecture(AindModel):
    """Description of model architecture"""

    backbone: ModelBackbone = Field(..., title="Backbone")
    layers: int = Field(..., title="Layers")
    parameters: AindGenericType = Field(..., title="Parameters")
    notes: Optional[str] = Field(default=None, title="Notes")


class PerformanceMetric(AindModel):
    """Description of a performance metric"""

    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")


class ModelEvaluation(AindModel):
    """Description of model training"""

    data: str = Field(..., title="Path to training data")
    data_description: Optional[str] = Field(default=None, title="Description of training data") 
    date: AwareDatetimeWithDefault = Field(..., title="Date trained") #not sure we need datetime
    validation_folds: Optional[int] = Field(default=None, title="Validation folds")
    performance: List[PerformanceMetric] = Field(..., title="Training performance")
    notes: Optional[str] = Field(default=None, title="Notes")


class Model(AindCoreModel):
    """Description of an analysis model"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/model.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.0.1"] = Field("0.0.1")

    name: str = Field(..., title="Name")
    license: str = Field(..., title="License")
    developer_full_name: Optional[List[str]] = Field(default=None, title="Name of developer")
    developer_institution: Optional[Organization.ONE_OF] = Field(default=None, title="Institute where developed")
    modality: Modality.ONE_OF = Field(..., title="Modality")
    model_architecture: ModelArchitecture = Field(..., title="Model architecture")
    software: List[Software] = Field(..., title="software")
    direct_use: str = Field(..., title="Intended model use", description="Semantic description of intended use")
    limitations: Optional[str] = Field(default=None, title="Model limitations")
    training: List[ModelEvaluation] = Field(..., title="Training")
    evaluations: Optional[List[ModelEvaluation]] = Field(default=[], title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
