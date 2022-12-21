""" example unit test file """

import datetime
import unittest

import pydantic

from aind_data_schema import EphysRig, EphysSession
from aind_data_schema.ephys.ephys_rig import (LaserModule, Manipulator,
                                              ManipulatorAngle)
from aind_data_schema.ephys.ephys_session import (CcfCoords, Coordinates3d,
                                                  EphysProbe, Stream)


class ExampleTest(unittest.TestCase):
    """an example test"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(pydantic.ValidationError):
            er = EphysRig()

        with self.assertRaises(pydantic.ValidationError):
            es = EphysSession()

        er = EphysRig(
            rig_id="1234",
            lasers=[
                LaserModule(
                    manufacturer="Hamamatsu",
                    serial_number="1234",
                    name="Laser A",
                    laser_manipulator=Manipulator(
                        manufacturer="Other",
                        serial_number="1234",
                        manipulator_angles=[
                            ManipulatorAngle(name="XY", value=1),
                            ManipulatorAngle(name="YZ", value=1),
                            ManipulatorAngle(name="XZ", value=1),
                        ],
                    ),
                )
            ],
        )

        assert er is not None

        es = EphysSession(
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            subject_id="1234",
            session_type="Test",
            rig_id="1234",
            probe_streams=[
                Stream(
                    stream_start_time=datetime.datetime.now(),
                    stream_stop_time=datetime.datetime.now(),
                    probes=[
                        EphysProbe(
                            name="Probe A",
                            tip_targeted_structure="VISl4",
                            targeted_ccf_coordinates=CcfCoords(
                                ml="1", ap="1", dv="1"
                            ),
                            manipulator_coordinates=Coordinates3d(
                                x="1", y="1", z="1"
                            ),
                        )
                    ],
                    lasers=[],
                )
            ],
        )

        assert es is not None


if __name__ == "__main__":
    unittest.main()
