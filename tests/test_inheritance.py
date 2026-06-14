"""Tests for Metadata.from_metadata inheritance logic"""

import unittest
from datetime import datetime, timezone

from aind_data_schema_models.data_name_patterns import DataLevel
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.identifiers import Code, Person
from aind_data_schema.core.data_description import DataDescription, Funding
from aind_data_schema.core.metadata import Metadata
from aind_data_schema.core.processing import DataProcess, Processing, ProcessName, ProcessStage
from aind_data_schema.core.quality_control import QCMetric, QCStatus, QualityControl, Stage, Status
from aind_data_schema.core.subject import Subject
from aind_data_schema.utils.inheritance import (
    _accumulate_processing,
    _accumulate_quality_control,
    _get_root_asset_name,
    _get_unique_subject_ids,
    _inherit_instrument_and_acquisition,
    _inherit_subject_and_procedures,
)

from examples.data_description import d as example_dd
from examples.ephys_instrument import inst as example_inst
from examples.processing import p as example_processing
from examples.quality_control import q as example_qc
from examples.subject import s as example_subject


t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

example_code = Code(url="https://github.com/example", version="0.1")


_counter = 0


def _make_metadata(subject_id="123456"):
    global _counter
    _counter += 1
    dd = DataDescription(
        modalities=[Modality.ECEPHYS],
        subject_id=subject_id,
        creation_time=datetime(2022, 2, 21, 16, 30, _counter, tzinfo=timezone.utc),
        institution=Organization.AIND,
        investigators=[Person(name="Jane Smith")],
        funding_source=[Funding(funder=Organization.AI)],
        project_name="Test project",
        data_level=DataLevel.RAW,
    )
    sub = Subject.model_validate(example_subject.model_dump())
    sub.subject_id = subject_id
    return Metadata(
        name=dd.name,
        location=f"s3://bucket/{dd.name}",
        subject=sub,
        data_description=dd,
        processing=example_processing,
        quality_control=example_qc,
    )


class TestFromMetadataSingleSource(unittest.TestCase):
    """Tests for Metadata.from_metadata with a single source"""

    def setUp(self):
        self.source = _make_metadata()
        self.new_processing = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    process_type=ProcessName.ANALYSIS,
                    name="Derived analysis",
                    experimenters=["Dr. Test"],
                    stage=ProcessStage.ANALYSIS,
                    start_date_time=t,
                    end_date_time=t,
                    code=example_code,
                ),
            ]
        )
        self.new_qc = QualityControl(
            metrics=[
                QCMetric(
                    name="Derived metric",
                    modality=Modality.ECEPHYS,
                    stage=Stage.PROCESSING,
                    value=0.95,
                    status_history=[QCStatus(evaluator="Auto", status=Status.PASS, timestamp=t)],
                    tags={"step": "derived"},
                ),
            ],
            default_grouping=["modality"],
        )

    def test_single_source_inherits_subject(self):
        result = Metadata.from_metadata(
            self.source,
            process_name="my-analysis",
            location="s3://bucket/derived",
        )
        self.assertIsNotNone(result.subject)
        self.assertEqual(result.subject.subject_id, "123456")

    def test_single_source_data_description_is_derived(self):
        result = Metadata.from_metadata(
            self.source,
            process_name="my-analysis",
            location="s3://bucket/derived",
        )
        self.assertIsNotNone(result.data_description)
        self.assertEqual(result.data_description.data_level, DataLevel.DERIVED)
        self.assertIn("my-analysis", result.data_description.name)

    def test_single_source_accumulates_processing(self):
        result = Metadata.from_metadata(
            self.source,
            process_name="my-analysis",
            location="s3://bucket/derived",
            new_processing=self.new_processing,
        )
        self.assertIsNotNone(result.processing)
        process_names = [dp.name for dp in result.processing.data_processes]
        self.assertIn("Derived analysis", process_names)
        self.assertGreater(
            len(result.processing.data_processes),
            len(self.new_processing.data_processes),
        )

    def test_single_source_accumulates_qc(self):
        result = Metadata.from_metadata(
            self.source,
            process_name="my-analysis",
            location="s3://bucket/derived",
            new_quality_control=self.new_qc,
        )
        self.assertIsNotNone(result.quality_control)
        metric_names = [m.name for m in result.quality_control.metrics]
        self.assertIn("Derived metric", metric_names)
        self.assertGreater(
            len(result.quality_control.metrics),
            len(self.new_qc.metrics),
        )

    def test_single_source_no_new_processing(self):
        result = Metadata.from_metadata(
            self.source,
            process_name="my-analysis",
            location="s3://bucket/derived",
        )
        self.assertIsNotNone(result.processing)
        self.assertEqual(
            len(result.processing.data_processes),
            len(example_processing.data_processes),
        )

    def test_accepts_single_metadata_not_list(self):
        result = Metadata.from_metadata(
            self.source,
            process_name="my-analysis",
            location="s3://bucket/derived",
        )
        self.assertIsNotNone(result.data_description)


