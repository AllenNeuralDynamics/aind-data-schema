""" test Rig """

import unittest
from datetime import date

from pydantic import ValidationError

from aind_data_schema.models.devices import (
    Calibration,
    Camera,
    CameraAssembly,
    DAQChannel,
    Detector,
    Disc,
    EphysAssembly,
    EphysProbe,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    NeuropixelsBasestation,
    Patch,
    StickMicroscopeAssembly,
)
from aind_data_schema.models.manufacturers import DORIC, FLIR, HAMAMATSU, IMEC, NEW_SCALE_TECHNOLOGIES, OTHER
from aind_data_schema.models.modalities import BEHAVIOR_VIDEOS, ECEPHYS, FIB, POPHYS, SLAP, TRAINED_BEHAVIOR
from aind_data_schema.rig import Rig


class RigTests(unittest.TestCase):
    """test rig schemas"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(ValidationError):
            Rig()

        daqs = [
            NeuropixelsBasestation(
                basestation_firmware_version="1",
                bsc_firmware_version="2",
                slot=0,
                manufacturer=IMEC,
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
                    manufacturer=NEW_SCALE_TECHNOLOGIES,
                    serial_number="4321",
                ),
                ephys_assembly_name="Ephys_assemblyA",
            )
        ]

        lms = [
            LaserAssembly(
                lasers=[
                    Laser(
                        manufacturer=HAMAMATSU,
                        serial_number="1234",
                        name="Laser A",
                        wavelength=488,
                    ),
                ],
                manipulator=Manipulator(
                    manufacturer=NEW_SCALE_TECHNOLOGIES,
                    serial_number="1234",
                ),
                laser_assembly_name="Laser_assembly",
            )
        ]

        rig = Rig(
            rig_id="1234",
            modification_date=date(2020, 10, 10),
            modalities=[ECEPHYS, FIB],
            daqs=daqs,
            cameras=[
                CameraAssembly(
                    camera_assembly_name="cam",
                    camera_target="Face bottom",
                    lens=Lens(manufacturer=OTHER),
                    camera=Camera(
                        name="Camera A",
                        manufacturer=OTHER,
                        data_interface="USB",
                        computer_name="ASDF",
                        max_frame_rate=144,
                        pixel_width=1,
                        pixel_height=1,
                        chroma="Color",
                    ),
                )
            ],
            stick_microscopes=[
                StickMicroscopeAssembly(
                    scope_assembly_name="fake name",
                    camera=Camera(
                        name="Camera A",
                        manufacturer=OTHER,
                        data_interface="USB",
                        computer_name="ASDF",
                        max_frame_rate=144,
                        pixel_width=1,
                        pixel_height=1,
                        chroma="Color",
                    ),
                    lens=Lens(manufacturer=OTHER),
                )
            ],
            light_sources=[
                Laser(
                    manufacturer=HAMAMATSU,
                    serial_number="1234",
                    name="Laser A",
                    wavelength=488,
                )
            ],
            laser_assemblies=lms,
            ephys_assemblies=ems,
            detectors=[
                Detector(
                    name="FLIR CMOS for Green Channel",
                    serial_number="21396991",
                    manufacturer=FLIR,
                    model="BFS-U3-20S40M",
                    detector_type="Camera",
                    data_interface="USB",
                    cooling="air",
                    immersion="air",
                    bin_width=4,
                    bin_height=4,
                    bin_mode="additive",
                    crop_width=200,
                    crop_height=200,
                    gain=2,
                    chroma="Monochrome",
                    bit_depth=16,
                )
            ],
            patch_cords=[
                Patch(
                    name="Bundle Branching Fiber-optic Patch Cord",
                    manufacturer=DORIC,
                    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                    core_diameter=200,
                    numerical_aperture=0.37,
                )
            ],
            mouse_platform=Disc(name="Disc A", radius=1),
            calibrations=[
                Calibration(
                    calibration_date=date(2020, 10, 10),
                    device_name="Laser A",
                    description="Laser power calibration",
                    input={"power percent": [10, 40, 80]},
                    output={"power mW": [2, 6, 10]},
                )
            ],
        )

        assert rig is not None

    def test_validator(self):
        """Test the rig file validators"""

        # A Rig model with ECEPHYS in the modality list requires
        # ephys_assemblies and stick microscopes
        with self.assertRaises(ValidationError) as e:
            Rig(
                modalities=[
                    ECEPHYS,
                    SLAP,
                    FIB,
                    BEHAVIOR_VIDEOS,
                    POPHYS,
                    TRAINED_BEHAVIOR,
                ],
                rig_id="1234",
                modification_date=date(2020, 10, 10),
                daqs=[
                    NeuropixelsBasestation(
                        basestation_firmware_version="1",
                        bsc_firmware_version="2",
                        slot=0,
                        manufacturer=IMEC,
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
                ],
                calibrations=[
                    Calibration(
                        calibration_date=date(2020, 10, 10),
                        device_name="Laser A",
                        description="Laser power calibration",
                        input={"power percent": [10, 40, 80]},
                        output={"power mW": [2, 6, 10]},
                    )
                ],
                mouse_platform=Disc(name="Disc A", radius=1),
            )
        self.assertTrue("ephys_assemblies field must be utilized for Ecephys modality" in repr(e.exception))
        self.assertTrue("stick_microscopes field must be utilized for Ecephys modality" in repr(e.exception))


if __name__ == "__main__":
    unittest.main()
