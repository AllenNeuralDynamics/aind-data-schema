""" example unit test file """

import datetime
import unittest

import pydantic

from aind_data_schema.coordinates import CcfCoords, Coordinates3d
from aind_data_schema.data_description import Modality
from aind_data_schema.session import EphysModule, EphysProbe, RewardDelivery, Session, Stream


class ExampleTest(unittest.TestCase):
    """an example test"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(pydantic.ValidationError):
            sess = Session()

        sess = Session(
            experimenter_full_name=["alice"],
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            subject_id="1234",
            session_type="Test",
            rig_id="1234",
            data_streams=[
                Stream(
                    stream_start_time=datetime.datetime.now(),
                    stream_end_time=datetime.datetime.now(),
                    stream_modalities=[Modality.ECEPHYS],
                    ephys_modules=[
                        EphysModule(
                            ephys_probes=[EphysProbe(name="Probe A")],
                            assembly_name="Ephys_assemblyA",
                            arc_angle=0,
                            module_angle=10,
                            primary_targeted_structure="VISlm",
                            targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                            manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                        ),
                    ],
                )
            ],
        )

        assert sess is not None

        with self.assertRaises(pydantic.ValidationError):
            RewardDelivery()

        with self.assertRaises(pydantic.ValidationError):
            RewardDelivery(reward_solution="Other")


if __name__ == "__main__":
    unittest.main()
