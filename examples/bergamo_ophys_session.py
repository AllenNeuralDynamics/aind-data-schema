""" example Bergamo ophys session """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.stimulus import PhotoStimulation, PhotoStimulationGroup
from aind_data_schema.core.session import (
    DetectorConfig,
    FieldOfView,
    LaserConfig,
    Session,
    StimulusEpoch,
    StimulusModality,
    Stream,
)

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

s = Session(
    experimenter_full_name=["John Doe"],
    session_start_time=t,
    session_end_time=t,
    subject_id="652567",
    session_type="BCI Photometry",
    iacuc_protocol="2115",
    rig_id="ophys_rig",
    mouse_platform_name="Mouse tube",
    active_mouse_platform=False,
    data_streams=[
        Stream(
            stream_start_time=t,
            stream_end_time=t,
            stream_modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
            light_sources=[
                LaserConfig(
                    name="Laser A",
                    wavelength=405,
                    wavelength_unit="nanometer",
                    excitation_power=10,
                    excitation_power_unit="milliwatt",
                ),
            ],
            detectors=[
                DetectorConfig(
                    name="PMT A",
                    exposure_time=0.1,
                    trigger_type="Internal",
                ),
            ],
            camera_names=["Face Camera"],
            ophys_fovs=[
                FieldOfView(
                    index=0,
                    imaging_depth=150,
                    targeted_structure="M1",
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_reference="Bregma",
                    fov_width=800,
                    fov_height=800,
                    magnification="1x",
                    fov_scale_factor=1.5,
                    frame_rate=20,
                ),
            ],
        ),
    ],
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_name="PhotoStimulation",
            stimulus_modalities=[StimulusModality.OPTOGENETICS],
            stimulus_parameters=[
                PhotoStimulation(
                    stimulus_name="Two group stim",
                    number_groups=2,
                    groups=[
                        PhotoStimulationGroup(
                            group_index=0,
                            number_of_neurons=12,
                            stimulation_laser_power=10,
                            number_trials=5,
                            number_spirals=3,
                            spiral_duration=2,
                            inter_spiral_interval=1,
                        ),
                        PhotoStimulationGroup(
                            group_index=2,
                            number_of_neurons=20,
                            stimulation_laser_power=10,
                            number_trials=5,
                            number_spirals=3,
                            spiral_duration=2,
                            inter_spiral_interval=1,
                        ),
                    ],
                    inter_trial_interval=10,
                ),
            ],
            stimulus_start_time=t,
            stimulus_end_time=t,
        ),
    ],
)

serialized = s.model_dump_json()
deserialized = Session.model_validate_json(serialized)
deserialized.write_standard_file(prefix="bergamo_ophys")
