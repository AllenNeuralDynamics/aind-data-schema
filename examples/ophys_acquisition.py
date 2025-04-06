""" example fiber photometry acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    SubjectDetails,
)
from aind_data_schema.components.configs import Channel, DetectorConfig, PatchCordConfig, LaserConfig

t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

a = Acquisition(
    experimenters=[Person(name="Scientist Smith")],
    acquisition_start_time=t,
    acquisition_end_time=t,
    subject_id="652567",
    experiment_type="Parameter Testing",
    instrument_id="ophys_inst",
    ethics_review_id="2115",
    subject_details=SubjectDetails(
        mouse_platform_name="Disc",
    ),
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.FIB],
            active_devices=[
                "Laser A",
                "Laser B",
                "Hamamatsu Camera",
                "Patch Cord A",
                "Patch Cord B",
            ],
            configurations=[
                PatchCordConfig(
                    device_name="Patch Cord A",
                    output_power=40,
                    output_power_unit="microwatt",
                    fiber_name="Fiber A",
                    channels=[
                        Channel(
                            channel_name="Channel A",
                            intended_measurement="Dopamine",
                            detector_configuration=DetectorConfig(
                                device_name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal"
                            ),
                            light_source_configuration=[
                                LaserConfig(
                                    device_name="Laser A",
                                    wavelength=405,
                                    wavelength_unit="nanometer",
                                    excitation_power=10,
                                    excitation_power_unit="milliwatt",
                                ),
                            ],
                        ),
                    ],
                ),
                PatchCordConfig(
                    device_name="Patch Cord B",
                    output_power=43,
                    output_power_unit="microwatt",
                    fiber_name="Fiber B",
                    channels=[
                        Channel(
                            channel_name="Channel B",
                            intended_measurement="GCaMP",
                            detector_configuration=DetectorConfig(
                                device_name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal"
                            ),
                            light_source_configuration=[
                                LaserConfig(
                                    device_name="Laser B",
                                    wavelength=473,
                                    wavelength_unit="nanometer",
                                    excitation_power=7,
                                    excitation_power_unit="milliwatt",
                                ),
                            ],
                        )
                    ],
                ),
            ],
        )
    ],
)
serialized = a.model_dump_json()
deserialized = Acquisition.model_validate_json(serialized)
deserialized.write_standard_file(prefix="ophys")
