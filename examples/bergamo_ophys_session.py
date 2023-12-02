""" example Bergamo ophys session """

import datetime

from aind_data_schema.core.session import DetectorConfig, FieldOfView, LaserConfig, Session, Stream
from aind_data_schema.models.modalities import Modality
from aind_data_schema.models.stimulus import PhotoStimulation, PhotoStimulationGroup, StimulusEpoch

t = datetime.datetime(2022, 7, 12, 7, 00, 00)

s = Session(
    experimenter_full_name=["John Doe"],
    session_start_time=t,
    session_end_time=t,
    subject_id="652567",
    session_type="BCI Photometry",
    iacuc_protocol="2115",
    rig_id="ophys_rig",
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
            mouse_platform_name="Mouse tube",
            active_mouse_platform=False,
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
            stimulus=PhotoStimulation(
                stimulus_name="PhotoStimulation",
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
            stimulus_start_time=t,
            stimulus_end_time=t,
        )
    ],
)

s.write_standard_file(prefix="bergamo_ophys")
