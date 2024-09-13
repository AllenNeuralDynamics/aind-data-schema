"""test quality metrics """

import unittest
from datetime import date

from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status


class QualityControlTests(unittest.TestCase):
    """test quality metrics schema"""

    def test_constructors(self):
        """testing constructors"""

        with self.assertRaises(ValidationError):
            q = QualityControl()

        test_eval = QCEvaluation(
            evaluation_name="Drift map",
            evaluator="Bob",
            evaluation_date=date.fromisoformat("2020-10-10"),
            evaluation_modality=Modality.ECEPHYS,
            evaluation_stage=Stage.PREPROCESSING,
            qc_metrics=[
                QCMetric(name="Multiple values example", value={"stuff": "in_a_dict"}),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    references=["s3://some-data-somewhere"],
                ),
            ],
            stage_status=Status.PASS,
        )

        q = QualityControl(
            overall_status_date=date.fromisoformat("2020-10-10"),
            overall_status=Status.PASS,
            evaluations=[test_eval],
        )

        assert q is not None


if __name__ == "__main__":
    unittest.main()
