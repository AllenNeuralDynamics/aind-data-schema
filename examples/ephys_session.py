"""Generates an example JSON file for an ephys session"""

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.devices import Software
from aind_data_schema.core.session import (
    CcfCoords,
    Coordinates3d,
    DomeModule,
    ManipulatorModule,
    Session,
    StimulusEpoch,
    StimulusModality,
    Stream,
    VisualStimulation,
)

session = Session(
    experimenter_full_name=["Max Quibble", "Finn Tickle"],
    subject_id="664484",
    session_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0, tzinfo=timezone.utc),
    session_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
    session_type="Receptive field mapping",
    iacuc_protocol="2109",
    rig_id="323_EPHYS1_20231003",
    active_mouse_platform=False,
    mouse_platform_name="Running Wheel",
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_name="Visual Stimulation",
            stimulus_modalities=[StimulusModality.VISUAL],
            stimulus_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stimulus_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=10, second=0, tzinfo=timezone.utc),
            software=[
                Software(
                    name="Bonsai",
                    version="2.7",
                    url="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                )
            ],
            stimulus_parameters=[
                VisualStimulation(
                    stimulus_name="Static Gratings",
                    stimulus_parameters={
                        "grating_orientations": [0, 45, 90, 135],
                        "grating_orientation_unit": "degrees",
                        "grating_spatial_frequencies": [0.02, 0.04, 0.08, 0.16, 0.32],
                        "grating_spatial_frequency_unit": "cycles/degree",
                    },
                )
            ],
        ),
        StimulusEpoch(
            stimulus_name="Visual Stimulation",
            stimulus_modalities=[StimulusModality.VISUAL],
            stimulus_start_time=datetime(year=2023, month=4, day=25, hour=3, minute=10, second=0, tzinfo=timezone.utc),
            stimulus_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
            software=[
                Software(
                    name="Bonsai",
                    version="2.7",
                    url="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                )
            ],
            stimulus_parameters=[
                VisualStimulation(
                    stimulus_name="Flashes",
                    stimulus_parameters={
                        "flash_interval": 5.0,
                        "flash_interval_unit": "seconds",
                        "flash_duration": 0.5,
                        "flash_duration_unit": "seconds",
                    },
                )
            ],
        ),
    ],
    data_streams=[
        Stream(
            stream_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stream_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
            stream_modalities=[Modality.ECEPHYS],
            daq_names=["Basestation Slot 3"],
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
                ManipulatorModule(
                    targeted_ccf_coordinates=[
                        CcfCoords(ml=8150, ap=3250, dv=7800),
                    ],
                    assembly_name="Ephys_assemblyA",
                    arc_angle=5.2,
                    module_angle=8,
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording"
                        " with a sudden shift in signals. Lots of motion. Maybe some implant motion."
                    ),
                ),
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=25,
                    module_angle=-22,
                    targeted_ccf_coordinates=[CcfCoords(ml=6637.28, ap=4265.02, dv=10707.35)],
                    assembly_name="Ephys_assemblyB",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
                    primary_targeted_structure="LC",
                    manipulator_coordinates=Coordinates3d(x=9015, y=7144, z=13262),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Trouble penetrating. Lots of compression, needed to move probe. Small amount of surface"
                        " bleeding/bruising. Initial Target: X;10070.3\tY:7476.6"
                    ),
                ),
            ],
        ),
        Stream(
            stream_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0, tzinfo=timezone.utc),
            stream_end_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stream_modalities=[Modality.ECEPHYS],
            notes="664484_2023-04-24_20-06-37; Surface Finding",
            daq_names=["Basestation Slot 3"],
            stick_microscopes=[
                DomeModule(
                    rotation_angle=0,
                    assembly_name="stick microscope 1",
                    arc_angle=-180,
                    module_angle=-180,
                    notes="did not record angles, did not calibrate.",
                ),
            ],
            ephys_modules=[
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=5.2,
                    module_angle=8,
                    targeted_ccf_coordinates=[CcfCoords(ml=8150, ap=3250, dv=7800)],
                    assembly_name="Ephys_assemblyA",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
                    primary_targeted_structure="LGd",
                    manipulator_coordinates=Coordinates3d(x=8422, y=4205, z=11087.5),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording"
                        " with a sudden shift in signals. Lots of motion. Maybe some implant motion."
                    ),
                ),
                ManipulatorModule(
                    rotation_angle=0,
                    arc_angle=25,
                    module_angle=-22,
                    targeted_ccf_coordinates=[CcfCoords(ml=6637.28, ap=4265.02, dv=10707.35)],
                    assembly_name="Ephys_assemblyB",
                    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
                    primary_targeted_structure="LC",
                    manipulator_coordinates=Coordinates3d(x=9015, y=7144, z=13262),
                    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
                    notes=(
                        "Trouble penetrating. Lots of compression, needed to move probe. Small amount of surface"
                        " bleeding/bruising. Initial Target: X;10070.3\tY:7476.6"
                    ),
                ),
            ],
        ),
    ],
)

serialized = session.model_dump_json()
deserialized = Session.model_validate_json(serialized)
deserialized.write_standard_file(prefix="ephys")
