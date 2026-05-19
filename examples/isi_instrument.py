"""Generates an example JSON file for an ISI (Intrinsic Signal Imaging) instrument

Based on the ISI Full Rig BOM (AIBS part 0113_000-00, Rev A).
The rig consists of:
  - ISI Table Assembly (0113_100-00)
  - ISI System Structure (0113_200-00)
  - Camera, Stage, and Mount Assembly (0113_300-00)
  - Headframe Clamp Assembly (0113_400-00)
  - ISI Eye Tracking Assembly (0123_500-00)
  - Camera/Lens Assembly (0113_550-00) with tandem Nikon lenses and Andor Zyla sCMOS
  - LED Light Ring Assembly (0113_530-00)
"""

import argparse
from datetime import date

from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.devices import (
    CameraChroma,
    CameraTarget,
    DataInterface,
    DetectorType,
    FilterType,
)
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import SizeUnit

from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.devices import (
    Camera,
    CameraAssembly,
    Computer,
    DAQDevice,
    Device,
    Filter,
    Lens,
    LightEmittingDiode,
    Monitor,
    MotorizedStage,
)
from aind_data_schema.core.instrument import Instrument

acquisition_computer = Computer(
    name="Acquisition Computer",
)

stim_computer = Computer(
    name="Stim Computer",
)

ni_daq = DAQDevice(
    name="DAQ",
    manufacturer=Organization.NATIONAL_INSTRUMENTS,
    model="USB-6008",
    data_interface=DataInterface.USB,
)

newport_linear_stage = MotorizedStage(
    name="Linear Stage",
    manufacturer=Organization.MKS_NEWPORT,
    model="M-ILS100PP",
    travel=100,
    travel_unit=SizeUnit.MM,
    notes="Controlled by Newport SMC100PP.",
)

newport_motor_controller = Device(
    name="Motor Controller",
    manufacturer=Organization.MKS_NEWPORT,
    model="SMC100PP",
)

isi_camera = Camera(
    name="ISI Camera",
    manufacturer=Organization.OXFORD_INSTRUMENTS,
    model="Zyla 5.5 sCMOS",
    detector_type=DetectorType.CAMERA,
    data_interface=DataInterface.USB,
    chroma=CameraChroma.BW,
)

isi_lens_35mm = Lens(
    name="Front Lens",
    manufacturer=Organization.NIKON,
    model="NIKKOR 35mm f/1.4",
    notes="Front lens of tandem-lens assembly.",
)

isi_lens_105mm = Lens(
    name="Rear Lens",
    manufacturer=Organization.NIKON,
    model="Micro-NIKKOR 105mm f/2.8",
    notes="Rear lens of tandem-lens assembly, facing the camera.",
)

isi_bandpass_filter = Filter(
    name="Bandpass Filter",
    manufacturer=Organization.SEMROCK,
    model="FF01-630/92-50",
    filter_type=FilterType.BANDPASS,
    center_wavelength=630,
    wavelength_unit=SizeUnit.NM,
)

isi_camera_assembly = CameraAssembly(
    name="ISI Brain Camera Assembly",
    target=CameraTarget.BRAIN,
    relative_position=[AnatomicalRelative.SUPERIOR],
    camera=isi_camera,
    lens=isi_lens_35mm,
    filter=isi_bandpass_filter,
)

eye_tracking_camera = Camera(
    name="Eye Tracking Camera",
    manufacturer=Organization.ALLIED,
    model="MAKO G-125C",
    detector_type=DetectorType.CAMERA,
    data_interface=DataInterface.ETH,
    chroma=CameraChroma.BW,
)

eye_tracking_lens = Lens(
    name="Eye Tracking Lens",
    manufacturer=Organization.INFINITY_PHOTO_OPTICAL,
    model="Proximity Series 130mm W.D./0.73x",
)

eye_tracking_camera_assembly = CameraAssembly(
    name="Eye Tracking Camera Assembly",
    target=CameraTarget.EYE,
    relative_position=[AnatomicalRelative.ANTERIOR],
    camera=eye_tracking_camera,
    lens=eye_tracking_lens,
)

eye_tracking_dichroic = Filter(
    name="Dichroic Filter",
    manufacturer=Organization.SEMROCK,
    model="FF750-SDi02-25x36",
    filter_type=FilterType.DICHROIC,
    cut_off_wavelength=750,
    wavelength_unit=SizeUnit.NM,
    notes="Separates 850 nm IR illumination for eye tracking.",
)

eye_tracking_ir_led = LightEmittingDiode(
    name="Eye Tracking IR LED",
    manufacturer=Organization.AMS_OSRAM,
    model="LZ4-40R608-0000",
    wavelength=850,
    wavelength_unit=SizeUnit.NM,
)

eye_tracking_collimating_lens = Lens(
    name="Collimating Lens",
    manufacturer=Organization.THORLABS,
    model="LB1092-B-ML",
)

led_ring_green = LightEmittingDiode(
    name="LED Ring Green",
    manufacturer=Organization.OTHER,
    model="C503B-GCN-CY0C0791",
    wavelength=527,
    wavelength_unit=SizeUnit.NM,
    notes="19 units in LED light ring assembly (0113_530-00).",
)

led_ring_red = LightEmittingDiode(
    name="LED Ring Red",
    manufacturer=Organization.OTHER,
    model="HLMP-EG08-Y2000",
    wavelength=635,
    wavelength_unit=SizeUnit.NM,
    notes="9 units in LED light ring assembly (0113_530-00).",
)

stimulus_monitor = Monitor(
    name="Stimulus Monitor",
    manufacturer=Organization.ASUS,
    model="PA248Q",
    refresh_rate=60,
    width=1920,
    height=1200,
    size_unit=SizeUnit.PX,
    viewing_distance=15,
    viewing_distance_unit=SizeUnit.CM,
    relative_position=[AnatomicalRelative.ANTERIOR],
)

temperature_controller = Device(
    name="Temperature Controller",
    manufacturer=Organization.WPI,
    model="ATC2000",
)

somnosuite = Device(
    name="SomnoSuite",
    manufacturer=Organization.KENT_SCIENTIFIC_CORPORATION,
    model="SOMNO",
    notes="Used with accessory facemasks (SOMNO-0801) and induction chamber (SOMNO-0705).",
)

physiosuite = Device(
    name="PhysioSuite",
    manufacturer=Organization.KENT_SCIENTIFIC_CORPORATION,
    model="PS-MSTAT-RT",
)

inst = Instrument(
    location="",
    instrument_id="ISIV.1",
    modification_date=date(2026, 5, 15),
    modalities=[Modality.ISI],
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    temperature_control=True,
    notes="",
    components=[
        acquisition_computer,
        stim_computer,
        ni_daq,
        newport_linear_stage,
        newport_motor_controller,
        isi_camera_assembly,
        isi_lens_105mm,
        eye_tracking_camera_assembly,
        eye_tracking_dichroic,
        eye_tracking_ir_led,
        eye_tracking_collimating_lens,
        led_ring_green,
        led_ring_red,
        stimulus_monitor,
        temperature_controller,
        somnosuite,
        physiosuite,
    ],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = inst.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="isi", output_directory=args.output_dir)
