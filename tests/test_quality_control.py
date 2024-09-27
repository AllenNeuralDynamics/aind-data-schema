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

        # check that evaluation status gets auto-set if it has never been set before
        self.assertEqual(test_eval.evaluation_status.status, Status.PASS)

        q = QualityControl(
            evaluations=[test_eval, test_eval],
        )

        # check that overall status gets auto-set if it has never been set before
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

    def test_allowed_failed_metrics(self):
        """Test that if you set the flag to allow failures that evaluations pass"""

        metric2 = QCMetric(
            name="Drift map pass/fail",
            value=False,
            description="Manual evaluation of whether the drift map looks good",
            reference="s3://some-data-somewhere",
            metric_status_history=[
                QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING)
            ],
        )

        # First check that a pending evaluation still evaluates properly
        evaluation = QCEvaluation(
            evaluation_name="Drift map",
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage=Stage.PROCESSING,
            allow_failed_metrics=False,
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
                metric2,
            ],
        )

        self.assertIsNone(evaluation.failed_metrics)

        evaluation.allow_failed_metrics = True
        evaluation.evaluate_status()

        self.assertEqual(evaluation.evaluation_status.status, Status.PENDING)

        # Replace the pending evaluation with a fail, evaluation should not evaluate to pass
        evaluation.qc_metrics[1].metric_status_history[0].status = Status.FAIL

        evaluation.evaluate_status()

        self.assertEqual(evaluation.evaluation_status.status, Status.PASS)

        metric2.metric_status_history[0].status = Status.FAIL
        self.assertEqual(evaluation.failed_metrics, [metric2])

    def test_metric_history_order(self):
        """Test that the order of the metric status history list is preserved when dumping"""
        t0 = datetime.fromisoformat("2020-10-10")
        t1 = datetime.fromisoformat("2020-10-11")
        t2 = datetime.fromisoformat("2020-10-12")

        evaluation = QCEvaluation(
            evaluation_name="Drift map",
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage=Stage.PROCESSING,
            qc_metrics=[
                QCMetric(
                    name="Multiple values example",
                    value={"stuff": "in_a_dict"},
                    metric_status_history=[
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
        roundtrip_t0 = evaluation_rebuild.qc_metrics[0].metric_status_history[0].timestamp
        roundtrip_t1 = evaluation_rebuild.qc_metrics[0].metric_status_history[1].timestamp
        roundtrip_t2 = evaluation_rebuild.qc_metrics[0].metric_status_history[2].timestamp

        roundtrip_t0 = roundtrip_t0.replace(tzinfo=None)
        roundtrip_t1 = roundtrip_t1.replace(tzinfo=None)
        roundtrip_t2 = roundtrip_t2.replace(tzinfo=None)

        self.assertEqual(roundtrip_t0, t0)
        self.assertEqual(roundtrip_t1, t1)
        self.assertEqual(roundtrip_t2, t2)


if __name__ == "__main__":
    unittest.main()
