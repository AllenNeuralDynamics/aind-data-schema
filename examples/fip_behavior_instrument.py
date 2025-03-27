# -*- coding: utf-8 -*-

""" example FIP ophys instrument """
from datetime import date, datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import FrequencyUnit, SizeUnit, PowerUnit

from aind_data_schema.components.measurements import Calibration
from aind_data_schema.components.devices import (
    CameraAssembly,
    CameraTarget,
    Camera,
    Organization,
    Lens,
    HarpDevice,
    HarpDeviceType,
    DAQChannel,
    DaqChannelType,
    LickSpoutAssembly,
    LickSpout,
    Device,
    LickSensorType,
    MotorizedStage,
    PatchCord,
    LightEmittingDiode,
    Detector,
    Objective,
    Filter,
    Tube,
    Computer,
)
from aind_data_schema.core.instrument import Instrument, Connection, ConnectionData, ConnectionDirection
from aind_data_schema.components.identifiers import Software
from aind_data_schema.components.coordinates import (
    AnatomicalRelative,
    CoordinateSystemLibrary,
)

bonsai_software = Software(name="Bonsai", version="2.5")

computer = Computer(
    name="W10DTJK7N0M3",
)
behavior_computer = Computer(
    name="behavior_computer",
)

camera1 = CameraAssembly(
    name="BehaviorVideography_FaceSide",
    target=CameraTarget.FACE,
    relative_position=[AnatomicalRelative.LEFT],
    camera=Camera(
        name="Side face camera",
        detector_type="Camera",
        manufacturer=Organization.AILIPU,
        model="ELP-USBFHD05MT-KL170IR",
        notes="The light intensity sensor was removed; IR illumination is constantly on",
        data_interface="USB",
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
    target=CameraTarget.FACE,
    relative_position=[AnatomicalRelative.INFERIOR],
    camera=Camera(
        name="Bottom face Camera",
        detector_type="Camera",
        manufacturer=Organization.AILIPU,
        model="ELP-USBFHD05MT-KL170IR",
        notes="The light intensity sensor was removed; IR illumination is constantly on",
        data_interface="USB",
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
    is_clock_generator=False,
    channels=[
        DAQChannel(channel_name="DO0", channel_type=DaqChannelType.DO),
        DAQChannel(channel_name="DO1", channel_type=DaqChannelType.DO),
        DAQChannel(channel_name="DI0", channel_type=DaqChannelType.DI),
        DAQChannel(channel_name="DI1", channel_type=DaqChannelType.DI),
        DAQChannel(channel_name="DI3", channel_type=DaqChannelType.DI),
    ],
)

connections = [
    Connection(
        device_names=["Harp Behavior", "Solenoid Left"],
        connection_data={
            "Harp Behavior": ConnectionData(
                direction=ConnectionDirection.SEND,
                channel="DO0",
            ),
            "Solenoid Left": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Harp Behavior", "Solenoid Right"],
        connection_data={
            "Harp Behavior": ConnectionData(
                direction=ConnectionDirection.SEND,
                channel="DO1",
            ),
            "Solenoid Right": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Harp Behavior", "Janelia_Lick_Detector Left"],
        connection_data={
            "Harp Behavior": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
                channel="DI0",
            ),
            "Janelia_Lick_Detector Left": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    ),
    Connection(
        device_names=["Harp Behavior", "Janelia_Lick_Detector Right"],
        connection_data={
            "Harp Behavior": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
                channel="DI1",
            ),
            "Janelia_Lick_Detector Right": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    ),
    Connection(
        device_names=["Harp Behavior", "Photometry Clock"],
        connection_data={
            "Harp Behavior": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
                channel="DI3",
            ),
            "Photometry Clock": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    ),
    Connection(
        device_names=["W10DTJK7N0M3", "Side face camera"],
        connection_data={
            "W10DTJK7N0M3": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Side face camera": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    ),
    Connection(
        device_names=["W10DTJK7N0M3", "Bottom face camera"],
        connection_data={
            "W10DTJK7N0M3": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Side face camera": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    ),
    Connection(
        device_names=["behavior_computer", "Harp Behavior"],
        connection_data={
            "behavior_computer": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Harp Behavior": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    )
]

lick_spout_assembly = LickSpoutAssembly(
    lick_spouts=[
        LickSpout(
            name="Left spout",
            spout_diameter=1.2,
            solenoid_valve=Device(name="Solenoid Left"),
            lick_sensor=Device(
                name="Janelia_Lick_Detector Left",
                manufacturer=Organization.JANELIA,
            ),
            lick_sensor_type=LickSensorType("Capacitive"),
        ),
        LickSpout(
            name="Right spout",
            spout_diameter=1.2,
            solenoid_valve=Device(name="Solenoid Right"),
            lick_sensor=Device(
                name="Janelia_Lick_Detector Right",
                manufacturer=Organization.JANELIA,
            ),
            lick_sensor_type=LickSensorType("Capacitive"),
        ),
    ],
    motorized_stage=MotorizedStage(
        name="NewScaleMotor for LickSpouts",
        manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
        travel=15.0,
        travel_unit=SizeUnit.MM,
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

tube = Tube(name="mouse_tube_foraging", diameter=4.0)

additional_device = Device(name="Photometry Clock")

calibrations = [
    Calibration(
        calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
        device_name="470nm LED",
        description="LED calibration",
        input=[0],
        input_unit=PowerUnit.PERCENT,
        output=[0.02],
        output_unit=PowerUnit.MW,
    ),
    Calibration(
        calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
        device_name="415nm LED",
        description="LED calibration",
        input=[0],
        input_unit=PowerUnit.PERCENT,
        output=[0.02],
        output_unit=PowerUnit.MW,
    ),
    Calibration(
        calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
        device_name="560nm LED",
        description="LED calibration",
        input=[0],
        input_unit=PowerUnit.PERCENT,
        output=[0.02],
        output_unit=PowerUnit.MW,
    ),
    # Water calibration comes here#
]

inst = Instrument(
    instrument_id="447_FIP-Behavior_20000101",
    modification_date=date(2000, 1, 1),
    modalities=[Modality.BEHAVIOR, Modality.FIB],
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    components=[
        camera1,
        camera2,
        harp_behavior,
        lick_spout_assembly,
        patch_cord,
        *light_sources,
        *detectors,
        objective,
        *filters,
        lens,
        additional_device,
    ],
    connections=connections,
    calibrations=calibrations,
)

inst.write_standard_file(prefix="fip_behavior")
