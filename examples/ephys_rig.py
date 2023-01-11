"""Generates an example JSON file for an ephys rig"""

from aind_data_schema.device import Camera, CameraAssembly, DAQChannel, Filter, Laser, Lens
from aind_data_schema.ephys.ephys_rig import (Disc, EphysModule, EphysProbe, EphysRig, HarpDevice, LaserModule,
                                              Manipulator, NeuropixelsBasestation, ProbePort, StickMicroscope)

# Describes a rig with running wheel, 2 behavior cameras, one Harp Behavior board,
# one dual-color laser module, one stick microscope, and 2 Neuropixels probes

behavior_computer = "W10DT72941"
ephys_computer = "W10DT72942"

running_wheel = Disc(name="Running Wheel", radius=15)

digital_out0 = DAQChannel(channel_name="DO0", device_name="Face Camera", channel_type="Digital Output")

digital_out1 = DAQChannel(channel_name="DO1", device_name="Body Camera", channel_type="Digital Output")

analog_input = DAQChannel(channel_name="AI0", device_name="Running Wheel", channel_type="Analog Input")

harp = HarpDevice(
    name="Harp Behavior",
    harp_device_type="Behavior",
    harp_device_version="2.1",
    computer_name=behavior_computer,
    channels=[digital_out0, digital_out1, analog_input],
)

port1 = ProbePort(index=1, probes=["Probe A"])

port2 = ProbePort(index=2, probes=["Probe B"])

basestation = NeuropixelsBasestation(
    name="Basestation Slot 3",
    basestation_firmware_version="2.019",
    bsc_firmware_version="2.199",
    slot=3,
    ports=[port1, port2],
    computer_name=ephys_computer,
)

red_laser = Laser(name="Red Laser", wavelength=473, manufacturer="Oxxius")

blue_laser = Laser(name="Blue Laser", wavelength=638, manufacturer="Oxxius")

laser_module = LaserModule(
    manipulator=Manipulator(serial_number="SN2937", manufacturer="New Scale Technologies"),
    lasers=[red_laser, blue_laser],
    arc_angle=20,
    module_angle=10,
)

probe_camera = Camera(
    name="Probe Camera",
    data_interface="USB",
    manufacturer="FLIR",
    computer_name=ephys_computer,
    max_frame_rate=50,
    pixel_width=1080,
    pixel_height=570,
    sensor_format='1/2.9"',
    chroma="Color",
)

microscope = StickMicroscope(camera=probe_camera, arc_angle=70, module_angle=20)

probeA = EphysProbe(name="Probe A", serial_number="9291019", probe_model="Neuropixels 1.0")

probeB = EphysProbe(name="Probe B", serial_number="9291020", probe_model="Neuropixels 1.0")

ephys_moduleA = EphysModule(
    manipulator=Manipulator(serial_number="SN2938", manufacturer="New Scale Technologies"),
    arc_angle=99,
    module_angle=20,
    rotation_angle=10,
    probes=[probeA],
)

ephys_moduleB = EphysModule(
    manipulator=Manipulator(serial_number="SN2939", manufacturer="New Scale Technologies"),
    arc_angle=120,
    module_angle=20,
    rotation_angle=15,
    probes=[probeB],
)


filt = Filter(filter_type="Long pass", manufacturer="Thorlabs", description="850 nm longpass filter")

lens = Lens(focal_length=15, manufacturer="Edmund Optics", max_aperture="f/2")

face_camera = Camera(
    name="Face Camera",
    data_interface="USB",
    manufacturer="FLIR",
    computer_name=behavior_computer,
    max_frame_rate=500,
    pixel_width=1080,
    pixel_height=570,
    sensor_format='1/2.9"',
    chroma="Monochrome",
)

camassm1 = CameraAssembly(camera_assembly_name="Face Camera Assembly", camera=face_camera, filter=filt, lens=lens)

body_camera = Camera(
    name="Body Camera",
    data_interface="USB",
    manufacturer="FLIR",
    computer_name=behavior_computer,
    max_frame_rate=500,
    pixel_width=1080,
    pixel_height=570,
    sensor_format='1/2.9"',
    chroma="Monochrome",
)

camassm2 = CameraAssembly(camera_assembly_name="Body Camera Assembly", camera=body_camera, filter=filt, lens=lens)

rig = EphysRig(
    rig_id="323_EPHYS1",
    ephys_modules=[ephys_moduleA, ephys_moduleB],
    cameras=[camassm1, camassm2],
    laser_modules=[laser_module],
    daqs=[basestation, harp],
    stick_microscopes=[microscope],
    mouse_platform=running_wheel,
)

rig.write_standard_file()
