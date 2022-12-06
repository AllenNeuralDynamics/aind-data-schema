""" example SmartSPIM instrument """
from aind_data_schema.imaging import instrument
import json


inst = instrument.Instrument(
    instrument_id="SmartSPIM02",
    type="smartSPIM",
    manufacturer="LifeCanvas",
    location="440 Westlake",
    objectives=[
        instrument.Objective(
            numerical_aperture=0.2,
            magnification=3.6,
            manufacturer="LifeCanvas",
            immersion="multi",
            notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
            serial_number="Unknown-1",
        ),
        instrument.Objective(
            numerical_aperture=0.12,
            magnification=1.625,
            manufacturer="LifeCanvas",
            immersion="multi",
            notes="Thorlabs TL2X-SAP with LifeCanvas dipping cap and correction optics.",
            serial_number="Unknown-2",
        ),
    ],
    detectors=[
        instrument.Detector(
            type="Camera",
            data_interface="USB",
            cooling="air",
            manufacturer="Hamamatsu",
            model="C14440-20UP",
            serial_number="001284",
        ),
    ],
    light_sources=[
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=445,
            max_power=200,
            filter_wheel_index=0,
            serial_number="VL08223M03",
            manufacturer="Vortran",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=488,
            max_power=150,
            filter_wheel_index=1,
            serial_number="VL08223M03",
            manufacturer="Vortran",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=561,
            max_power=150,
            filter_wheel_index=2,
            serial_number="VL08223M03",
            manufacturer="Vortran",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=594,
            max_power=100,
            filter_wheel_index=3,
            serial_number="VL08223M03",
            manufacturer="Vortran",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=639,
            max_power=160,
            filter_wheel_index=4,
            serial_number="VL08223M03",
            manufacturer="Vortran",
        ),
        instrument.Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=690,
            max_power=160,
            filter_wheel_index=5,
            serial_number="VL08223M03",
            manufacturer="Vortran",
        ),
    ],
    fluorescence_filters=[
        instrument.Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF01-469/35-25",
            filter_wheel_index=0,
            serial_number="Unknown-0",
        ),
        instrument.Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF01-525/45-25",
            filter_wheel_index=1,
            serial_number="Unknown-1",
        ),
        instrument.Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF01-593/40-25",
            filter_wheel_index=2,
            serial_number="Unknown-2",
        ),
        instrument.Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF01-624/40-25",
            filter_wheel_index=3,
            serial_number="Unknown-3",
        ),
        instrument.Filter(
            type="Band pass",
            manufacturer="Chroma",
            diameter=25,
            thickness=2.0,
            model="ET667/30m",
            filter_wheel_index=4,
            serial_number="Unknown-4",
        ),
        instrument.Filter(
            type="Long pass",
            manufacturer="Thorlabs",
            diameter=25,
            thickness=2.0,
            model="FELH0700",
            filter_wheel_index=5,
            serial_number="Unknown-5",
        ),
    ],
    optical_tables=[
        instrument.OpticalTable(
            length=36,
            width=48,
            vibration_control=False,
            model="VIS2424-IG2-125A",
            manufacturer="MKS Newport",
            serial_number="Unknown",
        )
    ],
    com_ports=[
        instrument.Com(hardware_name="Laser Launch", com_port="COM4"),
        instrument.Com(
            hardware_name="ASI Tiger",
            com_port="COM3",
        ),
        instrument.Com(
            hardware_name="MightyZap",
            com_port="COM9",
        ),
    ],
    humidity_control=False,
    temperature_control=False,
)

with open("aind_smartspim_instrument.json", "w") as f:
    f.write(inst.json(indent=3))
