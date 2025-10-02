"""test processing"""

import unittest
from datetime import datetime

import pydantic
from aind_data_schema_models.system_architecture import CPUArchitecture, OperatingSystem
from aind_data_schema_models.units import MemoryUnit

from aind_data_schema.components.identifiers import Code, DataAsset
from aind_data_schema.core.processing import (
    DataProcess,
    Processing,
    ProcessName,
    ProcessStage,
    ResourceTimestamped,
    ResourceUsage,
)

t = datetime.fromisoformat("2024-09-13T14:00:00")
code = Code(
    name="Example pipeline",
    input_data=[
        DataAsset(url="s3 path to inputs"),
    ],
    url="https://url/for/pipeline",
    version="0.1.1",
)


class ProcessingTest(unittest.TestCase):
    """tests for processing schema"""

    def test_constructors(self):
        """test creation"""

        with self.assertRaises(pydantic.ValidationError):
            Processing()

        # Create a valid Processing object
        p = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    experimenters=["Dr. Dan"],
                    process_type=ProcessName.ANALYSIS,
                    stage=ProcessStage.ANALYSIS,
                    code=code,
                    output_path="./path/to/outputs",
                    start_date_time=t,
                    end_date_time=t,
                ),
            ]
        )

        self.assertIsNotNone(p)
        self.assertEqual(p.data_processes[0].name, ProcessName.ANALYSIS)

        with self.assertRaises(pydantic.ValidationError) as e:
            DataProcess(process_type=ProcessName.OTHER, notes="")
        self.assertIn("stage", repr(e.exception))
        self.assertIn("code", repr(e.exception))
        self.assertIn("start_date_time", repr(e.exception))
        self.assertIn("notes", repr(e.exception))

    def test_resource_usage(self):
        """Test the ResourceUsage class"""

        resources = ResourceUsage(
            os=OperatingSystem.MACOS_SONOMA,
            architecture=CPUArchitecture.X86_64,
            cpu_usage=[ResourceTimestamped(timestamp=datetime.fromisoformat("2024-09-13"), usage=0.5)],
        )

        self.assertIsNotNone(resources)

        with self.assertRaises(pydantic.ValidationError):
            ResourceUsage()

    def test_resource_usage_unit_validators(self):
        """Test that unit validators work"""

        # Check ram
        with self.assertRaises(ValueError) as e:
            ResourceUsage(
                os=OperatingSystem.MACOS_SONOMA,
                architecture=CPUArchitecture.X86_64,
                cpu_usage=[ResourceTimestamped(timestamp=datetime.fromisoformat("2024-09-13"), usage=0.5)],
                ram=1,
            )

        expected_exception = "Unit ram_unit is required when ram is set"

        self.assertTrue(expected_exception in repr(e.exception))

        resources = ResourceUsage(
            os=OperatingSystem.MACOS_SONOMA,
            architecture=CPUArchitecture.X86_64,
            cpu_usage=[ResourceTimestamped(timestamp=datetime.fromisoformat("2024-09-13"), usage=0.5)],
            ram=1,
            ram_unit=MemoryUnit.GB,
        )
        self.assertIsNotNone(resources)

        # Check system memory
        with self.assertRaises(ValueError) as e:
            ResourceUsage(
                os=OperatingSystem.MACOS_SONOMA,
                architecture=CPUArchitecture.X86_64,
                cpu_usage=[ResourceTimestamped(timestamp=datetime.fromisoformat("2024-09-13"), usage=0.5)],
                system_memory=1,
            )

        expected_exception = "Unit system_memory_unit is required when system_memory is set"

        self.assertTrue(expected_exception in repr(e.exception))

        # Test with no data_processes
        # p = Processing(data_processes=[])
        # self.assertIsNotNone(p)

    def test_unique_process_names(self):
        """Test that process names are unique within a Processing object"""

        # Test with duplicate process names
        with self.assertRaises(ValueError) as e:
            Processing.create_with_sequential_process_graph(
                data_processes=[
                    DataProcess(
                        experimenters=["Dr. Dan"],
                        process_type=ProcessName.ANALYSIS,
                        stage=ProcessStage.ANALYSIS,
                        start_date_time=t,
                        end_date_time=t,
                        code=code,
                    ),
                    DataProcess(
                        experimenters=["Dr. Dan"],
                        process_type=ProcessName.ANALYSIS,
                        stage=ProcessStage.ANALYSIS,
                        start_date_time=t,
                        end_date_time=t,
                        code=code,
                    ),
                ]
            )
        self.assertIn("data_processes must have unique names", str(e.exception))

    def test_validate_data_processes(self):
        """Test the validate_data_processes method"""

        # Test with valid data_processes
        p = Processing.create_with_sequential_process_graph(
            data_processes=[
                DataProcess(
                    experimenters=["Dr. Dan"],
                    process_type=ProcessName.ANALYSIS,
                    stage=ProcessStage.ANALYSIS,
                    output_path="./path/to/outputs",
                    start_date_time=t,
                    end_date_time=t,
                    code=code,
                ),
            ]
        )
        self.assertIsNotNone(p)

        # Test with data_processes as a list of lists
        with self.assertRaises(pydantic.ValidationError):
            Processing(
                data_processes=[
                    [
                        DataProcess(
                            experimenters=["Dr. Dan"],
                            process_type=ProcessName.ANALYSIS,
                            stage=ProcessStage.ANALYSIS,
                            output_path="./path/to/outputs",
                            start_date_time=t,
                            end_date_time=t,
                            code=code,
                        ),
                    ]
                ],
                dependency_graph={ProcessName.ANALYSIS: []},
            )

    def test_rename_process(self):
        """Test the rename_process method"""
        # Create a processing object with multiple processes
        process1 = DataProcess(
            name="process1",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.COMPRESSION,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t,
            end_date_time=t,
        )
        process2 = DataProcess(
            name="process2",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.ANALYSIS,
            stage=ProcessStage.ANALYSIS,
            code=code,
            start_date_time=t,
            end_date_time=t,
        )
        process3 = DataProcess(
            name="process3",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.SPIKE_SORTING,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t,
            end_date_time=t,
        )

        # Create process graph where process2 depends on process1, and process3 depends on process2
        dependency_graph = {
            "process1": [],
            "process2": ["process1"],
            "process3": ["process2"],
        }

        p = Processing(data_processes=[process1, process2, process3], dependency_graph=dependency_graph)

        # Rename process2 to new_name
        p.rename_process("process2", "new_name")

        # Check that the process was renamed in data_processes
        process_names = [proc.name for proc in p.data_processes]
        self.assertIn("new_name", process_names)
        self.assertNotIn("process2", process_names)

        # Check that the process was renamed in dependency_graph keys
        self.assertIn("new_name", p.dependency_graph)
        self.assertNotIn("process2", p.dependency_graph)

        # Check that references to the process were updated in dependency_graph values
        self.assertEqual(p.dependency_graph["process3"], ["new_name"])
        self.assertEqual(p.dependency_graph["new_name"], ["process1"])

        # Test error case - renaming a process that doesn't exist
        with self.assertRaises(ValueError) as e:
            p.rename_process("non_existent", "another_name")
        self.assertIn("not found in data_processes", str(e.exception))

    def test_validate_process_graph(self):
        """Test the validate_process_graph method"""
        # Create a valid processing object
        process1 = DataProcess(
            name="process1",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.COMPRESSION,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t,
            end_date_time=t,
        )
        process2 = DataProcess(
            name="process2",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.ANALYSIS,
            stage=ProcessStage.ANALYSIS,
            code=code,
            start_date_time=t,
            end_date_time=t,
        )

        # Valid case - all processes are in dependency_graph and all keys in dependency_graph are processes
        dependency_graph = {
            "process1": [],
            "process2": ["process1"],
        }

        p = Processing(data_processes=[process1, process2], dependency_graph=dependency_graph)
        self.assertIsNotNone(p)

        # Invalid case 1 - process in data_processes not in dependency_graph
        process3 = DataProcess(
            name="process3",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.SPIKE_SORTING,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t,
            end_date_time=t,
        )

        with self.assertRaises(ValueError) as e:
            Processing(data_processes=[process1, process2, process3], dependency_graph=dependency_graph)
        self.assertIn("dependency_graph must include all processes in data_processes", str(e.exception))

        # Invalid case 2 - process in dependency_graph not in data_processes
        invalid_graph = {
            "process1": [],
            "process2": ["process1"],
            "process3": ["process2"],
        }

        with self.assertRaises(ValueError) as e:
            Processing(data_processes=[process1, process2], dependency_graph=invalid_graph)
        self.assertIn("data_processes must include all processes in dependency_graph", str(e.exception))

    def test_dependency_graph_none(self):
        """Tests that no issue is raised if dependency_graph is None"""
        processing = Processing(
            data_processes=[
                DataProcess(
                    start_date_time=datetime(2024, 10, 10, 1, 2, 3),
                    end_date_time=datetime(2024, 10, 11, 1, 2, 3),
                    process_type=ProcessName.COMPRESSION,
                    experimenters=["AIND Scientific Computing"],
                    stage=ProcessStage.PROCESSING,
                    code=Code(
                        url="www.example.com/ephys_compression",
                    ),
                ),
                DataProcess(
                    start_date_time=datetime(2024, 10, 10, 1, 2, 3),
                    end_date_time=datetime(2024, 10, 11, 1, 2, 4),
                    process_type=ProcessName.OTHER,
                    experimenters=["AIND Scientific Computing"],
                    stage=ProcessStage.PROCESSING,
                    code=Code(url=""),
                    notes="Data was copied.",
                ),
            ]
        )
        self.assertIsNone(processing.dependency_graph)

    def test_validate_pipeline_names(self):
        """Test the validate_pipeline_names method"""

        # Create valid pipelines
        pipelines = [
            Code(name="Pipeline1", url="https://example.com/pipeline1", version="1.0"),
            Code(name="Pipeline2", url="https://example.com/pipeline2", version="1.0"),
        ]

        # Create valid data_processes
        process1 = DataProcess(
            name="process1",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.COMPRESSION,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t,
            end_date_time=t,
            pipeline_name="Pipeline1",
        )
        process2 = DataProcess(
            name="process2",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.ANALYSIS,
            stage=ProcessStage.ANALYSIS,
            code=code,
            start_date_time=t,
            end_date_time=t,
            pipeline_name="Pipeline2",
        )

        # Valid case
        p = Processing(
            data_processes=[process1, process2],
            dependency_graph={"process1": [], "process2": ["process1"]},
            pipelines=pipelines,
        )
        self.assertIsNotNone(p)

        # Invalid case - pipeline_name not in pipelines list
        process3 = DataProcess(
            name="process3",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.SPIKE_SORTING,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t,
            end_date_time=t,
            pipeline_name="NonExistentPipeline",
        )

        with self.assertRaises(ValueError) as e:
            Processing(
                data_processes=[process1, process2, process3],
                dependency_graph={"process1": [], "process2": ["process1"], "process3": ["process2"]},
                pipelines=pipelines,
            )
        self.assertIn("Pipeline name 'NonExistentPipeline' not found in pipelines list", str(e.exception))

    def test_order_processes(self):
        """Test the order_processes method"""

        # Create processes with different start times (out of order)
        t1 = datetime.fromisoformat("2024-09-13T14:00:00")
        t2 = datetime.fromisoformat("2024-09-13T12:00:00")  # Earlier time
        t3 = datetime.fromisoformat("2024-09-13T16:00:00")  # Later time

        process1 = DataProcess(
            name="process1",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.COMPRESSION,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t1,
            end_date_time=t1,
        )
        process2 = DataProcess(
            name="process2",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.ANALYSIS,
            stage=ProcessStage.ANALYSIS,
            code=code,
            start_date_time=t2,
            end_date_time=t2,
        )
        process3 = DataProcess(
            name="process3",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.SPIKE_SORTING,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t3,
            end_date_time=t3,
        )

        # Create Processing with out-of-order processes
        dependency_graph = {"process1": [], "process2": [], "process3": []}
        p = Processing(data_processes=[process1, process2, process3], dependency_graph=dependency_graph)

        # Check that processes were reordered by start_date_time
        expected_order = [process2, process1, process3]  # t2 < t1 < t3
        actual_names = [proc.name for proc in p.data_processes]
        expected_names = [proc.name for proc in expected_order]
        self.assertEqual(actual_names, expected_names)

        # Check that notes were updated
        self.assertIn("Processes were reordered by start_date_time", p.notes)

        # Test with already ordered processes
        process4 = DataProcess(
            name="process4",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.COMPRESSION,
            stage=ProcessStage.PROCESSING,
            code=code,
            start_date_time=t1,
            end_date_time=t1,
        )
        process5 = DataProcess(
            name="process5",
            experimenters=["Dr. Dan"],
            process_type=ProcessName.ANALYSIS,
            stage=ProcessStage.ANALYSIS,
            code=code,
            start_date_time=t3,
            end_date_time=t3,
        )

        dependency_graph2 = {"process4": [], "process5": []}
        p2 = Processing(data_processes=[process4, process5], dependency_graph=dependency_graph2)

        # Check that order wasn't changed and no reordering note was added
        self.assertEqual([proc.name for proc in p2.data_processes], ["process4", "process5"])
        self.assertIsNone(p2.notes)

        # Test with existing notes
        dependency_graph3 = {"process1": [], "process2": [], "process3": []}
        p3 = Processing(
            data_processes=[process1, process2, process3], dependency_graph=dependency_graph3, notes="Existing notes"
        )

        # Check that reordering note was appended to existing notes
        self.assertIn("Existing notes; Processes were reordered by start_date_time", p3.notes)

        # Test with empty data_processes
        p4 = Processing(data_processes=[], dependency_graph={})
        self.assertEqual(len(p4.data_processes), 0)
        self.assertIsNone(p4.notes)


if __name__ == "__main__":
    unittest.main()
