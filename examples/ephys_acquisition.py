"""Generates an example JSON file for an ephys acquisition"""

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.identifiers import Person, Software, Code
from aind_data_schema.core.acquisition import (
    Acquisition,
    StimulusEpoch,
    DataStream,
    SubjectDetails,
)
from aind_data_schema.components.configs import (
    DomeModule,
    ManipulatorConfig,
    StimulusModality,
)
from aind_data_schema.components.coordinates import Coordinate, FloatAxis, AxisName
from aind_data_schema.components.stimulus import VisualStimulation
from aind_data_schema_models.brain_atlas import CCFStructure

bonsai_software = Software(name="Bonsai", version="2.7")


ephys_config_a = ManipulatorConfig(
    rotation_angle=0,
    arc_angle=5.2,
    module_angle=8,
    atlas_coordinates=[
        Coordinate(
            position=[
                FloatAxis(value=8150, axis=AxisName.ML),
                FloatAxis(value=3250, axis=AxisName.AP),
                FloatAxis(value=7800, axis=AxisName.SI),
            ]
        ),
    ],
    device_name="Ephys_assemblyA",
    coordinate_transform="behavior/calibration_info_np2_2023_04_24.npy",
    primary_targeted_structure=CCFStructure.LGD,
    manipulator_axis_position=[
        Coordinate(
            position=[
                FloatAxis(value=8422, axis=AxisName.ML),
                FloatAxis(value=4205, axis=AxisName.AP),
                FloatAxis(value=11087.5, axis=AxisName.SI),
            ]
        ),
    ],
    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
    notes=(
        "Moved Y to avoid blood vessel, X to avoid edge. Mouse made some noise during the recording"
        " with a sudden shift in signals. Lots of motion. Maybe some implant motion."
    ),
)

ephys_config_b = ManipulatorConfig(
    rotation_angle=0,
    arc_angle=25,
    module_angle=-22,
    atlas_coordinates=[
        Coordinate(
            position=[
                FloatAxis(value=8150, axis=AxisName.ML),
                FloatAxis(value=3250, axis=AxisName.AP),
                FloatAxis(value=7800, axis=AxisName.SI),
            ]
        ),
    ],
    device_name="Ephys_assemblyB",
    coordinate_transform="behavior/calibration_info_np2_2023_04_24.py",
    primary_targeted_structure=CCFStructure.LC,
    manipulator_axis_position=[
        Coordinate(
            position=[
                FloatAxis(value=8422, axis=AxisName.ML),
                FloatAxis(value=4205, axis=AxisName.AP),
                FloatAxis(value=11087.5, axis=AxisName.SI),
            ]
        ),
    ],
    calibration_date=datetime(year=2023, month=4, day=25, tzinfo=timezone.utc),
    notes=(
        "Trouble penetrating. Lots of compression, needed to move probe. Small amount of surface"
        " bleeding/bruising. Initial Target: X;10070.3\tY:7476.6"
    ),
)


stick_config_1 = DomeModule(
    rotation_angle=0,
    device_name="Stick_assembly_1",
    arc_angle=-180,
    module_angle=-180,
    notes="did not record angles, did not calibrate.",
)
stick_config_2 = DomeModule(
    rotation_angle=0,
    device_name="Stick_assembly_2",
    arc_angle=-180,
    module_angle=-180,
    notes="Did not record angles, did not calibrate",
)
stick_config_3 = DomeModule(
    rotation_angle=0,
    device_name="Stick_assembly_3",
    arc_angle=-180,
    module_angle=-180,
    notes="Did not record angles, did not calibrate",
)
stick_config_4 = DomeModule(
    rotation_angle=0,
    device_name="Stick_assembly_4",
    arc_angle=-180,
    module_angle=-180,
    notes="Did not record angles, did not calibrate",
)

acquisition = Acquisition(
    experimenters=[Person(name="John Smith")],
    subject_id="664484",
    acquisition_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0, tzinfo=timezone.utc),
    acquisition_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
    experiment_type="Receptive field mapping",
    instrument_id="323_EPHYS1_20231003",
    ethics_review_id="2109",
    subject_details=SubjectDetails(
        mouse_platform_name="Running Wheel",
    ),
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_name="Visual Stimulation",
            stimulus_modalities=[StimulusModality.VISUAL],
            stimulus_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stimulus_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=10, second=0, tzinfo=timezone.utc),
            code=Code(
                url="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                software=bonsai_software,
                parameters=VisualStimulation(
                    stimulus_name="Static Gratings",
                    stimulus_parameters={
                        "grating_orientations": [0, 45, 90, 135],
                        "grating_orientation_unit": "degrees",
                        "grating_spatial_frequencies": [0.02, 0.04, 0.08, 0.16, 0.32],
                        "grating_spatial_frequency_unit": "cycles/degree",
                    },
                ),
            ),
        ),
        StimulusEpoch(
            stimulus_name="Visual Stimulation",
            stimulus_modalities=[StimulusModality.VISUAL],
            stimulus_start_time=datetime(year=2023, month=4, day=25, hour=3, minute=10, second=0, tzinfo=timezone.utc),
            stimulus_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
            code=Code(
                url="https://github.com/fakeorg/GratingAndFlashes/gratings_and_flashes.bonsai",
                software=bonsai_software,
                parameters=VisualStimulation(
                    stimulus_name="Flashes",
                    stimulus_parameters={
                        "flash_interval": 5.0,
                        "flash_interval_unit": "seconds",
                        "flash_duration": 0.5,
                        "flash_duration_unit": "seconds",
                    },
                ),
            ),
        ),
    ],
    data_streams=[
        DataStream(
            stream_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            stream_end_time=datetime(year=2023, month=4, day=25, hour=3, minute=16, second=0, tzinfo=timezone.utc),
            modalities=[Modality.ECEPHYS],
            active_devices=[
                "Basestation Slot 3",
                "Stick_assembly_1",
                "Stick_assembly_2",
                "Stick_assembly_3",
                "Stick_assembly_4",
                "Ephys_assemblyA",
                "Ephys_assemblyB",
            ],
            configurations=[
                ephys_config_a,
                ephys_config_b,
                stick_config_1,
                stick_config_2,
                stick_config_3,
                stick_config_4,
            ],
        ),
        DataStream(
            stream_start_time=datetime(year=2023, month=4, day=25, hour=2, minute=35, second=0, tzinfo=timezone.utc),
            stream_end_time=datetime(year=2023, month=4, day=25, hour=2, minute=45, second=0, tzinfo=timezone.utc),
            modalities=[Modality.ECEPHYS],
            notes="664484_2023-04-24_20-06-37; Surface Finding",
            active_devices=[
                "Basestation Slot 3",
                "Stick_assembly_1",
                "Ephys_assemblyA",
                "Ephys_assemblyB",
            ],
            configurations=[
                stick_config_1,
            ],
        ),
    ],
)

serialized = acquisition.model_dump_json()
deserialized = Acquisition.model_validate_json(serialized)
deserialized.write_standard_file(prefix="ephys")
