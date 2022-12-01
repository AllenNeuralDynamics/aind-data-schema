""" example SmartSPIM instrument """

from aind_data_schema.imaging.instrument import (
    Instrument,
    Objective,
    Detector,
    Lightsource,
    Com,
    Filter,
    OpticalTable,
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
            serial_number="unknown",
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
            filter_wheel_index=0,
            serial_number="VL01222A11",
            manufacturer="Vortran",
        ),
        Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=561,
            max_power=150,
            filter_wheel_index=1,
            serial_number="417927",
            manufacturer="Coherent Scientific",
        ),
        Lightsource(
            type="laser",
            coupling="SMF",
            wavelength=647,
            max_power=160,
            filter_wheel_index=2,
            serial_number="VL01222A10",
            manufacturer="Vortran",
        ),
    ],
    optical_table=OpticalTable(
        model="VIS2424-IG2-125A",
        length=24,
        width=24,
        vibration_control=False,
        manufacturer="Newport",
        serial_number="Unknown",
    ),
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
            serial_number="Unknown",
        ),
        Filter(
            type="Band pass",
            manufacturer="Semrock",
            diameter=25,
            thickness=2.0,
            model="FF01-600/52-25",
            filter_wheel_index=1,
            serial_number="Unknown",
        ),
        Filter(
            type="Band pass",
            manufacturer="Chroma",
            diameter=25,
            thickness=2.0,
            model="ET690/50m",
            filter_wheel_index=2,
            serial_number="Unknown",
        ),
    ],
)

with open("instrument.json", "w") as f:
    f.write(inst.json(indent=3))
