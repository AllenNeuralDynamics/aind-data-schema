"""Generates an example JSON file for an ephys session"""

from datetime import datetime

from aind_data_schema.core.session import (
    DomeModule,
    EphysModule,
    EphysProbeConfig,
    LaserConfig,
    ManipulatorModule,
    Session,
    Stream,
)
from aind_data_schema.models.coordinates import Coordinates3d
from aind_data_schema.models.modalities import Modality

red_laser = LaserConfig(name="Red Laser", wavelength=700, excitation_power=100)

blue_laser = LaserConfig(name="Blue Laser", wavelength=350, excitation_power=50)

laser_module = ManipulatorModule(
    assembly_name="Laser_assemblyA",
    arc_angle=10,
    module_angle=15,
    primary_targeted_structure="VISp",
    manipulator_coordinates=Coordinates3d(x=1000, y=1000, z=1000),
)

ephys_module = EphysModule(
    assembly_name="Ephys_assemblyA",
    arc_angle=14,
    module_angle=20,
    primary_targeted_structure="VISp",
    manipulator_coordinates=Coordinates3d(x=1000, y=1000, z=1000),
    ephys_probes=[
        EphysProbeConfig(name="Probe A"),
        EphysProbeConfig(name="Probe B"),
    ],
)

stream = Stream(
    stream_start_time=datetime(2023, 1, 10, 8, 43, 00),
    stream_end_time=datetime(2023, 1, 10, 9, 43, 00),
    stream_modalities=[Modality.ECEPHYS, Modality.BEHAVIOR_VIDEOS],
    stick_microscopes=[
        DomeModule(
            assembly_name="Stick_assembly",
            arc_angle=24,
            module_angle=10,
        )
    ],
    ephys_modules=[ephys_module],
    manipulator_modules=[laser_module],
    daq_names=["Harp Behavior", "Basestation Slot 3"],
    camera_names=["Face Camera", "Body Camera"],
    mouse_platform_name="Running Wheel",
    active_mouse_platform=False,
)

session = Session(
    experimenter_full_name=["Jane Doe"],
    subject_id="100001",
    session_start_time=datetime(2023, 1, 10, 8, 40, 00),
    session_end_time=datetime(2023, 1, 10, 9, 46, 00),
    iacuc_protocol="1294",
    session_type="Test",
    rig_id="323_EPHYS1",
    animal_weight_prior=21.2,
    animal_weight_post=21.3,
    data_streams=[stream],
)

session.write_standard_file(prefix="ephys")
