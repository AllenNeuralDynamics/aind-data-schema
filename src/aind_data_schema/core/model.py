""" schema describing an analysis model """

from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import Field

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization

from aind_data_schema.base import AindCoreModel, AindGenericType, AindModel, AwareDatetimeWithDefault
from aind_data_schema.components.devices import Software


class Backbone(str, Enum):
    """Types of network backbones"""

    ALEXNET = "AlexNet"
    RESNET = "ResNet"
    VGGNET = "VGGNet"


class ModelArchitecture(AindModel):
    """Description of model architecture"""

    backbone: Backbone = Field(..., title="Backbone")
    layers: int = Field(..., title="Layers")
    parameters: AindGenericType = Field(..., title="Parameters")
    #notes?


class ScoreStatistics(AindModel):
    """Statistics for x-fold validation scores"""

    mean: Decimal = Field(..., title="Mean")
    std: Decimal = Field(..., title="Standard deviation")


class PerformanceScore(AindModel):
    """Description of performance metrics"""

    precision: Union[Decimal, ScoreStatistics] = Field(..., title="Precision")
    recall: Union[Decimal, ScoreStatistics] = Field(..., title="Recall")
    f1_score: Union[Decimal, ScoreStatistics] = Field(..., title="F1 score")


class ModelTraining(AindModel):
    """Description of model training"""

    training_data: str = Field(..., title="Path to training data")
    training_data_description: Optional[str] = Field(default=None, title="Description of training data") 
    training_date: AwareDatetimeWithDefault = Field(..., title="Date trained") #not sure we need datetime
    validation_folds: int = Field(..., title="Validation folds") #is the validation methods x-fold? or are there other validations? Enum?
    performance: PerformanceScore = Field(..., title="Training performance")
    notes: Optional[str] = Field(default=None, title="Notes")


class ModelEvaluation(AindModel):
    """Description of model evaluation"""

    evaluation_data: str = Field(..., title="Path to evaluation data")
    evaluation_data_description: Optional[str] = Field(default=None, title="Description of evaluation data")
    evaluation_date: AwareDatetimeWithDefault = Field(..., title="Date trained") #not sure we need datetime
    performance: PerformanceScore = Field(..., title="Evaluation performance")
    notes: Optional[str] = Field(default=None, title="Notes")


class Model(AindCoreModel):
    """Description of an analysis model"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/model.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["1.0.1"] = Field("0.0.1")

    name: str = Field(..., title="Name")
    developer_full_name: Optional[str] = Field(default=None, title="Name of developer")
    developer_institution: Organization.ONE_OF = Field(default=None, title="Institute where developed")
    modality: Modality.ONE_OF = Field(..., title="Modality")
    model_architecture: ModelArchitecture = Field(..., title="Model architecture")
    software: Software = Field(..., title="software")
    direct_use: str = Field(..., title="Intended model use", description="Semantic description of intended use")
    limitations: Optional[str] = Field(default=None, title="Model limitations")
    training: List[ModelTraining] = Field(..., title="Training")
    evaluations: Optional[List[ModelEvaluation]] = Field(default=[], title="Evaluations")
    notes: Optional[str] = Field(default=None, title="Notes")
