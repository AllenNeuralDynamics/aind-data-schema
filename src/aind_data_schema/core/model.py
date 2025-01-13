""" schema describing an analysis model """

from typing import Any, List, Literal, Optional

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.system_architecture import ModelBackbone
from pydantic import Field

from aind_data_schema.base import MetadataModel, MetadataCoreModel, GenericModel, GenericModelType
from aind_data_schema.components.devices import Software
from aind_data_schema.core.processing import DataProcess, ProcessName


class ModelArchitecture(MetadataModel):
    """Description of model architecture"""

    backbone: ModelBackbone = Field(..., title="Backbone", description="Core network architecture")
    software: List[Software] = Field(default=[], title="Software frameworks")
    layers: Optional[int] = Field(default=None, title="Layers")
    parameters: GenericModelType = Field(default=GenericModel(), title="Parameters")
    notes: Optional[str] = Field(default=None, title="Notes")


class PerformanceMetric(MetadataModel):
    """Description of a performance metric"""

    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")


class ModelEvaluation(DataProcess):
    """Description of model evaluation"""

    name: ProcessName = Field(ProcessName.MODEL_EVALUATION, title="Process name")
    performance: List[PerformanceMetric] = Field(..., title="Evaluation performance")


class ModelTraining(DataProcess):
    """Description of model training"""

    name: ProcessName = Field(ProcessName.MODEL_TRAINING, title="Process name")
    train_performance: List[PerformanceMetric] = Field(
        ..., title="Training performance", description="Performance on training set"
    )
    test_performance: Optional[List[PerformanceMetric]] = Field(
        default=None, title="Test performance", description="Performance on test data, evaluated during training"
    )
    test_data: Optional[str] = Field(
        default=None, title="Test data", description="Path or cross-validation/split approach"
    )


class Model(MetadataCoreModel):
    """Description of an analysis model"""

    _DESCRIBED_BY_URL = MetadataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/model.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.0.1"] = Field("0.0.1")

    name: str = Field(..., title="Name")
    license: str = Field(..., title="License")
    developer_full_name: Optional[List[str]] = Field(default=None, title="Name of developer")
    developer_institution: Optional[Organization.ONE_OF] = Field(default=None, title="Institute where developed")
    modality: List[Modality.ONE_OF] = Field(..., title="Modality")
    architecture: ModelArchitecture = Field(..., title="Model architecture")
    intended_use: str = Field(..., title="Intended model use", description="Semantic description of intended use")
    limitations: Optional[str] = Field(default=None, title="Model limitations")
    pretrained_source_url: Optional[str] = Field(default=None, title="Pretrained source URL")
    training: Optional[List[ModelTraining]] = Field(default=[], title="Training")
    evaluations: Optional[List[ModelEvaluation]] = Field(default=[], title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
