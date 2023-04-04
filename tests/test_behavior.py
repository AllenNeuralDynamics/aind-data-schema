""" tests for Behavior """

import datetime
import unittest

import pydantic

from aind_data_schema.behavior import BehaviorSession


class BehaviorTests(unittest.TestCase):
    """tests for behavior"""

    def test_constructors(self):
        """try building behavior"""

        with self.assertRaises(pydantic.ValidationError):
            b = BehaviorSession()

        now = datetime.datetime.now()

        b = BehaviorSession(
            subject_id="1234",
            experimenter_full_name="Fred Astaire",
            session_start_time=now,
            session_end_time=now,
            animal_weight_prior=20.1,
            animal_weight_post=19.7,
            behavior_type="Foraging",
            behavior_code="URL_to_code",
            code_version="0.1",
            input_parameters={"reward volume": 0.01},
            output_parameters={"trials": 72},
            water_consumed=820,
        )

        assert b is not None


if __name__ == "__main__":
    unittest.main()
