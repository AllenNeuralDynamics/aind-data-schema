"""example SLAP2 instrument"""

import argparse
from datetime import datetime

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, SizeUnit, SpeedUnit
from aind_data_schema_models.devices import CameraTarget, FilterType, DetectorType
from aind_data_schema_models.coordinates import AnatomicalRelative

from aind_data_schema.core.instrument import Instrument
from aind_data_schema.components.devices import (
    BinMode,
    Camera,
    CameraAssembly,
    HarpDevice,
    Cooling,
    DAQChannel,
    DaqChannelType,
    DAQDevice,
    DataInterface,
    Detector,
    Disc,
    Filter,
    Laser,
    Lens,
    Monitor,
    PockelsCell,
    Computer,
    Objective,
    Device,
    PolygonalScanner,
    DigitalMicromirrorDevice,
    PockelsCell,
    Microscope,
)
from aind_data_schema.components.connections import Connection
from aind_data_schema.components.coordinates import (
    CoordinateSystemLibrary,
    Affine,
    Translation,
)

computer_names = {
    "VCO": "w10dt714710",
    "SLAP2": "SLAP2-1-PC",
}

slap2_1_microscope = Microscope(
    name="SLAP2_1",
    manufacturer=Organization.MBF,
)

vco_1_computer = Computer(name=computer_names["VCO"])

harp_behavior = HarpDevice(
    name="VCO1_Behavior",
    harp_device_type=HarpDeviceType.BEHAVIOR,
    core_version="2.1",
    channels=[
        DAQChannel(channel_name="AI0", channel_type=DaqChannelType.AI),
        DAQChannel(channel_name="AI1", channel_type=DaqChannelType.AI),
        DAQChannel(channel_name="DO0", channel_type=DaqChannelType.DO),
        DAQChannel(channel_name="DO1", channel_type=DaqChannelType.DO),
        DAQChannel(channel_name="DI3", channel_type=DaqChannelType.DI),
    ],
    is_clock_generator=False,
)

cuttlefish_camtrigger = DAQDevice(
    name="VCO1_CuttlefishCamTrigger",
    data_interface=DataInterface.USB,
    manufacturer=Organization.AIND,
    channels=[
        DAQChannel(channel_name="PWM0", channel_type=DaqChannelType.DO),
        DAQChannel(channel_name="PWM2", channel_type=DaqChannelType.DO),
        DAQChannel(channel_name="PWM4", channel_type=DaqChannelType.DO),
    ],
    notes="Cuttlefish Cam Trigger",
)

timestamp_generator = HarpDevice(
    name="VCO1_TimeStampGenerator",
    harp_device_type=HarpDeviceType.TIMESTAMPGENERATORGEN3,
    is_clock_generator=True,
)

running_disc = Disc(
    name="MindScope Running Disc",
    serial_number=None,
    manufacturer=Organization.AIND,
    model=None,
    notes=None,
    surface_material="Kittrich Magic Cover Solid Grip Liner",
    radius=8.255,
    radius_unit="centimeter",
    encoder="CUI Devices AMT102-V",
    decoder="LS7366R",
)

face_camera_assembly = CameraAssembly(
    name="FaceCamera Assembly",
    target=CameraTarget.FACE,
    relative_position=[AnatomicalRelative.ANTERIOR],
    camera=Camera(
        name="FaceCamera",
        manufacturer=Organization.FLIR,
        model="BFS-U3-04S2M-CS",
        data_interface=DataInterface.USB,
        serial_number="25092525",
    ),
    lens=Lens(name="FaceCamera Lens", manufacturer=Organization.EDMUND_OPTICS, model="86-604"),
    filter=Filter(
        name="FaceCamera Filter",
        filter_type=FilterType.LONGPASS,
        manufacturer=Organization.SEMROCK,
        cut_off_wavelength=715,
        wavelength_unit=SizeUnit.NM,
        model="FF01-715/LP-25",
    ),
)

body_camera_assembly = CameraAssembly(
    name="BodyCamera Assembly",
    target=CameraTarget.BODY,
    relative_position=[AnatomicalRelative.LEFT],
    camera=Camera(
        name="BodyCamera",
        manufacturer=Organization.FLIR,
        model="BFS-U3-04S2M-CS",
        data_interface=DataInterface.USB,
        serial_number="25092522",
    ),
    lens=Lens(name="BodyCamera Lens", manufacturer=Organization.THORLABS, model="MVL6WA"),
    filter=Filter(
        name="BodyCamera Filter",
        filter_type=FilterType.LONGPASS,
        manufacturer=Organization.SEMROCK,
        cut_off_wavelength=747,
        wavelength_unit=SizeUnit.NM,
        model="FF01-747/33-25",
    ),
)

