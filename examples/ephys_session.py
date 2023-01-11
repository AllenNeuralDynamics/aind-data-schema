"""Generates an example JSON file for an ephys session"""

from datetime import datetime

from aind_data_schema.ephys.ephys_session import (Camera, Coordinates3d, DAQDevice, EphysProbe, EphysSession, Laser,
                                                  LaserModule, Stream)

red_laser = Laser(name="Red Laser", power_level=100)

blue_laser = Laser(name="Blue Laser", power_level=50)

laser_module = LaserModule(
    primary_targeted_structure="VISp",
    manipulator_coordinates=Coordinates3d(x=1000, y=1000, z=1000),
    lasers=[red_laser, blue_laser],
)

probeA = EphysProbe(
    name="Probe A", primary_targeted_structure="VISp", manipulator_coordinates=Coordinates3d(x=1000, y=1000, z=1000)
)

probeB = EphysProbe(
    name="Probe B", primary_targeted_structure="STR", manipulator_coordinates=Coordinates3d(x=1000, y=1000, z=1000)
)

harp = DAQDevice(name="Harp Behavior")

basestation = DAQDevice(name="Basestation Slot 3")

face_camera = Camera(name="Face Camera")

body_camera = Camera(name="Body Camera")

stream = Stream(
    stream_start_time=datetime(2023, 1, 10, 8, 43, 00),
    stream_end_time=datetime(2023, 1, 10, 9, 43, 00),
    probes=[probeA, probeB],
    laser_modules=[laser_module],
    daqs=[harp, basestation],
    cameras=[face_camera, body_camera],
)

session = EphysSession(
    experimenter_full_name="Josh Siegle",
    subject_id="100001",
    session_start_time=datetime(2023, 1, 10, 8, 40, 00),
    session_end_time=datetime(2023, 1, 10, 9, 46, 00),
    session_type="Test",
    rig_id="323_EPHYS1",
    data_streams=[stream],
)

session.write_standard_file()
