""" example SmartSPIM instrument """

from aind_data_schema.imaging.instrument import (
    Instrument,
    Objective,
    Detector,
    Lightsource,
    MotorizedStage,
    ScanningStage,
    Com,
    Filter,
    OpticalTable,
    AdditionalImagingDevice,
)

inst = Instrument(
    instrument_id="SmartSPIM01",
    type="smartSPIM",
    manufacturer="LifeCanvas",
    location="440 Westlake",
    objectives=[
        Objective(
            numerical_aperture=0.2,
            magnification=3.6,
            immersion="multi",
            manufacturer="Thorlabs",
            model="TL4X-SAP",
            serial_number="Unknown",
            notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
        ),
    ],
    detectors=[
        Detector(
            type="Camera",
            data_interface="USB",
            cooling="air",
            manufacturer="Hamamatsu",
            model="C14440-20UP",
            serial_number="001107",
        ),
    ],
    light_sources=[
        Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=488,
            max_power=150,
            serial_number="VL01222A11",
            manufacturer="Vortran",
            model="Stradus",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
        Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=561,
            max_power=150,
            serial_number="417927",
            manufacturer="Coherent Scientific",
            model="Obis",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
        Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=647,
            max_power=160,
            serial_number="VL01222A10",
            manufacturer="Vortran",
            model="Stradus",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
    ],
    motorized_stages=[
        MotorizedStage(
            model="LS-100",
            manufacturer="Applied Scientific Instrumentation",
            serial_number="Unknown-1",
            travel=100,
            notes="Focus stage",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer="IR Robot Co",
            serial_number="Unknown-5",
            travel=41,
            notes="Cylindrical lens #1",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer="IR Robot Co",
            serial_number="Unknown-6",
            travel=41,
            notes="Cylindrical lens #2",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer="IR Robot Co",
            serial_number="Unknown-7",
            travel=41,
            notes="Cylindrical lens #3",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer="IR Robot Co",
            serial_number="Unknown-8",
            travel=41,
            notes="Cylindrical lens #4",
        ),
    ],
    scanning_stages=[
        ScanningStage(
            model="LS-50",
            manufacturer="Applied Scientific Instrumentation",
            serial_number="Unknown-2",
            stage_axis_direction="Detection axis",
            stage_axis_name="Z",
            travel=50,
            notes="Sample stage Z",
        ),
        ScanningStage(
            model="LS-50",
            manufacturer="Applied Scientific Instrumentation",
            serial_number="Unknown-3",
            stage_axis_direction="Illumination axis",
            stage_axis_name="X",
            travel=50,
            notes="Sample stage X",
        ),
        ScanningStage(
            model="LS-50",
            manufacturer="Applied Scientific Instrumentation",
            serial_number="Unknown-4",
            stage_axis_direction="Perpendicular axis",
            stage_axis_name="Y",
            travel=50,
            notes="Sample stage Y",
        ),
    ],
    optical_tables=[
        OpticalTable(
            model="VIS2424-IG2-125A",
            length=24,
            width=24,
            vibration_control=False,
            manufacturer="MKS Newport",
            serial_number="Unknown",
        )
    ],
    humidity_control=False,
    temperature_control=False,
    com_ports=[
        Com(
            hardware_name="Laser Launch",
            com_port="COM3",
        ),
        Com(
            hardware_name="ASI Tiger",
            com_port="COM5",
        ),
        Com(hardware_name="MightyZap", com_port="COM4"),
    ],
    fluorescence_filters=[
        Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF03-525/50-25",
            filter_wheel_index=0,
            serial_number="Unknown-1",
        ),
        Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF01-600/52-25",
            filter_wheel_index=1,
            serial_number="Unknown-2",
        ),
        Filter(
            type="Band pass",
            manufacturer="Chroma",
            diameter=25,
            thickness=2.0,
            model="ET690/50m",
            filter_wheel_index=2,
            serial_number="Unknown-3",
        ),
    ],
    additional_devices=[
        AdditionalImagingDevice(
            type="Other",
            manufacturer="Optotune",
            model="EL-16-40-TC",
            serial_number="Unknown-1",
        ),
        AdditionalImagingDevice(
            type="Other",
            manufacturer="Optotune",
            model="EL-16-40-TC",
            serial_number="Unknown-2",
        ),
    ],
)

with open("aibs_smartspim_instrument.json", "w") as f:
    f.write(inst.json(indent=3))
