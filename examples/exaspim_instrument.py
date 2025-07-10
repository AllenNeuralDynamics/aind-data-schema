""" example ExaSPIM instrument """

import datetime

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit

from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    DAQChannel,
    DAQDevice,
    Detector,
    Filter,
    Laser,
    Objective,
    ScanningStage,
    Device,
    Computer,
    Microscope,
)
from aind_data_schema.components.connections import Connection
from aind_data_schema.core.instrument import Instrument
from aind_data_schema_models.modalities import Modality
from aind_data_schema.components.coordinates import CoordinateSystemLibrary

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
        serial_number="LAS-08307",
        manufacturer=Organization.OXXIUS,
        notes="Housed in commercial laser combiner",
    ),
    Laser(
        name="LAS-08308",
        coupling="Single-mode fiber",
        wavelength=488,
        serial_number="LAS-08308",
        manufacturer=Organization.OXXIUS,
        notes="Housed in commercial laser combiner",
    ),
    Laser(
        name="539251",
        coupling="Single-mode fiber",
        wavelength=561,
        serial_number="539251",
        manufacturer=Organization.OXXIUS,
        notes="Housed in commercial laser combiner",
    ),
    Laser(
        name="LAS-08309",
        coupling="Single-mode fiber",
        wavelength=638,
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
        model="ZET405/488/561/640mv2",
        center_wavelength=[405, 488, 561, 640],
        notes="Custom made filter",
    )
]

computer = Computer(
    name="Dev2-PC",
)

daqs = [
    DAQDevice(
        model="PCIe-6738",
        data_interface="USB",
        manufacturer=Organization.NATIONAL_INSTRUMENTS,
        name="Dev2",
        channels=[
            DAQChannel(
                channel_name="3",
                channel_type="Analog Output",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="5",
                channel_type="Analog Output",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="4",
                channel_type="Analog Output",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="2",
                channel_type="Analog Output",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="0",
                channel_type="Analog Output",
                sample_rate=10000,
                sample_rate_unit=FrequencyUnit.HZ,
            ),
            DAQChannel(
                channel_name="6",
                channel_type="Analog Output",
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

laser_launch = Device(
    name="Laser Launch",
)

asi_tiger = Device(
    name="ASI Tiger",
)

com_device = Device(
    name="COM Device",
)

connections = [
    Connection(
        source_device="COM Device",
        source_port="COM4",
        target_device="Laser Launch",
    ),
    Connection(
        source_device="COM Device",
        source_port="COM3",
        target_device="ASI Tiger",
    ),
    Connection(
        source_device="Dev2",
        source_port="3",
        target_device="LAS-08308",
    ),
    Connection(
        source_device="Dev2",
        source_port="5",
        target_device="539251",
    ),
    Connection(
        source_device="Dev2",
        source_port="4",
        target_device="LAS-08309",
    ),
    Connection(
        source_device="Dev2",
        source_port="2",
        target_device="stage-x",
    ),
    Connection(
        source_device="Dev2",
        source_port="0",
        target_device="TL-1",
    ),
    Connection(
        source_device="Dev2",
        source_port="6",
        target_device="LAS-08307",
    ),
    Connection(
        source_device="Dev2",
        target_device="Dev2-PC",
    ),
]

scope = Microscope(
    name="Microscope",
    manufacturer=Organization.CUSTOM,
)

inst = Instrument(
    location="440",
    instrument_id="exaSPIM1",
    modalities=[Modality.SPIM],
    modification_date=datetime.date(2023, 10, 4),
    coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
    components=[
        *objectives,
        *detectors,
        *lasers,
        *fluorescence_filters,
        *daqs,
        *scanning_stages,
        *additional_devices,
        com_device,
        laser_launch,
        asi_tiger,
        computer,
        scope,
    ],
    connections=connections,
    temperature_control=False,
)

if __name__ == "__main__":
    serialized = inst.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="exaspim")