class TestFromMetadataMultipleSameSubject(unittest.TestCase):
    """Tests for multiple sources with same subject but different acquisitions"""

    def setUp(self):
        self.source1 = _make_metadata(subject_id="123456")
        self.source2 = _make_metadata(subject_id="123456")

    def test_same_subject_inherits_subject(self):
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
        )
        self.assertIsNotNone(result.subject)
        self.assertEqual(result.subject.subject_id, "123456")

    def test_different_acquisitions_drops_instrument_and_acquisition(self):
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
        )
        self.assertIsNone(result.instrument)
        self.assertIsNone(result.acquisition)

    def test_different_acquisitions_does_not_accumulate_processing(self):
        new_proc = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    process_type=ProcessName.ANALYSIS,
                    name="New step",
                    experimenters=["Dr. Test"],
                    stage=ProcessStage.ANALYSIS,
                    start_date_time=t,
                    end_date_time=t,
                    code=example_code,
                ),
            ]
        )
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
            new_processing=new_proc,
        )
        self.assertEqual(len(result.processing.data_processes), 1)
        self.assertEqual(result.processing.data_processes[0].name, "New step")

    def test_different_acquisitions_does_not_accumulate_qc(self):
        new_qc = QualityControl(
            metrics=[
                QCMetric(
                    name="New QC",
                    modality=Modality.ECEPHYS,
                    stage=Stage.PROCESSING,
                    value=1.0,
                    status_history=[QCStatus(evaluator="Auto", status=Status.PASS, timestamp=t)],
                    tags={"step": "new"},
                ),
            ],
            default_grouping=["modality"],
        )
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
            new_quality_control=new_qc,
        )
        self.assertEqual(len(result.quality_control.metrics), 1)

    def test_source_data_lists_both_sources(self):
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
        )
        self.assertIsNotNone(result.data_description.source_data)
        self.assertEqual(len(result.data_description.source_data), 2)


class TestFromMetadataDifferentSubjects(unittest.TestCase):
    """Tests for multiple sources with different subjects"""

    def setUp(self):
        self.source1 = _make_metadata(subject_id="123456")
        self.source2 = _make_metadata(subject_id="789012")

    def test_different_subjects_drops_subject(self):
        new_proc = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    process_type=ProcessName.ANALYSIS,
                    name="New step",
                    experimenters=["Dr. Test"],
                    stage=ProcessStage.ANALYSIS,
                    start_date_time=t,
                    end_date_time=t,
                    code=example_code,
                ),
            ]
        )
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
            new_processing=new_proc,
        )
        self.assertIsNone(result.subject)

    def test_different_subjects_drops_procedures(self):
        new_proc = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    process_type=ProcessName.ANALYSIS,
                    name="New step",
                    experimenters=["Dr. Test"],
                    stage=ProcessStage.ANALYSIS,
                    start_date_time=t,
                    end_date_time=t,
                    code=example_code,
                ),
            ]
        )
        result = Metadata.from_metadata(
            [self.source1, self.source2],
            process_name="merge",
            location="s3://bucket/derived",
            new_processing=new_proc,
        )
        self.assertIsNone(result.procedures)


