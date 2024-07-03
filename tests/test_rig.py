""" test Rig """

import unittest
from datetime import date, datetime

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import ValidationError

from aind_data_schema.components.devices import (
    Calibration,
    Camera,
    CameraAssembly,
    CameraTarget,
    ChannelType,
    DAQChannel,
    Detector,
    DetectorType,
    Device,
    Disc,
    EphysAssembly,
    EphysProbe,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    NeuropixelsBasestation,
    Olfactometer,
    OlfactometerChannel,
    Patch,
)
from aind_data_schema.core.rig import Rig


class RigTests(unittest.TestCase):
    """test rig schemas"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(ValidationError):
            Rig()

        daqs = [
            NeuropixelsBasestation(
                name="Neuropixels basestation",
                basestation_firmware_version="1",
                bsc_firmware_version="2",
                slot=0,
                manufacturer=Organization.IMEC,
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
                    name="Probe manipulator",
                    manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                    serial_number="4321",
                ),
                name="Ephys_assemblyA",
            )
        ]

        lms = [
            LaserAssembly(
                lasers=[
                    Laser(
                        manufacturer=Organization.HAMAMATSU,
                        serial_number="1234",
                        name="Laser A",
                        wavelength=488,
                    ),
                ],
                manipulator=Manipulator(
                    name="Laser manipulator",
                    manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                    serial_number="1234",
                ),
                name="Laser_assembly",
                collimator=Device(name="Collimator A", device_type="Collimator"),
                fiber=Patch(
                    name="Bundle Branching Fiber-optic Patch Cord",
                    manufacturer=Organization.DORIC,
                    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                    core_diameter=200,
                    numerical_aperture=0.37,
                ),
            )
        ]

        rig = Rig(
            rig_id="123_EPHYS1-OPTO_20220101",
            modification_date=date(2020, 10, 10),
            modalities=[Modality.ECEPHYS, Modality.FIB],
            daqs=daqs,
            cameras=[
                CameraAssembly(
                    name="cam",
                    camera_target="Face bottom",
                    lens=Lens(name="Camera lens", manufacturer=Organization.OTHER),
                    camera=Camera(
                        name="Camera A",
                        detector_type=DetectorType.CAMERA,
                        manufacturer=Organization.OTHER,
                        data_interface="USB",
                        computer_name="ASDF",
                        frame_rate=144,
                        sensor_width=1,
                        sensor_height=1,
                        chroma="Color",
                    ),
                )
            ],
            stick_microscopes=[
                CameraAssembly(
                    name="Assembly A",
                    camera=Camera(
                        name="Camera A",
                        detector_type=DetectorType.CAMERA,
                        manufacturer=Organization.OTHER,
                        data_interface="USB",
                        computer_name="ASDF",
                        frame_rate=144,
                        sensor_width=1,
                        sensor_height=1,
                        chroma="Color",
                    ),
                    camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS A VALUE
                    lens=Lens(name="Lens A", manufacturer=Organization.OTHER),
                )
            ],
            light_sources=[
                Laser(
                    manufacturer=Organization.HAMAMATSU,
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
                    manufacturer=Organization.FLIR,
                    model="BFS-U3-20S40M",
                    detector_type=DetectorType.CAMERA,
                    data_interface="USB",
                    cooling="Air",
                    immersion="air",
                    bin_width=4,
                    bin_height=4,
                    bin_mode="Additive",
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
                    manufacturer=Organization.DORIC,
                    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                    core_diameter=200,
                    numerical_aperture=0.37,
                )
            ],
            stimulus_devices=[
                Olfactometer(
                    name="Olfactometer",
                    manufacturer=Organization.CHAMPALIMAUD,
                    model="1234",
                    serial_number="213456",
                    hardware_version="1",
                    is_clock_generator=False,
                    computer_name="W10XXX000",
                    channels=[
                        OlfactometerChannel(
                            channel_index=0,
                            channel_type=ChannelType.CARRIER,
                            flow_capacity=100,
                        ),
                        OlfactometerChannel(
                            channel_index=1,
                            channel_type=ChannelType.ODOR,
                            flow_capacity=100,
                        ),
                    ],
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
        with self.assertRaises(ValidationError):
            Rig(
                modalities=[
                    Modality.ECEPHYS,
                    Modality.SLAP,
                    Modality.FIB,
                    Modality.BEHAVIOR_VIDEOS,
                    Modality.POPHYS,
                    Modality.BEHAVIOR,
                ],
                rig_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                daqs=[
                    NeuropixelsBasestation(
                        name="Basestation",
                        basestation_firmware_version="1",
                        bsc_firmware_version="2",
                        slot=0,
                        manufacturer=Organization.IMEC,
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

        with self.assertRaises(ValidationError):
            daqs = [
                NeuropixelsBasestation(
                    name="Basestation",
                    basestation_firmware_version="1",
                    bsc_firmware_version="2",
                    slot=0,
                    manufacturer=Organization.IMEC,
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

            Rig(
                rig_id="123_EPHYS1-OPTO_20220101",
                modification_date=datetime.now(),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                daqs=daqs,
            )

        with self.assertRaises(ValueError):
            ems = [
                EphysAssembly(
                    probes=[EphysProbe(probe_model="Neuropixels 1.0", name="Probe A")],
                    manipulator=Manipulator(
                        name="Probe manipulator",
                        manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                        serial_number="4321",
                    ),
                    name="Ephys_assemblyA",
                )
            ]

            lms = [
                LaserAssembly(
                    lasers=[
                        Laser(
                            manufacturer=Organization.HAMAMATSU,
                            serial_number="1234",
                            name="Laser A",
                            wavelength=488,
                        ),
                    ],
                    manipulator=Manipulator(
                        name="Laser manipulator",
                        manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                        serial_number="1234",
                    ),
                    name="Laser_assembly",
                    collimator=Device(name="Collimator B", device_type="Collimator"),
                    fiber=Patch(
                        name="Bundle Branching Fiber-optic Patch Cord",
                        manufacturer=Organization.DORIC,
                        model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                        core_diameter=200,
                        numerical_aperture=0.37,
                    ),
                )
            ]

            Rig(
                rig_id="1234",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                daqs=daqs,
                cameras=[
                    CameraAssembly(
                        name="cam",
                        camera_target=CameraTarget.OTHER,
                        lens=Lens(name="Camera lens", manufacturer=Organization.OTHER),
                        camera=Camera(
                            name="Camera A",
                            detector_type=DetectorType.CAMERA,
                            manufacturer=Organization.OTHER,
                            data_interface="USB",
                            computer_name="ASDF",
                            frame_rate=144,
                            sensor_width=1,
                            sensor_height=1,
                            chroma="Color",
                        ),
                    )
                ],
                stick_microscopes=[
                    CameraAssembly(
                        name="Assembly A",
                        camera=Camera(
                            name="Camera A",
                            detector_type=DetectorType.CAMERA,
                            manufacturer=Organization.OTHER,
                            data_interface="USB",
                            computer_name="ASDF",
                            frame_rate=144,
                            sensor_width=1,
                            sensor_height=1,
                            chroma="Color",
                        ),
                        camera_target=CameraTarget.OTHER,
                        lens=Lens(name="Lens A", manufacturer=Organization.OTHER),
                    )
                ],
                light_sources=[
                    Laser(
                        manufacturer=Organization.HAMAMATSU,
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
                        manufacturer=Organization.FLIR,
                        model="BFS-U3-20S40M",
                        detector_type=DetectorType.CAMERA,
                        data_interface="USB",
                        cooling="Air",
                        immersion="air",
                        bin_width=4,
                        bin_height=4,
                        bin_mode="Additive",
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
                        manufacturer=Organization.DORIC,
                        model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                        core_diameter=200,
                        numerical_aperture=0.37,
                    )
                ],
                stimulus_devices=[
                    Olfactometer(
                        name="Olfactometer",
                        manufacturer=Organization.CHAMPALIMAUD,
                        model="1234",
                        serial_number="213456",
                        hardware_version="1",
                        is_clock_generator=False,
                        computer_name="W10XXX000",
                        channels=[
                            OlfactometerChannel(
                                channel_index=0,
                                channel_type=ChannelType.CARRIER,
                                flow_capacity=100,
                            ),
                            OlfactometerChannel(
                                channel_index=1,
                                channel_type=ChannelType.ODOR,
                                flow_capacity=100,
                            ),
                        ],
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

        # Tests that validators catch empty lists without KeyErrors
        with self.assertRaises(ValidationError):
            Rig(
                rig_id="123_EPHYS1-OPTO_20220101",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                daqs=daqs,
                cameras=[],
                stick_microscopes=[],
                light_sources=[],
                laser_assemblies=lms,
                ephys_assemblies=ems,
                detectors=[],
                patch_cords=[],
                stimulus_devices=[],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[],
            )

        with self.assertRaises(ValidationError):
            camera = CameraAssembly(
                name="cam",
                camera_target=CameraTarget.OTHER,
                lens=Lens(name="Camera lens", manufacturer=Organization.OTHER),
                camera=Camera(
                    name="Camera A",
                    detector_type=DetectorType.CAMERA,
                    manufacturer=Organization.OTHER,
                    data_interface="USB",
                    computer_name="ASDF",
                    frame_rate=144,
                    sensor_width=1,
                    sensor_height=1,
                    chroma="Color",
                ),
            )
            Rig(
                rig_id="123_EPHYS-OPTO_20200101",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                daqs=daqs,
                cameras=[camera],
                stick_microscopes=[
                    CameraAssembly(
                        name="Assembly A",
                        camera=Camera(
                            name="Camera A",
                            detector_type=DetectorType.CAMERA,
                            manufacturer=Organization.OTHER,
                            data_interface="USB",
                            computer_name="ASDF",
                            frame_rate=144,
                            sensor_width=1,
                            sensor_height=1,
                            chroma="Color",
                        ),
                        camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS A VALUE
                        lens=Lens(name="Lens A", manufacturer=Organization.OTHER),
                    )
                ],
                light_sources=[
                    Laser(
                        manufacturer=Organization.HAMAMATSU,
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
                        manufacturer=Organization.FLIR,
                        model="BFS-U3-20S40M",
                        detector_type=DetectorType.CAMERA,
                        data_interface="USB",
                        cooling="Air",
                        immersion="air",
                        bin_width=4,
                        bin_height=4,
                        bin_mode="Additive",
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
                        manufacturer=Organization.DORIC,
                        model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                        core_diameter=200,
                        numerical_aperture=0.37,
                    )
                ],
                stimulus_devices=[
                    Olfactometer(
                        name="Olfactometer",
                        manufacturer=Organization.CHAMPALIMAUD,
                        model="1234",
                        serial_number="213456",
                        hardware_version="1",
                        is_clock_generator=False,
                        computer_name="W10XXX000",
                        channels=[
                            OlfactometerChannel(
                                channel_index=0,
                                channel_type=ChannelType.CARRIER,
                                flow_capacity=100,
                            ),
                        ],
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

    def test_rig_id_validator(self):
        """Tests that rig_id validator works as expected"""
        daqs = [
            NeuropixelsBasestation(
                name="Neuropixels basestation",
                basestation_firmware_version="1",
                bsc_firmware_version="2",
                slot=0,
                manufacturer=Organization.IMEC,
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
                    name="Probe manipulator",
                    manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                    serial_number="4321",
                ),
                name="Ephys_assemblyA",
            )
        ]

        lms = [
            LaserAssembly(
                lasers=[
                    Laser(
                        manufacturer=Organization.HAMAMATSU,
                        serial_number="1234",
                        name="Laser A",
                        wavelength=488,
                    ),
                ],
                manipulator=Manipulator(
                    name="Laser manipulator",
                    manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
                    serial_number="1234",
                ),
                name="Laser_assembly",
                collimator=Device(name="Collimator A", device_type="Collimator"),
                fiber=Patch(
                    name="Bundle Branching Fiber-optic Patch Cord",
                    manufacturer=Organization.DORIC,
                    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
                    core_diameter=200,
                    numerical_aperture=0.37,
                ),
            )
        ]
        camera = CameraAssembly(
            name="cam",
            camera_target="Face bottom",
            lens=Lens(name="Camera lens", manufacturer=Organization.OTHER),
            camera=Camera(
                name="Camera A",
                detector_type=DetectorType.CAMERA,
                manufacturer=Organization.OTHER,
                data_interface="USB",
                computer_name="ASDF",
                frame_rate=144,
                sensor_width=1,
                sensor_height=1,
                chroma="Color",
            ),
        )

        stick_microscope = CameraAssembly(
            name="Assembly A",
            camera=Camera(
                name="Camera A",
                detector_type=DetectorType.CAMERA,
                manufacturer=Organization.OTHER,
                data_interface="USB",
                computer_name="ASDF",
                frame_rate=144,
                sensor_width=1,
                sensor_height=1,
                chroma="Color",
            ),
            camera_target=CameraTarget.BRAIN_SURFACE,  # NEEDS A VALUE
            lens=Lens(name="Lens A", manufacturer=Organization.OTHER),
        )
        light_source = Laser(
            manufacturer=Organization.HAMAMATSU,
            serial_number="1234",
            name="Laser A",
            wavelength=488,
        )
        detector = Detector(
            name="FLIR CMOS for Green Channel",
            serial_number="21396991",
            manufacturer=Organization.FLIR,
            model="BFS-U3-20S40M",
            detector_type=DetectorType.CAMERA,
            data_interface="USB",
            cooling="Air",
            immersion="air",
            bin_width=4,
            bin_height=4,
            bin_mode="Additive",
            crop_width=200,
            crop_height=200,
            gain=2,
            chroma="Monochrome",
            bit_depth=16,
        )
        patch_cord = Patch(
            name="Bundle Branching Fiber-optic Patch Cord",
            manufacturer=Organization.DORIC,
            model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
            core_diameter=200,
            numerical_aperture=0.37,
        )
        stimulus_device = Olfactometer(
            name="Olfactometer",
            manufacturer=Organization.CHAMPALIMAUD,
            model="1234",
            serial_number="213456",
            hardware_version="1",
            is_clock_generator=False,
            computer_name="W10XXX000",
            channels=[
                OlfactometerChannel(
                    channel_index=0,
                    channel_type=ChannelType.CARRIER,
                    flow_capacity=100,
                ),
                OlfactometerChannel(
                    channel_index=1,
                    channel_type=ChannelType.ODOR,
                    flow_capacity=100,
                ),
            ],
        )
        calibration = Calibration(
            calibration_date=date(2020, 10, 10),
            device_name="Laser A",
            description="Laser power calibration",
            input={"power percent": [10, 40, 80]},
            output={"power mW": [2, 6, 10]},
        )

        with self.assertRaises(ValidationError):
            Rig(
                rig_id="123",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                daqs=daqs,
                cameras=[camera],
                stick_microscopes=[stick_microscope],
                light_sources=[light_source],
                laser_assemblies=lms,
                ephys_assemblies=ems,
                detectors=[detector],
                patch_cords=[patch_cord],
                stimulus_devices=[stimulus_device],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[calibration],
            )
        with self.assertRaises(ValidationError):
            Rig(
                rig_id="123_EPHYS-OPTO_2020-01-01",
                modification_date=date(2020, 10, 10),
                modalities=[Modality.ECEPHYS, Modality.FIB],
                daqs=daqs,
                cameras=[camera],
                stick_microscopes=[stick_microscope],
                light_sources=[light_source],
                laser_assemblies=lms,
                ephys_assemblies=ems,
                detectors=[detector],
                patch_cords=[patch_cord],
                stimulus_devices=[stimulus_device],
                mouse_platform=Disc(name="Disc A", radius=1),
                calibrations=[calibration],
            )


if __name__ == "__main__":
    unittest.main()
