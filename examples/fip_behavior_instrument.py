# -*- coding: utf-8 -*-

""" example FIP ophys rig """
from datetime import date, datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import FrequencyUnit, SizeUnit

from aind_data_schema.components.devices import (
    Calibration,
    CameraAssembly,
    CameraTarget,
    Camera,
    Organization,
    Lens,
    HarpDevice,
    HarpDeviceType,
    DAQChannel,
    RewardDelivery,
    RewardSpout,
    SpoutSide,
    Device,
    LickSensorType,
    MotorizedStage,
    PatchCord,
    LightEmittingDiode,
    Detector,
    Objective,
    Filter,
    Tube,
)
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.components.identifiers import Software

bonsai_software = Software(name="Bonsai", version="2.5")

camera1 = CameraAssembly(
    name="BehaviorVideography_FaceSide",
    camera_target=CameraTarget.FACE_SIDE_LEFT,
    camera=Camera(
        name="Side face camera",
        detector_type="Camera",
        manufacturer=Organization.AILIPU,
        model="ELP-USBFHD05MT-KL170IR",
        notes="The light intensity sensor was removed; IR illumination is constantly on",
        data_interface="USB",
        computer_name="W10DTJK7N0M3",
        frame_rate=120,
        frame_rate_unit=FrequencyUnit.HZ,
        sensor_width=640,
        sensor_height=480,
        chroma="Color",
        cooling="Air",
        bin_mode="Additive",
        recording_software=bonsai_software,
    ),
    lens=Lens(
        name="Xenocam 1",
        model="XC0922LENS",
        manufacturer=Organization.OTHER,
        max_aperture="f/1.4",
        notes='Focal Length 9-22mm 1/3" IR F1.4',
    ),
)

camera2 = CameraAssembly(
    name="BehaviorVideography_FaceBottom",
    camera_target=CameraTarget.FACE_BOTTOM,
    camera=Camera(
        name="Bottom face Camera",
        detector_type="Camera",
        manufacturer=Organization.AILIPU,
        model="ELP-USBFHD05MT-KL170IR",
        notes="The light intensity sensor was removed; IR illumination is constantly on",
        data_interface="USB",
        computer_name="W10DTJK7N0M3",
        frame_rate=120,
        frame_rate_unit=FrequencyUnit.HZ,
        sensor_width=640,
        sensor_height=480,
        chroma="Color",
        cooling="Air",
        bin_mode="Additive",
        recording_software=bonsai_software,
    ),
    lens=Lens(
        name="Xenocam 2",
        model="XC0922LENS",
        manufacturer=Organization.OTHER,
        max_aperture="f/1.4",
        notes='Focal Length 9-22mm 1/3" IR F1.4',
    ),
)

harp_behavior = HarpDevice(
    name="Harp Behavior",
    harp_device_type=HarpDeviceType.BEHAVIOR,
    core_version="2.1",
    firmware_version="FTDI version:",
    computer_name="behavior_computer",
    is_clock_generator=False,
    channels=[
        DAQChannel(channel_name="DO0", device_name="Solenoid Left", channel_type="Digital Output"),
        DAQChannel(channel_name="DO1", device_name="Solenoid Right", channel_type="Digital Output"),
        DAQChannel(channel_name="DI0", device_name="Janelia_Lick_Detector Left", channel_type="Digital Input"),
        DAQChannel(channel_name="DI1", device_name="Janelia_Lick_Detector Right", channel_type="Digital Input"),
        DAQChannel(channel_name="DI3", device_name="Photometry Clock", channel_type="Digital Input"),
    ],
)

reward_delivery = RewardDelivery(
    reward_spouts=[
        RewardSpout(
            name="Left spout",
            side=SpoutSide.LEFT,
            spout_diameter=1.2,
            solenoid_valve=Device(name="Solenoid Left"),
            lick_sensor=Device(
                name="Janelia_Lick_Detector Left",
                manufacturer=Organization.JANELIA,
            ),
            lick_sensor_type=LickSensorType("Capacitive"),
        ),
        RewardSpout(
            name="Right spout",
            side=SpoutSide.RIGHT,
            spout_diameter=1.2,
            solenoid_valve=Device(name="Solenoid Right"),
            lick_sensor=Device(
                name="Janelia_Lick_Detector Right",
                manufacturer=Organization.JANELIA,
            ),
            lick_sensor_type=LickSensorType("Capacitive"),
        ),
    ],
    stage_type=MotorizedStage(
        name="NewScaleMotor for LickSpouts",
        manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
        travel=15.0,  # unit is mm
        firmware=("https://github.com/AllenNeuralDynamics/python-newscale,branch: axes-on-target,commit #7c17497"),
    ),
)

