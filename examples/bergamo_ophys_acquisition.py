""" example Bergamo ophys session """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import FrequencyUnit

from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.stimulus import PhotoStimulation, PhotoStimulationGroup
from aind_data_schema.core.acquisition import (
    Acquisition,
    StimulusEpoch,
    DataStream,
    SubjectDetails,
)
from aind_data_schema.components.configs import (
    DetectorConfig,
    FieldOfView,
    LaserConfig,
    StimulusModality,
)
from aind_data_schema_models.brain_atlas import CCFStructure

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

a = Acquisition(
    experimenters=[Person(name="John Smith")],
    acquisition_start_time=t,
    acquisition_end_time=t,
    subject_id="652567",
    acquisition_type="BCI Photometry",
    instrument_id="322_bergamo_20220705",
    ethics_review_id="2115",
    subject_details=SubjectDetails(
        mouse_platform_name="Mouse tube",
        active_mouse_platform=False,
    ),
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
            active_devices=[
                "Laser A",
                "PMT A",
                "Face Camera",
            ],
            configurations=[
                LaserConfig(
                    device_name="Laser A",
                    wavelength=405,
                    wavelength_unit="nanometer",
                    excitation_power=10,
                    excitation_power_unit="milliwatt",
                ),
                DetectorConfig(
                    device_name="PMT A",
                    exposure_time=0.1,
                    trigger_type="Internal",
                ),
                FieldOfView(
                    index=0,
                    imaging_depth=150,
                    targeted_structure=CCFStructure.MOP,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_reference="Bregma",
                    fov_width=800,
                    fov_height=800,
                    magnification="1x",
                    fov_scale_factor=1.5,
                    frame_rate=20,
                    frame_rate_unit=FrequencyUnit.HZ,
                ),
            ],
        ),
    ],
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_name="PhotoStimulation",
            modalities=[StimulusModality.OPTOGENETICS],
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

serialized = a.model_dump_json()
deserialized = Acquisition.model_validate_json(serialized)
deserialized.write_standard_file(prefix="bergamo_ophys")
