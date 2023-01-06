""" example unit test file """

import datetime
import unittest

import pydantic

from aind_data_schema.ephys import ephys_rig as er
from aind_data_schema.ephys import ephys_session as es


class ExampleTest(unittest.TestCase):
    """an example test"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(pydantic.ValidationError):
            rig = er.EphysRig()

        with self.assertRaises(pydantic.ValidationError):
            sess = es.EphysSession()

        rig = er.EphysRig(
            rig_id="1234",
            laser_modules=[
                er.LaserModule(
                    manufacturer="Other",
                    model="Unknown",
                    serial_number="1234",
                    lasers=[
                        er.Laser(
                            manufacturer="Hamamatsu",
                            serial_number="1234",
                            name="Laser A",
                            laser_manipulator=er.Manipulator(
                                manufacturer="Other",
                                serial_number="1234",
                                orientation=er.ModuleOrientation3d(
                                    arc_angle=1,
                                    rotation_angle=1,
                                    module_angle=1,
                                ),
                            ),
                        )
                    ],
                )
            ],
        )

        assert rig is not None

        sess = es.EphysSession(
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            subject_id="1234",
            session_type="Test",
            rig_id="1234",
            probe_streams=[
                es.Stream(
                    stream_start_time=datetime.datetime.now(),
                    stream_stop_time=datetime.datetime.now(),
                    probes=[
                        es.EphysProbe(
                            name="Probe A",
                            tip_targeted_structure="VISl4",
                            targeted_ccf_coordinates=es.CcfCoords(ml="1", ap="1", dv="1"),
                            manipulator_coordinates=er.Coordinates3d(x="1", y="1", z="1"),
                        )
                    ],
                    lasers=[],
                )
            ],
        )

        assert sess is not None


if __name__ == "__main__":
    unittest.main()
