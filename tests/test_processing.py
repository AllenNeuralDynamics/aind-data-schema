""" test processing """

import re
import unittest

import pydantic

from datetime import datetime

from aind_data_schema.core.processing import (
    DataProcess,
    PipelineProcess,
    Processing,
    ResourceUsage,
    ResourceTimestamped,
)
from aind_data_schema_models.system_architecture import OperatingSystem, CPUArchitecture
from aind_data_schema_models.units import MemoryUnit

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pydantic.__version__).group(1)


class ProcessingTest(unittest.TestCase):
    """tests for processing schema"""

    def test_constructors(self):
        """test creation"""

        with self.assertRaises(pydantic.ValidationError):
            Processing()

        p = Processing(
            processing_pipeline=PipelineProcess(processor_full_name="Processor", data_processes=[]),
        )

        with self.assertRaises(pydantic.ValidationError) as e:
            DataProcess(name="Other", notes="")

        expected_exception = (
            "8 validation errors for DataProcess\n"
            "software_version\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "start_date_time\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "end_date_time\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "input_location\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "output_location\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "code_url\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "parameters\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "notes\n"
            "  Value error, Notes cannot be empty if 'name' is Other. Describe the process name in the notes field."
            " [type=value_error, input_value='', input_type=str]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )

        self.assertIsNotNone(p)
        self.assertEqual(expected_exception, repr(e.exception))

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

        expected_exception = "RAM unit is required if RAM is provided"

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

        expected_exception = "System memory unit is required if system memory is provided"

        self.assertTrue(expected_exception in repr(e.exception))


if __name__ == "__main__":
    unittest.main()
