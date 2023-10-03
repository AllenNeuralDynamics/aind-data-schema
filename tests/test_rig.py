""" test Rig """

import datetime
import unittest

from pydantic import ValidationError

from aind_data_schema.device import (
    Calibration,
    Camera,
    CameraAssembly,
    DAQChannel,
    Disc,
    EphysAssembly,
    EphysProbe,
    HarpDevice,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    NeuropixelsBasestation
)
from aind_data_schema.manufacturers import Manufacturer
from aind_data_schema.rig import Rig

class RigTests(unittest.TestCase):
    """test rig schemas"""

    def test_constructors(self):
        """testing constructors"""
        with self.assertRaises(ValidationError):
            r = Rig()

        r = Rig(
            rig_id="12345",
            date_of_modification=datetime.datetime.now(),
            modalities=["Ophys"],
            mouse_platform=Disc(name="Disc A", radius=1),
            patch_cords=[],
            light_sources=[
                Laser(
                    manufacturer=Manufacturer.HAMAMATSU,
                    serial_number="1234",
                    name="Laser A",
                    wavelength=488,
                    )
                ],
            stimulus_devices=[],
            calibrations=[
                Calibration(
                    date_of_calibration=datetime.datetime.now(),
                    device_name="Laser A",
                    description="Laser power calibration",
                    input={"power percent":[10,40,80]},
                    output={"power mW": [2,6,10]},
                    )
                ],
            )

        assert r is not None


    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(ValidationError):
            rig = Rig()


        daqs = [
            NeuropixelsBasestation(
                basestation_firmware_version="1",
                bsc_firmware_version="2",
                slot=0,
                manufacturer=Manufacturer.IMEC,
                ports=[],
                computer_name="foo",
                channels=[
                    DAQChannel(
                        channel_name="123",
                        device_name="Laser A",
                        channel_type="Analog Output",
                    ),
                    DAQChannel(
                        channel_name="321",
                        device_name="Probe A",
                        channel_type="Analog Output",
                    ),
                    DAQChannel(
                        channel_name="234",
                        device_name="Camera A",
                        channel_type="Digital Output",
                    ),
                    DAQChannel(
                        channel_name="2354",
                        device_name="Disc A",
                        channel_type="Digital Output",
                    ),
                ],
            )
        ]

        ems = [
            EphysAssembly(
                probes=[EphysProbe(probe_model="Neuropixels 1.0", name="Probe A")],
                manipulator=Manipulator(
                    manufacturer=Manufacturer.NEW_SCALE_TECHNOLOGIES,
                    serial_number="4321",
                ),
                ephys_assembly_name="Ephys_assemblyA",
            )
        ]

        lms = [
            LaserAssembly(
                lasers=[
                    Laser(
                        manufacturer=Manufacturer.HAMAMATSU,
                        serial_number="1234",
                        name="Laser A",
                        wavelength=488,
                    ),
                ],
                manipulator=Manipulator(
                    manufacturer=Manufacturer.NEW_SCALE_TECHNOLOGIES,
                    serial_number="1234",
                ),
                laser_assembly_name="Laser_assembly",
            )
        ]

        # daq missing devices
        with self.assertRaises(ValidationError):
            rig = Rig(rig_id="1234", daqs=daqs)

        # probes missing ports
        with self.assertRaises(ValidationError):
            rig = Rig(
                daqs=[
                    HarpDevice(
                        computer_name="asdf",
                        harp_device_type="Sound Board",
                        harp_device_version="1",
                    ),
                    NeuropixelsBasestation(
                        basestation_firmware_version="1",
                        bsc_firmware_version="2",
                        slot=0,
                        manufacturer=Manufacturer.IMEC,
                        ports=[er.ProbePort(index=0, probes=["Probe B"])],
                        computer_name="foo",
                        channels=[
                            DAQChannel(
                                channel_name="321",
                                device_name="Probe A",
                                channel_type="Analog Output",
                            ),
                        ],
                    ),
                ],
                rig_id="1234",
                ephys_assemblies=ems,
            )

        rig = Rig(
            rig_id="1234",
            daqs=daqs,
            cameras=[
                CameraAssembly(
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
            laser_assemblies=lms,
            ephys_assemblies=ems,
            mouse_platform=Disc(name="Disc A", radius=1),
        )

        assert rig is not None