eye_camera_assembly = CameraAssembly(
    name="EyeCamera Assembly",
    target=CameraTarget.EYE,
    relative_position=[AnatomicalRelative.RIGHT],
    camera=Camera(
        name="EyeCamera",
        manufacturer=Organization.FLIR,
        model="BFS-U3-04S2M-CS",
        data_interface=DataInterface.USB,
        serial_number="25092545",
    ),
    lens=Lens(name="EyeCamera Lens", manufacturer=Organization.INFINITY_PHOTO_OPTICAL, model="213073"),
)

monitor = Monitor(
    name="Stimulus Screen",
    serial_number=None,
    manufacturer=Organization.LG,
    model="LP097QX1",
    width=2048,
    height=1536,
    size_unit=SizeUnit.PX,
    viewing_distance=15.1,
    viewing_distance_unit=SizeUnit.CM,
    refresh_rate=60,
    relative_position=[AnatomicalRelative.ANTERIOR, AnatomicalRelative.RIGHT],
)

photodiode = Device(
    name="Photodiode",
    manufacturer=Organization.AIND,
)

slap2_1_computer = Computer(name=computer_names["SLAP2"])

sipm_red = Detector(
    name="SiPM Red",
    detector_type=DetectorType.SiPM,
    manufacturer=Organization.HAMAMATSU,
    model="C13366-1960",
    serial_number="22C-002",
    data_interface=DataInterface.PCIE,
    cooling=Cooling.AIR,
    notes="SiPM detector",
)

sipm_green = Detector(
    name="SiPM Green",
    detector_type=DetectorType.SiPM,
    manufacturer=Organization.HAMAMATSU,
    model="C13366-5286",
    serial_number="16D-001",
    data_interface=DataInterface.PCIE,
    cooling=Cooling.AIR,
    notes="SiPM detector",
)

filter_red = Filter(
    name="Red Emission Filters",
    serial_number="None",
    manufacturer=Organization.SEMROCK,
    filter_type=FilterType.BANDPASS,
    cut_off_wavelength=725,
    cut_on_wavelength=585,
    center_wavelength=655,
    wavelength_unit=SizeUnit.NM,
    notes="Includes 585 dichroic mirror and 650/150 filter",
)

filter_green = Filter(
    name="Green Emission Filters",
    serial_number="None",
    manufacturer=Organization.SEMROCK,
    filter_type=FilterType.BANDPASS,
    cut_off_wavelength=580,
    cut_on_wavelength=500,
    center_wavelength=540,
    wavelength_unit=SizeUnit.NM,
    notes="Includes 585 dichroic mirror and 540/80 filter",
)

poly_scanner_rpm = 21500
poly_scanner_number_faces = 28
polygon = PolygonalScanner(
    name="Polygonal Scanner",
    manufacturer=Organization.CAMBRIDGE_TECHNOLOGY,
    speed=poly_scanner_rpm,
    speed_unit=SpeedUnit.RPM,
    number_faces=poly_scanner_number_faces,
)

pockelscell = PockelsCell(name="Pockels Cell", polygonal_scanner="Polygonal Scanner")

dmds_serial_numbers = ["14117", "14116"]
dmds_max_patterns = [800, 800]
dmds_invert = [False, False]
dmds_motion_padding_x = [0, 0]
dmds_motion_padding_y = [50, 50]
dmds_pixel_size = [0.00048173171943165054, 0.00048159140538133036]
dmds_start_phase = [-0.041281897483520513, 0.44534434150971336]
dmds_dmd_curtain = [[0.064890187222043413, 0.87507695142523756], [0.086187592847882244, 0.90714067455743808]]
dmds_line_shear_anchors = [[3.88924813, -3.36656499], [2.79574895, -3.24933243]]

dmds = [None] * 2
for dmd_idx in range(2):
    dmds[dmd_idx] = DigitalMicromirrorDevice(
        name=f"DMD{dmd_idx+1}",
        max_dmd_patterns=dmds_max_patterns[dmd_idx],
        invert_pixel_values=dmds_invert[dmd_idx],
        motion_padding_x=dmds_motion_padding_x[dmd_idx],
        motion_padding_y=dmds_motion_padding_y[dmd_idx],
        pixel_size=dmds_pixel_size[dmd_idx],
        start_phase=dmds_start_phase[dmd_idx],
        dmd_curtain=dmds_dmd_curtain[dmd_idx],
        line_shear_anchors=dmds_line_shear_anchors[dmd_idx],
        manufacturer=Organization.OTHER,
        serial_number=dmds_serial_numbers[dmd_idx],
        notes="ViALUX DMD",
    )

