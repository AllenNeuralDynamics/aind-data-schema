from datetime import datetime
from aind_data_schema.ephys.ephys_session import *

red_laser = Laser(name="Red Laser", power_level=100)

blue_laser = Laser(name="Blue Laser", power_level=50)

laser_module = LaserModule(primary_targeted_structure="VISp",
                        manipulator_coordinates=Coordinates3d(x=1000,y=1000,z=1000),
                        lasers=[red_laser, blue_laser])

probeA = EphysProbe(name="Probe A", primary_targeted_structure="VISp",
                  manipulator_coordinates=Coordinates3d(x=1000,y=1000,z=1000))

probeB = EphysProbe(name="Probe B", primary_targeted_structure="STR",
                  manipulator_coordinates=Coordinates3d(x=1000,y=1000,z=1000))

harp = DAQDevice(name="Harp Behavior")

basestation = DAQDevice(name="Basestation Slot 3")

face_camera = Camera(name="Face Camera")

body_camera = Camera(name="Body Camera")

stream = Stream(stream_start_time=datetime.now(),
                 stream_end_time=datetime.now(),
                 probes=[probeA, probeB],
                 laser_modules=[laser_module],
                 daqs=[harp, basestation],
                 cameras=[face_camera, body_camera])

session = EphysSession(experimenter_full_name="Josh Siegle",
                      subject_id=100001,
                      session_start_time = datetime.now(),
                      session_end_time=datetime.now(),
                      session_type="Test",
                      rig_id="323_EPHYS1",
                      data_streams=[stream])

with open("ephys_session.json", "w") as outfile:
    outfile.write(session.json(indent=2))