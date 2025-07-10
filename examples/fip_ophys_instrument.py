""" example FIP ophys instrument """

from datetime import date, datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import FrequencyUnit, PowerUnit

import aind_data_schema.components.devices as d
import aind_data_schema.core.instrument as r
from aind_data_schema.components.connections import Connection
from aind_data_schema.components.identifiers import Software
from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.measurements import Calibration
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema.components.devices import Computer

bonsai_software = Software(name="Bonsai", version="2.5")

computer = Computer(
    name="W10DTJK7N0M3",
)

camera_assembly_1 = d.CameraAssembly(
    name="BehaviorVideography_FaceSide",
    target=d.CameraTarget.FACE,
    relative_position=[AnatomicalRelative.LEFT],
    camera=d.Camera(
        name="Side face camera",
        detector_type="Camera",
        manufacturer=d.Organization.AILIPU,
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
    lens=d.Lens(
        name="Xenocam 1",
        model="XC0922LENS",
        manufacturer=d.Organization.OTHER,
        notes='Focal Length 9-22mm 1/3" IR F1.4',
    ),
)

camera_assembly_2 = d.CameraAssembly(
    name="BehaviorVideography_FaceBottom",
    target=d.CameraTarget.FACE,
    relative_position=[AnatomicalRelative.ANTERIOR, AnatomicalRelative.INFERIOR],
    camera=d.Camera(
        name="Bottom face Camera",
        detector_type="Camera",
        manufacturer=d.Organization.AILIPU,
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
    lens=d.Lens(
        name="Xenocam 2",
        model="XC0922LENS",
        manufacturer=d.Organization.OTHER,
        notes='Focal Length 9-22mm 1/3" IR F1.4',
    ),
)

patch_cord = d.FiberPatchCord(
    name="Bundle Branching Fiber-optic Patch Cord",
    manufacturer=d.Organization.DORIC,
    model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
    core_diameter=200,
    numerical_aperture=0.37,
)

light_source_1 = d.LightEmittingDiode(
    name="470nm LED",
    manufacturer=d.Organization.THORLABS,
    model="M470F3",
    wavelength=470,
)

light_source_2 = d.LightEmittingDiode(
    name="415nm LED",
    manufacturer=d.Organization.THORLABS,
    model="M415F3",
    wavelength=415,
)

light_source_3 = d.LightEmittingDiode(
    name="565nm LED",
    manufacturer=d.Organization.THORLABS,
    model="M565F3",
    wavelength=565,
)

detector_1 = d.Detector(
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
)

detector_2 = d.Detector(
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
)

objective = d.Objective(
    name="Objective",
    serial_number="128022336",
    manufacturer=d.Organization.NIKON,
    model="CFI Plan Apochromat Lambda D 10x",
    numerical_aperture=0.45,
    magnification=10,
    immersion="air",
)

filter_1 = d.Filter(
    name="Green emission filter",
    manufacturer=d.Organization.SEMROCK,
    model="FF01-520/35-25",
    filter_type="Band pass",
    center_wavelength=520,
)

filter_2 = d.Filter(
    name="Red emission filter",
    manufacturer=d.Organization.SEMROCK,
    model="FF01-600/37-25",
    filter_type="Band pass",
    center_wavelength=600,
)

filter_3 = d.Filter(
    name="Emission Dichroic",
    model="FF562-Di03-25x36",
    manufacturer=d.Organization.SEMROCK,
    filter_type="Dichroic",
    cut_off_wavelength=562,
)

filter_4 = d.Filter(
    name="dual-edge standard epi-fluorescence dichroic beamsplitter",
    model="FF493/574-Di01-25x36",
    manufacturer=d.Organization.SEMROCK,
    notes="BrightLine dual-edge standard epi-fluorescence dichroic beamsplitter",
    filter_type="Multiband",
    center_wavelength=[493, 574],
)

filter_5 = d.Filter(
    name="Excitation filter 410nm",
    manufacturer=d.Organization.THORLABS,
    model="FB410-10",
    filter_type="Band pass",
    center_wavelength=410,
)

filter_6 = d.Filter(
    name="Excitation filter 470nm",
    manufacturer=d.Organization.THORLABS,
    model="FB470-10",
    filter_type="Band pass",
    center_wavelength=470,
)

filter_7 = d.Filter(
    name="Excitation filter 560nm",
    manufacturer=d.Organization.THORLABS,
    model="FB560-10",
    filter_type="Band pass",
    center_wavelength=560,
)

filter_8 = d.Filter(
    name="450 Dichroic Longpass Filter",
    manufacturer=d.Organization.EDMUND_OPTICS,
    model="#69-898",
    filter_type="Dichroic",
    cut_off_wavelength=450,
)

filter_9 = d.Filter(
    name="500 Dichroic Longpass Filter",
    manufacturer=d.Organization.EDMUND_OPTICS,
    model="#69-899",
    filter_type="Dichroic",
    cut_off_wavelength=500,
)

lens = d.Lens(
    manufacturer=d.Organization.THORLABS,
    model="AC254-080-A-ML",
    name="Image focusing lens",
)

daq = d.HarpDevice(
    name="Harp Behavior",
    harp_device_type=d.HarpDeviceType.BEHAVIOR,
    core_version="2.1",
    is_clock_generator=False,
    channels=[
        d.DAQChannel(channel_name="DO0", channel_type="Digital Output"),
        d.DAQChannel(channel_name="DO1", channel_type="Digital Output"),
        d.DAQChannel(channel_name="DI0", channel_type="Digital Input"),
        d.DAQChannel(channel_name="DI1", channel_type="Digital Input"),
        d.DAQChannel(channel_name="DI3", channel_type="Digital Input"),
    ],
)
connections = [
    Connection(
        source_device="Harp Behavior",
        source_port="DO0",
        target_device="Solenoid Left",
    ),
    Connection(
        source_device="Harp Behavior",
        source_port="DO1",
        target_device="Solenoid Right",
    ),
    Connection(
        source_device="Janelia_Lick_Detector Left",
        target_device="Harp Behavior",
        target_port="DI0",
    ),
    Connection(
        source_device="Janelia_Lick_Detector Right",
        target_device="Harp Behavior",
        target_port="DI1",
    ),
    Connection(
        source_device="Photometry Clock",
        target_device="Harp Behavior",
        target_port="DI3",
    ),
    Connection(
        source_device="Side face camera",
        target_device="W10DTJK7N0M3",
    ),
    Connection(
        source_device="Bottom face camera",
        target_device="W10DTJK7N0M3",
    ),
    Connection(
        source_device="Harp Behavior",
        target_device="W10DTJK7N0M3",
    ),
]

mouse_platform = d.Disc(name="mouse_disc", radius=8.5)

stimulus_device = d.LickSpoutAssembly(
    name="Lick spout assembly",
    lick_spouts=[
        d.LickSpout(
            name="Left spout",
            spout_diameter=1.2,
            solenoid_valve=d.Device(name="Solenoid Left"),
            lick_sensor=d.Device(
                name="Lick-o-meter Left",
            ),
        ),
        d.LickSpout(
            name="Right spout",
            spout_diameter=1.2,
            solenoid_valve=d.Device(name="Solenoid Right"),
            lick_sensor=d.Device(
                name="Lick-o-meter Right",
            ),
        ),
    ],
)

additional_device = d.Device(name="Photometry Clock")

calibration = Calibration(
    calibration_date=datetime(2023, 10, 2, 3, 15, 22, tzinfo=timezone.utc),
    device_name="470nm LED",
    description="LED calibration",
    input=[1, 2, 3],
    input_unit=PowerUnit.PERCENT,
    output=[5, 10, 13],
    output_unit=PowerUnit.MW,
)

instrument = r.Instrument(
    location="428",
    instrument_id="FIP1",
    modification_date=date(2023, 10, 3),
    modalities=[Modality.FIB],
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    components=[
        camera_assembly_1,
        camera_assembly_2,
        patch_cord,
        light_source_1,
        light_source_2,
        light_source_3,
        detector_1,
        detector_2,
        objective,
        filter_1,
        filter_2,
        filter_3,
        filter_4,
        filter_5,
        filter_6,
        filter_7,
        filter_8,
        filter_9,
        lens,
        daq,
        stimulus_device,
        additional_device,
        mouse_platform,
    ],
    calibrations=[calibration],
)

if __name__ == "__main__":
    serialized = instrument.model_dump_json()
    deserialized = r.Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="fip_ophys")
