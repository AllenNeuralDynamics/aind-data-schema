"""tests for Model"""

import datetime
import unittest

import pydantic
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.system_architecture import ModelBackbone

from aind_data_schema.components.identifiers import Person, Software, Code, DataAsset
from aind_data_schema.core.model import Model, ModelArchitecture, ModelEvaluation, ModelTraining, PerformanceMetric
from aind_data_schema.core.processing import ProcessStage


class ModelTests(unittest.TestCase):
    """tests for model"""

    def test_constructors(self):
        """try building model"""

        with self.assertRaises(pydantic.ValidationError):
            Model()

        now = datetime.datetime.now()

        m = Model(
            name="2024_01_01_ResNet18_SmartSPIM",
            license="CC-BY-4.0",
            developers=[Person(name="Dr. Dan")],
            developer_institution=Organization.AIND,
            modalities=[Modality.SPIM],
            pretrained_source_url="url pretrained weights are from",
            architecture=ModelArchitecture(
                backbone=ModelBackbone.RESNET,
                layers=18,
                parameters={
                    "downsample": 1,
                    "input_shape": [14, 14, 26],
                },
                software=[
                    Software(
                        name="tensorflow",
                        version="2.11.0",
                    )
                ],
            ),
            intended_use="Cell counting for 488 channel of SmartSPIM data",
            limitations="Only trained on 488 channel",
            training=[
                ModelTraining(
                    stage=ProcessStage.PROCESSING,
                    experimenters=[Person(name="Dr. Dan")],
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
                    test_data="4:1 train/test split",
                    notes="note on training data selection",
                )
            ],
            evaluations=[
                ModelEvaluation(
                    stage=ProcessStage.PROCESSING,
                    experimenters=[Person(name="Dr. Dan")],
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

        Model.model_validate_json(m.model_dump_json())

        self.assertIsNotNone(m)


if __name__ == "__main__":
    unittest.main()
