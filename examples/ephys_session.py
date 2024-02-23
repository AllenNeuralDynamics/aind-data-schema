import datetime

from aind_data_schema.core.session import (
    CcfCoords,
    Coordinates3d,
    DomeModule,
    EphysModule,
    EphysProbeConfig,
    ManipulatorModule,
    Session,
    Stream,
)
from aind_data_schema.models.modalities import Modality
from aind_data_schema.models.stimulus import StimulusEpoch, VisualStimulation

session = Session(
    experimenter_full_name=["Max Quibble", "Finn Tickle"],
    subject_id="664484",
    session_start_time=datetime.datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0),
    session_end_time=datetime.datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0),
    session_type="Receptive field mapping",
    iacuc_protocol="2109",
    rig_id="323_EPHYS2-RF_2023-04-24_01",
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_start_time=datetime.datetime(year=2023, month=4, day=20, hour=0, minute=0, second=0),
            stimulus_end_time=datetime.datetime(year=2023, month=4, day=20, hour=0, minute=14, second=0),
            stimulus=VisualStimulation(
                stimulus_name="Static Gratings",
                stimulus_parameters={
                    'grating_orientations': [0, 45, 90, 135],
                    'grating_orientation_unit': 'degrees',
                    'grating_spatial_frequencies': [0.02, 0.04, 0.08, 0.16, 0.32],
                    'grating_unit': 'pixels/in'
                },
                stimulus_software="Bonsai",
                stimulus_software_version="2.7",
                stimulus_script="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                stimulus_script_version="1.0",
            ),
        ),
        StimulusEpoch(
            stimulus_start_time=datetime.datetime(year=2023, month=4, day=20, hour=0, minute=14, second=0),
            stimulus_end_time=datetime.datetime(year=2023, month=4, day=20, hour=0, minute=28, second=0),
            stimulus=VisualStimulation(
                stimulus_name="Flashes",
                stimulus_parameters={
                    'flash_interval': 5.0,
                    'flash_interval_unit': 'seconds',
                    'flash_duration': 0.5,
                    'flash_duration_unit': 'seconds',
                },
                stimulus_software="Bonsai",
                stimulus_software_version="2.7",
                stimulus_script="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                stimulus_script_version="1.0",
            ),
        )
    ],
    data_streams=[
        Stream(
            stream_start_time=datetime.datetime(year=2023, month=4, day=20, hour=21, minute=31, second=0),
            stream_end_time=datetime.datetime(year=2023, month=4, day=20, hour=22, minute=3, second=0),
            stream_modalities=[Modality.ECEPHYS],
            daq_names=["Basestation"],
            mouse_platform_name="mouse platform",
            active_mouse_platform=True,
            stick_microscopes=[
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 1",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="did not record angles, did not calibrate.",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 2",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 3",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 4",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
            ],
            ephys_modules=[
                EphysModule(
                    targeted_ccf_coordinates=[
                        CcfCoords(ml=8150, ap=3250, dv=7800),
                    ],
                    ephys_probes=[EphysProbeConfig(name="Probe A")],
                    assembly_name="ephys module 1",
                    arc_angle=5.2,
                    module_angle=8,
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime.datetime(year=2023, month=4, day=25),
                    notes="Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording with a sudden shift in signals. Lots of motion. Maybe some implant motion.",
                ),
                EphysModule(
                    rotation_angle=0,
                    arc_angle=25,
                    module_angle=-22,
                    targeted_ccf_coordinates=[CcfCoords(ml=6637.28, ap=4265.02, dv=10707.35)],
                    ephys_probes=[],
                    assembly_name="ephys module 2",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
                    primary_targeted_structure="LC",
                    manipulator_coordinates=Coordinates3d(x=9015, y=7144, z=13262),
                    calibration_date=datetime.datetime(year=2023, month=4, day=25),
                    notes="Trouble penitrating. Lots of compression, needed to move probe. Small amount of surface bleeding/bruising. Initial Target: X;10070.3\tY:7476.6",
                ),
            ],
        ),
        Stream(
            stream_start_time=datetime.datetime(year=2023, month=4, day=25, hour=3, minute=6, second=0),
            stream_end_time=datetime.datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0),
            stream_modalities=[Modality.ECEPHYS],
            notes="664484_2023-04-24_20-06-37; Surface Finding",
            daq_names=["Basestation"],
            mouse_platform_name="mouse platform",
            active_mouse_platform=True,
            stick_microscopes=[
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 1",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="did not record angles, did not calibrate.",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 2",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 3",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 4",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="Did not record angles, did not calibrate",
                ),
            ],
            ephys_modules=[
                EphysModule(
                    rotation_angle=0,
                    arc_angle=5.2,
                    module_angle=8,
                    targeted_ccf_coordinates=[CcfCoords(ml=8150, ap=3250, dv=7800)],
                    ephys_probes=[EphysProbeConfig(name="Probe A")],
                    assembly_name="ephys module 1",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime.datetime(year=2023, month=4, day=25),
                    notes="Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording with a sudden shift in signals. Lots of motion. Maybe some implant motion.",
                ),
                EphysModule(
                    rotation_angle=0,
                    arc_angle=25,
                    module_angle=-22,
                    targeted_ccf_coordinates=[CcfCoords(ml=6637.28, ap=4265.02, dv=10707.35)],
                    ephys_probes=[],
                    assembly_name="ephys module 2",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
                    primary_targeted_structure="LC",
                    manipulator_coordinates=Coordinates3d(x=9015, y=7144, z=13262),
                    calibration_date=datetime.datetime(year=2023, month=4, day=25),
                    notes="Trouble penitrating. Lots of compression, needed to move probe. Small amount of surface bleeding/bruising. Initial Target: X;10070.3\tY:7476.6",
                ),
            ],
        ),
    ],
)

session.write_standard_file(prefix="ephys")
