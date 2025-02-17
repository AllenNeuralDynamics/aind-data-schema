""" example FIP ophys rig """

from datetime import date, datetime, timezone

from aind_data_schema_models.modalities import Modality

import aind_data_schema.components.devices as d
import aind_data_schema.core.rig as r

rig = r.Rig(
    rig_id="428_FIP1_20231003",
    modification_date=date(2023, 10, 3),
    modalities=[Modality.FIB],
    cameras=[
        d.CameraAssembly(
            name="BehaviorVideography_FaceSide",
            camera_target=d.CameraTarget.FACE_SIDE_LEFT,
            camera=d.Camera(
                name="Side face camera",
                detector_type="Camera",
                serial_number="TBD",
                manufacturer=d.Organization.AILIPU,
                model="ELP-USBFHD05MT-KL170IR",
                notes="The light intensity sensor was removed; IR illumination is constantly on",
                data_interface="USB",
                computer_name="W10DTJK7N0M3",
                frame_rate=120,
                sensor_width=640,
                sensor_height=480,
                chroma="Color",
                cooling="Air",
                bin_mode="Additive",
                recording_software=d.Software(name="Bonsai", version="2.5"),
            ),
            lens=d.Lens(
                name="Xenocam 1",
                model="XC0922LENS",
                serial_number="unknown",
                manufacturer=d.Organization.OTHER,
                max_aperture="f/1.4",
                notes='Focal Length 9-22mm 1/3" IR F1.4',
            ),
        ),
        d.CameraAssembly(
            name="BehaviorVideography_FaceBottom",
            camera_target=d.CameraTarget.FACE_BOTTOM,
            camera=d.Camera(
                name="Bottom face Camera",
                detector_type="Camera",
                serial_number="TBD",
                manufacturer=d.Organization.AILIPU,
                model="ELP-USBFHD05MT-KL170IR",
                notes="The light intensity sensor was removed; IR illumination is constantly on",
                data_interface="USB",
                computer_name="W10DTJK7N0M3",
                frame_rate=120,
                sensor_width=640,
                sensor_height=480,
                chroma="Color",
                cooling="Air",
                bin_mode="Additive",
                recording_software=d.Software(name="Bonsai", version="2.5"),
            ),
            lens=d.Lens(
                name="Xenocam 2",
                model="XC0922LENS",
                serial_number="unknown",
                manufacturer=d.Organization.OTHER,
                max_aperture="f/1.4",
                notes='Focal Length 9-22mm 1/3" IR F1.4',
            ),
        ),
    ],
    patch_cords=[
        d.Patch(
            name="Bundle Branching Fiber-optic Patch Cord",
            manufacturer=d.Organization.DORIC,
            model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
            core_diameter=200,
            numerical_aperture=0.37,
        )
    ],
    light_sources=[
        d.LightEmittingDiode(
            name="470nm LED",
            manufacturer=d.Organization.THORLABS,
            model="M470F3",
            wavelength=470,
        ),
        d.LightEmittingDiode(
            name="415nm LED",
            manufacturer=d.Organization.THORLABS,
            model="M415F3",
            wavelength=415,
        ),
        d.LightEmittingDiode(
            name="565nm LED",
            manufacturer=d.Organization.THORLABS,
            model="M565F3",
            wavelength=565,
        ),
    ],
    detectors=[
        d.Detector(
            name="Green CMOS",
            serial_number="21396991",
            manufacturer=d.Organization.FLIR,
            model="BFS-U3-20S40M",
            detector_type="Camera",
            data_interface="USB",
            cooling="Air",
            immersion="air",
            bin_width=4,
            bin_height=4,
            bin_mode="Additive",
            crop_offset_x=0,
            crop_offset_y=0,
            crop_width=200,
            crop_height=200,
            gain=2,
            chroma="Monochrome",
            bit_depth=16,
        ),
        d.Detector(
            name="Red CMOS",
            serial_number="21396991",
            manufacturer=d.Organization.FLIR,
            model="BFS-U3-20S40M",
            detector_type="Camera",
            data_interface="USB",
            cooling="Air",
            immersion="air",
            bin_width=4,
            bin_height=4,
            bin_mode="Additive",
            crop_offset_x=0,
            crop_offset_y=0,
            crop_width=200,
            crop_height=200,
            gain=2,
            chroma="Monochrome",
            bit_depth=16,
        ),
    ],
    objectives=[
        d.Objective(
            name="Objective",
            serial_number="128022336",
            manufacturer=d.Organization.NIKON,
            model="CFI Plan Apochromat Lambda D 10x",
            numerical_aperture=0.45,
            magnification=10,
            immersion="air",
        )
    ],
    filters=[
        d.Filter(
            name="Green emission filter",
            manufacturer=d.Organization.SEMROCK,
            model="FF01-520/35-25",
            filter_type="Band pass",
            center_wavelength=520,
            diameter=25,
        ),
        d.Filter(
            name="Red emission filter",
            manufacturer=d.Organization.SEMROCK,
            model="FF01-600/37-25",
            filter_type="Band pass",
            center_wavelength=600,
            diameter=25,
        ),
        d.Filter(
            name="Emission Dichroic",
            model="FF562-Di03-25x36",
            manufacturer=d.Organization.SEMROCK,
            filter_type="Dichroic",
            height=25,
            width=36,
            cut_off_wavelength=562,
        ),
        d.Filter(
            name="dual-edge standard epi-fluorescence dichroic beamsplitter",
            model="FF493/574-Di01-25x36",
            manufacturer=d.Organization.SEMROCK,
            notes="493/574 nm BrightLine dual-edge standard epi-fluorescence dichroic beamsplitter",
            filter_type="Multiband",
            width=36,
            height=24,
        ),
        d.Filter(
            name="Excitation filter 410nm",
            manufacturer=d.Organization.THORLABS,
            model="FB410-10",
            filter_type="Band pass",
            diameter=25,
            center_wavelength=410,
        ),
        d.Filter(
            name="Excitation filter 470nm",
            manufacturer=d.Organization.THORLABS,
            model="FB470-10",
            filter_type="Band pass",
            center_wavelength=470,
            diameter=25,
        ),
        d.Filter(
            name="Excitation filter 560nm",
            manufacturer=d.Organization.THORLABS,
            model="FB560-10",
            filter_type="Band pass",
            diameter=25,
            center_wavelength=560,
        ),
        d.Filter(
            name="450 Dichroic Longpass Filter",
            manufacturer=d.Organization.EDMUND_OPTICS,
            model="#69-898",
            filter_type="Dichroic",
            cut_off_wavelength=450,
            width=35.6,
            height=25.2,
        ),
        d.Filter(
            name="500 Dichroic Longpass Filter",
            manufacturer=d.Organization.EDMUND_OPTICS,
            model="#69-899",
            filter_type="Dichroic",
            cut_off_wavelength=500,
            width=35.6,
            height=23.2,
        ),
    ],
    lenses=[
        d.Lens(
            manufacturer=d.Organization.THORLABS,
            model="AC254-080-A-ML",
            name="Image focusing lens",
            focal_length=80,
            size=1,
        )
    ],
    daqs=[
        d.HarpDevice(
            name="Harp Behavior",
            harp_device_type=d.HarpDeviceType.BEHAVIOR,
            core_version="2.1",
            computer_name="behavior_computer",
            is_clock_generator=False,
            channels=[
                d.DAQChannel(channel_name="DO0", device_name="Solenoid Left", channel_type="Digital Output"),
                d.DAQChannel(channel_name="DO1", device_name="Solenoid Right", channel_type="Digital Output"),
                d.DAQChannel(channel_name="DI0", device_name="Lick-o-meter Left", channel_type="Digital Input"),
                d.DAQChannel(channel_name="DI1", device_name="Lick-o-meter Right", channel_type="Digital Input"),
                d.DAQChannel(channel_name="DI3", device_name="Photometry Clock", channel_type="Digital Input"),
            ],
        )
    ],
    mouse_platform=d.Disc(name="mouse_disc", radius=8.5),
    stimulus_devices=[
        d.RewardDelivery(
            reward_spouts=[
                d.RewardSpout(
                    name="Left spout",
                    side=d.SpoutSide.LEFT,
                    spout_diameter=1.2,
                    solenoid_valve=d.Device(device_type="Solenoid", name="Solenoid Left"),
                    lick_sensor=d.Device(
                        name="Lick-o-meter Left",
                        device_type="Lick detector",
                    ),
                ),
                d.RewardSpout(
                    name="Right spout",
                    side=d.SpoutSide.RIGHT,
                    spout_diameter=1.2,
                    solenoid_valve=d.Device(device_type="Solenoid", name="Solenoid Right"),
                    lick_sensor=d.Device(
                        name="Lick-o-meter Right",
                        device_type="Lick detector",
                    ),
                ),
            ]
        )
    ],
    additional_devices=[d.Device(device_type="Photometry Clock", name="Photometry Clock")],
    calibrations=[
        d.Calibration(
            calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
            device_name="470nm LED",
            description="LED calibration",
            input={"Power setting": [1, 2, 3]},
            output={"Power mW": [5, 10, 13]},
        )
    ],
)
serialized = rig.model_dump_json()
deserialized = r.Rig.model_validate_json(serialized)
deserialized.write_standard_file(prefix="fip_ophys")
