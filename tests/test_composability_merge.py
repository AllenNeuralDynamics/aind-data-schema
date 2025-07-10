"""Test for merge functions"""

import unittest
from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.identifiers import Code
from aind_data_schema.core.acquisition import AcquisitionSubjectDetails
from aind_data_schema.core.procedures import Procedures
from aind_data_schema.core.processing import DataProcess, Processing, ProcessName, ProcessStage
from aind_data_schema.core.quality_control import QCMetric, QCStatus, QualityControl, Stage, Status
from examples.exaspim_acquisition import acq
from examples.procedures import p, t, t2


class TestComposability(unittest.TestCase):
    """Tests for merge functions"""

    @classmethod
    def setUpClass(cls):
        """Load example files for testing"""
        cls.exaspim_acquisition = acq
        cls.procedures = p
        cls.procedures_time0 = t
        cls.procedures_time1 = t2

    def test_merge_quality_control(self):
        """Test adding two QualityControl objects"""

        metrics = [
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

        q1 = QualityControl(
            metrics=metrics,
            default_grouping=["Drift map"],
        )

        q2 = QualityControl(
            metrics=metrics + metrics,
            default_grouping=["Drift map"],
        )

        q3 = q1 + q2
        self.assertIsNotNone(q3)
        self.assertTrue(len(q3.metrics) == 6)

        # Test incompatible schema versions
        q1_orig_schema_v = q1.schema_version
        q1.schema_version = "0.1.0"

        with self.assertRaises(ValueError) as context:
            q1 + q2
        self.assertTrue(
            "Cannot combine QualityControl objects with different schema versions" in repr(context.exception)
        )

        # Test various versions of concatenating notes
        q1.schema_version = q1_orig_schema_v
        q1.notes = "note1"
        q2.notes = "note2"
        q3 = q1 + q2
        self.assertTrue(q3.notes == "note1\nnote2")

        q1.notes = None
        q3 = q1 + q2
        self.assertTrue(q3.notes == "note2")

        q1.notes = "note1"
        q2.notes = None
        q3 = q1 + q2
        self.assertTrue(q3.notes == "note1")

    def test_merge_acquisition(self):
        """Test merging two Acquisition objects"""

        t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

        acq1 = self.exaspim_acquisition.model_copy()
        acq2 = self.exaspim_acquisition.model_copy()

        merged_acq = acq1 + acq2

        self.assertEqual(len(merged_acq.experimenters), 2)
        self.assertEqual(len(merged_acq.maintenance), 2)
        self.assertEqual(len(merged_acq.calibrations), 2)
        self.assertEqual(len(merged_acq.data_streams), 2)
        self.assertEqual(merged_acq.acquisition_start_time, t)
        self.assertEqual(merged_acq.acquisition_end_time, t)
        self.assertEqual(merged_acq.acquisition_type, "ExaSPIM")

        # Test incompatible schema versions
        acq1_orig_schema_v = acq1.schema_version
        acq1.schema_version = "0.1.0"

        with self.assertRaises(ValueError) as context:
            acq1 + acq2
        self.assertTrue("Cannot combine Acquisition objects with different schema versions" in repr(context.exception))

        acq1.schema_version = acq1_orig_schema_v

        # Test incompatible subject IDs
        acq2.subject_id = "different_id"
        with self.assertRaises(ValueError) as context:
            acq1 + acq2
        self.assertTrue("Cannot combine Acquisition objects that differ in key fields" in repr(context.exception))

        # Test incompatible SubjectDetails
        acq2.subject_id = acq1.subject_id
        subject_details = AcquisitionSubjectDetails(
            mouse_platform_name="mouse_platform_name",
        )
        acq1.subject_details = subject_details
        acq2.subject_details = subject_details

        with self.assertRaises(ValueError) as context:
            acq1 + acq2
        self.assertTrue("SubjectDetails cannot be combined in Acquisition" in repr(context.exception))

    def test_procedures_add(self):
        """Test the __add__ method of Procedures"""

        p1 = self.procedures.model_copy()
        p2 = self.procedures.model_copy()

        combined = p1 + p2

        self.assertEqual(combined.subject_id, "625100")
        self.assertEqual(len(combined.subject_procedures), 4)
        self.assertEqual(combined.subject_procedures[0].start_date, self.procedures_time0.date())
        self.assertEqual(combined.subject_procedures[1].start_date, self.procedures_time1.date())
        self.assertEqual(combined.subject_procedures[2].start_date, self.procedures_time0.date())
        self.assertEqual(combined.subject_procedures[3].start_date, self.procedures_time1.date())

        # Test combining with different subject IDs raises ValueError
        p3 = Procedures(subject_id="different_id")
        with self.assertRaises(ValueError):
            _ = p1 + p3

        p2.schema_version = "0.0.0"
        with self.assertRaises(ValueError) as context:
            _ = p1 + p2

        self.assertIn("Schema versions must match to combine Procedures", str(context.exception))

    def test_add_processing_objects(self):
        """Test the __add__ method of Processing"""

        t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

        # Create two simple Processing objects
        p1 = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    experimenters=["Dr. Dan"],
                    process_type=ProcessName.ANALYSIS,
                    stage=ProcessStage.PROCESSING,
                    output_path="/path/to/outputs1",
                    start_date_time=t,
                    end_date_time=t,
                    code=Code(
                        url="https://url/for/analysis1",
                        version="0.1.1",
                    ),
                ),
            ],
            notes="First processing object",
        )

        p2 = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    experimenters=["Dr. Jane"],
                    process_type=ProcessName.COMPRESSION,
                    stage=ProcessStage.PROCESSING,
                    output_path="/path/to/outputs2",
                    start_date_time=t,
                    end_date_time=t,
                    code=Code(
                        url="https://url/for/compression",
                        version="0.1.1",
                    ),
                ),
            ],
            notes="Second processing object",
        )

        # Combine the two Processing objects
        combined = p1 + p2

        # Check that the combined object has the correct data_processes and notes
        self.assertEqual(len(combined.data_processes), 2)
        self.assertEqual(combined.data_processes[0].name, ProcessName.ANALYSIS)
        self.assertEqual(combined.data_processes[1].name, ProcessName.COMPRESSION)
        self.assertIn("First processing object", combined.notes)
        self.assertIn("Second processing object", combined.notes)
        # check combined dependency graph
        self.assertTrue(p1.dependency_graph.items() <= combined.dependency_graph.items())
        # remove the first process from p2_graph, check that rest of the graph is unchanged in combined graph
        p2.dependency_graph.pop(p2.process_names[0])
        self.assertTrue(p2.dependency_graph.items() <= combined.dependency_graph.items())
        # check that the graphs are linked properly
        self.assertEqual([p1.process_names[-1]], combined.dependency_graph[p2.process_names[0]])

        # Test with incompatible schema versions
        p3 = p2.model_copy()
        p3.schema_version = "0.0.0"

        with self.assertRaises(ValueError) as e:
            _ = p1 + p3
        self.assertIn("Cannot add Processing objects with different schema versions.", str(e.exception))

        # Test with duplicate processes
        with self.assertWarns(Warning) as w:
            combined = p1 + p1
        self.assertIn("Processing objects have repeated processes", str(w.warning))
        self.assertEqual(combined.data_processes[1].name, "Analysis_1")

        with self.assertWarns(Warning) as w:
            combined = combined + combined
        self.assertIn("Processing objects have repeated processes", str(w.warning))
        self.assertEqual(combined.data_processes[2].name, "Analysis_2")
        self.assertEqual(combined.data_processes[3].name, "Analysis_3")


if __name__ == "__main__":
    unittest.main()
