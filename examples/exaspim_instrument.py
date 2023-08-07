""" example ExaSPIM instrument """
from aind_data_schema.device import DAQChannel, DAQDevice, Manufacturer
from aind_data_schema.imaging import instrument

inst = instrument.Instrument(
    instrument_id="exaSPIM1-1",
    instrument_type="exaSPIM",
    manufacturer=Manufacturer.CUSTOM,
    objectives=[
        instrument.Objective(
            numerical_aperture=0.305,
            magnification=5,
            immersion="air",
            manufacturer=Manufacturer.OTHER,
            model="JM_DIAMOND 5.0X/1.3",
            serial_number="Unknown",
            notes="manufacturer collaboration between Schneider-Kreuznach and Vieworks",
        ),
    ],
    detectors=[
        instrument.Detector(
            type="Camera",
            data_interface="Coax",
            cooling="air",
            manufacturer=Manufacturer.VIEWORKS,
            model="VNP-604MX",
            serial_number="MB151BAY001",
        ),
    ],
    light_sources=[
        instrument.Lightsource(
            type="laser",
            coupling="Single-mode fiber",
            wavelength=405,
            max_power=200,
            serial_number="LAS-08307",
            manufacturer=Manufacturer.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="Single-mode fiber",
            wavelength=488,
            max_power=200,
            serial_number="LAS-08308",
            manufacturer=Manufacturer.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="Single-mode fiber",
            wavelength=561,
            max_power=200,
            serial_number="539251",
            manufacturer=Manufacturer.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="Single-mode fiber",
            wavelength=638,
            max_power=200,
            serial_number="LAS-08309",
            manufacturer=Manufacturer.OXXIUS,
            notes="Housed in commercial laser combiner",
        ),
    ],
    fluorescence_filters=[
        instrument.Filter(
            filter_type="Multiband",
            manufacturer=Manufacturer.CHROMA,
            diameter=44.05,
            thickness=1,
            model="ZET405/488/561/640mv2",
            notes="Custom made filter",
            filter_wheel_index=0,
            serial_number="Unknown-0",
        )
    ],
    daqs=[
        DAQDevice(
            model="PCIe-6738",
            data_interface="USB",
            computer_name="Dev2",
            manufacturer=Manufacturer.NATIONAL_INSTRUMENTS,
            name="Dev2",
            serial_number="Unknown",
            channels=[
                DAQChannel(channel_name="3", channel_type="Analog Output", device_name="LAS-08308", sample_rate=10000),
                DAQChannel(channel_name="5", channel_type="Analog Output", device_name="539251", sample_rate=10000),
                DAQChannel(channel_name="4", channel_type="Analog Output", device_name="LAS-08309", sample_rate=10000),
                DAQChannel(channel_name="2", channel_type="Analog Output", device_name="stage-x", sample_rate=10000),
                DAQChannel(channel_name="0", channel_type="Analog Output", device_name="TL-1", sample_rate=10000),
                DAQChannel(channel_name="6", channel_type="Analog Output", device_name="LAS-08307", sample_rate=10000),
            ],
        )
    ],
    scanning_stages=[
        instrument.ScanningStage(
            stage_axis_direction="Detection axis",
            stage_axis_name="X",
            travel=1000,
            model="MS-8000",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown",
        ),
        instrument.ScanningStage(
            stage_axis_direction="Perpendicular axis",
            stage_axis_name="Y",
            travel=1000,
            model="MS-8000",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown",
        ),
        instrument.ScanningStage(
            stage_axis_direction="Illumination axis",
            stage_axis_name="Z",
            travel=100,
            model="LS-100",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown",
        ),
    ],
    additional_devices=[
        instrument.AdditionalImagingDevice(
            type="Tunable lens",
            manufacturer=Manufacturer.OPTOTUNE,
            model="EL-16-40-TC-VIS-20D-C",
            serial_number="01",
        ),
        instrument.AdditionalImagingDevice(
            type="Rotation mount",
            manufacturer=Manufacturer.THORLABS,
            model="K10CR1",
            serial_number="01",
        ),
        instrument.AdditionalImagingDevice(
            type="Laser combiner",
            manufacturer=Manufacturer.OXXIUS,
            model="L6Cc",
            serial_number="L6CC-00513",
        ),
    ],
    optical_tables=[
        instrument.OpticalTable(
            length=36,
            width=48,
            vibration_control=True,
            model="VIS3648-PG2-325A",
            manufacturer=Manufacturer.MKS_NEWPORT,
            serial_number="Unknown",
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

inst.write_standard_file(prefix="exaspim")