objective = Objective(
    name="Leica Objective",
    numerical_aperture=1,
    magnification=20,
    manufacturer=Organization.LEICA,
    immersion="water",
    serial_number="0119",
    model="507704",
)

hwp = Device(
    name="Half-Wave Plate",
    manufacturer=Organization.THORLABS,
)

twophoton_laser = Laser(
    name="Monaco 150",
    manufacturer=Organization.COHERENT_SCIENTIFIC,
    serial_number="S0124263226",
    model="Monaco 150",
    wavelength=1035,
    notes="maximum power of 150W",
)

vdaq = DAQDevice(
    name="vDAQ",
    serial_number=None,
    manufacturer=Organization.OTHER,
    notes="Manufactured by MBF Bioscience",
    data_interface=DataInterface.PCIE,
    channels=[
        DAQChannel(channel_name="AO5", channel_type=DaqChannelType.AO),
        DAQChannel(channel_name="D0.0", channel_type=DaqChannelType.DI),
        DAQChannel(channel_name="D0.1", channel_type=DaqChannelType.DI),
        DAQChannel(channel_name="D0.4", channel_type=DaqChannelType.DO),
    ],
)

connections = [
    Connection(source_device="FaceCamera", target_device=computer_names["VCO"]),
    Connection(source_device="BodyCamera", target_device=computer_names["VCO"]),
    Connection(source_device="EyeCamera", target_device=computer_names["VCO"]),
    Connection(source_device="Stimulus Screen", target_device=computer_names["VCO"]),
    Connection(source_device="VCO1_Behavior", target_device=computer_names["VCO"]),
    Connection(source_device="Photodiode", target_device="VCO1_Behavior", target_port="AI0"),
    Connection(  # "BCI signal"
        source_device="vDAQ", source_port="AO5", target_device="VCO1_Behavior", target_port="AI1"
    ),
    Connection(  # START signal
        source_device="VCO1_Behavior", source_port="DO0", target_device="vDAQ", target_port="D0.0"
    ),
    Connection(  # STOP signal
        source_device="VCO1_Behavior", source_port="DO1", target_device="vDAQ", target_port="D0.1"
    ),
    Connection(  # SLAP2 cycle clock signal
        source_device="vDAQ", source_port="D0.4", target_device="VCO1_Behavior", target_port="DI3"
    ),
    Connection(
        source_device="VCO1_CuttlefishCamTrigger",
        source_port="PWM0",
        target_device="BodyCamera",
    ),
    Connection(
        source_device="VCO1_CuttlefishCamTrigger",
        source_port="PWM2",
        target_device="EyeCamera",
    ),
    Connection(
        source_device="VCO1_CuttlefishCamTrigger",
        source_port="PWM4",
        target_device="EyeCamera",
    ),
    Connection(
        source_device=computer_names["SLAP2"],
        target_device="vDAQ",
        send_and_receive=True,
    ),
    Connection(source_device="SiPM Red", target_device="vDAQ"),
    Connection(source_device="SiPM Green", target_device="vDAQ"),
    Connection(source_device=computer_names["SLAP2"], target_device="Half-Wave Plate"),
    Connection(source_device="vDAQ", target_device="DMD1"),
    Connection(source_device="vDAQ", target_device="DMD2"),
    Connection(source_device="vDAQ", target_device="Polygonal Scanner"),
]

instrument = Instrument(
    location="443",
    instrument_id="SLAP2_1_VCO_1",
    modification_date=datetime.now().date(),
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    modalities=[Modality.SLAP2, Modality.BEHAVIOR, Modality.BEHAVIOR_VIDEOS],
    notes="Devices and connections not currently directly controlled or read out by the user may not be listed here. Refer to SLAP2 or VCO resources for detailed hardware descriptions.",
    temperature_control=True,
    components=[
        # slap2 components
        slap2_1_computer,
        slap2_1_microscope,
        sipm_red,
        sipm_green,
        hwp,
        objective,
        twophoton_laser,
        vdaq,
        filter_green,
        filter_red,
        dmds[0],
        dmds[1],
        polygon,
        pockelscell,
        # vco components
        vco_1_computer,
        harp_behavior,
        cuttlefish_camtrigger,
        timestamp_generator,
        running_disc,
        face_camera_assembly,
        body_camera_assembly,
        eye_camera_assembly,
        monitor,
        photodiode,
    ],
    calibrations=[],
    connections=connections,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = instrument.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="slap2", output_directory=args.output_dir)
