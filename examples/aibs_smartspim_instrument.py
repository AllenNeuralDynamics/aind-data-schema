""" example SmartSPIM instrument """
import datetime

from aind_data_schema.device import (
    Detector,
    Filter,
    Laser,
    MotorizedStage,
    Objective,
)
from aind_data_schema.imaging.instrument import (
    AdditionalImagingDevice,
    Com,
    Instrument,
    OpticalTable,
    ScanningStage,
)
from aind_data_schema.manufacturers import Manufacturer

inst = Instrument(
    instrument_id="SmartSPIM2-2",
    modification_date=datetime.date(2023, 10, 4),
    instrument_type="SmartSPIM",
    manufacturer=Manufacturer.LIFECANVAS,
    objectives=[
        Objective(
            numerical_aperture=0.2,
            magnification=3.6,
            immersion="multi",
            manufacturer=Manufacturer.THORLABS,
            model="TL4X-SAP",
            serial_number="Unknown",
            notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
        ),
    ],
    detectors=[
        Detector(
            detector_type="Camera",
            data_interface="USB",
            cooling="air",
            manufacturer=Manufacturer.HAMAMATSU,
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
            manufacturer=Manufacturer.VORTRAN,
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
            manufacturer=Manufacturer.COHERENT_SCIENTIFIC,
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
            manufacturer=Manufacturer.VORTRAN,
            model="Stradus",
            notes="All lasers controlled via Vortran VersaLase System",
        ),
    ],
    motorized_stages=[
        MotorizedStage(
            model="LS-100",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown-0",
            travel=100,
            notes="Focus stage",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer=Manufacturer.MIGHTY_ZAP,
            serial_number="Unknown-1",
            travel=41,
            notes="Cylindrical lens #1",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer=Manufacturer.MIGHTY_ZAP,
            serial_number="Unknown-2",
            travel=41,
            notes="Cylindrical lens #2",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer=Manufacturer.MIGHTY_ZAP,
            serial_number="Unknown-3",
            travel=41,
            notes="Cylindrical lens #3",
        ),
        MotorizedStage(
            model="L12-20F-4",
            manufacturer=Manufacturer.MIGHTY_ZAP,
            serial_number="Unknown-4",
            travel=41,
            notes="Cylindrical lens #4",
        ),
    ],
    scanning_stages=[
        ScanningStage(
            model="LS-50",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown-0",
            stage_axis_direction="Detection axis",
            stage_axis_name="Z",
            travel=50,
            notes="Sample stage Z",
        ),
        ScanningStage(
            model="LS-50",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown-1",
            stage_axis_direction="Illumination axis",
            stage_axis_name="X",
            travel=50,
            notes="Sample stage X",
        ),
        ScanningStage(
            model="LS-50",
            manufacturer=Manufacturer.ASI,
            serial_number="Unknown-2",
            stage_axis_direction="Perpendicular axis",
            stage_axis_name="Y",
            travel=50,
            notes="Sample stage Y",
        ),
    ],
    optical_tables=[
        OpticalTable(
            model="CleanTop",  # model="VIS2424-IG2-125A", # ~3 months
            length=35,  # length=24,
            width=29,  # width=24,
            vibration_control=True,
            manufacturer=Manufacturer.TMC,
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
            name="Em_525",
            filter_type="Band pass",
            manufacturer=Manufacturer.SEMROCK,
            diameter=25,
            thickness=2.0,
            model="FF03-525/50-25",
            filter_wheel_index=0,
            serial_number="Unknown-1",
        ),
        Filter(
            name="Em_600",
            filter_type="Band pass",
            manufacturer=Manufacturer.SEMROCK,
            diameter=25,
            thickness=2.0,
            model="FF01-600/52-25",
            filter_wheel_index=1,
            serial_number="Unknown-2",
        ),
        Filter(
            name="Em_690",
            filter_type="Band pass",
            manufacturer=Manufacturer.CHROMA,
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
            manufacturer=Manufacturer.OPTOTUNE,
            model="EL-16-40-TC",
            serial_number="Unknown-1",
        ),
        AdditionalImagingDevice(
            type="Other",
            manufacturer=Manufacturer.OPTOTUNE,
            model="EL-16-40-TC",
            serial_number="Unknown-2",
        ),
        AdditionalImagingDevice(
            type="Sample Chamber",
            manufacturer=Manufacturer.LIFECANVAS,
            model="Large-uncoated-glass",
            serial_number="Unknown-1",
        ),
    ],
)

inst.write_standard_file(prefix="aibs_smartspim")
