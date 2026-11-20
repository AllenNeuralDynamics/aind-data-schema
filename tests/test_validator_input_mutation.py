"""Tests that before-mode validators do not edit the input passed to model_validate"""

import copy
import unittest
import warnings

from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.devices import Monitor
from aind_data_schema.components.stimulus import AuditoryStimulation
from aind_data_schema.core.quality_control import QualityControl


def monitor_dict() -> dict:
    """Return a serialized Monitor with contrast and brightness set"""
    return Monitor(
        name="test_monitor",
        manufacturer=Organization.ASUS,
        refresh_rate=60,
        width=1920,
        height=1080,
        viewing_distance=15.0,
        relative_position=[AnatomicalRelative.SUPERIOR],
        contrast=50,
        brightness=50,
    ).model_dump(mode="json")


class ValidatorInputMutationTests(unittest.TestCase):
    """Tests that model_validate leaves its input dict unchanged"""

    def assert_input_unchanged(self, model, data: dict):
        """Validate data with model and check that data was not edited"""
        original = copy.deepcopy(data)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            model.model_validate(data)
        self.assertEqual(data, original)

    def test_coerce_object_type(self):
        """Test that a mismatched object_type is not written back to the input"""
        data = monitor_dict()
        data["object_type"] = "Device"
        self.assert_input_unchanged(Monitor, data)

    def test_correct_typo(self):
        """Test that the sitmulus_name typo is not renamed in the input"""
        data = {"sitmulus_name": "test", "sample_frequency": 0.5}
        self.assert_input_unchanged(AuditoryStimulation, data)

    def test_add_units_if_needed(self):
        """Test that each default monitor unit is not added to the input"""
        for missing_unit in ["contrast_unit", "brightness_unit"]:
            with self.subTest(missing_unit=missing_unit):
                data = monitor_dict()
                del data[missing_unit]
                self.assert_input_unchanged(Monitor, data)

    def test_quality_control_backwards_compatibility(self):
        """Test that v2.2.X tags and default_grouping are not converted in the input"""
        data = {
            "metrics": [
                {
                    "object_type": "QC metric",
                    "name": "Old format metric",
                    "modality": {"name": "Extracellular electrophysiology", "abbreviation": "ecephys"},
                    "stage": "Processing",
                    "value": 42,
                    "status_history": [{"evaluator": "Test", "timestamp": "2020-10-10", "status": "Pass"}],
                    "tags": ["old_tag1", "old_tag2"],
                }
            ],
            "default_grouping": ["group1", "group2"],
        }
        self.assert_input_unchanged(QualityControl, data)


if __name__ == "__main__":
    unittest.main()