patch_cord = PatchCord(
    name="Bundle Branching Fiber-optic Patch Cord",
    manufacturer=Organization.DORIC,
    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
    core_diameter=200,
    numerical_aperture=0.37,
)

light_sources = [
    LightEmittingDiode(
        name="470nm LED",
        manufacturer=Organization.THORLABS,
        model="M470F3",
        wavelength=470,
    ),
    LightEmittingDiode(
        name="415nm LED",
        manufacturer=Organization.THORLABS,
        model="M415F3",
        wavelength=415,
    ),
    LightEmittingDiode(
        name="565nm LED",
        manufacturer=Organization.THORLABS,
        model="M565F3",
        wavelength=565,
    ),
]

detectors = [
    Detector(
        name="Green CMOS",
        serial_number="21396991",
        manufacturer=Organization.FLIR,
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
    Detector(
        name="Red CMOS",
        serial_number="21396991",
        manufacturer=Organization.FLIR,
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
]

objective = Objective(
    name="Objective",
    serial_number="128022336",
    manufacturer=Organization.NIKON,
    model="CFI Plan Apochromat Lambda D 10x",
    numerical_aperture=0.45,
    magnification=10,
    immersion="air",
)

filters = [
    Filter(
        name="Green emission filter",
        manufacturer=Organization.SEMROCK,
        model="FF01-520/35-25",
        filter_type="Band pass",
        center_wavelength=520,
        diameter=25,
    ),
    Filter(
        name="Red emission filter",
        manufacturer=Organization.SEMROCK,
        model="FF01-600/37-25",
        filter_type="Band pass",
        center_wavelength=600,
        diameter=25,
    ),
    Filter(
        name="Emission Dichroic",
        model="FF562-Di03-25x36",
        manufacturer=Organization.SEMROCK,
        filter_type="Dichroic",
        height=25,
        width=36,
        cut_off_wavelength=562,
    ),
    Filter(
        name="dual-edge standard epi-fluorescence dichroic beamsplitter",
        model="FF493/574-Di01-25x36",
        manufacturer=Organization.SEMROCK,
        notes="493/574 nm BrightLine dual-edge standard epi-fluorescence dichroic beamsplitter",
        filter_type="Multiband",
        width=36,
        height=24,
    ),
    Filter(
        name="Excitation filter 410nm",
        manufacturer=Organization.THORLABS,
        model="FB410-10",
        filter_type="Band pass",
        diameter=25,
        center_wavelength=410,
    ),
    Filter(
        name="Excitation filter 470nm",
        manufacturer=Organization.THORLABS,
        model="FB470-10",
        filter_type="Band pass",
        center_wavelength=470,
        diameter=25,
    ),
    Filter(
        name="Excitation filter 560nm",
        manufacturer=Organization.THORLABS,
        model="FB560-10",
        filter_type="Band pass",
        diameter=25,
        center_wavelength=560,
    ),
    Filter(
        name="450 Dichroic Longpass Filter",
        manufacturer=Organization.EDMUND_OPTICS,
        model="#69-898",
        filter_type="Dichroic",
        cut_off_wavelength=450,
        width=35.6,
        height=25.2,
    ),
    Filter(
        name="500 Dichroic Longpass Filter",
        manufacturer=Organization.EDMUND_OPTICS,
        model="#69-899",
        filter_type="Dichroic",
        cut_off_wavelength=500,
        width=35.6,
        height=23.2,
    ),
]

lens = Lens(
    manufacturer=Organization.THORLABS,
    model="AC254-080-A-ML",
    name="Image focusing lens",
    focal_length=80,
    focal_length_unit=SizeUnit.MM,
    size=1,
)

additional_device = Device(name="Photometry Clock")

calibrations = [
    Calibration(
        calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
        device_name="470nm LED",
        description="LED calibration",
        input={"Power setting": [0]},
        output={"Power mW": [0.02]},
    ),
    Calibration(
        calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
        device_name="415nm LED",
        description="LED calibration",
        input={"Power setting": [0]},
        output={"Power mW": [0.02]},
    ),
    Calibration(
        calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
        device_name="560nm LED",
        description="LED calibration",
        input={"Power setting": [0]},
        output={"Power mW": [0.02]},
    ),
    # Water calibration comes here#
]

inst = Instrument(
    instrument_id="447_FIP-Behavior_20000101",
    modification_date=date(2000, 1, 1),
    modalities=[Modality.BEHAVIOR, Modality.FIB],
    components=[
        camera1,
        camera2,
        harp_behavior,
        reward_delivery,
        patch_cord,
        *light_sources,
        *detectors,
        objective,
        *filters,
        lens,
        additional_device,
        Tube(name="mouse_tube_foraging", diameter=4.0),
    ],
    calibrations=calibrations,
)

inst.write_standard_file(prefix="fip_behavior")
