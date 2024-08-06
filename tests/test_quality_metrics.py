"""test quality metrics """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema_models.modalities import Modality
from aind_data_schema.core.quality_metrics import QualityMetrics, QCEvaluation


class QualityMetricsTests(unittest.TestCase):
    """test quality metrics schema"""

    def test_constructors(self):
        """testing constructors"""

        with self.assertRaises(ValidationError):
            q = QualityControl()

        now = datetime.datetime.now()

        q = QualityControl(
            overall_status_date=now.date(),
            overall_status="Pass",
            evaluations=[QCEvaluation(
                evaluator_full_name="Bob",
                evaluation_date=now.date(),
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
