""" test processing """

import unittest

import pydantic

from aind_data_schema.core.processing import DataProcess, PipelineProcess, Processing


class ProcessingTest(unittest.TestCase):
    """tests for processing schema"""

    def test_constructors(self):
        """test creation"""

        with self.assertRaises(pydantic.ValidationError):
            p = Processing()

        p = Processing(
            processing_pipeline=PipelineProcess(processor_full_name="Processor", data_processes=[]),
        )

        with self.assertRaises(pydantic.ValidationError):
            DataProcess(name="Other", notes="")

        assert p is not None


if __name__ == "__main__":
    unittest.main()
