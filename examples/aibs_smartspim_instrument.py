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
    ScanningStage,
    Device,
)
from aind_data_schema_models.modalities import Modality
from aind_data_schema.core.instrument import Instrument, Connection, ConnectionData, ConnectionDirection
from aind_data_schema.components.coordinates import (
    CoordinateSystemLibrary,
)

objective = Objective(
    name="TLX Objective",
    numerical_aperture=0.2,
    magnification=3.6,
    immersion="multi",
    manufacturer=Organization.THORLABS,
    model="TL4X-SAP",
    notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
)
camera1 = Detector(
    name="Camera 1",
    detector_type="Camera",
    data_interface="USB",
    cooling="Air",
    manufacturer=Organization.HAMAMATSU,
    model="C14440-20UP",
    serial_number="001107",
)
laser1 = Laser(
    name="Ex_488",
    coupling="Single-mode fiber",
    wavelength=488,
    serial_number="VL01222A11",
    manufacturer=Organization.VORTRAN,
    model="Stradus",
    notes="All lasers controlled via Vortran VersaLase System",
)
laser2 = Laser(
    name="Ex_561",
    coupling="Single-mode fiber",
    wavelength=561,
    serial_number="417927",
    manufacturer=Organization.COHERENT_SCIENTIFIC,
    model="Obis",
    notes="All lasers controlled via Vortran VersaLase System",
)
laser3 = Laser(
    name="Ex_647",
    coupling="Single-mode fiber",
    wavelength=647,
    serial_number="VL01222A10",
    manufacturer=Organization.VORTRAN,
    model="Stradus",
    notes="All lasers controlled via Vortran VersaLase System",
)
stage0 = MotorizedStage(
    name="Focus stage",
    model="LS-100",
    manufacturer=Organization.ASI,
    travel=100,
)
stage1 = MotorizedStage(
    name="Cylindrical lens #1",
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
)
stage2 = MotorizedStage(
    name="Cylindrical lens #2",
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
)
stage3 = MotorizedStage(
    name="Cylindrical lens #3",
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
)
stage4 = MotorizedStage(
    name="Cylindrical lens #4",
    model="L12-20F-4",
    manufacturer=Organization.IR_ROBOT_CO,
    travel=41,
)
scan_stage1 = ScanningStage(
    name="Sample stage Z",
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Detection axis",
    stage_axis_name="Z",
    travel=50,
)
scan_stage2 = ScanningStage(
    name="Sample stage X",
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Illumination axis",
    stage_axis_name="X",
    travel=50,
)
scan_stage3 = ScanningStage(
    name="Sample stage Y",
    model="LS-50",
    manufacturer=Organization.ASI,
    stage_axis_direction="Perpendicular axis",
    stage_axis_name="Y",
    travel=50,
)
filter0 = Filter(
    name="Em_525",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    model="FF03-525/50-25",
)
filter1 = Filter(
    name="Em_600",
    filter_type="Band pass",
    manufacturer=Organization.SEMROCK,
    model="FF01-600/52-25",
)
filter2 = Filter(
    name="Em_690",
    filter_type="Band pass",
    manufacturer=Organization.CHROMA,
    model="ET690/50m",
)
lens1 = AdditionalImagingDevice(
    name="Lens 1",
    imaging_device_type="Tunable lens",
    manufacturer=Organization.OPTOTUNE,
    model="EL-16-40-TC",
)
lens2 = AdditionalImagingDevice(
    name="Lens 2",
    imaging_device_type="Tunable lens",
    manufacturer=Organization.OPTOTUNE,
    model="EL-16-40-TC",
)
lens3 = AdditionalImagingDevice(
    name="Sample chamber",
    imaging_device_type="Sample Chamber",
    manufacturer=Organization.LIFECANVAS,
    model="Large-uncoated-glass",
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
        device_names=["COM Device", "Laser Launch"],
        connection_data={
            "Laser Launch": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "COM Device": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="COM4",
            ),
        },
    ),
    Connection(
        device_names=["Sample stage Z", "Sample stage X", "Sample stage Y", "ASI Tiger"],
        connection_data={
            "ASI Tiger": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="COM3",
            ),
            "Sample stage Z": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Sample stage Y": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Sample stage X": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Lens 1", "MightyZap"],
        connection_data={
            "MightyZap": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="COM9",
            ),
            "Lens 1": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
]

inst = Instrument(
    instrument_id="440_SmartSPIM2_20231004",
    modification_date=datetime.date(2023, 10, 4),
    coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
    modalities=[Modality.SPIM],
    manufacturer=Organization.LIFECANVAS,
    temperature_control=False,
    components=[
        objective,
        camera1,
        laser1,
        laser2,
        laser3,
        stage0,
        stage1,
        stage2,
        stage3,
        stage4,
        scan_stage1,
        scan_stage2,
        scan_stage3,
        filter0,
        filter1,
        filter2,
        lens1,
        lens2,
        lens3,
        laser_launch,
        asi_tiger,
        mighty_zap,
        com_device,
    ],
    connections=connections,
)

if __name__ == "__main__":
    serialized = inst.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="aibs_smartspim")
