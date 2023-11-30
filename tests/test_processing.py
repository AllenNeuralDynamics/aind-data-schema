""" test processing """

import unittest

import pydantic

from aind_data_schema.core.processing import DataProcess, PipelineProcess, Processing


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
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "start_date_time\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "end_date_time\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "input_location\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "output_location\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "code_url\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "parameters\n"
            "  Field required [type=missing, input_value={'name': 'Other', 'notes': ''}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "notes\n"
            "  Value error, Notes cannot be empty if 'name' is Other. Describe the process name in the notes field."
            " [type=value_error, input_value='', input_type=str]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/value_error"
        )

        self.assertIsNotNone(p)
        self.assertEqual(expected_exception, repr(e.exception))


if __name__ == "__main__":
    unittest.main()
