""" example ExaSPIM instrument """

import datetime

from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.devices import DAQChannel, DAQDevice, Detector, Filter, Laser
from aind_data_schema.core import instrument

inst = instrument.Instrument(
    instrument_id="440_exaSPIM1-20231004",
    instrument_type="exaSPIM",
    modification_date=datetime.date(2023, 10, 4),
    manufacturer=Organization.CUSTOM,
    objectives=[
        instrument.Objective(
            name="Custom Objective",
            numerical_aperture=0.305,
            magnification=5,
            immersion="air",
            manufacturer=Organization.OTHER,
            model="JM_DIAMOND 5.0X/1.3",
            notes="manufacturer collaboration between Schneider-Kreuznach and Vieworks",
        ),
    ],
    detectors=[
        Detector(
            name="Camera 1",
            detector_type="Camera",
            data_interface="Coax",
            cooling="Air",
            manufacturer=Organization.VIEWORKS,
            model="VNP-604MX",
            serial_number="MB151BAY001",
        ),
    ],
    light_sources=[
        Laser(
            name="LAS-08307",
            coupling="Single-mode fiber",
            wavelength=405,
            maximum_power=200,
            serial_number="LAS-08307",
            manufacturer=Organization.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
        Laser(
            name="LAS-08308",
            coupling="Single-mode fiber",
            wavelength=488,
            maximum_power=200,
            serial_number="LAS-08308",
            manufacturer=Organization.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
        Laser(
            name="539251",
            coupling="Single-mode fiber",
            wavelength=561,
            maximum_power=200,
            serial_number="539251",
            manufacturer=Organization.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
        Laser(
            name="LAS-08309",
            coupling="Single-mode fiber",
            wavelength=638,
            maximum_power=200,
            serial_number="LAS-08309",
            manufacturer=Organization.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
    ],
    fluorescence_filters=[
        Filter(
            name="Multiband filter",
            filter_type="Multiband",
            manufacturer=Organization.CHROMA,
            diameter=44.05,
            thickness=1,
            model="ZET405/488/561/640mv2",
            notes="Custom made filter",
            filter_wheel_index=0,
        )
    ],
    daqs=[
        DAQDevice(
            model="PCIe-6738",
            data_interface="USB",
            computer_name="Dev2",
            manufacturer=Organization.NATIONAL_INSTRUMENTS,
            name="Dev2",
            channels=[
                DAQChannel(
                    channel_name="3",
                    channel_type="Analog Output",
                    device_name="LAS-08308",
                    sample_rate=10000,
                ),
                DAQChannel(
                    channel_name="5",
                    channel_type="Analog Output",
                    device_name="539251",
                    sample_rate=10000,
                ),
                DAQChannel(
                    channel_name="4",
                    channel_type="Analog Output",
                    device_name="LAS-08309",
                    sample_rate=10000,
                ),
                DAQChannel(
                    channel_name="2",
                    channel_type="Analog Output",
                    device_name="stage-x",
                    sample_rate=10000,
                ),
                DAQChannel(
                    channel_name="0",
                    channel_type="Analog Output",
                    device_name="TL-1",
                    sample_rate=10000,
                ),
                DAQChannel(
                    channel_name="6",
                    channel_type="Analog Output",
                    device_name="LAS-08307",
                    sample_rate=10000,
                ),
            ],
        )
    ],
    scanning_stages=[
        instrument.ScanningStage(
            name="stage-x",
            stage_axis_direction="Detection axis",
            stage_axis_name="X",
            travel=1000,
            model="MS-8000",
            manufacturer=Organization.ASI,
        ),
        instrument.ScanningStage(
            name="stage-y",
            stage_axis_direction="Perpendicular axis",
            stage_axis_name="Y",
            travel=1000,
            model="MS-8000",
            manufacturer=Organization.ASI,
        ),
        instrument.ScanningStage(
            name="stage-z",
            stage_axis_direction="Illumination axis",
            stage_axis_name="Z",
            travel=100,
            model="LS-100",
            manufacturer=Organization.ASI,
        ),
    ],
    additional_devices=[
        instrument.AdditionalImagingDevice(
            imaging_device_type="Tunable lens",
            name="TL-1",
            manufacturer=Organization.OPTOTUNE,
            model="EL-16-40-TC-VIS-20D-C",
            serial_number="01",
        ),
        instrument.AdditionalImagingDevice(
            name="RM-1",
            imaging_device_type="Rotation mount",
            manufacturer=Organization.THORLABS,
            model="K10CR1",
            serial_number="01",
        ),
        instrument.AdditionalImagingDevice(
            name="LC-1",
            imaging_device_type="Laser combiner",
            manufacturer=Organization.OXXIUS,
            model="L6Cc",
            serial_number="L6CC-00513",
        ),
    ],
    optical_tables=[
        instrument.OpticalTable(
            name="Table",
            length=36,
            width=48,
            vibration_control=True,
            model="VIS3648-PG2-325A",
            manufacturer=Organization.MKS_NEWPORT,
        )
    ],
    com_ports=[
        instrument.Com(
            hardware_name="Laser Launch",
            com_port="COM2",
        ),
        instrument.Com(
            hardware_name="ASI Tiger",
            com_port="COM5",
        ),
    ],
    humidity_control=False,
    temperature_control=False,
)
serialized = inst.model_dump_json()
deserialized = instrument.Instrument.model_validate_json(serialized)
deserialized.write_standard_file(prefix="exaspim")
