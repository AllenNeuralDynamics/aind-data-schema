""" example ExaSPIM instrument """
from aind_data_schema.device import DaqChannel
from aind_data_schema.imaging import instrument

inst = instrument.Instrument(
    instrument_id="exaSPIM1-1",
    type="exaSPIM",
    manufacturer="Custom",
    location="440 Westlake",
    objectives=[
        instrument.Objective(
            numerical_aperture=0.305,
            magnification=5.0,
            immersion="air",
            manufacturer="Other",
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
            manufacturer="Vieworks",
            model="VNP-604MX",
            serial_number="MB151BAY001",
        ),
    ],
    light_sources=[
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=405,
            max_power=200,
            serial_number="LAS-08307",
            manufacturer="Oxxius",
            notes="Housed in commercial laser combiner",
            daq_channel=DaqChannel(index=6, type="Analog Output"),
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=488,
            max_power=200,
            serial_number="LAS-08308",
            manufacturer="Oxxius",
            notes="Housed in commercial laser combiner",
            daq_channel=DaqChannel(index=3, type="Analog Output"),
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=561,
            max_power=200,
            serial_number="539251",
            manufacturer="Oxxius",
            notes="Housed in commercial laser combiner",
            daq_channel=DaqChannel(index=5, type="Analog Output"),
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=638,
            max_power=200,
            serial_number="LAS-08309",
            manufacturer="Oxxius",
            notes="Housed in commercial laser combiner",
            daq_channel=DaqChannel(index=4, type="Analog Output"),
        ),
    ],
    fluorescence_filters=[
        instrument.Filter(
            type="Multiband",
            manufacturer="Chroma",
            diameter=44.05,
            thickness=1.0,
            model="ZET405/488/561/640mv2",
            notes="Custom made filter",
            filter_wheel_index=0,
            serial_number="Unknown-0",
        )
    ],
    daqs=[
        instrument.DAQ(
            model="PCIe-6738",
            manufacturer="National Instruments",
            device_name="Dev2",
            update_frequency="10000",
            number_active_channels=7,
            serial_number="Unknown",
        )
    ],
    scanning_stages=[
        instrument.ScanningStage(
            stage_axis_direction="Detection axis",
            stage_axis_name="X",
            travel=1000,
            model="MS-8000",
            manufacturer="Applied Scientific Instrumentation",
            daq_channel=DaqChannel(index=2, type="Analog Output"),
            serial_number="Unknown",
        ),
        instrument.ScanningStage(
            stage_axis_direction="Perpendicular axis",
            stage_axis_name="Y",
            travel=1000,
            model="MS-8000",
            manufacturer="Applied Scientific Instrumentation",
            serial_number="Unknown",
        ),
        instrument.ScanningStage(
            stage_axis_direction="Illumination axis",
            stage_axis_name="Z",
            travel=100,
            model="LS-100",
            manufacturer="Applied Scientific Instrumentation",
            serial_number="Unknown",
        ),
    ],
    additional_devices=[
        instrument.AdditionalImagingDevice(
            type="Tunable lens",
            manufacturer="Optotune",
            model="EL-16-40-TC-VIS-20D-C",
            serial_number="01",
            daq_channel=DaqChannel(index=0, type="Analog Output"),
        ),
        instrument.AdditionalImagingDevice(
            type="Rotation mount",
            manufacturer="Thorlabs",
            model="K10CR1",
            serial_number="01",
        ),
        instrument.AdditionalImagingDevice(
            type="Laser combiner",
            manufacturer="Oxxius",
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
            manufacturer="MKS Newport",
            serial_number="Unknown",
        )
    ],
    com_ports=[
        instrument.Com(hardware_name="Laser Launch", com_port="COM2",),
        instrument.Com(hardware_name="ASI Tiger", com_port="COM5",),
    ],
    humidity_control=False,
    temperature_control=False,
)

inst.write_standard_file(prefix="exaspim")
