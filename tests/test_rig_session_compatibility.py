"""Tests rig session compatibility check"""
import unittest

from aind_data_schema.components.devices import MousePlatform, DAQDevice
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session, Stream
from aind_data_schema.utils.compatibility_check import RigSessionCompatibility


class TestRigSessionCompatibility(unittest.TestCase):
    """Tests RigSessionCompatibility class"""

    # TODO: use example rig and session once examples are synced
    mouse_platform = MousePlatform.model_construct(name="some_mouse_platform")
    stream1 = Stream.model_construct(daq_names=["daq1", "daq2"])
    stream2 = Stream.model_construct(daq_names=["daq3", "daq4"])
    daq1 = DAQDevice.model_construct(name="daq1")
    daq2 = DAQDevice.model_construct(name="daq2")
    daq3 = DAQDevice.model_construct(name="daq3")
    rig = Rig.model_construct(rig_id="some_rig_id", mouse_platform=mouse_platform, daqs=[daq1, daq2, daq3])
    compatible_session = Session.model_construct(
        rig_id="some_rig_id", mouse_platform_name="some_mouse_platform", data_streams=[stream1, stream1]
    )
    noncompatible_session = Session.model_construct(
        rig_id="some_other_rig_id", mouse_platform_name="some_other_mouse_platform", data_streams=[stream1, stream2]
    )
    checker = RigSessionCompatibility(rig=rig, session=compatible_session)
    noncompatible_checker = RigSessionCompatibility(rig=rig, session=noncompatible_session)

    def test_compare_rig_id(self):
        """Tests compare rig_id"""
        self.assertIsNone(self.checker._compare_rig_id())
        self.assertIsInstance(self.noncompatible_checker._compare_rig_id(), ValueError)

    def test_compare_mouse_platform_name(self):
        """Tests compare mouse platform"""
        self.assertIsNone(self.checker._compare_mouse_platform_name())
        self.assertIsInstance(self.noncompatible_checker._compare_mouse_platform_name(), ValueError)

    def test_compare_daq_names(self):
        """Tests compare daq names"""
        self.assertIsNone(self.checker._compare_daq_names())
        self.assertIsInstance(self.noncompatible_checker._compare_daq_names(), ValueError)

    def test_run_compatibility_check(self):
        """Tests compatibility check"""
        self.assertIsNone(self.checker.run_compatibility_check())
        with self.assertRaises(ValueError):
            self.noncompatible_checker.run_compatibility_check()
