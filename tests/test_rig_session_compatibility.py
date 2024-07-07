"""Tests rig session compatibility check"""
import unittest

from aind_data_schema.utils.compatibility_check import RigSessionCompatibility
from examples.ephys_rig import rig as example_ephys_rig
from examples.ephys_session import session as example_ephys_session
from tests.resources.rig_session_compatibility.ephys_rig import rig as ephys_rig
from tests.resources.rig_session_compatibility.ephys_session import session as ephys_session
from tests.resources.rig_session_compatibility.fip_ophys_rig import rig as ophys_rig
from tests.resources.rig_session_compatibility.fip_ophys_session import s as ophys_session


class TestRigSessionCompatibility(unittest.TestCase):
    """Tests RigSessionCompatibility class"""

    ephys_check = RigSessionCompatibility(rig=ephys_rig, session=ephys_session)
    ophys_check = RigSessionCompatibility(rig=ophys_rig, session=ophys_session)

    def test_run_compatibility_check(self):
        """Tests compatibility check"""
        expected_error = "Rig ID in session 323_EPHYS2-RF_2023-04-24_01 does not match the rig's 323_EPHYS1_20231003."
        with self.assertRaises(ValueError) as context:
            self.ephys_check.run_compatibility_check()
        self.assertIn(expected_error, str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.ophys_check.run_compatibility_check()

    def test_check_examples_compatibility(self):
        """Tests that examples are compatible"""
        # check that ephys session and rig are synced
        example_ephys_check = RigSessionCompatibility(rig=example_ephys_rig, session=example_ephys_session)
        self.assertIsNone(example_ephys_check.run_compatibility_check())
