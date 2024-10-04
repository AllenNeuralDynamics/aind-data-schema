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
            name="Drift map",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    reference="s3://some-data-somewhere",
                    status_history=[
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
            name="Drift map",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    reference="s3://some-data-somewhere",
                    status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
            ],
        )

        # check that evaluation status gets auto-set if it has never been set before
        self.assertEqual(test_eval.status, Status.PASS)

        q = QualityControl(
            evaluations=[test_eval, test_eval],
        )

        # check that overall status gets auto-set if it has never been set before
        self.assertEqual(q.status, Status.PASS)

        # Add a pending metric to the first evaluation
        q.evaluations[0].metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
            )
        )

        self.assertEqual(q.status, Status.PENDING)

        # Add a failing metric to the first evaluation
        q.evaluations[0].metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
            )
        )

        self.assertEqual(q.status, Status.FAIL)

    def test_evaluation_status(self):
        """test that evaluation status goes to pass/pending/fail correctly"""
        evaluation = QCEvaluation(
            name="Drift map",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    status_history=[
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
                    status_history=[
                        QCStatus(
                            evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                        )
                    ],
                ),
            ],
        )

        self.assertEqual(evaluation.status, Status.PASS)

        # Add a pending metric, evaluation should now evaluate to pending
        evaluation.metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
            )
        )

        self.assertEqual(evaluation.status, Status.PENDING)

        # Add a failing metric, evaluation should now evaluate to fail
        evaluation.metrics.append(
            QCMetric(
                name="Drift map pass/fail",
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
            )
        )

        self.assertEqual(evaluation.status, Status.FAIL)

    def test_allowed_failed_metrics(self):
        """Test that if you set the flag to allow failures that evaluations pass"""

        metric2 = QCMetric(
            name="Drift map pass/fail",
            value=False,
            description="Manual evaluation of whether the drift map looks good",
            reference="s3://some-data-somewhere",
            status_history=[
                QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING)
            ],
        )

        # First check that a pending evaluation still evaluates properly
        evaluation = QCEvaluation(
            name="Drift map",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            allow_failed_metrics=False,
            metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    status_history=[
                        QCStatus(
                            evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                        )
                    ],
                ),
                metric2,
            ],
        )

        self.assertIsNone(evaluation.failed_metrics)

        evaluation.allow_failed_metrics = True

        self.assertEqual(evaluation.status, Status.PENDING)

        # Replace the pending evaluation with a fail, evaluation should not evaluate to pass
        evaluation.metrics[1].status_history[0].status = Status.FAIL

        self.assertEqual(evaluation.status, Status.PASS)

        metric2.status_history[0].status = Status.FAIL
        self.assertEqual(evaluation.failed_metrics, [metric2])

    def test_metric_history_order(self):
        """Test that the order of the metric status history list is preserved when dumping"""
        t0 = datetime.fromisoformat("2020-10-10")
        t1 = datetime.fromisoformat("2020-10-11")
        t2 = datetime.fromisoformat("2020-10-12")

        evaluation = QCEvaluation(
            name="Drift map",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    status_history=[
                        QCStatus(evaluator="Automated", timestamp=t0, status=Status.PASS),
                        QCStatus(evaluator="Automated", timestamp=t1, status=Status.PASS),
                        QCStatus(evaluator="Automated", timestamp=t2, status=Status.PASS),
                    ],
                ),
            ],
        )

        #  roundtrip to json to check that metric order is preserved
        json = evaluation.model_dump_json()
        evaluation_rebuild = QCEvaluation.model_validate_json(json)

        # because the actual model uses AwareDatetime objects we have to strip the timezone
        roundtrip_t0 = evaluation_rebuild.metrics[0].status_history[0].timestamp
        roundtrip_t1 = evaluation_rebuild.metrics[0].status_history[1].timestamp
        roundtrip_t2 = evaluation_rebuild.metrics[0].status_history[2].timestamp

        roundtrip_t0 = roundtrip_t0.replace(tzinfo=None)
        roundtrip_t1 = roundtrip_t1.replace(tzinfo=None)
        roundtrip_t2 = roundtrip_t2.replace(tzinfo=None)

        self.assertEqual(roundtrip_t0, t0)
        self.assertEqual(roundtrip_t1, t1)
        self.assertEqual(roundtrip_t2, t2)

    def test_metric_status(self):
        """Ensure that at least one status object exists for metric_status_history"""

        with self.assertRaises(ValueError) as context:
            QCMetric(
                name="Multiple values example",
                value={"stuff": "in_a_dict"},
                status_history=[],
            )

        expected_exception = "At least one QCStatus object must be provided"

        self.assertTrue(expected_exception in repr(context.exception))


if __name__ == "__main__":
    unittest.main()
