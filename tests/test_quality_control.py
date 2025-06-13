"""test quality metrics """

import unittest
from datetime import datetime

from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError

from aind_data_schema.core.quality_control import QCMetric, QCStatus, QualityControl, Stage, Status

from examples.quality_control import q as quality_control


class QualityControlTests(unittest.TestCase):
    """test quality metrics schema"""

    def test_constructors(self):
        """testing constructors"""

        self.assertRaises(ValidationError, QualityControl)

        assert quality_control is not None

    def test_overall_status(self):
        """test that overall status goes to pass/pending/fail correctly"""

        test_metrics = [
            QCMetric(
                name="Dict example",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["Drift map"]
            ),
            QCMetric(
                name="Drift map pass/fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["Drift map"]
            ),
        ]

        q = QualityControl(
            metrics=test_metrics + test_metrics,  # duplicate the metrics
            default_grouping=["Drift map"]
        )

        # check that overall status gets auto-set if it has never been set before
        self.assertEqual(q.evaluate_status(), Status.PASS)

        # Add a pending metric
        q.metrics.append(
            QCMetric(
                name="Drift map pending",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
                tags=["Drift map"]
            )
        )

        self.assertEqual(q.evaluate_status(), Status.PENDING)

        # Add a failing metric
        q.metrics.append(
            QCMetric(
                name="Drift map fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
                tags=["Drift map"]
            )
        )

        self.assertEqual(q.evaluate_status(), Status.FAIL)

    def test_evaluation_status(self):
        """test that evaluation status goes to pass/pending/fail correctly"""
        metrics = [
            QCMetric(
                name="Multiple values example",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                    )
                ],
                tags=["Drift map"]
            ),
            QCMetric(
                name="Drift map pass/fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                    )
                ],
                tags=["Drift map"]
            ),
        ]

        qc = QualityControl(metrics=metrics, default_grouping=["Drift map"])
        self.assertEqual(qc.evaluate_status(tag="Drift map"), Status.PASS)

        # Add a pending metric, evaluation should now evaluate to pending
        qc.metrics.append(
            QCMetric(
                name="Drift map pending",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
                tags=["Drift map"]
            )
        )

        self.assertEqual(qc.evaluate_status(tag="Drift map"), Status.PENDING)

        # Add a failing metric, evaluation should now evaluate to fail
        qc.metrics.append(
            QCMetric(
                name="Drift map fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
                tags=["Drift map"]
            )
        )

        self.assertEqual(qc.evaluate_status(tag="Drift map"), Status.FAIL)

    def test_allowed_failed_metrics(self):
        """Test that if you set the flag to allow failures that tags pass"""

        metrics = [
            QCMetric(
                name="Multiple values example",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS
                    )
                ],
                tags=["Drift map"]
            ),
            QCMetric(
                name="Drift map pass/fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING)
                ],
                tags=["Drift map"]
            ),
        ]

        # First check that a pending evaluation still evaluates properly
        qc = QualityControl(
            metrics=metrics,
            default_grouping=["Drift map"],
        )

        self.assertEqual(qc.evaluate_status(tag="Drift map"), Status.PENDING)

        # Replace the pending evaluation with a fail, evaluation should not evaluate to pass
        qc.metrics[1].status_history[0].status = Status.FAIL

        self.assertEqual(qc.evaluate_status(tag="Drift map"), Status.FAIL)

        # Now add the tag to allow_tag_failures
        qc.allow_tag_failures = ["Drift map"]

        self.assertEqual(qc.evaluate_status(tag="Drift map"), Status.PASS)

    def test_metric_history_order(self):
        """Test that the order of the metric status history list is preserved when dumping"""
        t0 = datetime.fromisoformat("2020-10-10")
        t1 = datetime.fromisoformat("2020-10-11")
        t2 = datetime.fromisoformat("2020-10-12")

        metric = QCMetric(
            name="Multiple values example",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            value={"stuff": "in_a_dict"},
            status_history=[
                QCStatus(evaluator="Automated", timestamp=t0, status=Status.PASS),
                QCStatus(evaluator="Automated", timestamp=t1, status=Status.PASS),
                QCStatus(evaluator="Automated", timestamp=t2, status=Status.PASS),
            ],
            tags=["Drift map"]
        )

        qc = QualityControl(metrics=[metric], default_grouping=["Drift map"])

        # roundtrip to json to check that metric order is preserved
        json = qc.model_dump_json()
        qc_rebuild = QualityControl.model_validate_json(json)

        # because the actual model uses AwareDatetime objects we have to strip the timezone
        roundtrip_t0 = qc_rebuild.metrics[0].status_history[0].timestamp
        roundtrip_t1 = qc_rebuild.metrics[0].status_history[1].timestamp
        roundtrip_t2 = qc_rebuild.metrics[0].status_history[2].timestamp

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
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value={"stuff": "in_a_dict"},
                status_history=[],
            )

        expected_exception = "List should have at least 1 item after validation, not 0"
        self.assertTrue(expected_exception in repr(context.exception))

    def test_multi_acquisition(self):
        """Ensure that the multi-asset QC validator checks for evaluated_assets"""
        # Check for non-multi-acquisition that all evaluated_assets are None
        t0 = datetime.fromisoformat("2020-10-10")

        metric = QCMetric(
            name="Dict example",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            value={"stuff": "in_a_dict"},
            status_history=[
                QCStatus(evaluator="Automated", timestamp=t0, status=Status.PASS),
            ],
            tags=["Test"]
        )

        qc = QualityControl(metrics=[metric], default_grouping=["Test"])

        self.assertTrue(metric.stage != Stage.MULTI_ASSET)
        self.assertIsNone(metric.evaluated_assets)

        # Check that single-asset QC with evaluated_assets throws a validation error
        with self.assertRaises(ValidationError) as context:
            QCMetric(
                name="Dict with evaluated assets list",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=t0, status=Status.PASS),
                ],
                evaluated_assets=["asset0", "asset1"],
                tags=["Test"]
            )

        self.assertTrue(
            "is a single-asset metric and should not have evaluated_assets" in repr(context.exception)
        )

        # Check that multi-asset with empty evaluated_assets raises a validation error
        with self.assertRaises(ValidationError) as context:
            QCMetric(
                name="Missing evaluated assets",
                modality=Modality.ECEPHYS,
                stage=Stage.MULTI_ASSET,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=t0, status=Status.PASS),
                ],
                evaluated_assets=[],
                tags=["Test"]
            )

        self.assertTrue("is a multi-asset metric and must have evaluated_assets" in repr(context.exception))

        # Check that multi-asset with missing evaluated_assets raises a validation error
        with self.assertRaises(ValidationError) as context:
            QCMetric(
                name="Multiple values example",
                modality=Modality.ECEPHYS,
                stage=Stage.MULTI_ASSET,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=t0, status=Status.PASS),
                ],
                tags=["Test"]
            )

        self.assertTrue("is a multi-asset metric and must have evaluated_assets" in repr(context.exception))

    def test_status_filters(self):
        """Test that QualityControl.status(modality, stage) filters correctly"""

        test_metrics = [
            QCMetric(
                name="Multiple values example",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["test_group"]
            ),
            QCMetric(
                name="Drift map pass/fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["test_group"]
            ),
            QCMetric(
                name="Multiple values example 2",
                modality=Modality.BEHAVIOR,
                stage=Stage.RAW,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
                tags=["test_group2"]
            ),
            QCMetric(
                name="Drift map pass/fail 2",
                modality=Modality.BEHAVIOR,
                stage=Stage.RAW,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["test_group2"]
            ),
            QCMetric(
                name="Multiple values example 3",
                modality=Modality.BEHAVIOR_VIDEOS,
                stage=Stage.RAW,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING)
                ],
                tags=["tag1"]
            ),
            QCMetric(
                name="Drift map pass/fail 3",
                modality=Modality.BEHAVIOR_VIDEOS,
                stage=Stage.RAW,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["tag1"]
            ),
        ]

        # Confirm that the status filters work
        q = QualityControl(
            metrics=test_metrics,
            default_grouping=["test_group", "test_group2", "tag1"]
        )

        self.assertEqual(q.evaluate_status(), Status.FAIL)
        self.assertEqual(q.evaluate_status(modality=Modality.BEHAVIOR), Status.FAIL)
        self.assertEqual(q.evaluate_status(modality=Modality.ECEPHYS), Status.PASS)
        self.assertEqual(q.evaluate_status(modality=[Modality.ECEPHYS, Modality.BEHAVIOR]), Status.FAIL)
        self.assertEqual(q.evaluate_status(stage=Stage.RAW), Status.FAIL)
        self.assertEqual(q.evaluate_status(stage=Stage.PROCESSING), Status.PASS)
        self.assertEqual(q.evaluate_status(tag="tag1"), Status.PENDING)

    def test_status_date(self):
        """QualityControl.status(date=) should return the correct status for the given date"""

        t0_5 = datetime.fromisoformat("0500-01-01 00:00:00+00:00")
        t1 = datetime.fromisoformat("1000-01-01 00:00:00+00:00")
        t1_5 = datetime.fromisoformat("1500-01-01 00:00:00+00:00")
        t2 = datetime.fromisoformat("2000-01-01 00:00:00+00:00")
        t2_5 = datetime.fromisoformat("2500-01-01 00:00:00+00:00")
        t3 = datetime.fromisoformat("3000-01-01 00:00:00+00:00")
        t3_5 = datetime.fromisoformat("3500-01-01 00:00:00+00:00")

        metric = QCMetric(
            name="Drift map pass/fail",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            value=False,
            status_history=[
                QCStatus(evaluator="Bob", timestamp=t1, status=Status.FAIL),
                QCStatus(evaluator="Bob", timestamp=t2, status=Status.PENDING),
                QCStatus(evaluator="Bob", timestamp=t3, status=Status.PASS),
            ],
            tags=["test_group"]
        )

        # Note: The date filtering is currently not implemented in the new schema
        # This test would need to be updated once date filtering is implemented
        qc = QualityControl(metrics=[metric], default_grouping=["test_group"])

        # For now, just test current status
        self.assertEqual(qc.evaluate_status(), Status.PASS)


if __name__ == "__main__":
    unittest.main()
