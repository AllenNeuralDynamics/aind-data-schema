""" example unit test file """

import datetime
import unittest

import pydantic

from aind_data_schema import EphysRig, EphysSession
from aind_data_schema.ephys.ephys_session import (
    EphysProbe,
    Stream,
    CcfCoords,
    Coordinates3d,
    ManipulatorAngles,
)


class ExampleTest(unittest.TestCase):
    """an example test"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(pydantic.ValidationError):
            er = EphysRig()

        with self.assertRaises(pydantic.ValidationError):
            es = EphysSession()

        er = EphysRig(rig_id="1234", devices=[])

        assert er is not None

        es = EphysSession(
            institution="AIND",
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            subject_id="1234",
            project_id="1234",
            session_type="Foraging A",
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
                            manipulator_angles=[
                                ManipulatorAngles(name="XY", value=1),
                                ManipulatorAngles(name="YZ", value=1),
                                ManipulatorAngles(name="XZ", value=1),
                            ],
                        )
                    ],
                    lasers=[],
                )
            ],
            ccf_version="CCFv3",
        )

        assert es is not None


if __name__ == "__main__":
    unittest.main()
