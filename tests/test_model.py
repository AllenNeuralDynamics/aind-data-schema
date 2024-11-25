""" tests for Model """

import datetime
import unittest

import pydantic
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.system_architecture import ModelBackbone

from aind_data_schema.components.devices import Software
from aind_data_schema.core.model import Model, ModelArchitecture, ModelEvaluation, ModelTraining, PerformanceMetric


class ModelTests(unittest.TestCase):
    """tests for model"""

    def test_constructors(self):
        """try building model"""

        with self.assertRaises(pydantic.ValidationError):
            Model()

        now = datetime.datetime.now()

        m = Model(
            name="2024_01_01_ResNet18_SmartSPIM.h5",
            license="CC-BY-4.0",
            developer_full_name=["Joe Schmoe"],
            developer_institution=Organization.AIND,
            modality=Modality.SPIM,
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
                    input_location=["s3 path to eval 1", "s3 path to eval 2"],
                    output_location="s3 path to trained model asset",
                    code_url="url for training code repo",
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
                    parameters={
                        "learning_rate": 0.0001,
                        "batch_size": 32,
                        "augmentation": True,
                    },
                    notes="note on training data selection",
                )
            ],
            evaluations=[
                ModelEvaluation(
                    input_location=["s3 path to eval 1", "s3 path to eval 2"],
                    output_location="s3 path (output asset or trained model asset if no output)",
                    code_url="url for evaluation code repo (or capsule?)",
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
