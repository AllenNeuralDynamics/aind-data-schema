""" test processing """

import unittest

import pydantic

from aind_data_schema import Processing
from aind_data_schema.processing import DataProcess, PipelineProcess


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
            DataProcess(name="Other")

        with self.assertRaises(pydantic.ValidationError):
            DataProcess(name="Other", notes="")

        assert p is not None


if __name__ == "__main__":
    unittest.main()
