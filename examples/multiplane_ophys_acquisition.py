""" example fiber photometry acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import PowerUnit, SizeUnit, FrequencyUnit

from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    SubjectDetails,
)
from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    FieldOfView,
    LaserConfig,
    MultiPlaneConfig,
    TriggerType,
    TwoPhotonImagingConfig,
)
from aind_data_schema_models.brain_atlas import CCFStructure

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

a = Acquisition(
    experimenters=[Person(name="John Smith")],
    acquisition_start_time=t,
    acquisition_end_time=t,
    subject_id="12345",
    experiment_type="Mesoscope",
    instrument_id="MESO.1",
    ethics_review_id="12345",
    subject_details=SubjectDetails(
        mouse_platform_name="disc",
    ),
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
            active_devices=["Mesoscope", "Eye", "Face", "Behavior", "Vasculature", "Laser A", "PMT 1"],
            configurations=[
                TwoPhotonImagingConfig(
                    channels=[
                        Channel(
                            channel_name="Green channel",
                            intended_measurement="GCaMP",
                            detector_configuration=DetectorConfig(
                                device_name="PMT 1", exposure_time=0.1, trigger_type=TriggerType.INTERNAL
                            ),
                            light_source_configurations=[
                                LaserConfig(
                                    device_name="Laser A",
                                    wavelength=920,
                                    wavelength_unit="nanometer",
                                    excitation_power=10,
                                    excitation_power_unit=PowerUnit.MW,
                                ),
                            ],
                        ),
                    ],
                    fields_of_view=[
                        FieldOfView(
                            channel_name="Green channel",
                            targeted_structure=CCFStructure.VISP,
                            fov_coordinate_ml=1.5,
                            fov_coordinate_ap=1.5,
                            fov_coordinate_unit=SizeUnit.UM,
                            fov_reference="Bregma",
                            fov_width=512,
                            fov_height=512,
                            fov_size_unit=SizeUnit.UM,
                            magnification="10x",
                            fov_scale_factor=0.78,
                            frame_rate=9.48,
                            frame_rate_unit=FrequencyUnit.HZ,
                            planes=[
                                MultiPlaneConfig(
                                    index=0,
                                    power=5,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=190,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=230,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=1,
                                ),
                                MultiPlaneConfig(
                                    index=1,
                                    power=42,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=232,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=257,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=0,
                                ),
                                MultiPlaneConfig(
                                    index=2,
                                    power=28,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=136,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=176,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=3,
                                ),
                                MultiPlaneConfig(
                                    index=3,
                                    power=28,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=282,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=307,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=2,
                                ),
                                MultiPlaneConfig(
                                    index=4,
                                    power=12,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=72,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=112,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=5,
                                ),
                                MultiPlaneConfig(
                                    index=5,
                                    power=12,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=326,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=351,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=4,
                                ),
                                MultiPlaneConfig(
                                    index=6,
                                    power=5,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=30,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=70,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=7,
                                ),
                                MultiPlaneConfig(
                                    index=7,
                                    power=5,
                                    power_unit=PowerUnit.PERCENT,
                                    scanimage_roi_index=0,
                                    imaging_depth=364,
                                    targeted_structure=CCFStructure.VISP,
                                    scanfield_z=389,
                                    scanfield_z_unit=SizeUnit.UM,
                                    coupled_plane_index=6,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ],
)

serialized = a.model_dump_json()
deserialized = Acquisition.model_validate_json(serialized)
deserialized.write_standard_file(prefix="multiplane_ophys")