class TestFromMetadataEdgeCases(unittest.TestCase):
    """Tests for edge cases"""

    def test_empty_list_raises(self):
        with self.assertRaises(ValueError):
            Metadata.from_metadata([], process_name="x", location="s3://bucket/x")

    def test_no_data_description_raises(self):
        m = Metadata(
            name="test",
            location="s3://bucket/test",
            processing=example_processing,
        )
        with self.assertRaises(ValueError):
            Metadata.from_metadata(m, process_name="x", location="s3://bucket/x")

    def test_result_name_matches_data_description(self):
        source = _make_metadata()
        result = Metadata.from_metadata(
            source,
            process_name="my-pipeline",
            location="s3://bucket/derived",
        )
        self.assertEqual(result.name, result.data_description.name)


class TestInternalHelpers(unittest.TestCase):
    """Direct tests for internal helper functions to ensure full coverage"""

    def setUp(self):
        self.source = _make_metadata()
        self.derived = Metadata.from_metadata(
            self.source,
            process_name="test-pipeline",
            location="s3://bucket/derived",
        )

    def test_get_root_asset_name_derived(self):
        root = _get_root_asset_name(self.derived.data_description)
        self.assertEqual(root, self.source.data_description.name)

    def test_get_root_asset_name_returns_none_for_non_raw_non_derived(self):
        simulated_dd = self.source.data_description.model_copy(update={"data_level": DataLevel.SIMULATED})
        self.assertIsNone(_get_root_asset_name(simulated_dd))

    def test_get_unique_subject_ids_from_data_description(self):
        no_subject = self.source.model_copy(update={"subject": None})
        ids = _get_unique_subject_ids([no_subject])
        self.assertEqual(ids, ["123456"])

    def test_inherit_subject_and_procedures_returns_none_when_no_subject_or_procedures(self):
        no_subject = self.source.model_copy(update={"subject": None, "procedures": None})
        subject, procedures = _inherit_subject_and_procedures([no_subject])
        self.assertIsNone(subject)
        self.assertIsNone(procedures)

    def test_inherit_instrument_and_acquisition_returns_instrument_when_set(self):
        with_inst = self.source.model_copy(update={"instrument": example_inst})
        instrument, acquisition = _inherit_instrument_and_acquisition([with_inst])
        self.assertIs(instrument, example_inst)
        self.assertIsNone(acquisition)

    def test_accumulate_processing_two_same_acquisition_sources(self):
        source_copy = Metadata.model_validate(self.source.model_dump())
        result = _accumulate_processing([self.source, source_copy])
        self.assertEqual(
            len(result.data_processes),
            2 * len(example_processing.data_processes),
        )

    def test_accumulate_processing_no_source_processing(self):
        no_proc = self.source.model_copy(update={"processing": None})
        result = _accumulate_processing([no_proc], new_processing=example_processing)
        self.assertIs(result, example_processing)

    def test_accumulate_quality_control_two_same_acquisition_sources(self):
        source_copy = Metadata.model_validate(self.source.model_dump())
        result = _accumulate_quality_control([self.source, source_copy])
        self.assertEqual(
            len(result.metrics),
            2 * len(example_qc.metrics),
        )

    def test_accumulate_quality_control_no_source_qc(self):
        no_qc = self.source.model_copy(update={"quality_control": None})
        result = _accumulate_quality_control([no_qc], new_quality_control=example_qc)
        self.assertIs(result, example_qc)


if __name__ == "__main__":
    unittest.main()
