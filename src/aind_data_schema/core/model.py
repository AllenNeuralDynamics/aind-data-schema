"""schema describing an analysis model"""

from typing import Annotated, Any, List, Literal, Optional, Union

from aind_data_schema_models.system_architecture import ModelArchitecture
from pydantic import Field

from aind_data_schema.base import DataCoreModel, DataModel, GenericModel, GenericModelType
from aind_data_schema.components.identifiers import Code, Software
from aind_data_schema.core.processing import DataProcess, ProcessName


class PerformanceMetric(DataModel):
    """Description of a performance metric"""

    name: str = Field(..., title="Metric name")
    value: Any = Field(..., title="Metric value")


class ModelEvaluation(DataProcess):
    """Description of model evaluation"""

    process_type: ProcessName = ProcessName.MODEL_EVALUATION
    performance: List[PerformanceMetric] = Field(..., title="Evaluation performance")


class ModelTraining(DataProcess):
    """Description of model training"""

    process_type: ProcessName = ProcessName.MODEL_TRAINING
    train_performance: List[PerformanceMetric] = Field(
        ..., title="Training performance", description="Performance on training set"
    )
    test_performance: Optional[List[PerformanceMetric]] = Field(
        default=None, title="Test performance", description="Performance on test data, evaluated during training"
    )
    test_data: Optional[str] = Field(
        default=None, title="Test data", description="Path or cross-validation/split approach"
    )


class ModelPretraining(DataModel):
    """Description of model pretraining"""

    source_url: str = Field(..., title="Pretrained source URL", description="URL for pretrained weights")


class Model(DataCoreModel):
    """Description of an analysis model"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/model.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["2.0.0"] = Field(default="2.0.0")

    name: str = Field(..., title="Name")
    version: str = Field(..., title="Version")
    example_run_code: Code = Field(
        title="Example run code", description="Code to run the model, possibly including example parameters/data"
    )
    architecture: ModelArchitecture = Field(..., title="architecture", description="Model architecture / type of model")
    software_framework: Optional[Software] = Field(default=None, title="Software framework")
    properties: GenericModelType = Field(
        default=GenericModel(),
        title="Properties",
        description="Additional properties of model, such as input signature or number of layers.",
    )
    intended_use: str = Field(..., title="Intended model use", description="Semantic description of intended use")
    limitations: Optional[str] = Field(default=None, title="Model limitations")
    training: List[Annotated[Union[ModelTraining, ModelPretraining], Field(discriminator="object_type")]] = Field(
        ..., title="Training", min_length=1
    )
    evaluations: List[ModelEvaluation] = Field(default=[], title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
