""" example SmartSPIM instrument """

import datetime

from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    Detector,
    Filter,
    Laser,
    MotorizedStage,
    Objective,
    OpticalTable,
    ScanningStage,
)
from aind_data_schema.core.instrument import Com, Instrument

inst = Instrument(
    instrument_id="440_SmartSPIM2_20231004",
    modification_date=datetime.date(2023, 10, 4),
    instrument_type="SmartSPIM",
    manufacturer=Organization.LIFECANVAS,
    objectives=[
        Objective(
            name="TLX Objective",
            numerical_aperture=0.2,
            magnification=3.6,
            immersion="multi",
            manufacturer=Organization.THORLABS,
            model="TL4X-SAP",
            notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
        ),
    ],
    detectors=[
        Detector(
            name="Camera 1",
            detector_type="Camera",
            data_interface="USB",
            cooling="Air",
            manufacturer=Organization.HAMAMATSU,
            model="C14440-20UP",
            serial_number="001107",
        ),
    ],
    light_sources=[
        Laser(
            name="Ex_488",
            device_type="Laser",
            coupling="Single-mode fiber",
            wavelength=488,
            maximum_power=150,
            serial_number="VL01222A11",
            manufacturer=Organization.VORTRAN,
            model="Stradus",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
        Laser(
            name="Ex_561",
            device_type="Laser",
            coupling="Single-mode fiber",
            wavelength=561,
            maximum_power=150,
            serial_number="417927",
            manufacturer=Organization.COHERENT_SCIENTIFIC,
            model="Obis",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
        Laser(
            name="Ex_647",
            device_type="Laser",
            coupling="Single-mode fiber",
            wavelength=647,
            maximum_power=160,
            serial_number="VL01222A10",
            manufacturer=Organization.VORTRAN,
            model="Stradus",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
    ],
    motorized_stages=[
        MotorizedStage(
            name="Focus stage",
            model="LS-100",
            manufacturer=Organization.ASI,
            travel=100,
        ),
        MotorizedStage(
            name="Cylindrical lens #1",
            model="L12-20F-4",
            manufacturer=Organization.IR_ROBOT_CO,
            travel=41,
        ),
        MotorizedStage(
            name="Cylindrical lens #2",
            model="L12-20F-4",
            manufacturer=Organization.IR_ROBOT_CO,
            travel=41,
        ),
        MotorizedStage(
            name="Cylindrical lens #3",
            model="L12-20F-4",
            manufacturer=Organization.IR_ROBOT_CO,
            travel=41,
        ),
        MotorizedStage(
            name="Cylindrical lens #4",
            model="L12-20F-4",
            manufacturer=Organization.IR_ROBOT_CO,
            travel=41,
        ),
    ],
    scanning_stages=[
        ScanningStage(
            name="Sample stage Z",
            model="LS-50",
            manufacturer=Organization.ASI,
            stage_axis_direction="Detection axis",
            stage_axis_name="Z",
            travel=50,
        ),
        ScanningStage(
            name="Sample stage X",
            model="LS-50",
            manufacturer=Organization.ASI,
            stage_axis_direction="Illumination axis",
            stage_axis_name="X",
            travel=50,
        ),
        ScanningStage(
            name="Sample stage Y",
            model="LS-50",
            manufacturer=Organization.ASI,
            stage_axis_direction="Perpendicular axis",
            stage_axis_name="Y",
            travel=50,
        ),
    ],
    optical_tables=[
        OpticalTable(
            name="Table",
            model="CleanTop",  # model="VIS2424-IG2-125A", # ~3 months
            length=35,  # length=24,
            width=29,  # width=24,
            vibration_control=True,
            manufacturer=Organization.TMC,
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
            name="Em_525",
            filter_type="Band pass",
            manufacturer=Organization.SEMROCK,
            diameter=25,
            thickness=2.0,
            model="FF03-525/50-25",
            filter_wheel_index=0,
        ),
        Filter(
            name="Em_600",
            filter_type="Band pass",
            manufacturer=Organization.SEMROCK,
            diameter=25,
            thickness=2.0,
            model="FF01-600/52-25",
            filter_wheel_index=1,
        ),
        Filter(
            name="Em_690",
            filter_type="Band pass",
            manufacturer=Organization.CHROMA,
            diameter=25,
            thickness=2.0,
            model="ET690/50m",
            filter_wheel_index=2,
        ),
    ],
    additional_devices=[
        AdditionalImagingDevice(
            name="Lens 1",
            imaging_device_type="Tunable lens",
            manufacturer=Organization.OPTOTUNE,
            model="EL-16-40-TC",
        ),
        AdditionalImagingDevice(
            name="Lens 2",
            imaging_device_type="Tunable lens",
            manufacturer=Organization.OPTOTUNE,
            model="EL-16-40-TC",
        ),
        AdditionalImagingDevice(
            name="Sample chamber",
            imaging_device_type="Sample Chamber",
            manufacturer=Organization.LIFECANVAS,
            model="Large-uncoated-glass",
        ),
    ],
)
serialized = inst.model_dump_json()
deserialized = Instrument.model_validate_json(serialized)
deserialized.write_standard_file(prefix="aibs_smartspim")
