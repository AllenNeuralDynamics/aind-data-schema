"""test quality metrics """

import unittest
from datetime import datetime

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
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage=Stage.PROCESSING,
            qc_metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    metric_status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    reference="s3://some-data-somewhere",
                    metric_status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
            ],
        )

        q = QualityControl(
            evaluations=[test_eval],
        )

        assert q is not None

    def test_overall_status(self):
        """test that overall status goes to pass/pending/fail correctly"""

        test_eval = QCEvaluation(
            evaluation_name="Drift map",
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage=Stage.PROCESSING,
            qc_metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    metric_status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    reference="s3://some-data-somewhere",
                    metric_status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
            ],
        )

        test_eval.evaluate_status()

        q = QualityControl(
            evaluations=[test_eval, test_eval],
        )

        q.evaluate_status()
        self.assertEqual(q.overall_status.status, Status.PASS)

        # Add a pending metric to the first evaluation
        q.evaluations[0].qc_metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                metric_status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
            )
        )

        q.evaluate_status()
        self.assertEqual(q.overall_status.status, Status.PENDING)

        # Add a failing metric to the first evaluation
        q.evaluations[0].qc_metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                metric_status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
            )
        )

        q.evaluate_status()
        self.assertEqual(q.overall_status.status, Status.FAIL)

    def test_evaluation_status(self):
        """test that evaluation status goes to pass/pending/fail correctly"""
        evaluation = QCEvaluation(
            evaluation_name="Drift map",
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage=Stage.PROCESSING,
            qc_metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    metric_status_history=[
                        QCStatus(
                            evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                        )
                    ],
                ),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    reference="s3://some-data-somewhere",
                    metric_status_history=[
                        QCStatus(
                            evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                        )
                    ],
                ),
            ],
        )

        evaluation.evaluate_status()

        self.assertEqual(evaluation.evaluation_status.status, Status.PASS)

        # Add a pending metric, evaluation should now evaluate to pending
        evaluation.qc_metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                metric_status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
            )
        )

        evaluation.evaluate_status()

        self.assertEqual(evaluation.evaluation_status.status, Status.PENDING)

        # Add a failing metric, evaluation should now evaluate to fail
        evaluation.qc_metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                metric_status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
            )
        )

        evaluation.evaluate_status()

        self.assertEqual(evaluation.evaluation_status.status, Status.FAIL)


if __name__ == "__main__":
    unittest.main()
