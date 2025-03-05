""" example ExaSPIM instrument """

import datetime

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import SizeUnit, FrequencyUnit

from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    DAQChannel,
    DAQDevice,
    Detector,
    Filter,
    Laser,
    Objective,
    OpticalTable,
    ScanningStage,
)
from aind_data_schema.core.instrument import Instrument, Com
from aind_data_schema_models.modalities import Modality

objectives = [
    Objective(
        name="Custom Objective",
        numerical_aperture=0.305,
        magnification=5,
        immersion="air",
        manufacturer=Organization.OTHER,
        model="JM_DIAMOND 5.0X/1.3",
        notes="manufacturer collaboration between Schneider-Kreuznach and Vieworks",
    ),
]

detectors = [
    Detector(
        name="Camera 1",
        detector_type="Camera",
        data_interface="Coax",
        cooling="Air",
        manufacturer=Organization.VIEWORKS,
        model="VNP-604MX",
        serial_number="MB151BAY001",
    ),
]

lasers = [
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
]

fluorescence_filters = [
    Filter(
        name="Multiband filter",
        filter_type="Multiband",
        manufacturer=Organization.CHROMA,
        diameter=44.05,
        thickness=1,
        thickness_unit=SizeUnit.MM,
        model="ZET405/488/561/640mv2",
        notes="Custom made filter",
        filter_wheel_index=0,
    )
]

daqs = [
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
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="5",
                channel_type="Analog Output",
                device_name="539251",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="4",
                channel_type="Analog Output",
                device_name="LAS-08309",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="2",
                channel_type="Analog Output",
                device_name="stage-x",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="0",
                channel_type="Analog Output",
                device_name="TL-1",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="6",
                channel_type="Analog Output",
                device_name="LAS-08307",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
        ],
    )
]

scanning_stages = [
    ScanningStage(
        name="stage-x",
        stage_axis_direction="Detection axis",
        stage_axis_name="X",
        travel=1000,
        model="MS-8000",
        manufacturer=Organization.ASI,
    ),
    ScanningStage(
        name="stage-y",
        stage_axis_direction="Perpendicular axis",
        stage_axis_name="Y",
        travel=1000,
        model="MS-8000",
        manufacturer=Organization.ASI,
    ),
    ScanningStage(
        name="stage-z",
        stage_axis_direction="Illumination axis",
        stage_axis_name="Z",
        travel=100,
        model="LS-100",
        manufacturer=Organization.ASI,
    ),
]

additional_devices = [
    AdditionalImagingDevice(
        imaging_device_type="Tunable lens",
        name="TL-1",
        manufacturer=Organization.OPTOTUNE,
        model="EL-16-40-TC-VIS-20D-C",
        serial_number="01",
    ),
    AdditionalImagingDevice(
        name="RM-1",
        imaging_device_type="Rotation mount",
        manufacturer=Organization.THORLABS,
        model="K10CR1",
        serial_number="01",
    ),
    AdditionalImagingDevice(
        name="LC-1",
        imaging_device_type="Laser combiner",
        manufacturer=Organization.OXXIUS,
        model="L6Cc",
        serial_number="L6CC-00513",
    ),
]

optical_tables = [
    OpticalTable(
        name="Table",
        length=36,
        width=48,
        vibration_control=True,
        model="VIS3648-PG2-325A",
        manufacturer=Organization.MKS_NEWPORT,
    )
]

inst = Instrument(
    instrument_id="440_exaSPIM1_20231004",
    modalities=[Modality.SPIM],
    instrument_type="exaSPIM",
    modification_date=datetime.date(2023, 10, 4),
    manufacturer=Organization.CUSTOM,
    components=[
        *objectives,
        *detectors,
        *lasers,
        *fluorescence_filters,
        *daqs,
        *scanning_stages,
        *additional_devices,
        *optical_tables,
    ],
    com_ports=[
        Com(
            hardware_name="Laser Launch",
            com_port="COM2",
        ),
        Com(
            hardware_name="ASI Tiger",
            com_port="COM5",
        ),
    ],
    temperature_control=False,
)

serialized = inst.model_dump_json()
deserialized = Instrument.model_validate_json(serialized)
deserialized.write_standard_file(prefix="exaspim")
