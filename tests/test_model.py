""" tests for Model """

import datetime
import unittest

import pydantic

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.system_architecture import ModelBackbone

from aind_data_schema.core.model import Model, ModelArchitecture, ModelEvaluation, ModelTraining, PerformanceMetric
from aind_data_schema.components.devices import Software


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
            developer_full_name="Joe Schmoe",
            developer_institution=Organization.AIND,
            modality=Modality.SPIM,
            model_architecture=ModelArchitecture(
                backbone=ModelBackbone.RESNET,
                layers=18,
                parameters={
                    "downsample": 1,
                    "input_shape": [
                        14,
                        14,
                        26
                    ],
                    "learning_rate": 0.0001,
                    "train_test_split": 0.8,
                    "batch_size": 32,
                    "augmentation": True,
                    "finetuning": True
                },
            ),
            software=[Software(
                name="tensorflow",
                version="2.11.0",
                )
            ],
            intended_use="Cell counting for 488 channel of SmartSPIM data",
            limitations="Only trained on 488 channel",
            training=[
                ModelTraining(
                    data="path to training set",
                    data_description="description of training set",
                    date=now,
                    performance=[
                        PerformanceMetric(
                            name="precision",
                            value=0.9
                        ),
                        PerformanceMetric(
                            name="recall",
                            value=0.85
                        )
                    ],
                    cross_validation_method="5-fold"
                )
            ],
            evaluations=[
                ModelEvaluation(
                    data="path to evaluation data",
                    data_description="description of evaluation set",
                    date=now,
                    performance=[
                        PerformanceMetric(
                            name="precision",
                            value="0.8"
                        )
                    ]
                )
            ]
        )

        Model.model_validate_json(m.model_dump_json())

        self.assertIsNotNone(m)


if __name__ == "__main__":
    unittest.main()
    