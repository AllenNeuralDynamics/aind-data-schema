"""test quality metrics """

import unittest
from datetime import datetime

from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError

from aind_data_schema.core.quality_control import (
    QCMetric,
    QCStatus,
    QualityControl,
    Stage,
    Status,
    _get_filtered_statuses,
    _get_status_by_date,
)

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
                tags=["Drift map"],
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
                tags=["Drift map"],
            ),
        ]

        self.assertEqual(test_metrics[0].status.status, Status.PASS)

        q = QualityControl(metrics=test_metrics + test_metrics, default_grouping=["Drift map"])  # duplicate the metrics

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
                tags=["Drift map"],
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
                tags=["Drift map"],
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
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["Drift map"],
            ),
            QCMetric(
                name="Drift map pass/fail",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                description="Manual evaluation of whether the drift map looks good",
                reference="s3://some-data-somewhere",
                status_history=[
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["Drift map"],
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
                tags=["Drift map"],
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
                tags=["Drift map"],
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
                    QCStatus(evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                ],
                tags=["Drift map"],
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
                        evaluator="Automated", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING
                    )
                ],
                tags=["Drift map"],
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
            tags=["Drift map"],
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
            tags=["Test"],
        )

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
                tags=["Test"],
            )

        self.assertTrue("is a single-asset metric and should not have evaluated_assets" in repr(context.exception))

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
                tags=["Test"],
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
                tags=["Test"],
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
                tags=["test_group"],
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
                tags=["test_group"],
            ),
            QCMetric(
                name="Multiple values example 2",
                modality=Modality.BEHAVIOR,
                stage=Stage.RAW,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.FAIL)
                ],
                tags=["test_group2"],
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
                tags=["test_group2"],
            ),
            QCMetric(
                name="Multiple values example 3",
                modality=Modality.BEHAVIOR_VIDEOS,
                stage=Stage.RAW,
                value={"stuff": "in_a_dict"},
                status_history=[
                    QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PENDING)
                ],
                tags=["tag1"],
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
                tags=["tag1"],
            ),
        ]

        # Confirm that the status filters work
        q = QualityControl(metrics=test_metrics, default_grouping=["test_group", "test_group2", "tag1"])

        # Check that the status field was built correctly
        self.assertEqual(
            q.status,
            {
                # Stages
                "Processing": Status.PASS,
                "Raw data": Status.FAIL,
                # Modalities
                "behavior": Status.FAIL,
                "behavior-videos": Status.PENDING,
                "ecephys": Status.PASS,
                # Tags
                "test_group": Status.PASS,
                "test_group2": Status.FAIL,
                "tag1": Status.PENDING,
            },
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

        t1 = datetime.fromisoformat("1000-01-01 00:00:00+00:00")
        t2 = datetime.fromisoformat("2000-01-01 00:00:00+00:00")
        t3 = datetime.fromisoformat("3000-01-01 00:00:00+00:00")

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
            tags=["test_group"],
        )

        # Note: The date filtering is currently not implemented in the new schema
        # This test would need to be updated once date filtering is implemented
        qc = QualityControl(metrics=[metric], default_grouping=["test_group"])

        self.assertEqual(qc.evaluate_status(date=t3), Status.PASS)
        self.assertEqual(qc.evaluate_status(date=t2), Status.PENDING)
        self.assertEqual(qc.evaluate_status(date=t1), Status.FAIL)

    def test_get_status_by_date_helper(self):
        """Test the _get_status_by_date helper function with various scenarios"""

        # Create timestamps for testing
        t1 = datetime.fromisoformat("2020-01-01T00:00:00+00:00")
        t2 = datetime.fromisoformat("2020-02-01T00:00:00+00:00")
        t3 = datetime.fromisoformat("2020-03-01T00:00:00+00:00")

        # Create a metric with multiple status history entries
        metric = QCMetric(
            name="Test metric",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            value=True,
            status_history=[
                QCStatus(evaluator="Alice", timestamp=t1, status=Status.FAIL),
                QCStatus(evaluator="Bob", timestamp=t2, status=Status.PENDING),
                QCStatus(evaluator="Charlie", timestamp=t3, status=Status.PASS),
            ],
            tags=["test"],
        )

        # Test getting status at different dates

        # Date before any status - should return earliest status
        early_date = datetime.fromisoformat("1999-01-01T00:00:00+00:00")
        self.assertEqual(_get_status_by_date(metric, early_date), Status.FAIL)

        # Date exactly at first status
        self.assertEqual(_get_status_by_date(metric, t1), Status.FAIL)

        # Date between first and second status
        between_t1_t2 = datetime.fromisoformat("2020-01-15T00:00:00+00:00")
        self.assertEqual(_get_status_by_date(metric, between_t1_t2), Status.FAIL)

        # Date exactly at second status
        self.assertEqual(_get_status_by_date(metric, t2), Status.PENDING)

        # Date between second and third status
        between_t2_t3 = datetime.fromisoformat("2020-02-15T00:00:00+00:00")
        self.assertEqual(_get_status_by_date(metric, between_t2_t3), Status.PENDING)

        # Date exactly at third status
        self.assertEqual(_get_status_by_date(metric, t3), Status.PASS)

        # Date after all statuses - should return most recent status
        future_date = datetime.fromisoformat("2025-01-01T00:00:00+00:00")
        self.assertEqual(_get_status_by_date(metric, future_date), Status.PASS)

        # Test with single status entry
        single_status_metric = QCMetric(
            name="Single status metric",
            modality=Modality.BEHAVIOR,
            stage=Stage.RAW,
            value=42,
            status_history=[
                QCStatus(evaluator="Dave", timestamp=t2, status=Status.PASS),
            ],
            tags=["single"],
        )

        # Date before single status - should return that status
        self.assertEqual(_get_status_by_date(single_status_metric, t1), Status.PASS)
        # Date at single status
        self.assertEqual(_get_status_by_date(single_status_metric, t2), Status.PASS)
        # Date after single status
        self.assertEqual(_get_status_by_date(single_status_metric, t3), Status.PASS)

    def test_get_filtered_statuses_helper(self):
        """Test the _get_filtered_statuses helper function with various filters"""

        # Create test date
        test_date = datetime.fromisoformat("2020-06-01T00:00:00+00:00")

        # Use existing quality_control example and add some test metrics
        test_metrics = list(quality_control.metrics)  # Copy existing metrics

        # Add some additional test metrics with different modalities, stages, and tags
        additional_metrics = [
            QCMetric(
                name="Test BEHAVIOR metric",
                modality=Modality.BEHAVIOR,
                stage=Stage.PROCESSING,
                value=True,
                status_history=[QCStatus(evaluator="Test", timestamp=test_date, status=Status.PASS)],
                tags=["behavior_tag", "shared_tag"],
            ),
            QCMetric(
                name="Test OPHYS metric",
                modality=Modality.POPHYS,
                stage=Stage.ANALYSIS,
                value=42,
                status_history=[QCStatus(evaluator="Test", timestamp=test_date, status=Status.FAIL)],
                tags=["ophys_tag", "shared_tag"],
            ),
            QCMetric(
                name="Test metric with early fail",
                modality=Modality.ECEPHYS,
                stage=Stage.RAW,
                value=False,
                status_history=[
                    QCStatus(
                        evaluator="Test",
                        timestamp=datetime.fromisoformat("2020-01-01T00:00:00+00:00"),
                        status=Status.FAIL,
                    ),
                    QCStatus(evaluator="Test", timestamp=test_date, status=Status.PASS),
                ],
                tags=["time_test"],
            ),
        ]

        all_metrics = test_metrics + additional_metrics

        # Test filtering by modality
        ecephys_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            modality_filter=[Modality.ECEPHYS],
        )
        # Should include ECEPHYS metrics from quality_control example + our test metric
        self.assertGreater(len(ecephys_statuses), 0)

        behavior_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            modality_filter=[Modality.BEHAVIOR],
        )
        self.assertEqual(len(behavior_statuses), 1)  # Our test BEHAVIOR metric
        self.assertEqual(behavior_statuses[0], Status.PASS)

        # Test filtering by stage
        raw_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            stage_filter=[Stage.RAW],
        )
        self.assertGreater(len(raw_statuses), 0)

        analysis_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            stage_filter=[Stage.ANALYSIS],
        )
        self.assertEqual(len(analysis_statuses), 1)  # Our test OPHYS metric
        self.assertEqual(analysis_statuses[0], Status.FAIL)

        # Test filtering by tag
        shared_tag_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            tag_filter=["shared_tag"],
        )
        self.assertEqual(len(shared_tag_statuses), 2)  # Our BEHAVIOR and OPHYS test metrics
        self.assertIn(Status.PASS, shared_tag_statuses)
        self.assertIn(Status.FAIL, shared_tag_statuses)

        # Test filtering by multiple criteria
        ecephys_raw_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            modality_filter=[Modality.ECEPHYS],
            stage_filter=[Stage.RAW],
        )
        self.assertGreater(len(ecephys_raw_statuses), 0)

        # Test date-based status retrieval
        earlier_date = datetime.fromisoformat("2020-03-01T00:00:00+00:00")
        time_test_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=earlier_date,
            tag_filter=["time_test"],
        )
        self.assertEqual(len(time_test_statuses), 1)
        self.assertEqual(time_test_statuses[0], Status.FAIL)  # Should get the earlier FAIL status

        # Test allow_tag_failures
        ophys_fail_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            tag_filter=["ophys_tag"],
            allow_tag_failures=["ophys_tag"],
        )
        self.assertEqual(len(ophys_fail_statuses), 1)
        self.assertEqual(ophys_fail_statuses[0], Status.PASS)  # FAIL converted to PASS

        # Test with no matching filters
        no_match_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            tag_filter=["nonexistent_tag"],
        )
        self.assertEqual(len(no_match_statuses), 0)

        # Test with empty metrics list
        empty_statuses = _get_filtered_statuses(
            metrics=[],
            date=test_date,
        )
        self.assertEqual(len(empty_statuses), 0)

        # Test multiple modalities and stages
        multi_modality_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            modality_filter=[Modality.BEHAVIOR, Modality.POPHYS],
        )
        self.assertEqual(len(multi_modality_statuses), 2)  # Our BEHAVIOR and OPHYS test metrics

        multi_stage_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            stage_filter=[Stage.PROCESSING, Stage.ANALYSIS],
        )
        self.assertEqual(len(multi_stage_statuses), 2)  # Our BEHAVIOR and OPHYS test metrics

        # Test filtering using a tuple mixing two tags
        tuple_tag_statuses = _get_filtered_statuses(
            metrics=all_metrics,
            date=test_date,
            tag_filter=["shared_tag"],
            allow_tag_failures=[("ophys_tag", "shared_tag")],
        )
        self.assertEqual(len(tuple_tag_statuses), 2)
        self.assertEqual(tuple_tag_statuses[0], Status.PASS)
        self.assertEqual(tuple_tag_statuses[1], Status.PASS)

    def test_helper_functions_integration(self):
        """Test that helper functions work correctly when used by QualityControl.evaluate_status"""

        # Create a test date
        test_date = datetime.fromisoformat("2020-06-01T00:00:00+00:00")

        # Create metrics with time-based status changes
        metrics = [
            QCMetric(
                name="Time-sensitive metric 1",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=True,
                status_history=[
                    QCStatus(
                        evaluator="Test",
                        timestamp=datetime.fromisoformat("2020-01-01T00:00:00+00:00"),
                        status=Status.FAIL,
                    ),
                    QCStatus(
                        evaluator="Test",
                        timestamp=datetime.fromisoformat("2020-06-01T00:00:00+00:00"),
                        status=Status.PASS,
                    ),
                ],
                tags=["time_sensitive"],
            ),
            QCMetric(
                name="Time-sensitive metric 2",
                modality=Modality.ECEPHYS,
                stage=Stage.PROCESSING,
                value=False,
                status_history=[
                    QCStatus(
                        evaluator="Test",
                        timestamp=datetime.fromisoformat("2020-01-01T00:00:00+00:00"),
                        status=Status.PASS,
                    ),
                    QCStatus(
                        evaluator="Test",
                        timestamp=datetime.fromisoformat("2020-07-01T00:00:00+00:00"),
                        status=Status.FAIL,
                    ),
                ],
                tags=["time_sensitive"],
            ),
        ]

        qc = QualityControl(
            metrics=metrics,
            default_grouping=["time_sensitive"],
        )

        # Test status at different times
        early_date = datetime.fromisoformat("2020-02-01T00:00:00+00:00")
        # At early date: metric 1 is FAIL, metric 2 is PASS -> overall FAIL
        early_status = qc.evaluate_status(date=early_date, tag="time_sensitive")
        self.assertEqual(early_status, Status.FAIL)

        # At test date: metric 1 is PASS, metric 2 is PASS -> overall PASS
        test_status = qc.evaluate_status(date=test_date, tag="time_sensitive")
        self.assertEqual(test_status, Status.PASS)

        # At late date: metric 1 is PASS, metric 2 is FAIL -> overall FAIL
        late_date = datetime.fromisoformat("2020-08-01T00:00:00+00:00")
        late_status = qc.evaluate_status(date=late_date, tag="time_sensitive")
        self.assertEqual(late_status, Status.FAIL)


if __name__ == "__main__":
    unittest.main()
