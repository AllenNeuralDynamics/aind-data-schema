"""Example model file"""

from aind_data_schema_models.system_architecture import ModelArchitecture

from aind_data_schema.components.identifiers import Code, DataAsset, Software
from aind_data_schema.core.model import Model, ModelEvaluation, ModelTraining, PerformanceMetric
from aind_data_schema.core.processing import ProcessStage
import datetime

now = datetime.datetime.now()


m = Model(
    name="2024_01_01_ResNet18_SmartSPIM",
    version="0.1",
    architecture=ModelArchitecture.RESNET,
    architecture_parameters={
        "layers": 18,
        "input_shape": [14, 14, 26],
    },
    software_framework=Software(
        name="tensorflow",
        version="2.11.0",
    ),
    intended_use="Cell counting for 488 channel of SmartSPIM data",
    limitations="Only trained on 488 channel",
    example_run_code=Code(
        url="url for model code repo",
        run_script="./predict.py",
    ),
    training=[
        ModelTraining(
            stage=ProcessStage.PROCESSING,
            experimenters=["Dr. Dan"],
            code=Code(
                input_data=[
                    DataAsset(url="s3 path to training data"),
                ],
                url="url for model code repo",
                run_script="./train.py",
                parameters={
                    "learning_rate": 0.0001,
                    "batch_size": 32,
                    "augmentation": True,
                },
            ),
            output_path="./trained_model.h5",
            start_date_time=now,
            end_date_time=now,
            train_performance=[
                PerformanceMetric(name="precision", value=0.9),
                PerformanceMetric(name="recall", value=0.85),
            ],
            test_performance=[
                PerformanceMetric(name="precision", value=0.8),
                PerformanceMetric(name="recall", value=0.8),
            ],
            test_evaluation_method="random 4:1 train/test split",
            notes="note on training data selection",
        )
    ],
    evaluations=[
        ModelEvaluation(
            stage=ProcessStage.PROCESSING,
            experimenters=["Dr. Dan"],
            code=Code(
                input_data=[
                    DataAsset(url="s3 path to eval data"),
                ],
                url="url for model code repo",
                run_script="./eval.py",
            ),
            start_date_time=now,
            end_date_time=now,
            performance=[PerformanceMetric(name="precision", value=0.8)],
        )
    ],
)


if __name__ == "__main__":
    serialized = m.model_dump_json()
    deserialized = Model.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="")
