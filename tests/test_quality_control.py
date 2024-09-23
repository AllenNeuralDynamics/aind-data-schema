"""test quality metrics """

import unittest
from datetime import date

from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status, QCStatus


class QualityControlTests(unittest.TestCase):
    """test quality metrics schema"""

    def test_constructors(self):
        """testing constructors"""

        with self.assertRaises(ValidationError):
            q = QualityControl()

        test_eval = QCEvaluation(
                evaluation_name="Drift map",
                evaluation_status=[
                    QCStatus(
                        evaluator="Fred Flintstone",
                        timestamp=date.fromisoformat("2020-10-10"),
                        status=Status.PASS
                    )
                ],
                evaluation_modality=Modality.ECEPHYS,
                evaluation_stage=Stage.PROCESSING,
                qc_metrics=[
                    QCMetric(
                        name="Multiple values example",
                        value={"stuff": "in_a_dict"}
                    ),
                    QCMetric(
                        name="Drift map pass/fail",
                        value=False,
                        description="Manual evaluation of whether the drift map looks good",
                        references=["s3://some-data-somewhere"]
                    )
                ],
            )

        q = QualityControl(
            overall_status=[
                QCStatus(
                    evaluator="Bob",
                    timestamp=date.fromisoformat("2020-10-10"),
                    status=Status.PASS
                )
            ],
            evaluations=[
                test_eval
            ],
        )

        assert q is not None


if __name__ == "__main__":
    unittest.main()
