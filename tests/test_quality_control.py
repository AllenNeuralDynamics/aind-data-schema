"""test quality metrics """

from datetime import date
import unittest

from pydantic import ValidationError

from aind_data_schema_models.modalities import Modality
from aind_data_schema.core.quality_control import QualityControl, QCEvaluation


class QualityControlTests(unittest.TestCase):
    """test quality metrics schema"""

    def test_constructors(self):
        """testing constructors"""

        with self.assertRaises(ValidationError):
            q = QualityControl()

        date = date.fromisoformat("2020-10-10")

        q = QualityControl(
            overall_status_date=date,
            overall_status="Pass",
            evaluations=[QCEvaluation(
                evaluator_full_name="Bob",
                evaluation_date=date,
                evaluation_modality=Modality.ECEPHYS,
                evaluation_stage="Spike sorting",
                qc_metrics={"number_good_units": [622]},
                stage_status="Pass",
                ),
            ],
        )

        assert q is not None


if __name__ == "__main__":
    unittest.main()
