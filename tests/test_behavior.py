""" tests for Behavior """

import datetime
import unittest

import pydantic

from aind_data_schema.device import (
    Camera,
    DAQChannel,
    Device,
    Lens,
    Manufacturer,
    MotorizedStage,
    SpoutSide,
    RewardSpout
)
from aind_data_schema.behavior import behavior_rig as br
from aind_data_schema.behavior import behavior_session as bs
from aind_data_schema.stimulus import BehaviorStimulation


class BehaviorTests(unittest.TestCase):
    """tests for behavior"""

    def test_constructors(self):
        """try building behavior"""

        with self.assertRaises(pydantic.ValidationError):
            b = bs.BehaviorSession()

        with self.assertRaises(pydantic.ValidationError):
            r = br.BehaviorRig()

        now = datetime.datetime.now()

        b = bs.BehaviorSession(
            subject_id="1234",
            experimenter_full_name="Fred Astaire",
            rig_id="AIND-Tower-4",
            session_start_time=now,
            session_end_time=now,
            animal_weight_prior=20.1,
            animal_weight_post=19.7,
            behavior_type="Foraging",
            session_number=3,
            stimulus_epochs=[
                bs.StimulusEpoch(
                    stimulus=BehaviorStimulation(
                        behavior_name="Foraging",
                        behavior_software="Bonsai",
                        behavior_software_version="0.1",
                        behavior_script="URL_to_code",
                        behavior_script_version="0.1",
                        input_parameters={"reward volume": 0.01},
                    ),
                    stimulus_start_time=now.time(),
                    stimulus_end_time=now.time(),
                )
            ],
            output_parameters={},
            reward_consumed_during_training=820,
            reward_consumed_total=1020,
            trials_total=551,
            trials_finished=343,
            trials_rewarded=146,
        )

        assert b is not None

        daqs = [
            br.DAQDevice(
                manufacturer=Manufacturer.OEPS,
                model="PCIe-6343",
                data_interface="PCIe",
                computer_name="foo",
                channels=[
                    DAQChannel(channel_name="123", device_name="Laser A", channel_type="Analog Output"),
                    DAQChannel(channel_name="234", device_name="Camera A", channel_type="Digital Output"),
                    DAQChannel(channel_name="2354", device_name="Camera B", channel_type="Digital Output"),
                ],
            )
        ]

        rd = br.RewardDelivery(
            stimulus_device="Reward delivery",
            stage_type=MotorizedStage(
                manufacturer=Manufacturer.THORLABS,
                model="Z825B",
                serial_number="1234",
                travel=25,
            ),
            reward_spouts=[
                RewardSpout(
                    side=SpoutSide.LEFT,
                    name="Spout A",
                    manufacturer=Manufacturer.OTHER,
                    model="BD223",
                    spout_diameter=0.853,
                    solenoid_valve=Device(
                        manufacturer=Manufacturer.LEE,
                        model="LHDA1231415H",
                        serial_number="1234",
                    ),
                ),
                RewardSpout(
                    side=SpoutSide.RIGHT,
                    name="Spout B",
                    manufacturer=Manufacturer.OTHER,
                    model="BD223",
                    spout_diameter=0.853,
                    solenoid_valve=Device(
                        manufacturer=Manufacturer.LEE,
                        model="LHDA1231415H",
                        serial_number="4321",
                    )
                )
            ]
        )

        r = br.BehaviorRig(
            rig_id="1234",
            mouse_platform=br.Tube(
                platform_type="Tube",
                diameter=8,
                name="Mouse Tube",
                manufacturer=Manufacturer.CUSTOM,
            ),
            daqs=daqs,
            stimulus_devices=[
                rd,
            ],
            cameras=[
                br.CameraAssembly(
                    camera_assembly_name="cam",
                    camera_target="Face bottom",
                    lens=Lens(manufacturer=Manufacturer.OTHER),
                    camera=Camera(
                        name="Camera A",
                        manufacturer=Manufacturer.OTHER,
                        data_interface="USB",
                        computer_name="ASDF",
                        max_frame_rate=144,
                        pixel_width=1,
                        pixel_height=1,
                        chroma="Color",
                    ),
                )
            ],
            calibrations=[br.Calibration(
                date_of_calibration=now,
                device_name="Spout A",
                description="Reward spout calibration",
                input={"number drops": 1},
                output={"volume (uL)": 5},
                )
            ],
        )

        assert r is not None


if __name__ == "__main__":
    unittest.main()
