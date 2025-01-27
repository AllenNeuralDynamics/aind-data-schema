import datetime
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import SizeUnit

from aind_data_schema.components.devices import (
    Filter,
    ImagingInstrumentType,
    Laser,
    MotorizedStage,
    OpticalTable,
    ScanningStage,
)
from aind_data_schema.core.instrument import Com, Detector, Instrument, Objective
from aind_data_schema_models.modalities import Modality

objective_1 = Objective(
    name="TLX Objective 1",
    numerical_aperture=0.2,
    magnification=3.6,
    manufacturer=Organization.LIFECANVAS,
    immersion="multi",
    notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
    serial_number="Unknown-1",
)

objective_2 = Objective(
    name="TLX Objective 2",
    numerical_aperture=0.12,
    magnification=1.625,
    manufacturer=Organization.LIFECANVAS,
    immersion="multi",
    notes="Thorlabs TL2X-SAP with LifeCanvas dipping cap and correction optics.",
    serial_number="Unknown-2",
)

detector_1 = Detector(
    detector_type="Camera",
    data_interface="USB",
    name="Camera 1",
    cooling="Air",
    manufacturer=Organization.HAMAMATSU,
    model="C14440-20UP",
    serial_number="001284",
)

laser_1 = Laser(
    name="Ex_445",
    coupling="Single-mode fiber",
    wavelength=445,
    maximum_power=200,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_2 = Laser(
    name="Ex_488",
    coupling="Single-mode fiber",
    wavelength=488,
    maximum_power=150,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_3 = Laser(
    name="Ex_561",
    coupling="Single-mode fiber",
    wavelength=561,
    maximum_power=150,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_4 = Laser(
    name="Ex_594",
    coupling="Single-mode fiber",
    wavelength=594,
    maximum_power=100,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_5 = Laser(
    name="Ex_639",
    coupling="Single-mode fiber",
    wavelength=639,
    maximum_power=160,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_6 = Laser(
    name="Ex_690",
    coupling="Single-mode fiber",
    wavelength=690,
    maximum_power=160,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

filter_1 = Filter(
    name="Em_469",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    diameter=25,
    thickness=2.0,
    thickness_unit=SizeUnit.MM,
    model="FF01-469/35-25",
    filter_wheel_index=0,
    serial_number="Unknown-0",
)

filter_2 = Filter(
    name="Em_525",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    diameter=25,
    thickness=2.0,
    thickness_unit=SizeUnit.MM,
    model="FF01-525/45-25",
    filter_wheel_index=1,
    serial_number="Unknown-1",
)

filter_3 = Filter(
    name="Em_593",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    diameter=25,
    thickness=2.0,
    thickness_unit=SizeUnit.MM,
    model="FF01-593/40-25",
    filter_wheel_index=2,
    serial_number="Unknown-2",
)

filter_4 = Filter(
    name="Em_624",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    diameter=25,
    thickness=2.0,
    thickness_unit=SizeUnit.MM,
    model="FF01-624/40-25",
    filter_wheel_index=3,
    serial_number="Unknown-3",
)

filter_5 = Filter(
    name="Em_667",
    filter_type="Band pass",
    manufacturer=Organization.CHROMA,
    diameter=25,
    thickness=2.0,
    thickness_unit=SizeUnit.MM,
    model="ET667/30m",
    filter_wheel_index=4,
    serial_number="Unknown-4",
)

filter_6 = Filter(
    name="Em_700",
    filter_type="Long pass",
    manufacturer=Organization.THORLABS,
    diameter=25,
    thickness=2.0,
    thickness_unit=SizeUnit.MM,
    model="FELH0700",
    filter_wheel_index=5,
    serial_number="Unknown-5",
)

motorized_stage_1 = MotorizedStage(
    model="LS-100",
    manufacturer=Organization.ASI,
    serial_number="Unknown-1",
    travel=100,
    name="Focus stage",
)

motorized_stage_2 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    serial_number="Unknown-5",
    travel=41,
    name="Cylindrical lens #1",
)

motorized_stage_3 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    serial_number="Unknown-6",
    travel=41,
    name="Cylindrical lens #2",
)

motorized_stage_4 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    serial_number="Unknown-7",
    travel=41,
    name="Cylindrical lens #3",
)

motorized_stage_5 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    serial_number="Unknown-8",
    travel=41,
    name="Cylindrical lens #4",
)

scanning_stage_1 = ScanningStage(
    model="LS-50",
    manufacturer=Organization.ASI,
    serial_number="Unknown-2",
    stage_axis_direction="Detection axis",
    stage_axis_name="Z",
    travel=50,
    name="Sample stage Z",
)

scanning_stage_2 = ScanningStage(
    model="LS-50",
    manufacturer=Organization.ASI,
    serial_number="Unknown-3",
    stage_axis_direction="Illumination axis",
    stage_axis_name="X",
    travel=50,
    name="Sample stage X",
)

scanning_stage_3 = ScanningStage(
    model="LS-50",
    manufacturer=Organization.ASI,
    serial_number="Unknown-4",
    stage_axis_direction="Perpendicular axis",
    stage_axis_name="Y",
    travel=50,
    name="Sample stage Y",
)

optical_table_1 = OpticalTable(
    name="Main optical table",
    length=36,
    width=48,
    vibration_control=False,
    model="VIS2424-IG2-125A",
    manufacturer=Organization.MKS_NEWPORT,
    serial_number="Unknown",
)

objectives = [objective_1, objective_2]
detectors = [detector_1]
lasers = [laser_1, laser_2, laser_3, laser_4, laser_5, laser_6]
fluorescence_filters = [filter_1, filter_2, filter_3, filter_4, filter_5, filter_6]
motorized_stages = [motorized_stage_1, motorized_stage_2, motorized_stage_3, motorized_stage_4, motorized_stage_5]
scanning_stages = [scanning_stage_1, scanning_stage_2, scanning_stage_3]
optical_tables = [optical_table_1]

inst = Instrument(
    instrument_id="440_SmartSPIM1_20231004",
    instrument_type=ImagingInstrumentType.SMARTSPIM,
    manufacturer=Organization.LIFECANVAS,
    modification_date=datetime.date(2023, 10, 4),
    modalities=[Modality.SPIM],
    components=[
        *objectives,
        *detectors,
        *lasers,
        *fluorescence_filters,
        *motorized_stages,
        *scanning_stages,
        *optical_tables,
    ],
    com_ports=[
        Com(hardware_name="Laser Launch", com_port="COM4"),
        Com(
            hardware_name="ASI Tiger",
            com_port="COM3",
        ),
        Com(
            hardware_name="MightyZap",
            com_port="COM9",
        ),
    ],
    temperature_control=False,
)
