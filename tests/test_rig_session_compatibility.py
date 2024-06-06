"""Tests rig session compatibility check"""
import unittest
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session
from aind_data_schema.components.devices import MousePlatform
from aind_data_schema.utils.compatibility_check import RigSessionCompatibility


class TestRigSessionCompatibility(unittest.TestCase):
    """Tests RigSessionCompatibility class"""

    # TODO: use example rig and session once examples are synced
    mouse_platform = MousePlatform.model_construct(name="some_mouse_platform")
    rig = Rig.model_construct(rig_id="some_rig_id", mouse_platform=mouse_platform)
    compatible_session = Session.model_construct(rig_id="some_rig_id", mouse_platform_name="some_mouse_platform")
    noncompatible_session = Session.model_construct(
        rig_id="some_other_rig_id", mouse_platform_name="some_other_mouse_platform"
    )

    checker = RigSessionCompatibility(rig=rig, session=compatible_session)
    noncompatible_checker = RigSessionCompatibility(rig=rig, session=noncompatible_session)

    def test_compare_rig_id(self):
        """Tests compare rig_id"""
        self.assertTrue(self.checker.compare_rig_id())
        self.assertFalse(self.noncompatible_checker.compare_rig_id())

    def test_compare_mouse_platform_name(self):
        """Tests compare mouse platform"""
        self.assertTrue(self.checker.compare_mouse_platform_name())
        self.assertFalse(self.noncompatible_checker.compare_mouse_platform_name())

    def test_run_compatibility_check(self):
        """Tests compatibility check"""
        comparison_dict = self.checker.run_compatibility_check()
        self.assertTrue(comparison_dict["rig_id"])
        self.assertTrue(comparison_dict["mouse_platform_name"])

        with self.assertRaises(ValueError):
            self.noncompatible_checker.run_compatibility_check()
