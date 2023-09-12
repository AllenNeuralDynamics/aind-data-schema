""" test Ophys """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema.ophys.ophys_rig import OphysRig
from aind_data_schema.ophys.ophys_session import FiberPhotometrySession, Stack, StackChannel


class OphysTests(unittest.TestCase):
    """test ophys schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            r = OphysRig()

        """testing constructors"""
        with self.assertRaises(ValidationError):
            s = FiberPhotometrySession()

        r = OphysRig(rig_id="12345", patch_cords=[], light_sources=[], stimulus_devices=[])

        assert r is not None
        now = datetime.datetime.now()

        s = FiberPhotometrySession(
            experimenter_full_name=["alice"],
            session_start_time=now,
            session_end_time=now,
            subject_id="123456",
            session_type="asdf",
            rig_id="asdf",
            light_sources=[],
            coupling_array=[],
            patch_cords=[],
        )

        assert s is not None

        stack = Stack(
            experimenter_full_name=["Frank Borman"],
            session_start_time = now,
            session_end_time = now,
            subject_id = "123456",
            session_type = "cortical stack",
            rig_id = "meso_1",
            light_sources = [],
            channels=[
                StackChannel(
                    channel_name="Red channel",
                    start_depth=100,
                    end_depth=400,
                )
            ],
            number_of_planes = 60,
            step_size = 5.0,
            number_of_plane_repeats_per_volume = 80,
            number_of_volume_repeats = 1,
            fov_coordinate_ml = 40.3,
            fov_coordinate_ap = 10.1,
            fov_reference = "Reticle center",
            fov_width = 400,
            fov_height = 400,
            magnification = "2X",
            fov_scale_factor = 1.8,
            frame_rate = 30.0,
        )

        assert stack is not None


if __name__ == "__main__":
    unittest.main()
