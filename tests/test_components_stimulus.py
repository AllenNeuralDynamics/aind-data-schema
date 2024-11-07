"""Test components.stimulus"""

import unittest
from aind_data_schema.components.stimulus import AuditoryStimulation


class StimulusTests(unittest.TestCase):
    """tests device schemas"""

    def test_typo(self):
        """tests that the sitmulus typo is corrected"""
        a = AuditoryStimulation(
            stimulus_type="Auditory Stimulation",
            sitmulus_name="test",
            sample_frequency=0.5,
        )

        a_dict = a.model_dump()
        a_dict["sitmulus_name"] = a_dict.pop("stimulus_name")

        self.assertEqual(a.model_dump(), AuditoryStimulation(**a_dict).model_dump())
