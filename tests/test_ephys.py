""" example unit test file """

import datetime
import unittest

import pydantic

from aind_data_schema.device import DAQChannel, Lens
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

        daqs = [
            er.NeuropixelsBasestation(
                basestation_firmware_version="1",
                bsc_firmware_version="2",
                slot=0,
                manufacturer="Other",
                ports=[],
                computer_name="foo",
                channels=[
                    DAQChannel(channel_name="123", device_name="Laser A", channel_type="Analog Output"),
                    DAQChannel(channel_name="321", device_name="Probe A", channel_type="Analog Output"),
                    DAQChannel(channel_name="234", device_name="Camera A", channel_type="Digital Output"),
                    DAQChannel(channel_name="2354", device_name="Disc A", channel_type="Digital Output"),
                ],
            )
        ]

        ems = [
            er.EphysModule(
                probes=[er.EphysProbe(probe_model="Neuropixels 1.0", name="Probe A")],
                arc_angle=0,
                module_angle=0,
                manipulator=er.Manipulator(
                    manufacturer="New Scale Technologies",
                    serial_number="4321",
                ),
            )
        ]

        lms = [
            er.LaserModule(
                lasers=[
                    er.Laser(
                        manufacturer="Hamamatsu",
                        serial_number="1234",
                        name="Laser A",
                        wavelength=488,
                    ),
                ],
                arc_angle=1,
                rotation_angle=1,
                module_angle=1,
                manipulator=er.Manipulator(
                    manufacturer="New Scale Technologies",
                    serial_number="1234",
                ),
            )
        ]

        # daq missing devices
        with self.assertRaises(pydantic.ValidationError):
            rig = er.EphysRig(rig_id="1234", daqs=daqs)

        # probes missing ports
        with self.assertRaises(pydantic.ValidationError):
            rig = er.EphysRig(
                daqs=[
                    er.HarpDevice(computer_name="asdf", harp_device_type="Sound Board", harp_device_version="1"),
                    er.NeuropixelsBasestation(
                        basestation_firmware_version="1",
                        bsc_firmware_version="2",
                        slot=0,
                        manufacturer="Other",
                        ports=[er.ProbePort(index=0, probes=["Probe B"])],
                        computer_name="foo",
                        channels=[
                            DAQChannel(channel_name="321", device_name="Probe A", channel_type="Analog Output"),
                        ],
                    ),
                ],
                rig_id="1234",
                ephys_modules=ems,
            )

        rig = er.EphysRig(
            rig_id="1234",
            daqs=daqs,
            cameras=[
                er.CameraAssembly(
                    camera_assembly_name="cam",
                    lens=Lens(manufacturer="Other"),
                    camera=er.Camera(
                        name="Camera A",
                        manufacturer="Other",
                        data_interface="USB",
                        computer_name="ASDF",
                        max_frame_rate=144,
                        pixel_width=1,
                        pixel_height=1,
                        chroma="Color",
                    ),
                )
            ],
            laser_modules=lms,
            ephys_modules=ems,
            mouse_platform=er.Disc(name="Disc A", radius=1),
        )

        assert rig is not None

        sess = es.EphysSession(
            experimenter_full_name="alice",
            session_start_time=datetime.datetime.now(),
            session_end_time=datetime.datetime.now(),
            subject_id="1234",
            session_type="Test",
            rig_id="1234",
            data_streams=[
                es.Stream(
                    stream_start_time=datetime.datetime.now(),
                    stream_end_time=datetime.datetime.now(),
                    probes=[
                        es.EphysProbe(
                            name="Probe A",
                            primary_targeted_structure="VISl4",
                            targeted_ccf_coordinates=[es.CcfCoords(ml="1", ap="1", dv="1")],
                            manipulator_coordinates=er.Coordinates3d(x="1", y="1", z="1"),
                        )
                    ],
                    laser_modules=[],
                    daqs=[],
                    cameras=[],
                )
            ],
        )

        assert sess is not None


if __name__ == "__main__":
    unittest.main()
