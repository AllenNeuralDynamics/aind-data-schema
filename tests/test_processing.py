""" test processing """

import unittest

import pydantic

from aind_data_schema import Processing
from aind_data_schema.processing import AnalysisProcess, PipelineProcess


class ProcessingTest(unittest.TestCase):
    """tests for processing schema"""

    def test_constructors(self):
        """test creation"""

        with self.assertRaises(pydantic.ValidationError):
            p = Processing()

        p = Processing(
            processing_pipeline=PipelineProcess(processing_person="Processor", data_processes=[]),
            analysis=AnalysisProcess(
                analyzing_person="Analyzer", data_processes=[], description="this was an analysis"
            ),
        )

        assert p is not None


if __name__ == "__main__":
    unittest.main()
