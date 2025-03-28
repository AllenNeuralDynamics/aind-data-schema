""" schema describing an analysis model """

from typing import Any, List, Literal, Optional

from aind_data_schema_models.system_architecture import ModelBackbone
from pydantic import Field

from aind_data_schema.base import DataCoreModel, DataModel, GenericModel, GenericModelType
from aind_data_schema.components.identifiers import Code, Person, Software
from aind_data_schema.core.processing import DataProcess, ProcessName


class ModelArchitecture(DataModel):
    """Description of model architecture"""

    backbone: ModelBackbone = Field(..., title="Backbone", description="Core network architecture")
    software: List[Software] = Field(default=[], title="Software packages")
    layers: Optional[int] = Field(default=None, title="Layers")
    parameters: GenericModelType = Field(default=GenericModel(), title="Parameters")
    notes: Optional[str] = Field(default=None, title="Notes")


class PerformanceMetric(DataModel):
    """Description of a performance metric"""

    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")


class ModelEvaluation(DataProcess):
    """Description of model evaluation"""

    process_type: ProcessName = Field(ProcessName.MODEL_EVALUATION, title="Process name")
    performance: List[PerformanceMetric] = Field(..., title="Evaluation performance")


class ModelTraining(DataProcess):
    """Description of model training"""

    process_type: ProcessName = Field(ProcessName.MODEL_TRAINING, title="Process name")
    train_performance: List[PerformanceMetric] = Field(
        ..., title="Training performance", description="Performance on training set"
    )
    test_performance: Optional[List[PerformanceMetric]] = Field(
        default=None, title="Test performance", description="Performance on test data, evaluated during training"
    )
    test_data: Optional[str] = Field(
        default=None, title="Test data", description="Path or cross-validation/split approach"
    )


class Model(DataCoreModel):
    """Description of an analysis model"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/model.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["2.0.0"] = Field(default="2.0.0")

    name: str = Field(..., title="Name")
    code: Optional[Code] = Field(
        default=None,
        title="Code",
        description="Code to run the model, possibly including reference to sample data"
    )
    architecture: ModelArchitecture = Field(..., title="Model architecture")
    intended_use: str = Field(..., title="Intended model use", description="Semantic description of intended use")
    limitations: Optional[str] = Field(default=None, title="Model limitations")
    pretrained_source_url: Optional[str] = Field(default=None, title="Pretrained source URL")
    training: List[ModelTraining] = Field(default=[], title="Training")
    evaluations: List[ModelEvaluation] = Field(default=[], title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
