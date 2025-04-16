""" example Bergamo ophys acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import FrequencyUnit

from aind_data_schema.components.identifiers import Person, Code
from aind_data_schema.components.stimulus import PhotoStimulation, PhotoStimulationGroup
from aind_data_schema.core.acquisition import (
    Acquisition,
    StimulusEpoch,
    DataStream,
    AcquisitionSubjectDetails,
)
from aind_data_schema.components.acquisition_configs import (
    Channel,
    DetectorConfig,
    FieldOfView,
    LaserConfig,
    SinglePlaneConfig,
    StimulusModality,
    ImagingConfig,
)
from aind_data_schema.components.coordinates import Coordinate, CoordinateSystemLibrary
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
    ethics_review_id=["2115"],
    subject_details=AcquisitionSubjectDetails(
        mouse_platform_name="Mouse tube",
    ),
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
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
                ImagingConfig(
                    channels=[
                        Channel(
                            channel_name="Green channel",
                            intended_measurement="GCaMP",
                            detector=DetectorConfig(
                                device_name="PMT A",
                                exposure_time=0.1,
                                trigger_type="Internal",
                            ),
                            light_source_configurations=[
                                LaserConfig(
                                    device_name="Laser A",
                                    wavelength=405,
                                    wavelength_unit="nanometer",
                                    power=10,
                                    power_unit="milliwatt",
                                ),
                            ],
                        ),
                    ],
                    images=[
                        FieldOfView(
                            channel_name="Green channel",
                            targeted_structure=CCFStructure.MOP,
                            center_coordinate=Coordinate(
                                system_name="BREGMA_ARI",
                                position=[1.5, 1.5, 0],
                            ),
                            fov_width=800,
                            fov_height=800,
                            magnification="1x",
                            fov_scale_factor=1.5,
                            frame_rate=20,
                            frame_rate_unit=FrequencyUnit.HZ,
                            planes=[
                                SinglePlaneConfig(
                                    imaging_depth=150,
                                )
                            ],
                        )
                    ],
                )
            ],
        ),
    ],
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_name="PhotoStimulation",
            stimulus_modalities=[StimulusModality.OPTOGENETICS],
            code=Code(
                url="https://www.github.com/AllenInstitute/aind-photo-stim",
                parameters=PhotoStimulation(
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
            ),
            stimulus_start_time=t,
            stimulus_end_time=t,
        ),
    ],
)

if __name__ == "__main__":
    serialized = a.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="bergamo_ophys")
