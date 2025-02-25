""" test processing """

import re
import unittest
from datetime import datetime

import pydantic
from aind_data_schema_models.system_architecture import CPUArchitecture, OperatingSystem
from aind_data_schema_models.units import MemoryUnit

from aind_data_schema.components.identifiers import Person, Code
from aind_data_schema.core.processing import (
    DataProcess,
    ProcessName,
    Processing,
    ResourceTimestamped,
    ResourceUsage,
    ProcessStage,
)

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pydantic.__version__).group(1)
t = datetime.fromisoformat("2024-09-13T14:00:00")


class ProcessingTest(unittest.TestCase):
    """tests for processing schema"""

    def test_constructors(self):
        """test creation"""

        with self.assertRaises(pydantic.ValidationError):
            Processing()

        # Create a valid Processing object
        p = Processing(
            data_processes=[
                DataProcess(
                    experimenters=[Person(name="Dr. Dan")],
                    name=ProcessName.ANALYSIS,
                    stage=ProcessStage.PROCESSING,
                    input_location="/path/to/inputs",
                    output_location="/path/to/outputs",
                    start_date_time=t,
                    end_date_time=t,
                    code=Code(
                        url="https://url/for/pipeline",
                        version="0.1.1",
                    ),
                ),
            ]
        )

        self.assertIsNotNone(p)

        with self.assertRaises(pydantic.ValidationError) as e:
            DataProcess(name="Other", notes="")
        self.assertIn("stage", repr(e.exception))
        self.assertIn("code", repr(e.exception))
        self.assertIn("start_date_time", repr(e.exception))
        self.assertIn("end_date_time", repr(e.exception))
        self.assertIn("input_location", repr(e.exception))
        self.assertIn("output_location", repr(e.exception))
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


if __name__ == "__main__":
    unittest.main()
