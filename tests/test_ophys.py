""" test Ophys """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema import OphysSession, OphysRig


class OphysTests(unittest.TestCase):
    """test ophys schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            r = OphysRig()

        """testing constructors"""
        with self.assertRaises(ValidationError):
            s = OphysSession()

        r = OphysRig(rig_id="12345", patch_cords=[], lasers=[])

        assert r is not None
        now = datetime.datetime.now()

        s = OphysSession(
            experimenter_full_name="alice",
            session_start_time=now,
            session_end_time=now,
            subject_id="123456",
            session_type="asdf",
            rig_id="asdf",
            lasers=[],
            coupling_array=[],
            patch_cords=[],
        )

        assert s is not None


if __name__ == "__main__":
    unittest.main()
