""" example SmartSPIM instrument """

from datetime import date

from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.devices import (
    Filter,
    Laser,
    MotorizedStage,
    ScanningStage,
    Device,
)
from aind_data_schema.components.connections import Connection
from aind_data_schema.core.instrument import (
    Detector,
    Instrument,
    Objective,
    Microscope,
)
from aind_data_schema_models.modalities import Modality
from aind_data_schema.components.coordinates import CoordinateSystemLibrary

objective_1 = Objective(
    name="TLX Objective 1",
    numerical_aperture=0.2,
    magnification=3.6,
    manufacturer=Organization.LIFECANVAS,
    immersion="multi",
    notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
)

objective_2 = Objective(
    name="TLX Objective 2",
    numerical_aperture=0.12,
    magnification=1.625,
    manufacturer=Organization.LIFECANVAS,
    immersion="multi",
    notes="Thorlabs TL2X-SAP with LifeCanvas dipping cap and correction optics.",
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
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_2 = Laser(
    name="Ex_488",
    coupling="Single-mode fiber",
    wavelength=488,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_3 = Laser(
    name="Ex_561",
    coupling="Single-mode fiber",
    wavelength=561,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_4 = Laser(
    name="Ex_594",
    coupling="Single-mode fiber",
    wavelength=594,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_5 = Laser(
    name="Ex_639",
    coupling="Single-mode fiber",
    wavelength=639,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

laser_6 = Laser(
    name="Ex_690",
    coupling="Single-mode fiber",
    wavelength=690,
    serial_number="VL08223M03",
    manufacturer=Organization.VORTRAN,
)

filter_1 = Filter(
    name="Em_469",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    model="FF01-469/35-25",
)

filter_2 = Filter(
    name="Em_525",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    model="FF01-525/45-25",
)

filter_3 = Filter(
    name="Em_593",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    model="FF01-593/40-25",
)

filter_4 = Filter(
    name="Em_624",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    model="FF01-624/40-25",
)

filter_5 = Filter(
    name="Em_667",
    filter_type="Band pass",
    manufacturer=Organization.CHROMA,
    model="ET667/30m",
)

filter_6 = Filter(
    name="Em_700",
    filter_type="Long pass",
    manufacturer=Organization.THORLABS,
    model="FELH0700",
)

motorized_stage_1 = MotorizedStage(
    model="LS-100",
    manufacturer=Organization.ASI,
    travel=100,
    name="Focus stage",
)

motorized_stage_2 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
    name="Cylindrical lens #1",
)

motorized_stage_3 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
    name="Cylindrical lens #2",
)

motorized_stage_4 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
    name="Cylindrical lens #3",
)

motorized_stage_5 = MotorizedStage(
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
    name="Cylindrical lens #4",
)

scanning_stage_1 = ScanningStage(
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Detection axis",
    stage_axis_name="Z",
    travel=50,
    name="Sample stage Z",
)

scanning_stage_2 = ScanningStage(
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Illumination axis",
    stage_axis_name="X",
    travel=50,
    name="Sample stage X",
)

scanning_stage_3 = ScanningStage(
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Perpendicular axis",
    stage_axis_name="Y",
    travel=50,
    name="Sample stage Y",
)

laser_launch = Device(
    name="Laser Launch",
)

asi_tiger = Device(
    name="ASI Tiger",
)
mighty_zap = Device(
    name="MightyZap",
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
        source_device="COM Device",
        source_port="COM9",
        target_device="MightyZap",
    ),
]

objectives = [objective_1, objective_2]
detectors = [detector_1]
lasers = [laser_1, laser_2, laser_3, laser_4, laser_5, laser_6]
fluorescence_filters = [filter_1, filter_2, filter_3, filter_4, filter_5, filter_6]
motorized_stages = [motorized_stage_1, motorized_stage_2, motorized_stage_3, motorized_stage_4, motorized_stage_5]
scanning_stages = [scanning_stage_1, scanning_stage_2, scanning_stage_3]

scope = Microscope(
    name="Microscope",
    manufacturer=Organization.LIFECANVAS,
)

inst = Instrument(
    location="440",
    instrument_id="SmartSPIM1",
    modification_date=date(2023, 10, 4),
    coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
    modalities=[Modality.SPIM],
    components=[
        scope,
        *objectives,
        *detectors,
        *lasers,
        *fluorescence_filters,
        *motorized_stages,
        *scanning_stages,
        laser_launch,
        asi_tiger,
        mighty_zap,
        com_device,
    ],
    connections=connections,
    temperature_control=False,
)

if __name__ == "__main__":
    serialized = inst.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="aind_smartspim")
